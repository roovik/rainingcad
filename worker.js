// rainingcad.com: static site (./site) plus a small Worker for book access codes. No accounts.
// /inside/<book>/<n>/  -> chapters past the free ones need the signed cookie rc_a, else a redirect to /unlock/ (rules in /gate.json from tools/build_rcd.py)
// /api/redeem          -> POST {code}: checks the code in CodesDB, adds its books to the cookie on this device
// /api/access          -> GET: what this device can read
// /api/admin/*         -> the owner's code admin, with the x-admin-key header matching the ADMIN_KEY secret (set in the Cloudflare dashboard)
// /api/offer, /api/subscribe, /api/me, /api/notes, /api/note, /api/notes-bulk -> the free Dog Year and Cat Year subscription (email, sync key, notes that follow the reader across devices) until FREE_UNTIL
// Access keys: a book (bk-...), 'books' (every book) or 'all' (everything).
import { DurableObject } from 'cloudflare:workers';

// The free subscription runs until the end of Dec 31, 2026 (Israel time). Change this one date to end or extend the offer.
const FREE_UNTIL = Date.parse('2026-12-31T23:59:59+02:00');
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
async function readSub(env, request) {
  const c = (request.headers.get('cookie') || '').match(/(?:^|;\s*)rc_s=([^;]+)/); if (!c) return null;
  const [body, sig] = c[1].split('.'); if (!body || !sig) return null;
  try {
    const ok = await crypto.subtle.verify('HMAC', await gateKey(env), Uint8Array.from(unb64u(sig), x => x.charCodeAt(0)), new TextEncoder().encode(body)); if (!ok) return null;
    const p = JSON.parse(unb64u(body)); return p.u > NOW() && p.i ? p : null;
  } catch (e) { return null; }
}
const subCookie = async (env, id) => `rc_s=${await sign(env, { i: id, u: FREE_UNTIL })}; Path=/; Max-Age=${Math.max(60, Math.floor((FREE_UNTIL - NOW()) / 1000))}; HttpOnly; Secure; SameSite=Lax`;
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
      if (p === '/api/offer') return json({ ok: true, until: FREE_UNTIL, open: NOW() <= FREE_UNTIL });
      if (p === '/api/me') { const S = await readSub(env, request); return json({ ok: true, sub: !!S, until: S ? S.u : 0 }); }
      if (p === '/api/subscribe' && request.method === 'POST') {
        let b = {}; try { b = await request.json(); } catch (e) {}
        if (b.website) return json({ ok: true, until: FREE_UNTIL });   // honeypot: bots fill this hidden field
        const r = await (await stub(env).fetch('https://internal/sub', { method: 'POST', body: JSON.stringify({ email: b.email, key: b.key, books: b.books, source: clean(b.source, 60), ip: request.headers.get('cf-connecting-ip') || '', country: (request.cf && request.cf.country) || '' }) })).json();
        if (!r.ok) return json(r, r.status || 400);
        return json({ ok: true, until: FREE_UNTIL, books: r.books, key: r.key || null, isnew: r.isnew }, 200, { 'set-cookie': await subCookie(env, r.id) });
      }
      if (p === '/api/notes' || p === '/api/note' || p === '/api/notes-bulk') {
        const S = await readSub(env, request); if (!S) return json({ ok: false, error: 'not-subscribed' }, 401);
        let body = {}; if (request.method === 'POST') { try { body = await request.json(); } catch (e) {} }
        return stub(env).fetch('https://internal' + p.replace('/api', ''), { method: 'POST', body: JSON.stringify(Object.assign(body, { id: S.i })) });
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
    this.sql.exec('CREATE TABLE IF NOT EXISTS subs (id TEXT PRIMARY KEY, email TEXT UNIQUE, key TEXT, books TEXT, created INTEGER, source TEXT, country TEXT)');
    this.sql.exec('CREATE TABLE IF NOT EXISTS notes (id TEXT, k TEXT, v TEXT, title TEXT, u INTEGER, PRIMARY KEY (id, k))');
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
    if (p === '/sub') {
      if (this.limited('s:' + b.ip, 8, 10)) return json({ ok: false, error: 'slow-down', status: 429 });
      const email = clean(b.email, 120).toLowerCase();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return json({ ok: false, error: 'bad-email', status: 400 });
      const s = this.one('SELECT * FROM subs WHERE email = ?', email), key = clean(b.key, 30).toUpperCase().replace(/[^A-Z0-9]/g, '');
      if (s) return key && s.key.replace(/-/g, '') === key ? json({ ok: true, id: s.id, books: s.books.split(','), isnew: false }) : json({ ok: false, error: 'have-key', status: 409 });
      if (NOW() > FREE_UNTIL) return json({ ok: false, error: 'offer-ended', status: 410 });
      const bk = (Array.isArray(b.books) ? b.books : []).filter(x => x === 'dy' || x === 'cy'), books = bk.length ? bk : ['dy', 'cy'], id = hex(12), nk = code4() + '-' + code4() + '-' + code4();
      this.sql.exec('INSERT INTO subs (id, email, key, books, created, source, country) VALUES (?, ?, ?, ?, ?, ?, ?)', id, email, nk, books.join(','), NOW(), clean(b.source, 60), clean(b.country, 4));
      return json({ ok: true, id, key: nk, books, isnew: true });
    }
    if (p === '/notes') return json({ ok: true, notes: Object.fromEntries(this.all('SELECT k, v, title, u FROM notes WHERE id = ?', b.id).map(r => [r.k, { v: r.v, t: r.title, u: r.u }])) });
    const okKey = k => /^(dy27|cy27):[A-Za-z0-9\/_-]{1,30}$/.test(k);
    if (p === '/note') {
      const k = clean(b.k, 40); if (!okKey(k)) return json({ ok: false, error: 'bad-key' }, 400);
      const v = String(b.v == null ? '' : b.v).slice(0, 20000), u = NOW();
      if (!v.trim()) this.sql.exec('DELETE FROM notes WHERE id = ? AND k = ?', b.id, k);
      else this.sql.exec('INSERT INTO notes (id, k, v, title, u) VALUES (?, ?, ?, ?, ?) ON CONFLICT (id, k) DO UPDATE SET v = excluded.v, title = excluded.title, u = excluded.u', b.id, k, v, clean(b.t, 80), u);
      return json({ ok: true, u });
    }
    if (p === '/notes-bulk') {
      let n = 0; for (const it of (Array.isArray(b.items) ? b.items : []).slice(0, 400)) {
        const k = clean(it.k, 40), v = String(it.v == null ? '' : it.v).slice(0, 20000), u = Math.min(NOW(), +it.u || 0); if (!okKey(k) || !v.trim()) continue;
        const ex = this.one('SELECT u FROM notes WHERE id = ? AND k = ?', b.id, k); if (ex && ex.u >= u) continue;
        this.sql.exec('INSERT INTO notes (id, k, v, title, u) VALUES (?, ?, ?, ?, ?) ON CONFLICT (id, k) DO UPDATE SET v = excluded.v, title = excluded.title, u = excluded.u', b.id, k, v, clean(it.t, 80), u || NOW()); n++;
      } return json({ ok: true, n });
    }
    if (p === '/admin/subs') return json({ ok: true, subs: this.all('SELECT email, books, created, source, country FROM subs ORDER BY created DESC LIMIT 5000'), notes: this.one('SELECT COUNT(*) AS n FROM notes').n });
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
