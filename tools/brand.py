"""The موثّق brand marks, drawn from the type itself.

python -I tools/brand.py   (from the project root; needs research/font-src/Vazirmatn[wght].ttf)

The wordmark is the word موثّق shaped by HarfBuzz in Vazirmatn Black and outlined, so the logo
needs no font. Its shadda (the sign of doubling, شدّة: tightening) is drawn in sealing-wax red:
the one mark that says the word has been made firm. The seal mark is that same shadda pressed
into a wax disc: the knot of the cord that ties an exhibit, under its seal.
"""
import io
import math
import os

import uharfbuzz as hb
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'research', 'font-src', 'Vazirmatn[wght].ttf')
OUT = os.path.join(ROOT, 'assets', 'brand')
os.makedirs(OUT, exist_ok=True)

INK, WAX, WAX_DEEP, WAX_HI, SHEET = '#15171A', '#B0241C', '#7E1712', '#D24A3A', '#FFFFFF'


def instance(wght):
    font = instancer.instantiateVariableFont(TTFont(SRC), {'wght': wght})
    buf = io.BytesIO()
    font.save(buf)
    data = buf.getvalue()
    return TTFont(io.BytesIO(data)), data


def svg_d(contour):
    d = ''
    for op, pts in contour:
        if op == 'moveTo':
            d += 'M%.1f %.1f' % pts[0]
        elif op == 'lineTo':
            d += 'L%.1f %.1f' % pts[0]
        elif op == 'qCurveTo':
            # TrueType quadratic spline with implied on-curve points
            for i in range(len(pts) - 1):
                c1, nxt = pts[i], pts[i + 1]
                if i < len(pts) - 2:
                    nxt = ((c1[0] + pts[i + 1][0]) / 2, (c1[1] + pts[i + 1][1]) / 2)
                d += 'Q%.1f %.1f %.1f %.1f' % (c1[0], c1[1], nxt[0], nxt[1])
        elif op == 'curveTo':
            d += 'C%.1f %.1f %.1f %.1f %.1f %.1f' % (*pts[0], *pts[1], *pts[2])
        elif op == 'closePath':
            d += 'Z'
    return d


def shape(text, wght=900):
    """Outline `text` contour by contour: [(path_d, kind, bounds)], kind in body|dot|shadda.

    Vazirmatn draws its dots as diamonds; here every dot becomes a round, pressed drop.
    """
    font, data = instance(wght)
    face = hb.Face(data)
    hbfont = hb.Font(face)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {'kern': True, 'liga': True})
    glyphs = font.getGlyphSet()
    upm = font['head'].unitsPerEm
    cmap = {v: k for k, v in font.getBestCmap().items()}
    shadda_names = {n for n, u in cmap.items() if u == 0x0651}
    out, x = [], 0
    xs, ys = [], []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = font.getGlyphName(info.codepoint)
        rec = DecomposingRecordingPen(glyphs)
        glyphs[name].draw(rec)
        ox, oy = x + pos.x_offset, -pos.y_offset
        contours, cur = [], []
        for op, args in rec.value:
            pts = [(ox + px, oy - py) for px, py in args]
            cur.append((op, pts))
            if op in ('closePath', 'endPath'):
                contours.append(cur)
                cur = []
        parsed = []
        for c in contours:
            allp = [p for _, pts in c for p in pts]
            if not allp:
                continue
            bx = (min(p[0] for p in allp), min(p[1] for p in allp), max(p[0] for p in allp), max(p[1] for p in allp))
            xs += [bx[0], bx[2]]
            ys += [bx[1], bx[3]]
            area = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(allp, allp[1:] + allp[:1])) / 2
            parsed.append((svg_d(c), bx, area))
        if not parsed:
            x += pos.x_advance
            continue
        outer = max(parsed, key=lambda p: abs(p[2]))[2] > 0   # winding of the glyph's main outline
        body = ''
        for d, bx, area in parsed:
            w, h = bx[2] - bx[0], bx[3] - bx[1]
            is_outer = (area > 0) == outer
            if name not in shadda_names and is_outer and max(w, h) < 0.2 * upm and abs(w - h) < 0.35 * max(w, h):
                out.append((d, 'dot', bx))          # a dot: drawn as a round drop
            else:
                body += d                             # outlines and their counters stay one path
        if body:
            gb = (min(p[1][0] for p in parsed), min(p[1][1] for p in parsed), max(p[1][2] for p in parsed), max(p[1][3] for p in parsed))
            out.append((body, 'shadda' if name in shadda_names else 'body', gb))
        x += pos.x_advance
    return out, (min(xs), min(ys), max(xs), max(ys)), upm


