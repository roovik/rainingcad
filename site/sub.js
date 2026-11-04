/* rainingcad.com: the free Dog Year and Cat Year subscription. Loaded by menu.js on every page.
   Banner, signup forms (any element with data-rc-form or data-rc-promo), and notes that sync for subscribers. API: worker.js. */
(function () {
  var P = location.pathname, DEF = 'December 31, 2026', UNTIL = DEF, OPEN = true;
  function $(s, e) { return (e || document).querySelector(s); }
  function ls(k, v) { try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} return null; }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  function api(path, body) {
    var o = body ? { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body), credentials: 'same-origin' } : { credentials: 'same-origin' };
    return fetch('/api/' + path, o).then(function (r) { return r.json().catch(function () { return { ok: false, error: 'network' }; }); }, function () { return { ok: false, error: 'network' }; });
  }
  function getSub() { try { var o = JSON.parse(ls('rc-sub') || 'null'); return o && o.u > Date.now() ? o : null; } catch (e) { return null; } }
  var sub = getSub();
  var ERR = { 'bad-email': 'That email does not look right. Check it and try again.', 'slow-down': 'Too many tries. Please wait a few minutes.', network: 'No connection. Try again.', 'offer-ended': 'The free subscription ended on December 31, 2026.', 'have-key': 'This email is already subscribed. Enter your sync key to use it on this device.' };

  var css = '.rcb{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;background:#2A2A2D;color:#F3F2EC;padding:9px 40px 9px 14px;font:500 14px/1.35 Hanken,system-ui,sans-serif;position:relative;text-align:center}'
    + '.rcb b{color:#E8C873}.rcb a.rcb-go{background:#E8C873;color:#2A2A2D;text-decoration:none;font:800 11px Hanken,sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:8px 14px;white-space:nowrap}'
    + '.rcb button{all:unset;cursor:pointer;position:absolute;right:10px;top:50%;transform:translateY(-50%);font:400 22px/1 Hanken,sans-serif;padding:4px 8px;color:#F3F2EC}'
    + '.rcs{border:2px solid var(--gold-deep,#876217);background:#FBFAF6;padding:22px 24px;margin:26px 0}.rcs h2,.rcs h3{font:800 clamp(24px,4vw,32px)/1.1 Spectral,Georgia,serif;margin:0 0 8px;color:#2A2A2D}'
    + '.rcs .rcs-k0{font:600 11px Hanken,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep,#876217);margin:0 0 8px}.rcs p{margin:0 0 12px;font:18px/1.5 Spectral,Georgia,serif;color:#2A2A2D}'
    + '.rcs-row{display:flex;gap:10px;flex-wrap:wrap}.rcs-row input{flex:1 1 240px;min-width:0;font:18px Spectral,Georgia,serif;padding:13px 14px;border:1px solid rgba(42,42,45,.4);background:#fff;color:#2A2A2D}'
    + '.rcs-b{cursor:pointer;font:800 13px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase;padding:14px 22px;border:2px solid var(--gold-deep,#876217);background:var(--gold-deep,#876217);color:#fff}.rcs-b[disabled]{opacity:.6;cursor:wait}'
    + '.rcs-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;opacity:0}.rcs-k{display:block;margin:12px 0 0}.rcs-k[hidden]{display:none}.rcs-k input{font:18px Spectral,Georgia,serif;padding:11px 12px;border:1px solid rgba(42,42,45,.4);width:100%;max-width:320px;text-transform:uppercase}'
    + '.rcs-k span{display:block;font:700 11px Hanken,sans-serif;letter-spacing:.16em;text-transform:uppercase;margin-bottom:4px}.rcs-pick{display:flex;gap:18px;flex-wrap:wrap;margin:12px 0 0;font:16px Spectral,Georgia,serif}.rcs-pick label{display:flex;gap:8px;align-items:center;cursor:pointer}'
    + '.rcs-m{min-height:1.2em;margin:10px 0 0!important;font:600 14px Hanken,sans-serif!important;color:#a33a2c!important}.rcs-fine{font:13px/1.45 Hanken,sans-serif!important;color:#6F6F74!important;margin:10px 0 0!important}'
    + '.rcs-key{font:800 26px Hanken,sans-serif;letter-spacing:.12em;background:#fff;border:1px dashed var(--gold-deep,#876217);padding:12px 16px;display:inline-block;margin:6px 0 12px;color:#2A2A2D}.rcs .btns{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0}'
    + '.rcs .btns a,.rcs .btns button{cursor:pointer;font:700 12px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;padding:12px 18px;border:2px solid var(--gold-deep,#876217);color:var(--gold-deep,#876217);background:transparent}.rcs .btns .main{background:var(--gold-deep,#876217);color:#fff}'
    + '.rcs.done{background:#f0f6f1;border-color:#2f6b4f}.rcs.mini{padding:14px 18px}.rcs.mini p{margin:0;font-size:16px}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function pushLocal() {   // notes written before subscribing go up with the first sign-in
    var items = []; try { for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (/^(dy27|cy27):/.test(k) && !/:(title|ts)$/.test(k)) items.push({ k: k, v: localStorage.getItem(k), t: localStorage.getItem(k + ':title') || '', u: +localStorage.getItem(k + ':ts') || Date.now() }); } } catch (e) {}
    return items.length ? api('notes-bulk', { items: items }) : Promise.resolve();
  }
  function success(host, r) {
    sub = { u: r.until }; ls('rc-sub', JSON.stringify(sub));
    host.className = 'rcs done'; var until = new Date(r.until).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    host.innerHTML = '<p class="rcs-k0">You are in</p><h2>' + (r.isnew ? 'You are subscribed.' : 'Welcome back.') + '</h2><p>Free until ' + esc(until) + '. Your notes in Dog Year and Cat Year now save to your account and follow you to every device.</p>'
      + (r.key ? '<p><b>Your sync key</b> (to use your notes on another phone or computer, subscribe there with this email and this key):</p><div class="rcs-key" id="rcs-key">' + esc(r.key) + '</div><div class="btns"><button type="button" id="rcs-copy">Copy key</button></div><p class="rcs-fine">It is saved on this device. A screenshot or a note to yourself is enough.</p>' : '')
      + '<div class="btns"><a class="main" href="/DY2027/">Open Dog Year</a><a href="/CY2027/">Open Cat Year</a></div>';
    var c = $('#rcs-copy', host); if (c) c.onclick = function () { var t = r.key; (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { c.textContent = 'Copied'; }, function () { c.textContent = t; }); };
    pushLocal().then(initNotes);
    var bn = $('.rcb'); if (bn) bn.remove();
  }
  function form(host, mode) {
    host.innerHTML = '<form class="rcs-f" novalidate><div class="rcs-row"><input type="email" name="email" required autocomplete="email" inputmode="email" placeholder="Your email" aria-label="Your email"><button class="rcs-b" type="submit">Subscribe free</button></div>'
      + (mode === 'pick' ? '<div class="rcs-pick"><label><input type="checkbox" name="dy" checked> Dog Year</label><label><input type="checkbox" name="cy" checked> Cat Year</label></div>' : '')
      + '<input class="rcs-hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><label class="rcs-k" hidden><span>Sync key</span><input name="key" autocomplete="off" autocapitalize="characters" placeholder="XXXX-XXXX-XXXX"></label>'
      + '<p class="rcs-m" role="alert"></p><p class="rcs-fine">No card. No password. Free until ' + esc(UNTIL) + '. Your email is used only for this subscription and occasional news from Raining Cats &amp; Dogs.</p></form>';
    var f = $('form', host), box = host.closest('.rcs') || host;
    f.onsubmit = function (e) {
      e.preventDefault(); var m = $('.rcs-m', f), b = $('button', f), books = mode === 'pick' ? [f.dy.checked ? 'dy' : '', f.cy.checked ? 'cy' : ''].filter(Boolean) : ['dy', 'cy'];
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.email.value.trim())) { m.textContent = ERR['bad-email']; f.email.focus(); return; }
      if (!books.length) { m.textContent = 'Pick Dog Year, Cat Year or both.'; return; }
      m.textContent = ''; b.disabled = true; b.textContent = 'One moment';
      api('subscribe', { email: f.email.value.trim(), key: f.key.value, books: books, source: P, website: f.website.value }).then(function (r) {
        b.disabled = false; b.textContent = 'Subscribe free';
        if (r.ok) return success(box, r);
        if (r.error === 'have-key') $('.rcs-k', f).hidden = false;
        m.textContent = ERR[r.error] || 'Something went wrong. Please try again.';
      });
    };
  }
  function box(host, kind) {   // kind: dy, cy, both, pick
    host.className = 'rcs';
    if (sub) { host.className = 'rcs mini done'; host.innerHTML = '<p><b>You are subscribed.</b> Your notes sync on this device until ' + esc(new Date(sub.u).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })) + '.</p>'; return; }
    var t = { dy: ['Dog Year', 'A new breed every week, and the notes you write about your dog.'], cy: ['Cat Year', 'A new breed every week, and the notes you write about your cat.'] }[kind];
    var h = kind === 'dy' || kind === 'cy' ? '<p class="rcs-k0">Free until ' + esc(UNTIL) + '</p><h2>Subscribe to ' + t[0] + ', free</h2><p>' + t[1] + ' Subscribers keep their notes in one place that follows them from phone to laptop, and nothing is lost if the browser is cleared. <a href="/subscribe/">Why subscribe</a></p>'
      : kind === 'both' ? '<p class="rcs-k0">Free until ' + esc(UNTIL) + '</p><h2>Subscribe to Dog Year and Cat Year, free</h2><p>Keep your notes on every device and never lose them. One email, no card, no password. <a href="/subscribe/">Why subscribe</a></p>' : '';
    host.innerHTML = h + '<div class="rcs-form"></div>'; form($('.rcs-form', host), kind === 'pick' ? 'pick' : 'one');
  }
  function banner() {
    if (!OPEN || sub || /^\/(subscribe|admin|unlock|redeem|quiz)\b/.test(P)) return;
    var x = +ls('rc-sub-x') || 0; if (Date.now() - x < 3 * 86400000) return;
    var d = document.createElement('div'); d.className = 'rcb';
    d.innerHTML = '<span><b>Free until ' + esc(UNTIL) + '.</b> Subscribe to Dog Year and Cat Year. Your notes follow you to every device.</span><a class="rcb-go" href="/subscribe/">Subscribe free</a><button type="button" aria-label="Close">&times;</button>';
    $('button', d).onclick = function () { ls('rc-sub-x', String(Date.now())); d.remove(); };
    var pin = $('nav.pin'); if (pin) pin.parentNode.insertBefore(d, pin.nextSibling); else document.body.insertBefore(d, document.body.firstChild);
  }
  function initNotes() {
    var b = $('#notes'); if (!b) return; var ta = $('textarea', b), s = $('.saved', b); if (!ta || !s) return;
    var pre = /^\/CY2027/.test(P) ? 'cy27' : 'dy27', key = pre + ':' + b.dataset.key;
    if (!sub) { s.innerHTML = 'Notes are saved on this device only. <a href="/subscribe/">Subscribe free</a> to sync them everywhere until ' + esc(UNTIL) + '.'; return; }
    if (b.dataset.rcsync) return; b.dataset.rcsync = '1'; s.textContent = 'Synced to your account.';
    api('notes').then(function (r) {
      if (!r.ok) { if (r.error === 'not-subscribed') { ls('rc-sub', null); sub = null; initNotes(); } return; }
      Object.keys(r.notes || {}).forEach(function (k) { var n = r.notes[k], ts = +ls(k + ':ts') || 0; if (!ls(k) || ts < n.u) { ls(k, n.v); ls(k + ':title', n.t); ls(k + ':ts', String(n.u)); } });
      var v = ls(key); if (v != null && v !== ta.value && !ta.matches(':focus')) ta.value = v;
    });
    var t; ta.addEventListener('input', function () { clearTimeout(t); s.textContent = 'Saving…'; t = setTimeout(function () {
      api('note', { k: key, v: ta.value, t: b.dataset.title }).then(function (r) { if (r.ok) { ls(key + ':ts', String(r.u)); s.textContent = 'Saved and synced.'; } else s.textContent = 'Saved on this device. Sync will retry on your next note.'; });
    }, 1200); });
  }
  function start() {
    [].forEach.call(document.querySelectorAll('[data-rc-form]'), function (h) { if (OPEN || sub) box(h, h.getAttribute('data-rc-form')); else h.innerHTML = '<div class="rcs"><h2>The free subscription has ended</h2><p>It ran until ' + esc(UNTIL) + '. Your notes stay on your device and you can download them any time.</p></div>'; });
    banner(); initNotes();
  }
  api('offer').then(function (r) { if (r && r.ok && r.until) { UNTIL = new Date(r.until).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }); OPEN = r.open !== false; } }).then(function () {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
  });
})();
