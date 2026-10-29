/* موثّق — the home table: the intro (seal pressed, cord run, parcel opened), the exhibits laid on the
   table and tied to the lead seal by cords that hang, sway and tighten, and the method cord tied knot by
   knot as the reader scrolls. Everything here is decoration over working HTML: without it the page reads
   the same. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wide = () => matchMedia('(min-width: 1025px)').matches;
  const ss = { get: (k) => { try { return sessionStorage.getItem(k); } catch { return null; } }, set: (k, v) => { try { sessionStorage.setItem(k, v); } catch {} } };
  const G = window.gsap;

  /* ---------- the headline rises line by line once the table is open ---------- */
  const lines = $('[data-lines]');
  const reveal = () => { if (lines) requestAnimationFrame(() => lines.classList.add('is-in')); document.dispatchEvent(new Event('mw:open')); };

  /* ---------- intro ---------- */
  function intro() {
    const tpl = $('#intro-tpl');
    const forced = /[?&]loader\b/.test(location.search);
    /* arriving from another page under the closed parcel: no second intro; the lines rise as it opens */
    if (!forced && document.documentElement.classList.contains('nav-in')) { ss.set('mw-in', '1'); document.addEventListener('mw:veil', reveal, { once: true }); return; }
    if (!tpl || !G || reduce || (!forced && ss.get('mw-in'))) { reveal(); return; }
    ss.set('mw-in', '1');
    const box = document.createElement('div');
    box.className = 'intro';
    box.setAttribute('aria-hidden', 'true');
    box.innerHTML = `<div class="intro-half top"></div><div class="intro-half bot"></div>
      <div class="intro-stage"><svg class="intro-cord" viewBox="0 0 1000 40" preserveAspectRatio="none"><path d="M1010 18 Q500 30 -10 18"/></svg>
      <div class="intro-seal">${tpl.innerHTML}<span class="intro-drop"></span></div></div>
      <button class="intro-skip" type="button" tabindex="-1">تخطَّ</button>`;
    document.body.append(box);
    document.documentElement.style.overflow = 'hidden';
    const seal = $('.intro-seal .wax', box), drop = $('.intro-drop', box), word = $('.intro-word', box);
    const cord = $('.intro-cord path', box), len = cord.getTotalLength();
    const logo = $('.mast .brand .mark');
    const done = () => { box.remove(); document.documentElement.style.overflow = ''; reveal(); };
    let closed = false;
    const finish = () => { if (!closed) { closed = true; done(); } };
    const tl = G.timeline({ onComplete: finish });
    setTimeout(finish, 6500);
    G.set(cord, { strokeDasharray: len, strokeDashoffset: len });
    G.set(seal, { opacity: 0 });
    tl.fromTo(drop, { y: -innerHeight * 0.62, scaleX: 0.8, scaleY: 1.25 }, { y: 0, scaleX: 1, scaleY: 1, duration: 0.6, ease: 'power2.in' })
      .to(drop, { scaleX: 1.6, scaleY: 0.58, duration: 0.11, ease: 'power1.out' })
      .to(drop, { scale: 3.6, opacity: 0, duration: 0.3, ease: 'power2.out' })
      .fromTo(seal, { scale: 1.32, rotation: -16, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.62, ease: 'back.out(1.7)' }, '<')
      .to(cord, { strokeDashoffset: 0, duration: 0.72, ease: 'power2.inOut' }, '-=0.3')
      .fromTo(word, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.45, ease: 'power2.out' }, '-=0.45')
      .addLabel('open', '+=0.32')
      .to($('.top', box), { yPercent: -100, duration: 0.95, ease: 'expo.inOut' }, 'open')
      .to($('.bot', box), { yPercent: 100, duration: 0.95, ease: 'expo.inOut' }, 'open')
      .to([$('.intro-cord', box), word, $('.intro-skip', box)], { opacity: 0, duration: 0.25 }, 'open');
    if (logo) {
      tl.add(() => {
        const a = seal.getBoundingClientRect(), b = logo.getBoundingClientRect();
        G.to(seal, { x: b.left + b.width / 2 - (a.left + a.width / 2), y: b.top + b.height / 2 - (a.top + a.height / 2),
          scale: b.width / a.width, duration: 0.95, ease: 'expo.inOut' });
        G.to(seal, { opacity: 0, duration: 0.2, delay: 0.85 });
      }, 'open');
    }
    const skip = () => { if (tl.progress() < 1) tl.progress(1); };
    $('.intro-skip', box).addEventListener('click', skip);
    ['keydown', 'wheel', 'touchstart'].forEach((ev) => addEventListener(ev, skip, { once: true, passive: true }));
    box.addEventListener('pointerdown', skip);
  }

  /* ---------- the table ---------- */
  const pile = $('[data-pile]');
  let exs = [], cords = null;
  if (pile) {
    exs = $$('.ex', pile);
    exs.forEach((el, i) => { el.dataset.i = i; });
    const tabs = $$('[data-tab]');
    const setInert = () => exs.forEach((el) => { const back = el.dataset.slot !== '0'; $('.ex-in', el).inert = back && wide(); });
    const front = () => exs.find((e) => e.dataset.slot === '0');
    function bring(el) {
      const cur = front();
      if (!el || el === cur) return;
      const slot = el.dataset.slot;
      cur.dataset.slot = slot;
      el.dataset.slot = '0';
      $('.tag', cur).classList.remove('is-reversed');
      $('.tag', el).classList.add('is-reversed');
      el.classList.remove('is-pressed'); void el.offsetWidth; el.classList.add('is-pressed');
      setTimeout(() => el.classList.remove('is-pressed'), 900);
      setInert();
      tabs.forEach((t) => { const on = t.dataset.tab === el.dataset.i; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; });
      if (cords) cords.swap();
    }
    pile.addEventListener('click', (e) => {
      const a = e.target.closest('[data-pick]');
      if (!a) return;
      e.preventDefault();
      bring(a.closest('.ex'));
      const f = front(); setTimeout(() => $('.ex-in a, .ex-in button', f)?.focus({ preventScroll: true }), 50);
    });
    exs.forEach((el) => {
      el.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse' && el.dataset.slot !== '0') { el.classList.add('is-lift'); cords && cords.hover(+el.dataset.i); } });
      el.addEventListener('pointerleave', () => { el.classList.remove('is-lift'); cords && cords.hover(-1); });
      $('[data-pick]', el)?.addEventListener('focus', () => { el.classList.add('is-lift'); cords && cords.hover(+el.dataset.i); });
      $('[data-pick]', el)?.addEventListener('blur', () => { el.classList.remove('is-lift'); cords && cords.hover(-1); });
    });
    tabs.forEach((t) => {
      t.addEventListener('click', () => bring(exs[+t.dataset.tab]));
      t.addEventListener('keydown', (e) => {
        const d = { ArrowLeft: 1, ArrowRight: -1 }[e.key]; if (!d) return;
        e.preventDefault(); const n = (tabs.indexOf(t) + d + tabs.length) % tabs.length; tabs[n].focus(); bring(exs[+tabs[n].dataset.tab]);
      });
    });
    setInert();
    addEventListener('resize', setInert);
    /* the exhibit in front is scaled to the table, however long its real content runs */
    const fit = () => {
      const room = pile.clientHeight - 28;
      exs.forEach((el) => { const h = $('.tag', el).offsetHeight; if (h) el.style.setProperty('--fit', Math.min(0.8, room / h).toFixed(3)); });
    };
    fit(); (document.fonts ? document.fonts.ready : Promise.resolve()).then(fit);
    addEventListener('resize', fit);

    /* parallax: exhibits sit at different heights above the table */
    let mx = 0, my = 0, px = 0, py = 0;
    const hero = pile.closest('.hero');
    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect();
      mx = (e.clientX - r.left) / r.width - 0.5; my = (e.clientY - r.top) / r.height - 0.5;
    });
    hero.addEventListener('pointerleave', () => { mx = 0; my = 0; });
    const parallax = () => {
      px += (mx - px) * 0.07; py += (my - py) * 0.07;
      exs.forEach((el) => {
        const s = +el.dataset.slot, d = s === 0 ? 7 : 16 + s * 4;
        const inn = el.firstElementChild;
        inn.style.setProperty('--px', (px * -d).toFixed(2) + 'px');
        inn.style.setProperty('--py', (py * -d).toFixed(2) + 'px');
      });
    };

    /* cords: verlet ropes from the lead seal to every other exhibit's hole */
    const cv = $('.pile-cords', pile), ctx = cv.getContext('2d');
    const N = 16;
    const ropes = new Map();
    let hot = -1, dpr = 1, W = 0, H = 0, running = false, visible = true;
    const center = (el) => { const r = el.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; };
    function size() {
      const r = cv.getBoundingClientRect(); dpr = Math.min(2, devicePixelRatio || 1);
      W = r.width; H = r.height; cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    }
    function anchors() {
      const r = cv.getBoundingClientRect(), f = front();
      const sealEl = f && $('.tag-seal', f);
      if (!sealEl) return null;
      const [ax, ay] = center(sealEl);
      const out = [];
      exs.forEach((el) => {
        if (el === f) return;
        const hole = $('.tag-hole', el);
        if (!hole) return;
        const [bx, by] = center(hole);
        out.push({ i: +el.dataset.i, a: [ax - r.left, ay - r.top], b: [bx - r.left, by - r.top] });
      });
      return out;
    }
    function rope(i, a, b) {
      let R = ropes.get(i);
      if (!R) {
        R = []; for (let k = 0; k < N; k++) { const t = k / (N - 1); const x = a[0] + (b[0] - a[0]) * t, y = a[1] + (b[1] - a[1]) * t; R.push([x, y, x, y]); }
        ropes.set(i, R);
      }
      return R;
    }
    function step() {
      const A = anchors(); if (!A) return;
      const live = new Set(A.map((x) => x.i));
      [...ropes.keys()].forEach((k) => { if (!live.has(k)) ropes.delete(k); });
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      A.forEach(({ i, a, b }) => {
        const R = rope(i, a, b);
        const dist = Math.hypot(b[0] - a[0], b[1] - a[1]);
        const slack = hot === i ? 1.005 : 1.13;
        const seg = (dist * slack) / (N - 1);
        if (!reduce) {
          for (let k = 1; k < N - 1; k++) {
            const p = R[k], vx = (p[0] - p[2]) * 0.972, vy = (p[1] - p[3]) * 0.972;
            p[2] = p[0]; p[3] = p[1]; p[0] += vx; p[1] += vy + 0.42;
          }
        }
        for (let it = 0; it < (reduce ? 60 : 14); it++) {
          R[0][0] = a[0]; R[0][1] = a[1]; R[N - 1][0] = b[0]; R[N - 1][1] = b[1];
          for (let k = 0; k < N - 1; k++) {
            const p = R[k], q = R[k + 1];
            const dx = q[0] - p[0], dy = q[1] - p[1], d = Math.hypot(dx, dy) || 0.0001, diff = (d - seg) / d / 2;
            if (k > 0) { p[0] += dx * diff; p[1] += dy * diff; }
            if (k + 1 < N - 1) { q[0] -= dx * diff; q[1] -= dy * diff; }
          }
          if (reduce) { for (let k = 1; k < N - 1; k++) R[k][1] += 0.6; }
        }
        ctx.beginPath(); ctx.moveTo(R[0][0], R[0][1]);
        for (let k = 1; k < N - 1; k++) { const mxp = (R[k][0] + R[k + 1][0]) / 2, myp = (R[k][1] + R[k + 1][1]) / 2; ctx.quadraticCurveTo(R[k][0], R[k][1], mxp, myp); }
        ctx.lineTo(R[N - 1][0], R[N - 1][1]);
        ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        ctx.strokeStyle = hot === i ? '#15171A' : '#69717A'; ctx.lineWidth = hot === i ? 2.6 : 2.1; ctx.setLineDash([]); ctx.stroke();
        ctx.strokeStyle = hot === i ? 'rgba(255,255,255,.28)' : 'rgba(255,255,255,.38)'; ctx.lineWidth = 0.9; ctx.setLineDash([2.2, 3.2]); ctx.stroke();
      });
    }
    function loop() {
      if (!running) return;
      parallax(); step();
      requestAnimationFrame(loop);
    }
    const inView = () => { const r = pile.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; };
    const start = () => { if (!running && wide() && (visible || inView())) { running = true; size(); requestAnimationFrame(loop); } };
    const stop = () => { running = false; };
    cords = {
      hover(i) { hot = i; if (reduce) step(); },
      swap() { if (reduce) setTimeout(step, 1100); },
    };
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; visible ? start() : stop(); }).observe(pile);
    start();
    window.__mwTable = { get running() { return running; }, get visible() { return visible; } };
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    addEventListener('resize', () => { if (wide()) { size(); start(); } else stop(); if (reduce) step(); });
    if (reduce) { size(); step(); }
  }

  /* ---------- how to read: the large seal takes the state you point at ---------- */
  const demo = $('[data-key-demo]');
  if (demo) {
    const views = $$('[data-state-view]', demo), label = $('[data-key-label]', demo);
    $$('.seal-key li[data-state]').forEach((li) => {
      const show = () => {
        views.forEach((v) => v.classList.toggle('is-on', v.dataset.stateView === li.dataset.state));
        if (label) label.textContent = li.querySelector('b').textContent;
        $$('.seal-key li').forEach((x) => x.classList.toggle('is-on', x === li));
      };
      li.addEventListener('pointerenter', show); li.addEventListener('focusin', show); li.addEventListener('click', show);
    });
  }

  /* ---------- the method cord is tied knot by knot as you scroll ---------- */
  const steps = $('.method-strip .cord-steps');
  if (steps && G && window.ScrollTrigger && !reduce) {
    G.registerPlugin(ScrollTrigger);
    const knots = $$('li', steps);
    steps.classList.add('is-tying');
    ScrollTrigger.create({
      trigger: steps, start: 'top 85%', end: 'bottom 45%', scrub: true,
      onUpdate: (st) => {
        steps.style.setProperty('--p', st.progress.toFixed(3));
        const n = Math.round(st.progress * knots.length);
        knots.forEach((k, i) => k.classList.toggle('is-tied', i < n));
      },
    });
  }

  /* ---------- the case is rebuilt as you scroll ---------- */
  const kase = $('[data-case]');
  if (kase && G && window.ScrollTrigger && !reduce && wide()) {
    G.registerPlugin(ScrollTrigger);
    kase.classList.add('is-scrolly');
    const stepsEl = $$('.case-step', kase), views = $$('.cs-view', kase);
    const at = (n) => $$(`[data-in="${n}"]`, kase);
    const cordsP = $$('.cs-cords path', kase), svgC = $('.cs-cords', kase), stage = $('.case-stage', kase);
    const layCords = () => {
      const r = stage.getBoundingClientRect(); svgC.setAttribute('viewBox', `0 0 ${r.width} ${r.height}`);
      const sl = $('.cs-seal', kase), sr = { x: sl.offsetLeft + sl.offsetWidth / 2, y: sl.offsetTop + sl.offsetHeight / 2 };
      $$('.cs-rule', kase).forEach((card, i) => {
        const x = card.offsetLeft, y = card.offsetTop - card.offsetHeight / 2 + 18, p = cordsP[i]; if (!p) return;
        p.setAttribute('d', `M${sr.x.toFixed(1)} ${sr.y.toFixed(1)} Q${((sr.x + x) / 2).toFixed(1)} ${(Math.max(sr.y, y) + 60).toFixed(1)} ${x.toFixed(1)} ${y.toFixed(1)}`);
        const L = p.getTotalLength(); p.style.strokeDasharray = L; if (!p.dataset.drawn) p.style.strokeDashoffset = L;
      });
    };
    layCords(); addEventListener('resize', layCords);
    const state = (k) => views.forEach((v) => v.classList.toggle('is-on', v.dataset.stateView === k));
    const tl = G.timeline({ defaults: { ease: 'power3.out' } });
    const drop = (els, pos) => tl.fromTo(els, { opacity: 0, y: -46, scale: 1.06, rotation: '-=6' }, { opacity: 1, y: 0, scale: 1, rotation: '+=6', duration: 1, stagger: 0.25 }, pos);
    G.set($$('[data-in]', kase).filter((e) => e.dataset.in !== '0'), { opacity: 0 });
    G.set($('.cs-seal', kase), { opacity: 0, scale: 1.3 });
    tl.addLabel('s0');
    tl.to($('.cs-seal', kase), { opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(1.8)' }, 's0+=0.2')
      .addLabel('s1', '+=0.6');
    drop(at(1), 's1');
    tl.addLabel('s2', '+=0.8');
    drop(at(2).filter((e) => !e.classList.contains('cs-seam')), 's2');
    tl.fromTo($('.cs-seam', kase), { opacity: 1, scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: 'power2.inOut' }, 's2+=0.5')
      .addLabel('s3', '+=0.8');
    drop(at(3), 's3');
    tl.addLabel('s4', '+=0.8');
    drop(at(4), 's4');
    tl.to(cordsP, { strokeDashoffset: 0, duration: 1.1, stagger: 0.15, ease: 'power2.inOut', onComplete: () => cordsP.forEach((p) => (p.dataset.drawn = '1')) }, 's4+=0.3')
      .addLabel('s5', '+=0.6')
      .to({}, { duration: 1 });
    const labels = ['s0', 's1', 's2', 's3', 's4', 's5'].map((l) => tl.labels[l] / tl.duration());
    const seals = ['in_progress', 'in_progress', 'rereview', 'specific', 'specific', 'specific'];
    let cur = -1;
    ScrollTrigger.create({
      trigger: kase, start: 'top top', end: () => '+=' + Math.round(innerHeight * 4.2), invalidateOnRefresh: true, pin: $('.case-pin', kase), scrub: 0.6, animation: tl,
      onUpdate: (st) => {
        let n = 0; labels.forEach((p, i) => { if (st.progress >= p - 0.02) n = i; });
        if (n !== cur) { cur = n; stepsEl.forEach((s, i) => s.classList.toggle('is-on', i === n)); state(seals[n]); }
      },
    });
  }

  intro();
})();
