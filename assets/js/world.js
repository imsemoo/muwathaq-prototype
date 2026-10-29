/* موثّق — the world's shared motion: cords that hang and tighten between records that really link,
   records laid on the table as they come into view, knots tied as the reader passes them, and the loose
   cord of the 404. Loaded on every page after site.js; every effect sits on top of working HTML. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wide = () => matchMedia('(min-width: 1025px)').matches;

  /* ---------- a verlet rope between two points ---------- */
  class Rope {
    constructor(n = 16) { this.n = n; this.p = null; }
    step(a, b, { slack = 1.12, gravity = 0.42, wind = 0, iter = 14, freeEnd = false } = {}) {
      const n = this.n;
      if (!this.p) { this.p = []; for (let k = 0; k < n; k++) { const t = k / (n - 1); const x = a[0] + (b[0] - a[0]) * t, y = a[1] + (b[1] - a[1]) * t; this.p.push([x, y, x, y]); } }
      const P = this.p, last = freeEnd ? n : n - 1;
      const seg = (Math.hypot(b[0] - a[0], b[1] - a[1]) * slack) / (n - 1);
      if (!reduce) {
        for (let k = 1; k < last; k++) {
          const q = P[k], vx = (q[0] - q[2]) * 0.972, vy = (q[1] - q[3]) * 0.972;
          q[2] = q[0]; q[3] = q[1]; q[0] += vx + wind * (k / n); q[1] += vy + gravity;
        }
      }
      for (let it = 0; it < (reduce ? 60 : iter); it++) {
        P[0][0] = a[0]; P[0][1] = a[1];
        if (!freeEnd) { P[n - 1][0] = b[0]; P[n - 1][1] = b[1]; }
        for (let k = 0; k < n - 1; k++) {
          const p = P[k], q = P[k + 1];
          const dx = q[0] - p[0], dy = q[1] - p[1], d = Math.hypot(dx, dy) || 0.0001, diff = (d - seg) / d / 2;
          if (k > 0) { p[0] += dx * diff; p[1] += dy * diff; }
          if (k + 1 < last) { q[0] -= dx * diff; q[1] -= dy * diff; }
        }
        if (reduce) for (let k = 1; k < last; k++) P[k][1] += 0.5;
      }
      return P;
    }
    draw(ctx, hot) {
      const P = this.p, n = this.n;
      ctx.beginPath(); ctx.moveTo(P[0][0], P[0][1]);
      for (let k = 1; k < n - 1; k++) ctx.quadraticCurveTo(P[k][0], P[k][1], (P[k][0] + P[k + 1][0]) / 2, (P[k][1] + P[k + 1][1]) / 2);
      ctx.lineTo(P[n - 1][0], P[n - 1][1]);
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.setLineDash([]); ctx.strokeStyle = hot ? '#15171A' : '#69717A'; ctx.lineWidth = hot ? 2.6 : 2; ctx.stroke();
      ctx.setLineDash([2.2, 3.2]); ctx.strokeStyle = 'rgba(255,255,255,.34)'; ctx.lineWidth = 0.9; ctx.stroke();
      ctx.setLineDash([]);
    }
  }
  window.MWRope = Rope;

  /* a canvas that runs only while visible */
  function animator(canvas, frame, watch, gate = () => true) {
    const ctx = canvas.getContext('2d');
    let dpr = 1, W = 0, H = 0, run = false, seen = true;
    const size = () => { const r = canvas.getBoundingClientRect(); dpr = Math.min(2, devicePixelRatio || 1); W = r.width; H = r.height; canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr); };
    const tick = () => { if (!run) return; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H); frame(ctx, canvas.getBoundingClientRect()); requestAnimationFrame(tick); };
    const start = () => { if (!run && seen && gate()) { run = true; size(); requestAnimationFrame(tick); } };
    const stop = () => { run = false; ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, canvas.width, canvas.height); };
    new IntersectionObserver(([e]) => { seen = e.isIntersecting; seen ? start() : stop(); }).observe(watch || canvas);
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    addEventListener('resize', () => { size(); gate() ? start() : stop(); });
    if (reduce) { size(); setTimeout(() => { ctx.setTransform(dpr, 0, 0, dpr, 0, 0); frame(ctx, canvas.getBoundingClientRect()); }, 400); return { start() {}, stop() {}, size }; }
    start();
    return { start, stop, size };
  }

  /* ---------- record pages: cords from the seal to every linked record ---------- */
  $$('[data-cords]').forEach((box) => {
    const from = $('[data-cord-from]', box), targets = $$('[data-cord-to]', box);
    const old = $('svg.cords', box); if (old) old.remove();
    if (!from || !targets.length) return;
    const cv = document.createElement('canvas');   /* viewport-sized: records can be thousands of pixels tall */
    cv.className = 'rope-canvas'; cv.setAttribute('aria-hidden', 'true');
    document.body.prepend(cv);
    const ropes = targets.map(() => new Rope(18));
    let hot = -1, t0 = performance.now();
    targets.forEach((t, i) => {
      ['mouseenter', 'focusin'].forEach((ev) => t.addEventListener(ev, () => { hot = i; }));
      ['mouseleave', 'focusout'].forEach((ev) => t.addEventListener(ev, () => { if (hot === i) hot = -1; }));
    });
    const c = (el) => el.getBoundingClientRect();
    animator(cv, (ctx, r) => {
      if (!wide()) return;
      const s = c(from); if (s.bottom < -40) return;
      const a = [s.left + s.width / 2 - r.left, s.top + s.height / 2 - r.top];
      const wind = reduce ? 0 : Math.sin((performance.now() - t0) / 1600) * 0.06;
      targets.forEach((t, i) => {
        const q = c(t); if (!q.width || q.top > innerHeight + 30 || q.bottom < 0) return;
        const b = [q.right - r.left + 1, q.top - r.top + Math.min(30, q.height / 2)];
        ropes[i].step(a, b, { slack: hot === i ? 1.004 : 1.1, wind, gravity: 0.38 });
        ropes[i].draw(ctx, hot === i);
      });
    }, box, wide);
  });

  /* ---------- records are laid on the table as they come into view ---------- */
  if (!reduce && 'IntersectionObserver' in window) {
    const sel = '.read > .photo, .read > .sheet, .read > .rows, .read > .accounts, .read > .official, .read > .verify, .read > blockquote.official, .read .timeline > li, .triad, .uses, .minis > li, .two-col-note, .method-side .sheet, .id-grid .sheet, .submit-side .sheet, .act-grid .act';
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-laid'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
    let i = 0;
    $$(sel).forEach((el) => {
      if (el.getBoundingClientRect().top < innerHeight * 0.92) return;
      el.classList.add('lay'); el.style.setProperty('--d', ((i++ % 4) * 50) + 'ms'); io.observe(el);
    });
  }

  /* ---------- knots are tied as the reader passes them ---------- */
  $$('[data-tie]').forEach((list) => {
    const knots = $$(':scope > li', list);
    if (reduce) { knots.forEach((k) => k.classList.add('is-tied')); return; }
    list.classList.add('is-tying');
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-tied'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -38% 0px' });
    knots.forEach((k) => io.observe(k));
  });

  /* ---------- the archive's time rope: one knot per incident ---------- */
  $$('[data-timerope]').forEach((box) => {
    const tip = $('.tr-tip', box);
    $$('.tr-knot', box).forEach((k) => {
      const show = () => {
        tip.textContent = k.dataset.label; tip.hidden = false;
        const r = box.getBoundingClientRect(), q = k.getBoundingClientRect();
        tip.style.left = Math.max(8, Math.min(r.width - tip.offsetWidth - 8, q.left - r.left + q.width / 2 - tip.offsetWidth / 2)) + 'px';
        const row = document.querySelector(`.rows [data-cord-to="${k.dataset.id}"]`); $$('.row.is-hot').forEach((x) => x.classList.remove('is-hot')); row && row.classList.add('is-hot');
      };
      const hide = () => { tip.hidden = true; $$('.row.is-hot').forEach((x) => x.classList.remove('is-hot')); };
      k.addEventListener('mouseenter', show); k.addEventListener('focus', show);
      k.addEventListener('mouseleave', hide); k.addEventListener('blur', hide);
    });
  });

  /* ---------- 404: a loose cord, its seal never pressed ---------- */
  const loose = $('[data-loose]');
  if (loose) {
    const cv = $('canvas', loose), sealEl = $('.loose-seal', loose), rope = new Rope(22);
    let mx = null, my = null;
    loose.addEventListener('pointermove', (e) => { const r = cv.getBoundingClientRect(); mx = e.clientX - r.left; my = e.clientY - r.top; });
    loose.addEventListener('pointerleave', () => { mx = null; });
    animator(cv, (ctx, r) => {
      const a = [r.width * 0.5, -4];
      const P = rope.step(a, [r.width * 0.5, r.height * 0.62], { slack: 1, gravity: 0.5, freeEnd: true, iter: 18 });
      const end = P[P.length - 1];
      if (mx !== null) { const dx = mx - end[0], dy = my - end[1], d = Math.hypot(dx, dy); if (d < 160) { end[0] += dx * 0.06; end[1] += dy * 0.06; } }
      rope.draw(ctx, false);
      sealEl.style.transform = `translate(${(end[0] - r.width / 2).toFixed(1)}px, ${end[1].toFixed(1)}px) rotate(${((end[0] - P[P.length - 3][0]) * 2).toFixed(1)}deg)`;
    });
  }
})();
