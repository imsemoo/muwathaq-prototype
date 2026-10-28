// Visual QA probe. Paste the whole file into the browser's JavaScript tool
// after the page has settled at the viewport under test. It waits for web fonts,
// then measures; it never changes the page. Every list is capped so the result stays readable.
await (document.fonts ? document.fonts.ready : Promise.resolve());
(() => {
  const CAP = 12;
  const W = window.innerWidth;
  const H = window.innerHeight;
  const short = (src) => {
    try { const u = new URL(src, location.href); return u.pathname.split("/").slice(-2).join("/"); } catch { return String(src).slice(-60); }
  };
  // A parent that clips horizontally (carousels, scrollers) keeps its children from widening the page.
  const clippedByAncestor = (el) => {
    for (let n = el.parentElement; n && n !== document.body; n = n.parentElement) {
      if (["hidden", "clip", "auto", "scroll"].includes(getComputedStyle(n).overflowX)) return true;
    }
    return false;
  };
  const path = (el) => {
    const parts = [];
    for (let n = el; n && n.nodeType === 1 && parts.length < 4; n = n.parentElement) {
      let s = n.tagName.toLowerCase();
      if (n.id) { s += `#${n.id}`; parts.unshift(s); break; }
      const cls = [...n.classList].slice(0, 2).join(".");
      if (cls) s += `.${cls}`;
      parts.unshift(s);
    }
    return parts.join(" > ");
  };
  const visible = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden" || +cs.opacity === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const all = [...document.body.querySelectorAll("*")].filter((el) => !["SCRIPT", "STYLE", "NOSCRIPT", "TEMPLATE"].includes(el.tagName));

  // 1. Horizontal overflow: the page scrolls sideways, and which elements stick out.
  const pageOverflow = document.documentElement.scrollWidth - W;
  const sticking = [];
  for (const el of all) {
    if (sticking.length >= CAP) break;
    if (!visible(el)) continue;
    const cs = getComputedStyle(el);
    if (cs.position === "fixed") continue;
    const r = el.getBoundingClientRect();
    if ((r.right > W + 1 || r.left < -1) && !clippedByAncestor(el)) {
      // Report the outermost offender only, not every child inside it.
      if (!sticking.some((s) => s.el.contains(el))) sticking.push({ el, left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width) });
    }
  }

  // 2. Clipped text: an element's own text cut by overflow hidden without an ellipsis.
  //    Containers (carousels) and visually hidden labels (1px sr-only boxes) are skipped.
  const clipped = [];
  for (const el of all) {
    if (clipped.length >= CAP) break;
    const ownText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (!ownText || !visible(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width <= 2 || r.height <= 2) continue;
    const cs = getComputedStyle(el);
    const hides = cs.overflow === "hidden" || cs.overflowX === "hidden" || cs.overflowY === "hidden";
    if (!hides || cs.textOverflow === "ellipsis" || cs.webkitLineClamp !== "none") continue;
    if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 2) clipped.push(path(el));
  }

  // 3. Images: broken, missing alt, no intrinsic size (layout shift), far larger than displayed.
  const imgs = [...document.images];
  const dpr = window.devicePixelRatio || 1;
  const img = { total: imgs.length, broken: [], noAlt: [], noSize: [], oversized: [], lazyAboveFold: [] };
  for (const im of imgs) {
    const src = im.currentSrc || im.src ? short(im.currentSrc || im.src) : "";
    if (im.complete && im.naturalWidth === 0 && src) img.broken.push(src);
    if (!im.hasAttribute("alt")) img.noAlt.push(src || path(im));
    if (!im.getAttribute("width") && !im.getAttribute("height") && !getComputedStyle(im).aspectRatio.includes("/")) img.noSize.push(src);
    const r = im.getBoundingClientRect();
    if (r.width > 0 && im.naturalWidth > r.width * dpr * 2 && im.naturalWidth > 600) img.oversized.push(`${src} natural ${im.naturalWidth}px, shown ${Math.round(r.width)}px`);
    if (im.loading === "lazy" && r.top < H && r.bottom > 0) img.lazyAboveFold.push(src);
  }
  for (const k of ["broken", "noAlt", "noSize", "oversized", "lazyAboveFold"]) img[k] = img[k].slice(0, CAP);

  // 4. Small tap targets (WCAG 2.5.8 asks for 24 x 24 CSS px; inline text links are exempt).
  const small = [];
  for (const el of document.querySelectorAll("button, input:not([type=hidden]), select, textarea, [role=button], a")) {
    if (small.length >= CAP) break;
    if (!visible(el)) continue;
    if (el.tagName === "A" && getComputedStyle(el).display === "inline" && el.closest("p, li, td, figcaption")) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 24 || r.height < 24) small.push(`${path(el)} ${Math.round(r.width)}x${Math.round(r.height)}`);
  }

  // 5. Structure: h1 count, skipped heading levels, landmarks, unlabeled controls.
  const heads = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")].filter(visible).map((h) => +h.tagName[1]);
  const skips = [];
  heads.forEach((lvl, i) => { if (i && lvl > heads[i - 1] + 1) skips.push(`h${heads[i - 1]} -> h${lvl}`); });
  const unlabeled = [...document.querySelectorAll("input:not([type=hidden]):not([type=submit]):not([type=button]), select, textarea")]
    .filter((el) => visible(el) && !el.getAttribute("aria-label") && !el.getAttribute("aria-labelledby") && !el.closest("label") && !(el.id && document.querySelector(`label[for="${CSS.escape(el.id)}"]`)))
    .slice(0, CAP).map(path);

  // 6. Contrast of visible text against its nearest opaque background (approximate:
  //    background images and gradients are skipped and reported as unknown).
  const rgb = (s) => (s.match(/[\d.]+/g) || []).map(Number);
  const lum = ([r, g, b]) => [r, g, b].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }).reduce((a, v, i) => a + v * [0.2126, 0.7152, 0.0722][i], 0);
  const bgOf = (el) => {
    for (let n = el; n; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage !== "none") return null;
      const c = rgb(cs.backgroundColor);
      if (c.length >= 3 && (c[3] === undefined || c[3] > 0.95)) return c;
    }
    return [255, 255, 255];
  };
  const lowContrast = [];
  let checked = 0, unknown = 0;
  for (const el of all) {
    if (checked >= 400 || lowContrast.length >= CAP) break;
    const own = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (!own || !visible(el)) continue;
    checked++;
    const cs = getComputedStyle(el);
    const bg = bgOf(el);
    if (!bg) { unknown++; continue; }
    const fg = rgb(cs.color);
    const [a, b] = [lum(fg), lum(bg)].sort((x, y) => y - x);
    const ratio = (a + 0.05) / (b + 0.05);
    const size = parseFloat(cs.fontSize);
    const large = size >= 24 || (size >= 18.66 && +cs.fontWeight >= 700);
    if (ratio < (large ? 3 : 4.5)) lowContrast.push(`${path(el)} ${ratio.toFixed(2)}:1 (${size}px)`);
  }

  // 7. Fonts actually in use, and whether the webfonts finished loading.
  const families = new Set();
  for (const sel of ["body", "h1", "h2", "p", "button", "nav a"]) {
    const el = document.querySelector(sel);
    if (el) families.add(getComputedStyle(el).fontFamily.split(",")[0].trim());
  }

  return {
    viewport: `${W}x${H} @${Math.round(dpr * 100) / 100}x`,
    lang: document.documentElement.lang || "(missing)",
    dir: document.documentElement.dir || getComputedStyle(document.documentElement).direction,
    horizontalOverflowPx: pageOverflow > 0 ? pageOverflow : 0,
    elementsOutsideViewport: sticking.map((s) => `${path(s.el)} left ${s.left} right ${s.right}`),
    clippedText: clipped,
    images: img,
    smallTapTargets: small,
    h1Count: heads.filter((h) => h === 1).length,
    headingSkips: skips.slice(0, CAP),
    landmarks: ["header", "nav", "main", "footer"].filter((t) => document.querySelector(`${t}, [role=${t === "header" ? "banner" : t === "footer" ? "contentinfo" : t === "nav" ? "navigation" : "main"}]`)),
    unlabeledControls: unlabeled,
    lowContrast,
    contrastChecked: checked,
    contrastUnknown: unknown,
    fontsInUse: [...families],
    fontsStatus: document.fonts ? document.fonts.status : "n/a",
    domNodes: all.length,
  };
})()
