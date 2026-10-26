// rainingcad.com: static site (./site) plus a small Worker for book access codes. No accounts.
// /inside/<book>/<n>/  -> chapters past the free ones need the signed cookie rc_a, else a redirect to /unlock/ (rules in /gate.json from tools/build_rcd.py)
// /api/redeem          -> POST {code}: checks the code in CodesDB, adds its books to the cookie on this device
// /api/access          -> GET: what this device can read
// /api/admin/*         -> the owner's code admin, with the x-admin-key header matching the ADMIN_KEY secret (set in the Cloudflare dashboard)
// Access keys: a book (bk-...), 'books' (every book) or 'all' (everything).
import { DurableObject } from 'cloudflare:workers';

const DAY = 86400000, NOW = () => Date.now();
const json = (o, s = 200, h = {}) => new Response(JSON.stringify(o), { status: s, headers: { 'content-type': 'application/json', 'cache-control': 'no-store', ...h } });
const clean = (s, n) => String(s == null ? '' : s).replace(/[\u0000-\u001f<>]/g, '').trim().slice(0, n);
const hex = n => [...crypto.getRandomValues(new Uint8Array(n))].map(b => b.toString(16).padStart(2, '0')).join('');
const ALPH = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const code4 = () => [...crypto.getRandomValues(new Uint8Array(4))].map(b => ALPH[b % ALPH.length]).join('');
const b64u = s => btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const unb64u = s => atob(s.replace(/-/g, '+').replace(/_/g, '/'));

let GATE = null, GKEY = null;
async function gateKey(env) {
  if (!GKEY) { const r = await stub(env).fetch('https://internal/gatekey'); GKEY = await crypto.subtle.importKey('raw', new TextEncoder().encode(await r.text()), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign', 'verify']); }
  return GKEY;
}
const stub = env => env.CODES.get(env.CODES.idFromName('main'));
async function sign(env, payload) { const body = b64u(JSON.stringify(payload)); const sig = await crypto.subtle.sign('HMAC', await gateKey(env), new TextEncoder().encode(body)); return body + '.' + b64u(String.fromCharCode(...new Uint8Array(sig))); }
async function readPass(env, request) {
  const c = (request.headers.get('cookie') || '').match(/(?:^|;\s*)rc_a=([^;]+)/); if (!c) return {};
  const [body, sig] = c[1].split('.'); if (!body || !sig) return {};
  try {
    const ok = await crypto.subtle.verify('HMAC', await gateKey(env), Uint8Array.from(unb64u(sig), x => x.charCodeAt(0)), new TextEncoder().encode(body)); if (!ok) return {};
    const p = JSON.parse(unb64u(body)), out = {}; for (const k in p.a || {}) if (p.a[k] > NOW()) out[k] = p.a[k]; return out;
  } catch (e) { return {}; }
}
const covers = (A, id) => !!(A.all || A.books || A[id]);
async function gate(request, env, url) {
  if (!GATE) { const r = await env.ASSETS.fetch(new Request(url.origin + '/gate.json')); GATE = r.ok ? await r.json() : {}; }
  for (const id in GATE) {
    const g = GATE[id], m = url.pathname.match(new RegExp(g.re)); if (!m) continue;
    if (g.free.includes(+m[1])) return null;
    if (covers(await readPass(env, request), id)) return null;
    return Response.redirect(url.origin + '/unlock/?c=' + id + '&l=' + encodeURIComponent(m[1]) + '&next=' + encodeURIComponent(url.pathname), 302);
  }
  return null;
}
function sameOrigin(request, url) { const o = request.headers.get('origin'); return !o || new URL(o).host === url.host; }
async function keyOk(request, env) {
  const a = env.ADMIN_KEY || '', b = request.headers.get('x-admin-key') || '';
  if (a.length < 12 || a.length !== b.length) return false;
  const x = new TextEncoder().encode(a), y = new TextEncoder().encode(b); let d = 0; for (let i = 0; i < x.length; i++) d |= x[i] ^ y[i]; return d === 0;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url), p = url.pathname;
    if (request.method === 'GET' && p.startsWith('/inside/')) { const r = await gate(request, env, url); if (r) return r; }
    if (p.startsWith('/api/')) {
      if (request.method === 'POST' && (!sameOrigin(request, url) || !(request.headers.get('content-type') || '').includes('application/json'))) return json({ ok: false, error: 'bad-request' }, 403);
      if (p === '/api/access') return json({ ok: true, access: await readPass(env, request) });
      if (p === '/api/redeem' && request.method === 'POST') {
        let b = {}; try { b = await request.json(); } catch (e) {}
        const r = await (await stub(env).fetch('https://internal/redeem', { method: 'POST', body: JSON.stringify({ code: clean(b.code, 30).toUpperCase(), ip: request.headers.get('cf-connecting-ip') || '', country: (request.cf && request.cf.country) || '' }) })).json();
        if (!r.ok) return json(r, r.status || 400);
        const A = await readPass(env, request); r.books.forEach(k => { A[k] = Math.max(A[k] || 0, r.until); });
        const exp = Math.max(...Object.values(A));
        return json({ ok: true, books: r.books, until: r.until }, 200, { 'set-cookie': `rc_a=${await sign(env, { a: A })}; Path=/; Max-Age=${Math.max(60, Math.floor((exp - NOW()) / 1000))}; HttpOnly; Secure; SameSite=Lax` });
      }
      if (p.startsWith('/api/admin/')) {
        if (!env.ADMIN_KEY) return json({ ok: false, error: 'no-admin-key' }, 503);
        if (!(await keyOk(request, env))) return json({ ok: false, error: 'wrong-key' }, 401);
        return stub(env).fetch('https://internal' + p.replace('/api', ''), { method: request.method, body: request.method === 'POST' ? await request.text() : undefined });
      }
      return json({ ok: false, error: 'not-found' }, 404);
    }
    return env.ASSETS.fetch(request);
  }
};

