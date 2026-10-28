// Dead-space probe: rasterise everything that paints (text, images, svg, canvas, controls, and any box with a
// background, border or shadow) onto a 40 px grid over the page's content width, then report empty regions
// at least 200 px tall and 320 px wide. Run in the page after it settles.
await (document.fonts ? document.fonts.ready : Promise.resolve());
(() => {
  const C = 40, W = document.documentElement.clientWidth, H = document.documentElement.scrollHeight;
  const wrap = document.querySelector('main .wrap') || document.body;
  const wr = wrap.getBoundingClientRect();
  const x0 = Math.max(0, wr.left), x1 = Math.min(W, wr.right);
  const cols = Math.ceil((x1 - x0) / C), rows = Math.ceil(H / C);
  const grid = new Uint8Array(cols * rows);
  const mark = (r) => {
    const top = r.top + scrollY, bot = r.bottom + scrollY;
    if (r.width < 2 || r.height < 2) return;
    for (let y = Math.max(0, Math.floor(top / C)); y < Math.min(rows, Math.ceil(bot / C)); y++)
      for (let x = Math.max(0, Math.floor((r.left - x0) / C)); x < Math.min(cols, Math.ceil((r.right - x0) / C)); x++) grid[y * cols + x] = 1;
  };
  const paints = (el, cs) => {
    if (['IMG', 'SVG', 'CANVAS', 'INPUT', 'SELECT', 'TEXTAREA', 'BUTTON', 'VIDEO'].includes(el.tagName.toUpperCase())) return true;
    const bg = cs.backgroundColor, bd = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth);
    const opaque = bg && !/rgba\(0, 0, 0, 0\)|transparent/.test(bg) && bg !== getComputedStyle(document.body).backgroundColor;
    return opaque || bd > 0 || cs.boxShadow !== 'none';
  };
  for (const el of document.body.querySelectorAll('main *, footer')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
    if (paints(el, cs)) mark(el.getBoundingClientRect());
    // a sticky panel travels down its parent as the reader scrolls, so it fills that whole track
    if (cs.position === 'sticky') { const r = el.getBoundingClientRect(), pr = el.parentElement.getBoundingClientRect(); mark({ left: r.left, right: r.right, width: r.width, top: r.top, bottom: pr.bottom, height: pr.bottom - r.top }); }
  }
  const walker = document.createTreeWalker(document.querySelector('main'), NodeFilter.SHOW_TEXT);
  for (let n; (n = walker.nextNode());) {
    if (!n.textContent.trim()) continue;
    const range = document.createRange(); range.selectNodeContents(n);
    for (const r of range.getClientRects()) mark(r);
  }
  // empty regions: maximal rectangles found greedily from row runs
  const out = [];
  const used = new Uint8Array(cols * rows);
  const mainTop = document.querySelector('main').getBoundingClientRect().top + scrollY;
  const mainBot = document.querySelector('main').getBoundingClientRect().bottom + scrollY;
  for (let y = Math.floor(mainTop / C); y < Math.min(rows, Math.ceil(mainBot / C)); y++) {
    for (let x = 0; x < cols; x++) {
      if (grid[y * cols + x] || used[y * cols + x]) continue;
      let w = 0; while (x + w < cols && !grid[y * cols + x + w] && !used[y * cols + x + w]) w++;
      let h = 1; outer: while (y + h < rows) { for (let k = 0; k < w; k++) if (grid[(y + h) * cols + x + k]) break outer; h++; }
      if (w * C >= 320 && h * C >= 200) {
        out.push({ top: y * C, height: h * C, left: Math.round(x0 + x * C), width: w * C });
        for (let yy = y; yy < y + h; yy++) for (let k = 0; k < w; k++) used[yy * cols + x + k] = 1;
      }
      x += w;
    }
  }
  return { page: location.pathname, height: H, empty: out.sort((a, b) => b.width * b.height - a.width * a.height).slice(0, 8) };
})();
