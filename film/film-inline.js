/* film-inline.js — embeds the scroll-scrub clay film INSIDE a normal page.
   Desktop: a sticky-pinned section that scrubs the clips by scroll position, then
   releases into the next section. Mobile: a clean stacked scroll (no scroll-jack),
   each scene autoplaying as it enters view. Namespaced .ifilm-*; never touches
   html/body. mountInlineFilm(sectionEl, {sections:[{id,label,still,clip,clipMobile,
   accent,title,body,scroll,linger}], accent, diveScroll}).
   HARDEN-1 (panel review 2026-08-27): forced-mode override honored first, touch
   laptops keep desktop mode, fetch failure backoff, object-URL revocation +
   pagehide/pageshow lifecycle, seek-deadlock timeout, priming seeks, cadence-aware
   layout invalidation (height/orientation/fonts/content-above), mobile start/stop
   symmetry, hidden-tab idling, a11y on dots and copy layers. Visuals unchanged. */
(function () {
  function el(t, c) { var n = document.createElement(t); if (c) n.className = c; return n; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var clamp = function (x, a, b) { a = a == null ? 0 : a; b = b == null ? 1 : b; return Math.min(b, Math.max(a, x)); };
  var smooth = function (x) { x = clamp(x); return x * x * (3 - 2 * x); };
  var lingerEase = function (x, L) { L = clamp(L); var c = x - 0.5; return (1 - L) * x + L * (4 * c * c * c + 0.5); };

  function injectCSS() {
    if (document.getElementById('ifilm-css')) return;
    var css = `
    .ifilm{position:relative;background:var(--paper,#FBF8F2);--if-blue:#6FC9E8;}
    .ifilm-pin{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;transform:translateZ(0);background:var(--paper,#FBF8F2);}
    .ifilm-stage{position:absolute;inset:0;z-index:1;}
    .ifilm-scene{position:absolute;inset:0;opacity:0;overflow:hidden;will-change:opacity;}
    .ifilm-scene__still,.ifilm-scene__video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 44%;}
    .ifilm-scene__still{will-change:transform;} .ifilm-scene.has-clip .ifilm-scene__still{opacity:0;} .ifilm-scene__video{z-index:1;}
    /* legibility wedge: cream copy over a warm-dark blurred panel on the left */
    .ifilm-grade{position:absolute;inset:0;z-index:12;pointer-events:none;background:radial-gradient(125% 95% at 50% 40%, transparent 44%, rgba(20,17,10,.30) 100%);}
    .ifilm-wedge{position:absolute;inset:0;z-index:14;pointer-events:none;
      -webkit-backdrop-filter:blur(18px) saturate(.9) brightness(.72);backdrop-filter:blur(18px) saturate(.9) brightness(.72);
      background:linear-gradient(90deg, rgba(20,17,10,.86) 0%, rgba(20,17,10,.8) 16%, rgba(20,17,10,.66) 30%, rgba(20,17,10,.5) 40%, rgba(20,17,10,.3) 50%, rgba(20,17,10,.12) 62%, rgba(20,17,10,0) 74%);
      -webkit-mask-image:linear-gradient(90deg,#000 0%,#000 34%,rgba(0,0,0,.5) 50%,rgba(0,0,0,.15) 62%,transparent 72%);
      mask-image:linear-gradient(90deg,#000 0%,#000 34%,rgba(0,0,0,.5) 50%,rgba(0,0,0,.15) 62%,transparent 72%);}
    @supports not (backdrop-filter: blur(1px)){ .ifilm-wedge{background-color:rgba(20,17,10,.5);} }
    .ifilm-copylayer{position:absolute;inset:0;z-index:20;pointer-events:none;}
    .ifilm-copy{position:absolute;left:6vw;top:50%;transform:translateY(-50%);width:min(38vw,540px);opacity:0;will-change:opacity,transform;}
    .ifilm-copy__num{font-family:var(--mono,ui-monospace,Menlo,monospace);font-size:12px;letter-spacing:.12em;color:rgba(251,248,242,.5);}
    .ifilm-copy__eyebrow{display:block;margin-top:14px;font-family:var(--mono,ui-monospace,monospace);font-weight:600;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--if-blue);}
    .ifilm-copy__title{font-family:var(--display,Georgia,serif);font-weight:450;color:#FBF8F2;font-size:clamp(1.9rem,3.6vw,3rem);line-height:1.06;letter-spacing:-.018em;margin:14px 0 0;text-shadow:0 1px 2px rgba(20,17,10,.5),0 2px 16px rgba(20,17,10,.3);max-width:16ch;}
    .ifilm-copy__body{margin-top:18px;font-size:clamp(1rem,1vw + .7rem,1.12rem);line-height:1.5;color:rgba(251,248,242,.88);max-width:34ch;text-shadow:0 1px 10px rgba(20,17,10,.5);font-family:var(--sans,system-ui,sans-serif);}
    .ifilm-route{position:absolute;right:clamp(14px,2.2vw,30px);top:50%;z-index:40;transform:translateY(-50%);display:flex;flex-direction:column;gap:20px;padding:16px 10px;}
    .ifilm-route::before{content:"";position:absolute;left:50%;top:20px;bottom:20px;width:2px;transform:translateX(-50%);background:rgba(251,248,242,.2);}
    .ifilm-route__dot{position:relative;border:0;background:transparent;cursor:pointer;width:14px;height:14px;display:grid;place-items:center;}
    .ifilm-route__dot i{width:9px;height:9px;border-radius:50%;background:rgba(251,248,242,.35);transition:transform .3s,background .3s,box-shadow .3s;}
    .ifilm-route__dot:hover i{transform:scale(1.25);background:#fff;}
    .ifilm-route__dot.is-active i{background:var(--if-blue);transform:scale(1.4);box-shadow:0 0 0 5px rgba(111,201,232,.22);}
    .ifilm-route__label{position:absolute;right:24px;top:50%;transform:translateY(-50%) translateX(6px);white-space:nowrap;font:600 .74rem var(--sans,system-ui);color:#14110A;background:rgba(251,248,242,.92);padding:5px 11px;border-radius:999px;opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;}
    .ifilm-route__dot:hover .ifilm-route__label,.ifilm-route__dot.is-active .ifilm-route__label{opacity:1;transform:translateY(-50%);}
    /* ---- mobile stacked ---- */
    .ifilm-m{position:relative;padding:2vh 0 4vh;overflow:hidden;overflow:clip;}
    .ifilm-mscene{position:relative;padding:5vh 20px 0 20px;opacity:1;transform:none;}
    @media (hover:hover) and (pointer:fine){.ifilm-mscene{opacity:0;transform:translateY(30px);transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .8s cubic-bezier(.2,.7,.2,1);}.ifilm-mscene.in{opacity:1;transform:none;}}
    .ifilm-mcard{position:relative;border-radius:18px;overflow:hidden;aspect-ratio:4/5;background:#1a1610;box-shadow:0 20px 50px rgba(20,17,10,.18);}
    .ifilm-mcard img,.ifilm-mcard video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 42%;}
    .ifilm-mcard video{opacity:0;pointer-events:none;}
    .ifilm-mcard.is-playing video{opacity:1;}
    .ifilm-mcard.is-playing img{opacity:0;}
    .ifilm-mcopy{padding:18px 4px 0;}
    .ifilm-meyebrow{font-family:var(--mono,monospace);font-weight:600;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#2596BE;}
    .ifilm-mtitle{font-family:var(--display,Georgia,serif);font-weight:450;font-size:clamp(1.6rem,6vw,2rem);line-height:1.1;letter-spacing:-.01em;color:#14110A;margin:10px 0 0;max-width:18ch;}
    .ifilm-mbody{font-family:var(--sans,system-ui);font-size:1rem;line-height:1.5;color:#574F40;margin:12px 0 0;max-width:40ch;}
    @media(prefers-reduced-motion:reduce){.ifilm-mscene{opacity:1;transform:none;transition:none;}}
    `;
    var st = el('style'); st.id = 'ifilm-css'; st.textContent = css; document.head.appendChild(st);
  }

  function isMobile() {
    /* Forced mode wins outright: it must not be shadowed by capability
       checks or it is untestable on touch hardware (panel finding). */
    if (window.__ifilmForce === 'mobile') return true;
    if (window.__ifilmForce === 'desktop') return false;
    /* A bare maxTouchPoints check misclassifies touch laptops and iPads in
       desktop mode. Mobile = small viewport, or genuinely coarse-and-
       hoverless primary input. */
    return window.matchMedia('(max-width:860px)').matches ||
           window.matchMedia('(hover:none) and (pointer:coarse)').matches;
  }

  function mountInlineFilm(section, config) {
    var SECTIONS = (config && config.sections) || [];
    if (!SECTIONS.length) return;                  /* bail BEFORE wiping */
    if (section.dataset.ifilmMounted) return;      /* double-mount guard */
    section.dataset.ifilmMounted = '1';
    injectCSS();
    section.classList.add('ifilm');
    section.innerHTML = '';
    var N = SECTIONS.length;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (isMobile()) { buildMobile(section, SECTIONS, reduce); return; }

    /* ---------- DESKTOP: pinned scrub ---------- */
    var DIVE_W = config.diveScroll || 1.7;
    var CROSS = Math.max(0.02, (config.crossfade != null) ? config.crossfade : 0.2);
    var pin = el('div', 'ifilm-pin');
    var stage = el('div', 'ifilm-stage');
    var grade = el('div', 'ifilm-grade');
    var wedge = el('div', 'ifilm-wedge');
    var copylayer = el('div', 'ifilm-copylayer');
    var route = el('div', 'ifilm-route');
    pin.appendChild(stage); pin.appendChild(grade); pin.appendChild(wedge);
    pin.appendChild(copylayer); pin.appendChild(route);
    section.appendChild(pin);

    var segs = SECTIONS.map(function (s, i) {
      var scene = el('div', 'ifilm-scene'); scene.style.setProperty('--sw-accent', s.accent || '');
      var img = el('img', 'ifilm-scene__still'); img.alt = ''; img.decoding = 'async';
      if (s.still) img.src = s.still;
      scene.appendChild(img); stage.appendChild(scene);
      return { s: s, i: i, el: scene, img: img, video: null, blobUrl: null,
               hasClip: false, loading: false, ready: false, fails: 0,
               cur: 0, target: 0, visible: false, seekAt: 0, lastPrime: 0,
               w: s.scroll || DIVE_W, linger: s.linger || 0 };
    });

    var copies = [], dots = [];
    SECTIONS.forEach(function (s, i) {
      var c = el('article', 'ifilm-copy');
      c.innerHTML =
        '<span class="ifilm-copy__num">' + pad(i + 1) + ' / ' + pad(N) + '</span>' +
        (s.eyebrow ? '<span class="ifilm-copy__eyebrow">' + esc(s.eyebrow) + '</span>' : '') +
        (s.title ? '<h3 class="ifilm-copy__title">' + esc(s.title) + '</h3>' : '') +
        (s.body ? '<p class="ifilm-copy__body">' + esc(s.body) + '</p>' : '');
      c.setAttribute('aria-hidden', 'true');
      copylayer.appendChild(c); copies.push(c);
      var dot = el('button', 'ifilm-route__dot');
      dot.type = 'button';
      dot.setAttribute('aria-label', 'Go to scene ' + (i + 1) + (s.label ? ': ' + s.label : ''));
      dot.innerHTML = '<span class="ifilm-route__label">' + esc(s.label || '') + '</span><i></i>';
      dot.addEventListener('click', function () { jumpTo(i); });
      route.appendChild(dot); dots.push(dot);
    });

    function pad(n) { return String(n).padStart(2, '0'); }
    var vh = window.innerHeight, totalW = 0, sectionTop = 0, activeIndex = -1,
        ticking = false, laidW = window.innerWidth, laidH = window.innerHeight,
        nearFilm = true, lastBodyH = 0;

    function layout() {
      vh = window.innerHeight; laidW = window.innerWidth; laidH = window.innerHeight;
      var off = 0;
      segs.forEach(function (g) { g.start = off * vh; off += g.w; g.end = off * vh; });
      totalW = off;
      section.style.height = ((totalW + 1) * vh) + 'px';
      sectionTop = section.getBoundingClientRect().top + (window.scrollY || window.pageYOffset);
      read();
    }
    function jumpTo(i) {
      var g = segs[i]; window.scrollTo({ top: sectionTop + g.start + (g.end - g.start) * 0.5, behavior: reduce ? 'instant' : 'smooth' });
    }
    function detachClip(g) {
      if (g.video) { try { g.video.removeAttribute('src'); g.video.load(); } catch (e) {} g.video.remove(); }
      if (g.blobUrl) { try { URL.revokeObjectURL(g.blobUrl); } catch (e) {} }
      g.video = null; g.blobUrl = null; g.hasClip = false; g.ready = false;
      g.el.classList.remove('has-clip');
    }
    function loadClip(g) {
      /* Two failures = permanent still (no per-scroll-frame retry storm). */
      if (reduce || g.loading || g.hasClip || !g.s.clip || g.fails >= 2) return;
      g.loading = true;
      fetch(g.s.clip).then(function (r) { return r.ok ? r.blob() : Promise.reject(0); }).then(function (blob) {
        var v = document.createElement('video'); v.className = 'ifilm-scene__video';
        v.muted = true; v.playsInline = true; v.preload = 'auto'; v.setAttribute('muted', ''); v.setAttribute('playsinline', '');
        g.blobUrl = URL.createObjectURL(blob);
        v.src = g.blobUrl;
        v.addEventListener('loadedmetadata', function () { g.ready = true; read(); });
        v.addEventListener('seeked', function () { if (g.video === v) g.el.classList.add('has-clip'); }, { once: true });
        v.addEventListener('loadeddata', function () { try { v.pause(); } catch (e) {} });
        v.addEventListener('error', function () { g.fails = 2; detachClip(g); });
        g.el.appendChild(v); g.video = v; g.hasClip = true; g.loading = false;
      }).catch(function () { g.loading = false; g.fails++; });
    }
    function read() {
      var sy = window.scrollY || window.pageYOffset;
      nearFilm = sy > sectionTop - 2 * vh && sy < sectionTop + (totalW + 1) * vh + vh;
      var y = clamp(sy - sectionTop, 0, totalW * vh);
      var fade = CROSS * vh, ci = 0;
      for (var i = 0; i < segs.length; i++) if (y >= segs[i].start) ci = i;
      for (i = 0; i < segs.length; i++) {
        var g = segs[i];
        if (nearFilm && y > g.start - 1.6 * vh && y < g.end + 1.6 * vh) loadClip(g);
        var local = clamp((y - g.start) / (g.end - g.start), 0, 1);
        g.target = g.linger ? lingerEase(local, g.linger) : local;
        var outside = 0; if (y < g.start) outside = g.start - y; else if (y > g.end) outside = y - g.end;
        var op = smooth(1 - outside / fade);
        g.el.style.opacity = op; g.visible = op > 0.001;
        g.el.style.zIndex = (i === ci) ? '10' : String(2 + Math.round(op * 6));
        if (!g.hasClip || !g.ready) { var sc = reduce ? 1 : 1.03 + local * 0.12; g.img.style.transform = 'scale(' + sc.toFixed(3) + ')'; }
      }
      for (i = 0; i < N; i++) {
        var g2 = segs[i]; var pr = clamp((y - g2.start) / (g2.end - g2.start), 0, 1);
        var before = y < g2.start, after = y > g2.end, cop;
        if (i === 0) cop = after ? 0 : (pr < 0.5 ? 1 : smooth(1 - (pr - 0.5) / 0.5));
        else if (i === N - 1) cop = before ? 0 : smooth(pr / 0.45);
        else cop = (before || after) ? 0 : smooth(1 - Math.abs(pr - 0.5) / 0.5);
        copies[i].style.opacity = cop;
        copies[i].setAttribute('aria-hidden', cop < 0.5 ? 'true' : 'false');
        copies[i].style.transform = reduce ? 'none' : 'translateY(' + ((0.5 - pr) * 3) + 'vh)';
      }
      var near = clamp(ci, 0, N - 1);
      if (near !== activeIndex) {
        activeIndex = near;
        dots.forEach(function (d, k) {
          d.classList.toggle('is-active', k === near);
          if (k === near) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current');
        });
      }
      ticking = false;
    }
    function seekTo(g, t, now) {
      try { g.video.currentTime = t; g.seekAt = now; } catch (e) {}
    }
    function raf() {
      requestAnimationFrame(raf);
      if (document.hidden || !nearFilm) return;   /* idle when irrelevant */
      var now = performance.now();
      for (var i = 0; i < segs.length; i++) {
        var g = segs[i]; if (!g.hasClip || !g.ready || !g.video) continue;
        var dur = g.video.duration || 1;
        if (!g.visible) {
          /* Snap the scrub model without a per-frame seek, but issue ONE
             throttled priming seek so re-entry starts on the right frame. */
          g.cur = g.target;
          if (!g.video.seeking && now - g.lastPrime > 400 &&
              Math.abs(g.video.currentTime - g.cur * dur) > 0.2) {
            g.lastPrime = now; seekTo(g, clamp(g.cur, 0, 0.999) * dur, now);
          }
          continue;
        }
        /* seeking-guard with a deadlock timeout: Safari can drop a seeked
           event across bfcache/background transitions. */
        if (g.video.seeking && now - g.seekAt < 600) continue;
        g.cur += (g.target - g.cur) * (reduce ? 1 : 0.18);
        var t = clamp(g.cur, 0, 0.999) * dur;
        if (Math.abs(g.video.currentTime - t) > 0.033) seekTo(g, t, now);
      }
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(read); } }, { passive: true });
    window.addEventListener('resize', function () { if (window.innerWidth !== laidW || window.innerHeight !== laidH) layout(); });
    window.addEventListener('orientationchange', function () { setTimeout(layout, 120); });
    if (window.visualViewport) window.visualViewport.addEventListener('resize', function () { if (window.innerHeight !== laidH) layout(); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { layout(); });
    /* Content growth ABOVE the film (late reveals, font swap) shifts
       sectionTop; watch the body and relayout when its height changes. */
    if (window.ResizeObserver) {
      var bro = new ResizeObserver(function () {
        var h = document.body.getBoundingClientRect().height;
        if (Math.abs(h - lastBodyH) > 4) { lastBodyH = h; layout(); }
      });
      bro.observe(document.body);
    }
    window.addEventListener('pagehide', function (e) {
      segs.forEach(function (g) { if (g.video) { try { g.video.pause(); } catch (x) {} } });
      if (!e.persisted) segs.forEach(function (g) { if (g.blobUrl) { try { URL.revokeObjectURL(g.blobUrl); } catch (x) {} } });
    });
    window.addEventListener('pageshow', function (e) { if (e.persisted) layout(); });
    if (document.readyState === 'complete') layout();
    else window.addEventListener('load', layout);
    layout(); requestAnimationFrame(raf);
  }

  function buildMobile(section, SECTIONS, reduce) {
    var m = el('div', 'ifilm-m'); var html = '';
    SECTIONS.forEach(function (s) {
      var clip = s.clipMobile || s.clip || '';
      var still = s.still || '';
      html += '<section class="ifilm-mscene" data-clip="' + esc(clip) + '">' +
        '<div class="ifilm-mcard"><img src="' + esc(still) + '" alt="" decoding="async" loading="lazy">' +
        (clip && !reduce ? '<video muted loop playsinline webkit-playsinline preload="none" poster="' + esc(still) + '"></video>' : '') +
        '</div>' +
        '<div class="ifilm-mcopy"><div class="ifilm-meyebrow">' + esc(s.eyebrow || '') + '</div>' +
        '<h3 class="ifilm-mtitle">' + esc(s.title || '') + '</h3>' +
        '<p class="ifilm-mbody">' + esc(s.body || '') + '</p></div></section>';
    });
    m.innerHTML = html; section.appendChild(m);
    var canUseVideo = !reduce;
    function startScene(n) {
      n.classList.add('in');
      if (!canUseVideo || n.dataset.starting === '1') return;
      var v = n.querySelector('video');
      if (v) {
        n.dataset.starting = '1';
        v.controls = false;
        v.removeAttribute('controls');
        v.disableRemotePlayback = true;
        v.muted = true;               /* property, not just the attribute */
        if (!v.src) v.src = n.getAttribute('data-clip');
        var p = v.play();
        if (p && p.then) p.then(function () {
          n.dataset.starting = '';
          var card = v.closest('.ifilm-mcard');
          if (card) card.classList.add('is-playing');
        }).catch(function () { n.dataset.starting = ''; });
        else n.dataset.starting = '';
      }
    }
    function stopScene(n) {
      var v = n.querySelector('video');
      if (v) { try { v.pause(); } catch (x) {} var card = v.closest('.ifilm-mcard'); if (card) card.classList.remove('is-playing'); }
    }
    /* threshold [0, .14]: a card that only peeked in (never crossing .14)
       still gets an exit callback, so every start has a guaranteed stop. */
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting && e.intersectionRatio >= 0.14) { startScene(e.target); }
        else if (!e.isIntersecting) { stopScene(e.target); }
      });
    }, { rootMargin: '-8% 0px -12% 0px', threshold: [0, 0.14] });
    m.querySelectorAll('.ifilm-mscene').forEach(function (n) { io.observe(n); });
    function mSweep() {
      if (document.hidden) return;
      m.querySelectorAll('.ifilm-mscene:not(.in)').forEach(function (n) {
        var r = n.getBoundingClientRect();
        if (r.top < window.innerHeight * 0.98 && r.bottom > 0) startScene(n);
      });
    }
    setTimeout(mSweep, 900); setInterval(mSweep, 800);
    document.addEventListener('scroll', mSweep, { capture: true, passive: true });
    window.addEventListener('pagehide', function () {
      m.querySelectorAll('.ifilm-mscene').forEach(stopScene);
    });
    window.addEventListener('pageshow', function (e) { if (e.persisted) setTimeout(mSweep, 60); });
  }

  window.mountInlineFilm = mountInlineFilm;
})();
