/* Cert: draws a certificate on a canvas (1600 x 1130), and saves, prints or shares it. Shared by the Bitch-O-Meter,
   the rainingcad.com book quizzes and the Idiom Magic courses (each passes its own theme and words).
   Cert.draw(canvas, o) -> Promise. o = {theme, img, kicker, title, pre, name, body, score, seal:[lines], sign:[[name, role], [name, role]], brand}
   theme = {paper, tint, ink, soft, accent, accent2, frame, serif, sans, sealInk}
   Cert.row(o) -> share buttons HTML, Cert.bind(el, o) wires copy and native share. o = {url, text, title} */
var Cert = (function () {
  function img(src) { return new Promise(function (r) { if (!src) return r(null); var i = new Image(); i.onload = function () { r(i); }; i.onerror = function () { r(null); }; i.src = src; }); }
  function lines(c, text, maxW) {
    var w = String(text).split(/\s+/), out = [], cur = '';
    w.forEach(function (x) { var t = cur ? cur + ' ' + x : x; if (c.measureText(t).width > maxW && cur) { out.push(cur); cur = x; } else cur = t; });
    if (cur) out.push(cur); return out;
  }
  function fit(c, font, size, text, maxW) { var s = size; do { c.font = font.replace('#', s); s -= 2; } while (c.measureText(text).width > maxW && s > 20); }
  function spaced(c, text, x, y, sp) { try { c.letterSpacing = sp + 'px'; } catch (e) {} c.fillText(text, x, y); try { c.letterSpacing = '0px'; } catch (e) {} }
  function star(c, x, y, r1, r2, n) { c.beginPath(); for (var i = 0; i < n * 2; i++) { var r = i % 2 ? r2 : r1, a = Math.PI * i / n - Math.PI / 2; c.lineTo(x + r * Math.cos(a), y + r * Math.sin(a)); } c.closePath(); }
  async function draw(cv, o) {
    var T = o.theme, W = 1600, H = 1130; cv.width = W; cv.height = H; var c = cv.getContext('2d');
    try { await Promise.all(['800 60px ' + T.serif, 'italic 600 60px ' + T.serif, '700 20px ' + T.sans, '400 30px ' + T.serif].map(function (f) { return document.fonts.load(f); })); } catch (e) {}
    var pic = await img(o.img);
    c.fillStyle = T.paper; c.fillRect(0, 0, W, H);
    c.strokeStyle = T.tint; c.lineWidth = 1; for (var d = -H; d < W; d += 22) { c.beginPath(); c.moveTo(d, 0); c.lineTo(d + H, H); c.stroke(); }
    c.fillStyle = T.paper; c.fillRect(96, 96, W - 192, H - 192);
    c.strokeStyle = T.frame; c.lineWidth = 16; c.strokeRect(40, 40, W - 80, H - 80);
    c.strokeStyle = T.accent; c.lineWidth = 3; c.strokeRect(78, 78, W - 156, H - 156);
    c.lineWidth = 1.5; c.strokeRect(90, 90, W - 180, H - 180);
    [[78, 78], [W - 78, 78], [78, H - 78], [W - 78, H - 78]].forEach(function (p) { c.save(); c.translate(p[0], p[1]); c.rotate(Math.PI / 4); c.fillStyle = T.accent; c.fillRect(-14, -14, 28, 28); c.fillStyle = T.paper; c.fillRect(-6, -6, 12, 12); c.restore(); });
    c.textAlign = 'center'; c.textBaseline = 'alphabetic';
    var y = 190;
    if (pic) {
      var R = 92, cx = W / 2, cy = 200; c.save(); c.beginPath(); c.arc(cx, cy, R, 0, 7); c.clip();
      var s = Math.max(2 * R / pic.width, 2 * R / pic.height), iw = pic.width * s, ih = pic.height * s; c.drawImage(pic, cx - iw / 2, cy - R - (ih - 2 * R) * .2, iw, ih); c.restore();
      c.strokeStyle = T.accent; c.lineWidth = 7; c.beginPath(); c.arc(cx, cy, R + 4, 0, 7); c.stroke(); y = 350;
    }
    c.fillStyle = T.accent2; c.font = '700 24px ' + T.sans; spaced(c, String(o.kicker || 'Official certificate').toUpperCase(), W / 2, y, 7);
    c.fillStyle = T.ink; fit(c, '800 #px ' + T.serif, 96, o.title, 1240); c.fillText(o.title, W / 2, y + 96);
    c.fillStyle = T.soft; c.font = 'italic 400 32px ' + T.serif; c.fillText(o.pre || 'This certifies that', W / 2, y + 156);
    c.fillStyle = T.accent2; fit(c, 'italic 600 #px ' + T.serif, 74, o.name, 1100); c.fillText(o.name, W / 2, y + 236);
    var nw = Math.min(1100, Math.max(420, c.measureText(o.name).width + 80)); c.strokeStyle = T.ink; c.lineWidth = 2; c.beginPath(); c.moveTo(W / 2 - nw / 2, y + 258); c.lineTo(W / 2 + nw / 2, y + 258); c.stroke();
    c.fillStyle = T.ink; c.font = '400 29px ' + T.serif; var L = lines(c, o.body, 1120).slice(0, 4);
    L.forEach(function (l, i) { c.fillText(l, W / 2, y + 308 + i * 40); });
    var by = y + 308 + L.length * 40 + 18;
    if (o.score) { c.fillStyle = T.accent2; c.font = '700 21px ' + T.sans; spaced(c, String(o.score).toUpperCase(), W / 2, by, 4); }
    var sy = H - 175;
    (o.sign || []).slice(0, 2).forEach(function (sg, i) {
      var x = i ? W - 360 : 360; c.fillStyle = T.ink; fit(c, 'italic 600 #px ' + T.serif, 40, sg[0], 380); c.fillText(sg[0], x, sy);
      c.strokeStyle = T.ink; c.lineWidth = 1.5; c.beginPath(); c.moveTo(x - 190, sy + 16); c.lineTo(x + 190, sy + 16); c.stroke();
      c.fillStyle = T.soft; c.font = '700 15px ' + T.sans; spaced(c, String(sg[1]).toUpperCase(), x, sy + 44, 3);
    });
    var sx = W / 2, scy = H - 190; c.fillStyle = T.accent; star(c, sx, scy, 96, 84, 24); c.fill();
    c.strokeStyle = T.sealInk; c.lineWidth = 2.5; c.beginPath(); c.arc(sx, scy, 70, 0, 7); c.stroke(); c.beginPath(); c.arc(sx, scy, 62, 0, 7); c.stroke();
    var S = (o.seal || []).slice(0, 3); c.fillStyle = T.sealInk;
    S.forEach(function (t, i) { fit(c, '800 #px ' + T.sans, 22, t, 110); c.fillText(t, sx, scy + (i - (S.length - 1) / 2) * 26 + 8); });
    if (o.brand) { c.fillStyle = T.soft; c.font = '700 14px ' + T.sans; spaced(c, String(o.brand).toUpperCase(), W / 2, H - 52, 4); }
  }
  function blob(cv) { return new Promise(function (r) { cv.toBlob(r, 'image/png'); }); }
  function download(cv, name) { return blob(cv).then(function (b) { var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = name; document.body.appendChild(a); a.click(); a.remove(); }); }
  function print(cv) {
    var d = document.getElementById('cert-print'); if (!d) { d = document.createElement('div'); d.id = 'cert-print'; document.body.appendChild(d); }
    if (!document.getElementById('cert-print-css')) { var st = document.createElement('style'); st.id = 'cert-print-css'; st.textContent = '#cert-print{display:none}@media print{@page{size:landscape;margin:8mm}html.cert-printing body>*:not(#cert-print){display:none!important}html.cert-printing #cert-print{display:block}#cert-print img{width:100%;height:auto}}'; document.head.appendChild(st); }
    d.innerHTML = '<img alt="" src="' + cv.toDataURL('image/png') + '">'; document.documentElement.classList.add('cert-printing');
    setTimeout(function () { window.print(); document.documentElement.classList.remove('cert-printing'); }, 60);
  }
  function shareImage(cv, name, o) {
    return blob(cv).then(function (b) {
      var f = new File([b], name, { type: 'image/png' });
      if (navigator.canShare && navigator.canShare({ files: [f] })) return navigator.share({ files: [f], title: o.title, text: o.text + ' ' + o.url }).then(function () { return true; }, function () { return true; });
      return false;
    });
  }
  function enc(s) { return encodeURIComponent(s); }
  function row(o) {
    var t = o.text, u = o.url, both = t + ' ' + u;
    return '<div class="cert-share" role="group" aria-label="Share">'
      + '<a href="https://wa.me/?text=' + enc(both) + '" target="_blank" rel="noopener">WhatsApp</a>'
      + '<a href="https://www.facebook.com/sharer/sharer.php?u=' + enc(u) + '" target="_blank" rel="noopener">Facebook</a>'
      + '<a href="https://twitter.com/intent/tweet?text=' + enc(t) + '&url=' + enc(u) + '" target="_blank" rel="noopener">X</a>'
      + '<a href="https://www.linkedin.com/sharing/share-offsite/?url=' + enc(u) + '" target="_blank" rel="noopener">LinkedIn</a>'
      + '<a href="mailto:?subject=' + enc(o.title || '') + '&body=' + enc(both) + '">Email</a>'
      + '<button type="button" data-cert-copy>Copy link</button>'
      + (navigator.share ? '<button type="button" data-cert-native>More</button>' : '') + '</div>';
  }
  function bind(el, o) {
    var cp = el.querySelector('[data-cert-copy]'), nt = el.querySelector('[data-cert-native]');
    if (cp) cp.onclick = function () { var done = function () { cp.textContent = 'Copied'; setTimeout(function () { cp.textContent = 'Copy link'; }, 1800); }; if (navigator.clipboard) navigator.clipboard.writeText(o.text + ' ' + o.url).then(done, done); };
    if (nt) nt.onclick = function () { navigator.share({ title: o.title, text: o.text, url: o.url }).catch(function () {}); };
  }
  return { draw: draw, download: download, print: print, shareImage: shareImage, row: row, bind: bind };
})();