def draw(paths, upm, ink, accent, round_px=0.016, dot_k=0.8):
    """SVG for outlined contours: round dots, softened corners, the shadda in the accent."""
    soft = round_px * upm
    parts = []
    for d, kind, (x0, y0, x1, y1) in paths:
        if kind == 'dot':
            r = (x1 - x0 + y1 - y0) / 4 * dot_k
            parts.append(f'<circle cx="{(x0 + x1) / 2:.1f}" cy="{(y0 + y1) / 2:.1f}" r="{r:.1f}" fill="{ink}"/>')
        else:
            col = accent if kind == 'shadda' else ink
            parts.append(f'<path d="{d}" fill="{col}" stroke="{col}" stroke-width="{soft:.1f}" stroke-linejoin="round"/>')
    return ''.join(parts)


def wax_edge(cx, cy, r, lobes=9, amp=0.045, seed=0.7, steps=180):
    """A pressed-wax rim: a circle pushed out in soft, uneven lobes (smooth, no corners)."""
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        k = 1 + amp * math.sin(lobes * t + seed) + amp * 0.45 * math.sin((lobes + 4) * t + 2 * seed)
        pts.append((cx + r * k * math.cos(t), cy + r * k * math.sin(t)))
    d = 'M%.2f %.2f ' % pts[0]
    # Catmull-Rom through the samples -> cubic Béziers, closed
    n = len(pts)
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += 'C%.2f %.2f %.2f %.2f %.2f %.2f ' % (*c1, *c2, *p2)
    return d + 'Z'


# The shadda as a cord: one continuous stroke, two cups, round ends (viewBox 64 x 64).
CORD = 'M17.5 26.5C17.5 33.6 20.6 37 24.8 37C29 37 32 33.6 32 28.4C32 33.6 35 37 39.2 37C43.4 37 46.5 33.6 46.5 26.5'


def mark(fill=WAX, rim=WAX_DEEP, cord=SHEET, lobes=True):
    edge = wax_edge(32, 32, 27.5) if lobes else 'M32 4.5a27.5 27.5 0 1 1 0 55a27.5 27.5 0 1 1 0-55Z'
    return (f'<path d="{edge}" fill="{fill}"/>'
            f'<circle cx="32" cy="32" r="20.5" fill="none" stroke="{rim}" stroke-opacity=".55" stroke-width="1.6"/>'
            f'<path d="{CORD}" fill="none" stroke="{cord}" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>')


def svg(view, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def tha_seal(edge_r=27.5):
    """The seal: ث, the root letter of وثق (to bind fast, to trust), reversed out of wax.
    Its three round dots read as the three independent sources a fact is checked against."""
    paths, (x0, y0, x1, y1), upm = shape('ث')
    w, h = x1 - x0, y1 - y0
    s = 31 / max(w, h)
    g = draw(paths, upm, SHEET, SHEET, dot_k=0.7)
    return (f'<path d="{wax_edge(32, 32, edge_r)}" fill="{WAX}"/>'
            f'<circle cx="32" cy="32" r="{edge_r - 5.2:.1f}" fill="none" stroke="{WAX_DEEP}" stroke-opacity=".45" stroke-width="1.2"/>'
            f'<g transform="translate({32 - s * (x0 + w / 2):.2f} {33.6 - s * (y0 + h / 2):.2f}) scale({s:.5f})">{g}</g>')


def main():
    paths, (x0, y0, x1, y1), upm = shape('موثّق')
    pad = 60
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    t = f'translate({pad - x0:.1f} {pad - y0:.1f})'
    open(os.path.join(OUT, 'wordmark.svg'), 'w', encoding='utf-8').write(
        svg(f'0 0 {w:.0f} {h:.0f}', f'<g transform="{t}">{draw(paths, upm, INK, WAX)}</g>', 'موثّق'))
    open(os.path.join(OUT, 'wordmark-reversed.svg'), 'w', encoding='utf-8').write(
        svg(f'0 0 {w:.0f} {h:.0f}', f'<g transform="{t}">{draw(paths, upm, SHEET, WAX_HI)}</g>', 'موثّق'))
    seal = tha_seal()
    open(os.path.join(OUT, 'mark.svg'), 'w', encoding='utf-8').write(svg('0 0 64 64', seal, 'موثّق'))
    open(os.path.join(OUT, 'mark-ink.svg'), 'w', encoding='utf-8').write(
        svg('0 0 64 64', seal.replace(WAX, INK).replace(WAX_DEEP, '#000'), 'موثّق'))
    fav = tha_seal(29.5).replace(wax_edge(32, 32, 29.5), 'M32 2.5a29.5 29.5 0 1 1 0 59a29.5 29.5 0 1 1 0-59Z')
    open(os.path.join(ROOT, 'favicon.svg'), 'w', encoding='utf-8').write(svg('0 0 64 64', fav, 'موثّق'))
    print('wordmark', round(w), 'x', round(h), 'upm', upm, 'kinds', [k for _, k, _ in paths])


if __name__ == '__main__':
    main()