export class CodesDB extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env); this.sql = ctx.storage.sql;
    this.sql.exec('CREATE TABLE IF NOT EXISTS codes (code TEXT PRIMARY KEY, books TEXT, days INTEGER, uses_max INTEGER, uses INTEGER DEFAULT 0, expires INTEGER DEFAULT 0, note TEXT, created INTEGER)');
    this.sql.exec('CREATE TABLE IF NOT EXISTS uses (code TEXT, at INTEGER, country TEXT)');
    this.sql.exec('CREATE TABLE IF NOT EXISTS hits (k TEXT, at INTEGER)');
    this.sql.exec('CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT)');
  }
  one(q, ...a) { return [...this.sql.exec(q, ...a)][0] || null; }
  all(q, ...a) { return [...this.sql.exec(q, ...a)]; }
  limited(k, max, mins) {
    this.sql.exec('DELETE FROM hits WHERE at < ?', NOW() - 60 * 60000);
    const n = this.one('SELECT COUNT(*) AS n FROM hits WHERE k = ? AND at > ?', k, NOW() - mins * 60000).n;
    if (n >= max) return true; this.sql.exec('INSERT INTO hits (k, at) VALUES (?, ?)', k, NOW()); return false;
  }
  async fetch(req) {
    const url = new URL(req.url), p = url.pathname; let b = {}; if (req.method === 'POST') { try { b = await req.json(); } catch (e) {} }
    if (p === '/gatekey') { let r = this.one("SELECT v FROM kv WHERE k = 'gatekey'"); if (!r) { this.sql.exec("INSERT INTO kv (k, v) VALUES ('gatekey', ?)", hex(32)); r = this.one("SELECT v FROM kv WHERE k = 'gatekey'"); } return new Response(r.v); }
    if (p === '/redeem') {
      if (this.limited('r:' + b.ip, 10, 10)) return json({ ok: false, error: 'slow-down', status: 429 });
      const c = this.one('SELECT * FROM codes WHERE code = ?', b.code);
      if (!c) return json({ ok: false, error: 'bad-code', status: 404 });
      if (c.expires && c.expires < NOW()) return json({ ok: false, error: 'code-expired', status: 410 });
      if (c.uses >= c.uses_max) return json({ ok: false, error: 'code-used-up', status: 410 });
      this.sql.exec('UPDATE codes SET uses = uses + 1 WHERE code = ?', c.code);
      this.sql.exec('INSERT INTO uses (code, at, country) VALUES (?, ?, ?)', c.code, NOW(), clean(b.country, 4));
      return json({ ok: true, books: c.books.split(','), until: NOW() + c.days * DAY });
    }
    if (p === '/admin/codes') return json({ ok: true, codes: this.all('SELECT * FROM codes ORDER BY created DESC LIMIT 500'), uses: this.all('SELECT * FROM uses ORDER BY at DESC LIMIT 200') });
    if (p === '/admin/code' && req.method === 'POST') {
      const books = (Array.isArray(b.books) ? b.books : []).map(x => clean(x, 40)).filter(x => /^[a-z0-9-]+$/.test(x)).slice(0, 40);
      if (!books.length) return json({ ok: false, error: 'pick-books' }, 400);
      const days = Math.max(1, Math.min(3650, +b.days || 365)), uses = Math.max(1, Math.min(100000, +b.uses || 1)), n = Math.max(1, Math.min(100, +b.count || 1));
      const expires = b.expires ? Date.parse(b.expires) || 0 : 0, custom = clean(b.custom, 24).toUpperCase().replace(/[^A-Z0-9-]/g, ''), out = [];
      if (custom && this.one('SELECT code FROM codes WHERE code = ?', custom)) return json({ ok: false, error: 'code-taken' }, 409);
      for (let i = 0; i < (custom ? 1 : n); i++) {
        let c = custom; if (!c) do { c = 'RCD-' + code4() + '-' + code4(); } while (this.one('SELECT code FROM codes WHERE code = ?', c));
        this.sql.exec('INSERT INTO codes (code, books, days, uses_max, uses, expires, note, created) VALUES (?, ?, ?, ?, 0, ?, ?, ?)', c, books.join(','), days, uses, expires, clean(b.note, 200), NOW()); out.push(c);
      }
      return json({ ok: true, codes: out });
    }
    if (p === '/admin/code-end' && req.method === 'POST') { this.sql.exec('UPDATE codes SET expires = ? WHERE code = ?', NOW() - 1, clean(b.code, 30)); return json({ ok: true }); }
    return json({ ok: false, error: 'not-found' }, 404);
  }
}
