/* موثّق — direction B, «المتن والحاشية».
   The folio reads one sentence at a time: its wash of lapis, its number, its gloss in the margin, and the
   luhaq, the copyist's line, written from the sentence out to its source. Everything here sits on working HTML:
   without script the text, its numbered references and the margin all read and link as they are. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wide = () => matchMedia('(min-width: 1025px)').matches;

  /* smooth scroll, as in direction A */
  if (!reduce && window.Lenis) {
    const lenis = new window.Lenis({ duration: 1.05, smoothWheel: true });
    window.__lenis = lenis;
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }

  /* ---------- the folio ---------- */
  const folio = $('[data-folio]');
  if (folio) {
    const claims = $$('[data-claim]', folio);
    const refs = $$('[data-ref]', folio);
    const glosses = $$('[data-gloss]', folio);
    const svg = $('.luhaq', folio), path = $('.luhaq-line', folio), dot = $('.luhaq-dot', folio);
    const n = glosses.length;
    let cur = 0, t = 1, drawing = 0, timer = 0, held = false, seen = true;

    /* the hook rises from the reference into the leading above its line, runs out to the margin, then bends to the gloss */
    const geometry = () => {
      const ref = refs.find((r) => +r.dataset.ref === cur), gl = glosses[cur - 1];
      if (!ref || !gl || !wide()) return null;
      const box = folio.getBoundingClientRect();
      const r = ref.getBoundingClientRect(), g = $('.gloss-mark', gl).getBoundingClientRect();
      const lh = parseFloat(getComputedStyle(ref.parentElement).lineHeight) || 40;
      const sx = r.left - box.left - 3, sy = r.top - box.top + r.height / 2;
      const up = sy - lh * 0.5, rad = 8;
      const hx = $('.hashiya', folio).getBoundingClientRect().right - box.left;
      const gx = g.right - box.left + 6, gy = g.top - box.top + g.height / 2;
      const ex = hx + 18;
      const d = `M${sx.toFixed(1)} ${sy.toFixed(1)}V${(up + rad).toFixed(1)}Q${sx.toFixed(1)} ${up.toFixed(1)} ${(sx - rad).toFixed(1)} ${up.toFixed(1)}` +
        `H${ex.toFixed(1)}C${(ex - 34).toFixed(1)} ${up.toFixed(1)} ${(gx + 44).toFixed(1)} ${gy.toFixed(1)} ${gx.toFixed(1)} ${gy.toFixed(1)}`;
      return { d, gx, gy };
    };
    const paint = () => {
      const g = geometry();
      if (!g) { path.setAttribute('d', ''); dot.style.opacity = 0; return; }
      path.setAttribute('d', g.d);
      const len = path.getTotalLength();
      path.style.strokeDasharray = `${(len * t).toFixed(1)} ${len.toFixed(1)}`;
      dot.setAttribute('cx', g.gx); dot.setAttribute('cy', g.gy);
      dot.style.opacity = t >= 0.98 ? 1 : 0;
    };
    const draw = () => {
      cancelAnimationFrame(drawing);
      if (reduce) { t = 1; paint(); return; }
      const t0 = performance.now(), dur = 1100;
      const step = (now) => {
        const k = Math.min(1, (now - t0) / dur);
        t = 1 - Math.pow(1 - k, 3);
        paint();
        if (k < 1) drawing = requestAnimationFrame(step);
      };
      t = 0; drawing = requestAnimationFrame(step);
    };
    const set = (i) => {
      if (i === cur) return;
      cur = i;
      claims.forEach((c) => c.classList.toggle('is-on', +c.dataset.claim === i));
      refs.forEach((r) => r.classList.toggle('is-on', +r.dataset.ref === i));
      glosses.forEach((g) => g.classList.toggle('is-on', +g.dataset.gloss === i));
      draw();
    };
    const next = () => set((cur % n) + 1);
    const run = () => {
      clearInterval(timer);
      if (reduce || held || !seen || document.hidden || !wide()) return;
      timer = setInterval(next, 5200);
    };

    folio.classList.add('is-live');
    const pick = (i) => { set(i); };
    refs.forEach((r) => {
      const i = +r.dataset.ref;
      r.addEventListener('mouseenter', () => pick(i)); r.addEventListener('focus', () => pick(i));
      r.addEventListener('click', (e) => { if (wide()) { e.preventDefault(); pick(i); } });
    });
    claims.forEach((c) => c.addEventListener('mouseenter', () => pick(+c.dataset.claim)));
    glosses.forEach((g) => { const i = +g.dataset.gloss; g.addEventListener('mouseenter', () => pick(i)); g.addEventListener('focusin', () => pick(i)); g.addEventListener('click', () => pick(i)); });
    ['.file', '.hashiya'].forEach((s) => {
      const el = $(s, folio);
      el.addEventListener('pointerenter', () => { held = true; run(); });
      el.addEventListener('pointerleave', () => { held = false; run(); });
      el.addEventListener('focusin', () => { held = true; run(); });
      el.addEventListener('focusout', () => { held = false; run(); });
    });
    new IntersectionObserver(([e]) => { seen = e.isIntersecting; run(); }).observe(folio);
    document.addEventListener('visibilitychange', run);
    addEventListener('resize', () => { paint(); run(); });
    /* the margin is sticky and the page scrolls smoothly: follow both every frame while the folio is in view */
    const follow = () => { if (seen && wide() && t >= 1) paint(); requestAnimationFrame(follow); };
    requestAnimationFrame(follow);
    const begin = () => setTimeout(() => { set(1); run(); }, reduce ? 0 : 700);
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => {
      if (document.documentElement.classList.contains('js-open')) addEventListener('mwb:opened', begin, { once: true }); else begin();
    });
  }

  /* ---------- the opening: the copyist writes the word, draws its luhaq, signs it صح, and the page opens ---------- */
  const html = document.documentElement;
  const opening = $('[data-opening-box]');
  if (opening) {
    let ended = false;
    const end = () => {
      if (ended) return; ended = true;
      html.classList.remove('js-open');
      try { sessionStorage.setItem('mwb-in', '1'); } catch (e) {}
      opening.remove();
      dispatchEvent(new Event('mwb:opened'));
      if (window.ScrollTrigger) window.ScrollTrigger.refresh();
    };
    if (!html.classList.contains('js-open') || !window.gsap) end();
    else {
      const g = window.gsap;
      const hook = $('.op-hook path', opening), len = hook.getTotalLength();
      hook.style.strokeDasharray = len; hook.style.strokeDashoffset = len;
      const mk = $('.op-mark', opening);
      let fly = { x: 0, y: 0, s: 1 };
      const aim = () => {
        const a = mk.getBoundingClientRect(), b = $('.brand img').getBoundingClientRect();
        fly = { x: b.left + b.width / 2 - (a.left + a.width / 2), y: b.top + b.height / 2 - (a.top + a.height / 2), s: b.width / a.width };
      };
      const tl = g.timeline({ onComplete: end });
      tl.to($$('.op-rules i', opening), { scaleX: 1, duration: 0.8, ease: 'power2.out', stagger: 0.045 }, 0)
        .to($('.op-word', opening), { clipPath: 'inset(0 0 0 0%)', duration: 1.05, ease: 'power1.inOut' }, 0.35)
        .to(hook, { strokeDashoffset: 0, duration: 0.6, ease: 'power2.inOut' }, 1.35)
        .to($('.op-sah', opening), { clipPath: 'inset(0 0 0 0%)', duration: 0.5, ease: 'power1.out' }, 1.9)
        .fromTo($('.op-line', opening), { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out' }, 2.15)
        .add(aim, 2.75)
        .to([$('.op-rules', opening), $('.op-line', opening), $('.op-skip', opening)], { opacity: 0, duration: 0.35 }, 2.75)
        .to(mk, { x: () => fly.x, y: () => fly.y, scale: () => fly.s, duration: 0.95, ease: 'power3.inOut' }, 2.8)
        .to(opening, { backgroundColor: 'rgba(255,255,255,0)', duration: 0.7, ease: 'power1.in' }, 2.95)
        .set(mk, { opacity: 0 }, 3.78);
      const skip = () => { if (tl.progress() < 1) tl.progress(1); };
      $('.op-skip', opening).addEventListener('click', skip);
      ['keydown', 'wheel', 'touchstart', 'pointerdown'].forEach((ev) => addEventListener(ev, skip, { once: true, passive: true }));
      setTimeout(end, 7000);   /* never trap the reader behind the opening */
    }
  }

  /* ---------- the collation: INC-0012 collated sentence by sentence as the reader scrolls ---------- */
  const col = $('[data-collate]');
  if (col && window.gsap && window.ScrollTrigger && !reduce && wide()) {
    const g = window.gsap, ST = window.ScrollTrigger;
    g.registerPlugin(ST);
    if (window.__lenis) window.__lenis.on('scroll', ST.update);
    col.classList.add('is-scrub');
    const pin = $('.collate-pin', col);
    const cl = (n) => $$(`[data-cl="${n}"]`, col), cg = (n) => $(`[data-cg="${n}"]`, col);
    const paths = $$('[data-cline]', col);
    const prog = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
    const from = { 1: '[data-cref="1"]', 2: '[data-cref="2"]', 3: '[data-strike]', 4: '[data-cref="4"]', 5: '[data-cref="5"]' };
    const lh = () => parseFloat(getComputedStyle($('.col-text', col)).lineHeight) || 50;
    const paint = () => {
      const box = pin.getBoundingClientRect(), edge = $('.col-hashiya', col).getBoundingClientRect().right - box.left;
      paths.forEach((p) => {
        const n = +p.dataset.cline, k = prog[n];
        if (k <= 0) { p.setAttribute('d', ''); return; }
        const a = $(from[n], col), rects = a.getClientRects(), r = rects[rects.length - 1] || a.getBoundingClientRect();
        const m = $('.cg-mark', cg(n)).getBoundingClientRect();
        /* the variant's line runs through the leading below its phrase, so it never crosses the correction written above */
        const below = n === 3, sx = r.left - box.left - 3, sy = r.top - box.top + r.height / 2, up = below ? sy + lh() * 0.44 : sy - lh() * 0.42, rad = 8, vy = below ? up - rad : up + rad;
        const gx = m.right - box.left + 6, gy = m.top - box.top + m.height / 2, ex = edge + 16 + (n - 1) * 3;
        p.setAttribute('d', `M${sx.toFixed(1)} ${sy.toFixed(1)}V${vy.toFixed(1)}Q${sx.toFixed(1)} ${up.toFixed(1)} ${(sx - rad).toFixed(1)} ${up.toFixed(1)}H${ex.toFixed(1)}C${(ex - 30).toFixed(1)} ${up.toFixed(1)} ${(gx + 40).toFixed(1)} ${gy.toFixed(1)} ${gx.toFixed(1)} ${gy.toFixed(1)}`);
        const len = p.getTotalLength();
        p.style.strokeDasharray = `${(len * k).toFixed(1)} ${len.toFixed(1)}`;
        p.style.opacity = n === 3 ? 0.75 : 1;
      });
    };
    const verdicts = [['in_progress', 'بلغ · التحقق جار', 1], ['partial', 'كذا · نقلت كما وردت', 2], ['rereview', 'خ · رواية مغايرة', 3], ['specific', 'معا · مصدران مستقلان', 4], ['complete', 'صح · مكتمل وفق المنهجية', 5]];
    const label = $('[data-cv-label]', col), stepN = $('[data-cv-n]', col);
    let shown = -1;
    const sync = (t) => {
      const i = t < 2 ? 0 : t < 4 ? 1 : t < 7 ? 2 : t < 9 ? 3 : 4;
      if (i !== shown) {
        shown = i;
        $$('[data-cv]', col).forEach((v) => v.classList.toggle('is-on', v.dataset.cv === verdicts[i][0]));
        label.textContent = verdicts[i][1]; stepN.textContent = verdicts[i][2];
      }
      cg(2).classList.toggle('is-varied', t >= 5.9);
      const on = t < 2 ? [1] : t < 4 ? [2] : t < 5.4 ? [3] : t < 7 ? [2] : [4, 5];
      $$('.cg', col).forEach((x) => x.classList.toggle('is-on', on.includes(+x.dataset.cg)));
    };
    /* the scrubbed timeline lags the scroll a little, so the record follows the timeline's own time, not the scrollbar */
    const tl = g.timeline({
      defaults: { ease: 'none' },
      onUpdate() { sync(this.time()); paint(); },
      scrollTrigger: { trigger: col, start: 'top top', end: () => '+=' + Math.round(innerHeight * 4.2), pin: true, scrub: 0.6, anticipatePin: 1, onRefresh: paint },
    });
    const claim = (n) => $('.c-claim', cl(n)[0]);
    tl.to(cl(1), { opacity: 1, duration: 0.4 }, 0)
      .to(claim(1), { backgroundSize: '100% 100%', duration: 0.8 }, 0.2)
      .to(cg(1), { opacity: 1, x: 0, duration: 0.5 }, 0.6)
      .to(prog, { 1: 1, duration: 0.8 }, 0.8)
      .to(cl(2), { opacity: 1, duration: 0.4 }, 2)
      .to(claim(2), { backgroundSize: '100% 100%', duration: 0.8 }, 2.2)
      .to(cg(2), { opacity: 1, x: 0, duration: 0.5 }, 2.6)
      .to(prog, { 2: 1, duration: 0.8 }, 2.8)
      .to(cg(3), { opacity: 1, x: 0, duration: 0.5 }, 4)
      .to(prog, { 3: 1, duration: 0.8 }, 4.2)
      .to($('[data-strike]', col), { backgroundSize: '100% 2px', duration: 0.8 }, 5.4)
      .to($('[data-sawab]', col), { opacity: 1, y: 0, duration: 0.6 }, 6)
      .to(cl(4), { opacity: 1, duration: 0.4 }, 7)
      .to(claim(4), { backgroundSize: '100% 100%', duration: 0.8 }, 7.2)
      .to([cg(4), cg(5)], { opacity: 1, x: 0, duration: 0.5, stagger: 0.2 }, 7.5)
      .to(prog, { 4: 1, 5: 1, duration: 0.9 }, 7.8)
      .to(cl(6), { opacity: 1, duration: 0.5, stagger: 0.25 }, 9)
      .to({}, { duration: 1 }, 9.8);
    sync(0);
    addEventListener('resize', paint);
  }

  /* ---------- the isnad: the chain is drawn down to each link as the reader reaches it ---------- */
  const chain = $('[data-chain]');
  if (chain && window.gsap && window.ScrollTrigger && !reduce) {
    window.gsap.registerPlugin(window.ScrollTrigger);
    const links = $$('[data-link]', chain);
    chain.classList.add('is-scrub');
    chain.style.setProperty('--fill', 0);
    const lit = (p) => {
      chain.style.setProperty('--fill', p.toFixed(3));
      const h = chain.clientHeight - 44;
      links.forEach((li) => li.classList.toggle('is-lit', li.offsetTop + 22 - 22 <= h * p + 2));
    };
    window.ScrollTrigger.create({ trigger: chain, start: 'top 72%', end: 'bottom 58%', scrub: 0.4, onUpdate: (st) => lit(st.progress) });
    lit(0);
  }

  /* ---------- the copyists' signs ---------- */
  const signs = $$('[data-sign]');
  if (signs.length) {
    const views = $$('[data-sign-view]'), label = $('[data-sign-label]');
    const show = (li) => {
      signs.forEach((s) => s.classList.toggle('is-on', s === li));
      views.forEach((v) => v.classList.toggle('is-on', v.dataset.signView === li.dataset.sign));
      if (label) label.textContent = $('b', li).textContent;
    };
    signs.forEach((li) => { li.addEventListener('mouseenter', () => show(li)); li.addEventListener('focus', () => show(li)); });
  }

  /* ---------- identity: the one motion, replayable ---------- */
  const demo = $('[data-demo]');
  if (demo) {
    const claim = $('[data-demo-claim]', demo), ref = $('[data-demo-ref]', demo), line = $('.id-demo-line path', demo);
    /* the same hook as the folio's: up into the leading above the reference, out, then down to the gloss */
    const shape = () => {
      const box = demo.getBoundingClientRect(), r = ref.getBoundingClientRect(), g = $('.id-demo-gloss .mark', demo).getBoundingClientRect();
      if (!g.width || getComputedStyle(demo).gridTemplateColumns.split(' ').length < 2) { line.setAttribute('d', ''); return 0; }
      const sx = r.left - box.left - 3, sy = r.top - box.top + r.height / 2, up = sy - 20, rad = 7;
      const gx = g.right - box.left + 6, gy = g.top - box.top + g.height / 2, ex = gx + 40;
      line.setAttribute('d', `M${sx} ${sy}V${up + rad}Q${sx} ${up} ${sx - rad} ${up}H${ex}C${ex - 24} ${up} ${gx + 20} ${gy} ${gx} ${gy}`);
      return line.getTotalLength();
    };
    const play = () => {
      claim.classList.remove('is-on'); ref.classList.remove('is-on');
      const len = shape();
      line.style.transition = 'none'; line.style.strokeDasharray = len; line.style.strokeDashoffset = reduce ? 0 : len;
      void demo.offsetWidth;
      setTimeout(() => {
        claim.classList.add('is-on'); ref.classList.add('is-on');
        line.style.transition = 'stroke-dashoffset .9s cubic-bezier(.6,.02,.2,1) .7s'; line.style.strokeDashoffset = 0;
      }, 60);
    };
    addEventListener('resize', () => { const len = shape(); line.style.transition = 'none'; line.style.strokeDasharray = len; line.style.strokeDashoffset = 0; });
    new IntersectionObserver(([e], io) => { if (e.isIntersecting) { play(); io.disconnect(); } }, { threshold: 0.6 }).observe(demo);
    const btn = $('[data-replay]'); if (btn) btn.addEventListener('click', play);
  }

  /* ---------- the rest of the page is set as the reader reaches it ---------- */
  if (!reduce && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
    let i = 0;
    $$('.sec .sec-head, .leaves > li, .feature, .lines, .signs-demo, .signs-list > li, .isnad > li, .refs > li, .act, .id-sheet').forEach((el) => {
      if (el.getBoundingClientRect().top < innerHeight * 0.9) return;
      el.classList.add('reveal'); el.style.transitionDelay = ((i++ % 5) * 60) + 'ms'; io.observe(el);
    });
  }
})();
