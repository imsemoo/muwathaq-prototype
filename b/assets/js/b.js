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
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => setTimeout(() => { set(1); run(); }, reduce ? 0 : 900));
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
