/* rainingcad.com: access codes (unlock, redeem, admin) and the book quizzes with their certificates. Data in #rc-data (tools/build_rcd.py). Uses /cert.js. */
(function () {
  var D = JSON.parse(document.getElementById('rc-data').textContent), root = document.getElementById('rc-app'), Q = new URLSearchParams(location.search);
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  function $(s, el) { return (el || document).querySelector(s); }
  function st(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) {} return null; }
  function api(p, body, hdr) { var o = body ? { method: 'POST', headers: Object.assign({ 'content-type': 'application/json' }, hdr || {}), body: JSON.stringify(body) } : { headers: hdr || {} }; return fetch('/api/' + p, o).then(function (r) { return r.json().catch(function () { return { ok: false, error: 'network' }; }); }, function () { return { ok: false, error: 'network' }; }); }
  var ERR = { 'bad-code': 'That code is not right. Check the letters and try again.', 'code-expired': 'That code has ended.', 'code-used-up': 'That code has been used as many times as it allows.', 'slow-down': 'Too many tries. Wait a few minutes.', network: 'No connection. Try again.', 'wrong-key': 'Wrong admin key.', 'no-admin-key': 'The admin key is not set yet. Add ADMIN_KEY as a secret in the Cloudflare dashboard.', 'pick-books': 'Tick what the code opens.', 'code-taken': 'That code already exists.' };
  function msg(e) { return ERR[e] || 'Something went wrong (' + esc(e) + ').'; }
  var NAMES = { all: 'Everything', books: 'Every book' }; (D.books || []).forEach(function (b) { NAMES[b.id] = b.title; });
  function bookOf(k) { for (var i = 0; i < (D.books || []).length; i++) if (D.books[i].id === k) return D.books[i]; return null; }
  function day(t) { return new Date(t).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }); }
  function codeForm(after) {
    var f = document.createElement('form'); f.className = 'rc-box';
    f.innerHTML = '<h2>Enter your access code</h2><label>Code <input name="code" required autocomplete="off" autocapitalize="characters" placeholder="RCD-XXXX-XXXX"></label><button class="btn main" type="submit">Open</button><p class="rc-err" role="alert"></p>';
    f.onsubmit = function (e) { e.preventDefault(); var b = $('button', f); b.disabled = true; api('redeem', { code: f.code.value.trim() }).then(function (r) { b.disabled = false; if (!r.ok) { $('.rc-err', f).textContent = msg(r.error).replace(/&amp;/g, '&'); return; } after(r); }); };
    return f;
  }
  function haveList(A) { var ks = Object.keys(A || {}); return ks.length ? '<ul>' + ks.map(function (k) { return '<li><b>' + esc(NAMES[k] || k) + '</b> until ' + day(A[k]) + '</li>'; }).join('') + '</ul>' : '<p>No books open on this device yet.</p>'; }

  // ---------------------------------------------------------------- unlock: a locked chapter sends readers here
  if (D.page === 'unlock') {
    var c = Q.get('c') || '', B = bookOf(c), next = Q.get('next') || (B ? B.url : '/books/'), l = Q.get('l');
    if (!/^\/inside\//.test(next)) next = B ? B.url : '/books/';
    root.innerHTML = '<p class="kick">' + esc(B ? B.title : 'Raining Cats & Dogs') + ', read inside</p><h1>' + (l && /^\d+$/.test(l) ? 'Chapter ' + esc(l) + ' is in the full book' : 'Open the full book') + '</h1><p class="lead">The opening pages and chapter 1 are free. An access code opens the whole book on this device.</p>';
    root.appendChild(codeForm(function () { location.replace(next); }));
    var buy = (D.buy || {})[c]; if (buy) root.insertAdjacentHTML('beforeend', '<div class="rc-box"><h3>Prefer it in print?</h3><div class="btns">' + buy.map(function (x) { return '<a class="btn" href="' + esc(x[1]) + '" rel="noopener">' + esc(x[0]) + '</a>'; }).join('') + '</div></div>');
    if (B) root.insertAdjacentHTML('beforeend', '<p><a href="' + esc(B.url) + '">Back to the book</a></p>');
    return;
  }
  // ---------------------------------------------------------------- redeem: any code, and what this device can read
  if (D.page === 'redeem') {
    root.innerHTML = '<p class="kick">Access codes</p><h1>Have a code?</h1><p class="lead">Enter it here to read Raining Cats &amp; Dogs books online, on this device.</p>';
    var have = document.createElement('div'); have.className = 'rc-box';
    var show = function () { api('access').then(function (r) { var A = (r && r.access) || {}; have.innerHTML = '<h3>Open on this device</h3>' + haveList(A) + '<div class="btns">' + D.books.map(function (b) { return '<a class="btn" href="' + b.url + '">' + esc(b.title) + '</a>'; }).join('') + '</div>'; }); };
    root.appendChild(codeForm(function (r) { show(); root.querySelector('.rc-err').innerHTML = '<span class="rc-ok">Done. ' + esc(r.books.map(function (k) { return NAMES[k] || k; }).join(', ')) + ' open until ' + day(r.until) + '.</span>'; }));
    root.appendChild(have); show(); return;
  }
  // ---------------------------------------------------------------- admin: make codes, see uses. The key stays in this browser tab only.
  if (D.page === 'admin') {
    var K = null; try { K = sessionStorage.getItem('rc-admin'); } catch (e) {}
    var signin = function (err) {
      root.innerHTML = '<p class="kick">Owner</p><h1>Codes admin</h1><form class="rc-box" id="ak"><label>Admin key <input name="k" type="password" required autocomplete="current-password"></label><button class="btn main" type="submit">Sign in</button><p class="rc-err">' + (err ? msg(err) : '') + '</p></form>';
      $('#ak').onsubmit = function (e) { e.preventDefault(); K = this.k.value; try { sessionStorage.setItem('rc-admin', K); } catch (x) {} load(); };
    };
    var load = function () {
      if (!K) return signin();
      api('admin/codes', null, { 'x-admin-key': K }).then(function (r) {
        if (!r.ok) { try { sessionStorage.removeItem('rc-admin'); } catch (x) {} K = null; return signin(r.error); }
        var box = function (id, t, strong) { return '<label class="rc-chk"><input type="checkbox" name="books" value="' + esc(id) + '">' + (strong ? '<b>' + esc(t) + '</b>' : esc(t)) + '</label>'; };
        root.innerHTML = '<p class="kick">Owner</p><h1>Codes admin</h1><p class="lead">A code opens one book, several, every book or everything, on the device where it is entered. One use for a gift or a sale, many uses for a coupon.</p>'
          + '<form class="rc-box" id="mk"><h2>Make codes</h2><fieldset style="border:0;padding:0;margin:0"><legend class="kick" style="margin:8px 0">Opens</legend>' + box('all', 'Everything', 1) + box('books', 'Every book', 1) + D.books.map(function (b) { return box(b.id, b.title); }).join('') + '</fieldset>'
          + '<label>Days of access <input name="days" type="number" min="1" max="3650" value="365"></label><label>Uses per code <input name="uses" type="number" min="1" max="100000" value="1"></label>'
          + '<label>Your own code (optional) <input name="custom" maxlength="24" placeholder="PAWS10"></label><label>How many random codes <input name="count" type="number" min="1" max="100" value="1"></label>'
          + '<label>Ends on (optional) <input name="expires" type="date"></label><label>Note <input name="note" maxlength="200" placeholder="Newsletter, gift, launch"></label><button class="btn main" type="submit">Make</button><p class="rc-err" role="alert"></p></form>'
          + '<h2>Codes</h2>' + (r.codes.length ? '<div class="rc-wrapt"><table class="rc-tbl"><thead><tr><th>Code</th><th>Opens</th><th>Days</th><th>Used</th><th>Ends</th><th>Note</th><th>Made</th><th></th></tr></thead><tbody>' + r.codes.map(function (c) {
            var live = !(c.expires && c.expires < Date.now()) && c.uses < c.uses_max;
            return '<tr><td><code>' + esc(c.code) + '</code></td><td>' + esc(c.books.split(',').map(function (k) { return NAMES[k] || k; }).join(', ')) + '</td><td>' + c.days + '</td><td>' + c.uses + ' of ' + c.uses_max + '</td><td>' + (c.expires ? day(c.expires) : '') + '</td><td>' + esc(c.note || '') + '</td><td>' + day(c.created) + '</td><td>' + (live ? '<button class="btn" type="button" data-end="' + esc(c.code) + '" style="padding:6px 10px">End</button>' : 'Ended') + '</td></tr>'; }).join('') + '</tbody></table></div>' : '<p>None yet.</p>')
          + '<p><button class="btn" type="button" id="so">Sign out</button></p>';
        $('#mk').onsubmit = function (e) {
          e.preventDefault(); var f = this, books = [].slice.call(f.querySelectorAll('input[name=books]:checked')).map(function (i) { return i.value; });
          if (!books.length) { $('.rc-err', f).textContent = msg('pick-books'); return; }
          api('admin/code', { books: books, days: f.days.value, uses: f.uses.value, custom: f.custom.value, count: f.count.value, expires: f.expires.value, note: f.note.value }, { 'x-admin-key': K }).then(function (x) {
            if (!x.ok) { $('.rc-err', f).textContent = msg(x.error); return; } load(); setTimeout(function () { var e2 = $('#mk .rc-err'); if (e2) e2.innerHTML = '<span class="rc-ok">New: ' + x.codes.map(esc).join(' ') + '</span>'; }, 300);
          });
        };
        [].forEach.call(root.querySelectorAll('[data-end]'), function (b) { b.onclick = function () { api('admin/code-end', { code: b.dataset.end }, { 'x-admin-key': K }).then(load); }; });
        $('#so').onclick = function () { try { sessionStorage.removeItem('rc-admin'); } catch (x) {} K = null; signin(); };
      });
    };
    load(); return;
  }

  // ---------------------------------------------------------------- quizzes and certificates
  var CATS = /cat/i.test(D.book);
  var TH = { paper: '#FBFAF6', tint: 'rgba(176,130,43,.08)', ink: '#2A2A2D', soft: '#6F6F74', accent: '#B0822B', accent2: '#7a2a2a', frame: '#2A2A2D', serif: 'Spectral,Georgia,serif', sans: 'Hanken,system-ui,sans-serif', sealInk: '#fff' };
  var SIGN = CATS ? [['Sir Whiskers', 'Head of Napping'], ['Lady Purrington', 'Keeper of the Litter Book']] : [['Sir Barksalot', 'Chief Sniffer'], ['Duchess', 'Head of Good Boys']];
  var today = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  function opts(name, pct, date) { return { theme: TH, img: D.cover, kicker: D.cert.kicker || 'The Raining Cats & Dogs Kennel Club presents', title: D.cert.title, pre: 'This certifies that', name: name || (CATS ? 'A Most Excellent Cat Person' : 'A Very Good Human'), body: D.cert.body, score: D.rounds.length + ' rounds  ·  ' + pct + '% right  ·  ' + date, seal: D.cert.seal, sign: SIGN, brand: 'Raining Cats & Dogs  ·  ' + location.host }; }
  var invite = { url: location.origin + '/quiz/' + D.book + '/', title: 'The ' + D.title + ' Quiz', text: 'Think you know ' + (D.kind === 'breeds' ? 'your ' + (CATS ? 'cat' : 'dog') + ' breeds' : (CATS ? 'cat' : 'dog') + ' idioms') + '? Take the ' + D.title + ' quiz and beat my score.' };
  function inviteBox() { return '<div class="rc-box"><h3>Dare a friend</h3><p>Send the quiz and see who knows more.</p><div id="inv">' + Cert.row(invite) + '</div></div>'; }
  function wireInvite() { var r = $('#inv'); if (r) Cert.bind(r, invite); }
  function bookBox() { return '<div class="rc-box"><h3>The book</h3><div class="btns">' + (D.inside ? '<a class="btn" href="' + D.inside + '">Read inside, free</a>' : '') + D.links.map(function (x) { return '<a class="btn" href="' + esc(x[1]) + '" rel="noopener">' + esc(x[0]) + '</a>'; }).join('') + '</div></div>'; }

  if (D.page === 'certview') {   // a shared certificate
    var nm = (Q.get('n') || '').slice(0, 40), pc = Math.max(0, Math.min(100, parseInt(Q.get('p'), 10) || 0)), dd = (Q.get('d') || today).slice(0, 30);
    root.innerHTML = '<p class="kick">' + esc(D.title) + ' quiz</p><h1>' + esc(nm || 'Someone') + ' is officially ' + esc(D.cert.title) + '</h1><p class="lead">Think you can do better?</p><canvas id="cv" width="1600" height="1130" aria-label="The certificate"></canvas><div class="btns"><a class="btn main" href="/quiz/' + D.book + '/">Take the quiz</a></div>' + inviteBox() + bookBox();
    Cert.draw($('#cv'), opts(nm, pc, dd)); wireInvite(); return;
  }
  var KEY = function (i) { return 'rc-quiz-' + D.book + '-' + i; };
  function scoreOf(i) { var m = (st(KEY(i)) || '').match(/^(\d+)\/(\d+)$/); return m && +m[2] ? Math.round(m[1] / m[2] * 100) : null; }
  function home() {
    var done = 0, sum = 0;
    var items = D.rounds.map(function (r, i) { var p = scoreOf(i), ok = p != null && p >= D.pass; if (ok) { done++; sum += p; } return '<li class="' + (ok ? 'ok' : p != null ? 'low' : '') + '"><button type="button" data-r="' + i + '"><span class="num">' + (i + 1) + '</span><b>' + esc(r.name) + '</b><i>' + (p == null ? r.qs.length + ' questions' : p + '%' + (ok ? ' passed' : ', try again')) + '</i></button></li>'; }).join('');
    var all = done === D.rounds.length;
    root.innerHTML = '<p class="kick">' + esc(D.title) + '</p><h1>The ' + esc(D.title) + ' Quiz</h1><p class="lead">' + D.rounds.length + ' rounds. Score ' + D.pass + '% or more in every round and earn your certificate of <b>' + esc(D.cert.title) + '</b>.</p>'
      + '<div class="rq-bar"><i style="width:' + Math.round(done / D.rounds.length * 100) + '%"></i></div><p class="rc-code">' + done + ' of ' + D.rounds.length + ' rounds passed. Scores stay on this device.</p>'
      + '<ol class="rq-rounds">' + items + '</ol>' + (all ? '<div id="cert"></div>' : '') + inviteBox() + bookBox();
    [].forEach.call(root.querySelectorAll('[data-r]'), function (b) { b.onclick = function () { play(+b.dataset.r); }; });
    wireInvite(); if (all) certBlock(Math.round(sum / done));
  }
  function certBlock(pct) {
    var box = $('#cert'); box.className = 'rc-box';
    box.innerHTML = '<p class="kick">You earned it</p><h2>' + esc(D.cert.title) + '</h2><label>Name on your certificate <input id="cn" maxlength="40" autocomplete="name" placeholder="Your name"></label><canvas id="cv" width="1600" height="1130" aria-label="Your certificate"></canvas>'
      + '<div class="btns"><button class="btn main" type="button" id="cdl">Download</button><button class="btn" type="button" id="cpr">Print</button><button class="btn" type="button" id="csh">Share my certificate</button></div><div id="crow"></div>';
    var cv = $('#cv'), cn = $('#cn'); cn.value = st('rc-cert-name') || '';
    var sh = function () { return { url: location.origin + '/quiz/' + D.book + '/certificate/?n=' + encodeURIComponent(cn.value.trim()) + '&p=' + pct + '&d=' + encodeURIComponent(today), title: D.cert.title, text: 'Officially certified: ' + D.cert.title + '! ' + pct + '% on the ' + D.title + ' quiz. Can you beat me?' }; };
    var redraw = function () { Cert.draw(cv, opts(cn.value.trim(), pct, today)); var r = $('#crow'); r.innerHTML = Cert.row(sh()); Cert.bind(r, sh()); };
    var tm; cn.addEventListener('input', function () { clearTimeout(tm); tm = setTimeout(function () { st('rc-cert-name', cn.value.trim()); redraw(); }, 250); }); redraw();
    var fn = 'certificate-' + D.book + '.png';
    $('#cdl').onclick = function () { Cert.download(cv, fn); }; $('#cpr').onclick = function () { Cert.print(cv); };
    $('#csh').onclick = function () { Cert.shareImage(cv, fn, sh()).then(function (ok) { if (!ok) window.open('https://wa.me/?text=' + encodeURIComponent(sh().text + ' ' + sh().url), '_blank', 'noopener'); }); };
  }
  function shuf(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), x = a[i]; a[i] = a[j]; a[j] = x; } return a; }
  function play(ri) {
    var R = D.rounds[ri], i = 0, right = 0;
    function ask() {
      var q = R.qs[i], img = q.img || R.img, order = shuf(q.o.map(function (t, k) { return k; }));
      root.innerHTML = '<p class="kick">Round ' + (ri + 1) + ': ' + esc(R.name) + '</p><div class="rq-bar"><i style="width:' + Math.round(i / R.qs.length * 100) + '%"></i></div><p class="rc-code">Question ' + (i + 1) + ' of ' + R.qs.length + '</p>'
        + '<div class="rq-q' + (img ? '' : ' noimg') + '">' + (img ? '<img src="' + esc(img) + '" alt="">' : '') + '<div><h2>' + esc(q.q) + '</h2><div class="rq-opts">' + order.map(function (k) { return '<button type="button" data-k="' + k + '">' + esc(q.o[k]) + '</button>'; }).join('') + '</div><div id="rx"></div></div></div>';
      [].forEach.call(root.querySelectorAll('.rq-opts button'), function (b) { b.onclick = function () {
        var k = +b.dataset.k, ok = k === q.a; if (ok) right++;
        [].forEach.call(root.querySelectorAll('.rq-opts button'), function (x) { x.disabled = true; if (+x.dataset.k === q.a) x.classList.add('right'); else if (x === b) x.classList.add('wrong'); });
        $('#rx').innerHTML = '<p class="rq-x"><b>' + (ok ? 'Right.' : 'Not quite.') + '</b> ' + esc(q.x || '') + '</p><p><button class="btn main" type="button" id="nx">' + (i < R.qs.length - 1 ? 'Next question' : 'See my score') + '</button></p>';
        $('#nx').onclick = function () { i++; if (i < R.qs.length) ask(); else done(); }; $('#nx').focus({ preventScroll: true });
      }; });
      window.scrollTo({ top: root.offsetTop - 20, behavior: 'smooth' });
    }
    function done() {
      var prev = scoreOf(ri), pct = Math.round(right / R.qs.length * 100);
      if (prev == null || pct >= prev) st(KEY(ri), right + '/' + R.qs.length);
      var ok = pct >= D.pass, last = ri === D.rounds.length - 1;
      root.innerHTML = '<p class="kick">Round ' + (ri + 1) + ': ' + esc(R.name) + '</p><p class="rq-score">' + right + ' / ' + R.qs.length + '</p><p class="lead">' + (ok ? (pct === 100 ? 'Perfect. Not one wrong answer.' : 'Passed. Nicely done.') : 'You need ' + D.pass + '% to pass this round. Have another go.') + '</p>'
        + '<div class="btns">' + (D.rounds.every(function (r, k) { var x = scoreOf(k); return x != null && x >= D.pass; }) ? '<button class="btn main" type="button" id="gc">See my certificate</button>' : '') + (ok && !last ? '<button class="btn main" type="button" id="nr">Next round</button>' : '') + '<button class="btn" type="button" id="ag">Try this round again</button><button class="btn" type="button" id="hm">All rounds</button></div>';
      if ($('#nr')) $('#nr').onclick = function () { play(ri + 1); };
      $('#ag').onclick = function () { play(ri); }; $('#hm').onclick = home;
      if ($('#gc')) $('#gc').onclick = function () { home(); var c = $('#cert'); if (c) c.scrollIntoView({ behavior: 'smooth' }); };
      window.scrollTo({ top: root.offsetTop - 20, behavior: 'smooth' });
    }
    ask();
  }
  home();
})();
