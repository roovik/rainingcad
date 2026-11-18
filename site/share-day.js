// Dog Year 2027 and Cat Year 2027 day pages: "Share this day".
// The reader chooses whether to include their notes, sees (and can edit) exactly what will be shared, and sees a preview first.
// Without notes, the link is the day's own page. With notes, we make a private link (rainingcad.com/s/<id>/) that shows the day
// and the shared words, with its own link-preview picture; only people with the link can open it, and the reader can stop sharing.
(function () {
  'use strict';
  var box0 = document.getElementById('notes'); if (!box0) return;
  var ta0 = box0.querySelector('textarea'), path = location.pathname.replace(/\/?$/, '/');
  var DOG = /^\/DY2027\//.test(path), BOOK = DOG ? 'Dog Year 2027' : 'Cat Year 2027', TAG = DOG ? 'Every Day Has Its Dog' : 'Every Day Has Its Cat';
  var SITE = 'https://rainingcad.com', DAY_URL = SITE + path, SK = 'rcd-shares';
  function $(s, r) { return (r || document).querySelector(s); }
  function meta(p) { var m = document.querySelector('meta[property="' + p + '"]'); return m ? m.getAttribute('content') : ''; }
  var kick = ($('.kick') || {}).textContent || '', pic = $('img.big'), breed = pic ? pic.getAttribute('alt') || '' : '';
  var text0 = ($('.daytxt') || {}).textContent || meta('og:description') || '';
  var TITLE = (meta('og:title') || document.title).replace(/\s*·\s*(Dog|Cat) Year 2027\s*$/, '');
  if (!pic) { pic = new Image(); pic.src = meta('og:image'); }
  var C = { paper: '#F3F2EC', ink: '#2A2A2D', soft: '#6F6F74', gold: '#B0822B', deep: '#876217' };
  function store() { try { return JSON.parse(localStorage.getItem(SK) || '{}'); } catch (e) { return {}; } }
  function keep(o) { try { localStorage.setItem(SK, JSON.stringify(o)); } catch (e) {} }
  function sum(s) { var h = 0; for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return String(h); }
  function api(p, body) {
    return fetch('/api/' + p, { method: 'POST', credentials: 'same-origin', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return { ok: false, error: 'server' }; }); }, function () { return { ok: false, error: 'offline' }; });
  }
  function fonts() { return document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve(); }
  function lines(x, text, max) {
    var out = [];
    String(text).split('\n').forEach(function (para) { var cur = ''; para.split(/\s+/).forEach(function (w) { var t = cur ? cur + ' ' + w : w; if (x.measureText(t).width > max && cur) { out.push(cur); cur = w; } else cur = t; }); out.push(cur); });
    return out;
  }
  function clip(tl, n) { if (tl.length > n) { tl = tl.slice(0, n); tl[n - 1] = tl[n - 1].replace(/\s*\S*$/, '') + ' …'; } return tl; }
  function cover(x, img, dx, dy, dw, dh) {
    if (!img || !img.naturalWidth) { x.fillStyle = '#ddd'; x.fillRect(dx, dy, dw, dh); return; }
    var iw = img.naturalWidth, ih = img.naturalHeight, s = Math.max(dw / iw, dh / ih), sw = dw / s, sh = dh / s;
    x.drawImage(img, (iw - sw) / 2, (ih - sh) * .35, sw, sh, dx, dy, dw, dh);
  }
  // the picture card (1080 x 1350): photo on top, the day and your notes below
  function card(words) {
    var W = 1080, H = 1350, c = document.createElement('canvas'); c.width = W; c.height = H; var x = c.getContext('2d'), pad = 70;
    return fonts().then(function () {
      x.fillStyle = C.paper; x.fillRect(0, 0, W, H);
      // measure the words first, so the photo takes all the room they leave
      x.font = 'italic 34px Spectral, Georgia, serif'; var dl = clip(lines(x, text0, W - pad * 2), words ? 2 : 4);
      x.font = '400 31px Spectral, Georgia, serif'; var wl = words ? clip(lines(x, words, W - pad * 2 - 56), 9) : [];
      var need = 66 + 70 + dl.length * 46 + (words ? 34 + 40 + wl.length * 42 : 0) + 130;
      var ph = Math.max(560, H - need); cover(x, pic, 0, 0, W, ph);
      x.fillStyle = C.gold; x.fillRect(0, ph, W, 8);
      var y = ph + 66;
      x.fillStyle = C.deep; x.font = '700 24px Hanken, system-ui, sans-serif'; x.fillText((BOOK + ' · ' + kick).toUpperCase(), pad, y);
      x.fillStyle = C.ink; x.font = '800 54px Spectral, Georgia, serif'; y += 70; x.fillText(breed || TITLE, pad, y);
      x.font = 'italic 34px Spectral, Georgia, serif'; x.fillStyle = C.soft;
      dl.forEach(function (l) { y += 46; x.fillText(l, pad, y); });
      if (words) {
        y += 34; x.font = '400 31px Spectral, Georgia, serif';
        var tl = clip(wl, Math.max(1, Math.floor((H - 120 - y - 40) / 42)));
        x.fillStyle = '#fff'; x.fillRect(pad, y, W - pad * 2, 40 + tl.length * 42); x.fillStyle = C.gold; x.fillRect(pad, y, 6, 40 + tl.length * 42);
        x.fillStyle = C.ink; tl.forEach(function (l, i) { x.fillText(l, pad + 30, y + 52 + i * 42); });
      }
      x.fillStyle = C.deep; x.font = '700 24px Hanken, system-ui, sans-serif'; x.fillText((words ? 'From my notes · ' : '') + 'rainingcad.com/' + (DOG ? 'DY2027' : 'CY2027'), pad, H - 58);
      return c;
    });
  }
  // the link preview picture (1200 x 630): what WhatsApp, Facebook, X, LinkedIn and email show for a link with your notes
  function cardOG(words) {
    var W = 1200, H = 630, L = 560, c = document.createElement('canvas'); c.width = W; c.height = H; var x = c.getContext('2d'), pad = 44, R = W - L - pad * 2, X0 = L + pad;
    return fonts().then(function () {
      x.fillStyle = C.paper; x.fillRect(0, 0, W, H); cover(x, pic, 0, 0, L, H); x.fillStyle = C.gold; x.fillRect(L, 0, 6, H);
      var y = pad + 18;
      x.fillStyle = C.deep; x.font = '700 19px Hanken, system-ui, sans-serif'; x.fillText(BOOK.toUpperCase(), X0, y);
      x.fillStyle = C.soft; x.font = '600 22px Hanken, system-ui, sans-serif'; y += 36; x.fillText(kick.replace(/^Week \d+ · /, ''), X0, y);
      x.fillStyle = C.ink; x.font = '800 46px Spectral, Georgia, serif';
      clip(lines(x, breed || TITLE, R), 2).forEach(function (l) { y += 54; x.fillText(l, X0, y); });
      y += 18; x.font = 'italic 28px Spectral, Georgia, serif'; x.fillStyle = words ? C.ink : C.soft;
      clip(lines(x, words ? '“' + words.replace(/\s+/g, ' ') + '”' : text0, R), Math.max(1, Math.floor((H - 70 - y) / 36))).forEach(function (l) { y += 36; x.fillText(l, X0, y); });
      x.fillStyle = C.deep; x.font = '700 18px Hanken, system-ui, sans-serif'; x.fillText('RAININGCAD.COM', X0, H - 32);
      return c;
    });
  }

  var box = null, link = DAY_URL;
  function build() {
    box = document.createElement('div'); box.className = 'sh-box'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-labelledby', 'sh-h');
    box.innerHTML = '<div class="sh-card"><button type="button" class="sh-x" id="sh-close" aria-label="Close">&times;</button>'
      + '<h2 id="sh-h">Share this day</h2><p class="sh-sub"></p>'
      + '<label class="sh-inc"><input type="checkbox" id="sh-inc"> Include my notes</label>'
      + '<div id="sh-wr" hidden><textarea id="sh-text" rows="5" aria-label="What will be shared"></textarea>'
      + '<p class="sh-note">Only the words in this box are shared, and you can edit them first. They go on a private page that anyone with the link can open. You can stop sharing it at any time.</p>'
      + '<p><button type="button" class="sh-b dark" id="sh-make">Make my share link</button></p></div>'
      + '<div class="sh-lab">Preview</div><div class="sh-pvg"><div class="sh-lp"><img id="sh-og" alt="Link preview picture"><div class="sh-lpt"><b id="sh-lpt"></b><span id="sh-lpd"></span><small>rainingcad.com</small></div></div>'
      + '<figure class="sh-cf"><img id="sh-card" alt="Picture card"><figcaption>Picture card · tap to enlarge</figcaption></figure></div>'
      + '<div id="sh-go"><p class="sh-link"><input id="sh-url" readonly aria-label="Link"><button type="button" class="sh-b" id="sh-copy">Copy link</button></p>'
      + '<div class="sh-btns"><button type="button" class="sh-b dark" id="sh-native" hidden>Share…</button><a class="sh-b" id="sh-mail">Email</a>'
      + '<a class="sh-b" id="sh-wa" target="_blank" rel="noopener">WhatsApp</a><a class="sh-b" id="sh-fb" target="_blank" rel="noopener">Facebook</a>'
      + '<a class="sh-b" id="sh-x" target="_blank" rel="noopener">X</a><a class="sh-b" id="sh-in" target="_blank" rel="noopener">LinkedIn</a><button type="button" class="sh-b" id="sh-img">Save picture</button></div>'
      + '<p class="sh-note">For Instagram, save the picture and post it from your photos.</p>'
      + '<p id="sh-stopp" hidden><button type="button" class="sh-stop" id="sh-stop">Stop sharing my notes</button></p></div><p class="sh-status" id="sh-status" aria-live="polite"></p></div>';
    document.body.appendChild(box);
    var css = document.createElement('style');
    css.textContent = '.sh-open{font:700 12px Hanken,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#fff;background:#876217;border:2px solid #876217;padding:10px 16px;cursor:pointer;margin-left:8px}'
      + '.sh-box{position:fixed;inset:0;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;z-index:999;padding:14px}.sh-box[hidden]{display:none}'
      + '.sh-card{background:#F3F2EC;color:#2A2A2D;max-width:580px;width:100%;max-height:94vh;overflow:auto;padding:24px 22px;position:relative;border-top:4px solid #B0822B;font:16px/1.5 Hanken,sans-serif}'
      + '.sh-card h2{font:800 28px Spectral,serif;margin:0}.sh-sub{color:#6F6F74;margin:2px 0 14px;font-size:14px}.sh-x{position:absolute;top:8px;right:12px;border:0;background:none;font-size:30px;cursor:pointer;color:#6F6F74}'
      + '.sh-inc{display:flex;gap:8px;align-items:center;font-weight:700;margin:4px 0 10px}.sh-card textarea{width:100%;box-sizing:border-box;font:17px/1.5 Spectral,serif;padding:10px;border:1px solid rgba(42,42,45,.25);background:#fff}'
      + '.sh-note{font-size:13px;color:#6F6F74;margin:8px 0}.sh-lab{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#876217;margin:14px 0 6px}'
      + '.sh-pvg{display:grid;grid-template-columns:1fr 100px;gap:12px;align-items:start}.sh-lp{border:1px solid rgba(42,42,45,.2);background:#fff;overflow:hidden}.sh-lp img{display:block;width:100%;aspect-ratio:1200/630;object-fit:cover;background:#ddd}'
      + '.sh-lpt{padding:8px 12px 10px;display:flex;flex-direction:column;gap:2px;font-size:13px;line-height:1.35}.sh-lpt span{color:#555;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.sh-lpt small{color:#888}'
      + '.sh-cf{margin:0;cursor:zoom-in}.sh-cf img{width:100%;aspect-ratio:1080/1350;display:block;box-shadow:0 1px 4px rgba(0,0,0,.25)}.sh-cf figcaption{font-size:11px;color:#888;text-align:center;margin-top:4px}'
      + '.sh-pvg.big{grid-template-columns:1fr}.sh-pvg.big .sh-lp{display:none}.sh-pvg.big .sh-cf{cursor:zoom-out;max-width:380px;margin:0 auto}'
      + '.sh-link{display:flex;gap:8px;margin:14px 0 10px}.sh-link input{flex:1;min-width:0;font:14px Hanken,sans-serif;padding:8px 10px;border:1px solid rgba(42,42,45,.25)}'
      + '.sh-btns{display:flex;flex-wrap:wrap;gap:8px}.sh-b{font:700 12px Hanken,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#876217;background:none;border:2px solid #876217;padding:9px 14px;cursor:pointer;text-decoration:none;display:inline-block}'
      + '.sh-b.dark{background:#876217;color:#fff}.sh-b:disabled{opacity:.5}.sh-status{font-size:14px;color:#876217;min-height:1em;margin:10px 0 0}.sh-stop{background:none;border:0;color:#a33;text-decoration:underline;cursor:pointer;font:14px Hanken,sans-serif;padding:0}';
    document.head.appendChild(css);
    $('.sh-sub', box).textContent = kick + (breed ? ' · ' + breed : '');
    $('#sh-close', box).onclick = close;
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) close(); });
    $('#sh-inc', box).onchange = sync; $('#sh-text', box).oninput = sync; $('#sh-make', box).onclick = make; $('#sh-stop', box).onclick = stop;
    $('.sh-cf', box).onclick = function () { $('.sh-pvg', box).classList.toggle('big'); };
    $('#sh-copy', box).onclick = function () { var u = $('#sh-url', box); u.select(); (navigator.clipboard ? navigator.clipboard.writeText(u.value) : Promise.reject()).then(function () { say('Link copied.'); }, function () { document.execCommand('copy'); say('Link copied.'); }); };
    $('#sh-img', box).onclick = function () { card(words()).then(function (c) { c.toBlob(function (b) { var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = (DOG ? 'dog' : 'cat') + '-year-' + path.split('/').filter(Boolean).slice(1).join('-') + '.png'; document.body.appendChild(a); a.click(); a.remove(); say('Picture saved.'); }, 'image/png'); }); };
    if (navigator.share) { var n = $('#sh-native', box); n.hidden = false; n.onclick = native; }
  }
  function open() {
    if (!box) build();
    var w = ta0.value.trim(), inc = $('#sh-inc', box);
    $('#sh-text', box).value = w; inc.checked = false; inc.disabled = !w; inc.parentNode.title = w ? '' : 'No notes on this page yet';
    sync(); box.hidden = false; $('#sh-close', box).focus();
  }
  function close() { box.hidden = true; }
  function say(m) { $('#sh-status', box).textContent = m; }
  function words() { return $('#sh-inc', box).checked ? $('#sh-text', box).value.trim() : ''; }
  function msg() { var w = words(); return TITLE + ' · ' + BOOK + '\n' + text0 + (w ? '\n\nMy notes: ' + w : ''); }
  var pvT = null;
  function preview() {
    clearTimeout(pvT); pvT = setTimeout(function () {
      var w = words();
      $('#sh-lpt', box).textContent = TITLE + ' · ' + BOOK; $('#sh-lpd', box).textContent = w ? w.replace(/\s+/g, ' ') : text0;
      if (w) cardOG(w).then(function (c) { $('#sh-og', box).src = c.toDataURL('image/jpeg', .85); }); else $('#sh-og', box).src = meta('og:image');
      card(w).then(function (c) { $('#sh-card', box).src = c.toDataURL('image/jpeg', .8); });
    }, 250);
  }
  function sync() {
    preview();
    var w = words(), inc = $('#sh-inc', box).checked, saved = store()[path];
    $('#sh-wr', box).hidden = !inc;
    link = !inc ? DAY_URL : (saved && saved.sum === sum(w) ? SITE + '/s/' + saved.id + '/' : null);
    $('#sh-go', box).hidden = !link; $('#sh-make', box).textContent = saved ? 'Update my share link' : 'Make my share link';
    $('#sh-stopp', box).hidden = !(inc && saved);
    if (!link) { say(''); return; }
    var short = TITLE + (w ? ' — ' + (w.length > 160 ? w.slice(0, 157).replace(/\s*\S*$/, '') + ' …' : w) : '');
    $('#sh-url', box).value = link;
    $('#sh-mail', box).href = 'mailto:?subject=' + encodeURIComponent(TITLE + ' · ' + BOOK) + '&body=' + encodeURIComponent(msg() + '\n\n' + link);
    $('#sh-wa', box).href = 'https://wa.me/?text=' + encodeURIComponent(msg() + '\n\n' + link);
    $('#sh-fb', box).href = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(link);
    $('#sh-x', box).href = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(short.slice(0, 230)) + '&url=' + encodeURIComponent(link);
    $('#sh-in', box).href = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(link);
  }
  function make() {
    var w = words(); if (!w) { say('There is nothing to share yet.'); return; }
    var all = store(), old = all[path];
    say('Making your link…'); $('#sh-make', box).disabled = true;
    cardOG(w).then(function (c) { return api('share', { path: path, text: w, image: c.toDataURL('image/jpeg', .85).split(',')[1] }); }).then(function (r) {
      $('#sh-make', box).disabled = false;
      if (!r.ok) { say(r.error === 'slow-down' ? 'Too many links at once. Please try again in a little while.' : r.error === 'offline' ? 'You seem to be offline. Please try again.' : 'Sorry, the link could not be made.'); return; }
      if (old) api('share/' + old.id + '/delete', { secret: old.secret });
      all[path] = { id: r.id, secret: r.secret, sum: sum(w) }; keep(all); sync(); say('Your link is ready.');
    });
  }
  function stop() {
    var all = store(), s = all[path]; if (!s) return;
    api('share/' + s.id + '/delete', { secret: s.secret }).then(function (r) {
      if (!r.ok && r.error !== 'not-found') { say('Sorry, that did not work. Please try again.'); return; }
      delete all[path]; keep(all); $('#sh-inc', box).checked = false; sync(); say('Your notes are no longer shared. The link now shows nothing.');
    });
  }
  function native() {
    if (!link) return;
    card(words()).then(function (c) { return new Promise(function (ok) { c.toBlob(ok, 'image/png'); }); }).then(function (b) {
      var f = b && window.File ? new File([b], (DOG ? 'dog' : 'cat') + '-year.png', { type: 'image/png' }) : null, data = { title: TITLE, text: msg(), url: link };
      if (f && navigator.canShare && navigator.canShare({ files: [f] })) data.files = [f];
      return navigator.share(data);
    }).catch(function () {});
  }
  var b = document.createElement('button'); b.type = 'button'; b.className = 'sh-open'; b.textContent = 'Share this day';
  var dl = box0.querySelector('.dl'); if (dl) dl.parentNode.insertBefore(b, dl.nextSibling); else box0.appendChild(b);
  b.addEventListener('click', open);
})();
