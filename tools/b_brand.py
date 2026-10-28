"""Direction B, «المتن والحاشية»: the marks, drawn from the type itself.

python -I tools/b_brand.py   (from the project root; needs research/font-src/NotoNaskhArabic[wght].ttf, Amiri-Bold.ttf)

In Arabic manuscripts a word the copyist left out is written in the margin, and a short hooked line, the
لحق, runs from the gap in the text out to it; the addition is then signed صح, «verified». The wordmark is
موثّق set in Noto Naskh Arabic Bold, its لحق rising from the end of the word into the margin, signed صح in
lapis. The mark is that صح alone, the copyist's sign of a checked reading, reversed out of a lapis tile.
The copyists' other collation signs (بلغ، معا، خ، كذا) become the verification states.
"""
import io
import json
import os

import uharfbuzz as hb
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

from brand import svg_d

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, 'research', 'font-src')
OUT = os.path.join(ROOT, 'b', 'assets', 'brand')
os.makedirs(OUT, exist_ok=True)

INK, LAPIS, LAPIS_HI, SHEET = '#111417', '#2B44B8', '#9DAEFF', '#FFFFFF'
NASKH = os.path.join(FONTS, 'NotoNaskhArabic[wght].ttf')
AMIRI = os.path.join(FONTS, 'Amiri-Bold.ttf')


def load(path, wght=None):
    font = TTFont(path)
    if wght and 'fvar' in font:
        font = instancer.instantiateVariableFont(font, {'wght': wght})
    buf = io.BytesIO()
    font.save(buf)
    data = buf.getvalue()
    return TTFont(io.BytesIO(data)), data


def outline(path, text, wght=None):
    """`text` shaped by HarfBuzz and outlined as one SVG path (y down), with its bounds."""
    font, data = load(path, wght)
    hbfont = hb.Font(hb.Face(data))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {'kern': True, 'liga': True})
    glyphs = font.getGlyphSet()
    d, x, pts_all = '', 0, []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        rec = DecomposingRecordingPen(glyphs)
        glyphs[font.getGlyphName(info.codepoint)].draw(rec)
        ox, oy = x + pos.x_offset, -pos.y_offset
        cur = []
        for op, args in rec.value:
            pts = [(ox + px, oy - py) for px, py in args]
            pts_all += pts
            cur.append((op, pts))
            if op in ('closePath', 'endPath'):
                d += svg_d(cur)
                cur = []
        x += pos.x_advance
    xs, ys = [p[0] for p in pts_all], [p[1] for p in pts_all]
    return d, (min(xs), min(ys), max(xs), max(ys)), font['head'].unitsPerEm


def placed(path, text, box_w, box_h, cx, cy, fill, wght=None):
    """The outline of `text` scaled to fit box_w x box_h and centred on (cx, cy)."""
    d, (x0, y0, x1, y1), _ = outline(path, text, wght)
    s = min(box_w / (x1 - x0), box_h / (y1 - y0))
    tx, ty = cx - s * (x0 + x1) / 2, cy - s * (y0 + y1) / 2
    return f'<path d="{d}" fill="{fill}" transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})"/>', s


def svg(view, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def wordmark(ink, lapis):
    """موثّق with its لحق: from the end of the word up and out into the margin, signed صح."""
    d, (x0, y0, x1, y1), upm = outline(NASKH, 'موثّق', 700)
    h = y1 - y0
    word = f'<path d="{d}" fill="{ink}"/>'
    # the hook starts just past the last letter (the left end of the word in RTL), climbs, then turns into the margin
    sx, sy = x0 - 0.08 * h, y0 + 0.66 * h
    top = y0 + 0.1 * h
    tip = x0 - 0.5 * h
    sw = 0.062 * h
    r = 0.26 * h
    hook = (f'<path d="M{sx:.1f} {sy:.1f}V{top + r:.1f}Q{sx:.1f} {top:.1f} {sx - r:.1f} {top:.1f}H{tip:.1f}" '
            f'fill="none" stroke="{lapis}" stroke-width="{sw:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    sah, _ = placed(AMIRI, 'صح', 0.84 * h, 0.6 * h, tip - 0.5 * h, top - 0.02 * h, lapis)
    pad = 0.12 * h
    vx0, vy0 = tip - 0.96 * h - pad, top - 0.34 * h - pad
    vx1, vy1 = x1 + pad, y1 + pad
    return svg(f'{vx0:.0f} {vy0:.0f} {vx1 - vx0:.0f} {vy1 - vy0:.0f}', word + hook + sah, 'موثّق'), (vx1 - vx0) / (vy1 - vy0)


def tile(fill, glyph, r=15):
    sah, _ = placed(AMIRI, 'صح', 40, 30, 32, 34.5, glyph)
    return f'<rect x="2" y="2" width="60" height="60" rx="{r}" fill="{fill}"/>{sah}'


# the copyists' collation signs as verification states: (state, sign or None, filled)
MARKS = [('complete', 'صح', True), ('specific', 'معا', False), ('partial', 'كذا', False),
         ('in_progress', 'بلغ', False), ('rereview', 'خ', False), ('not_started', None, False)]


def marks():
    """One 40 x 40 symbol per state: the sign written in a ring; صح alone sits on a filled disc."""
    out = {}
    for state, sign, filled in MARKS:
        ring = (f'<circle cx="20" cy="20" r="18.2" fill="currentColor"/>' if filled else
                f'<circle cx="20" cy="20" r="17.6" fill="none" stroke="currentColor" stroke-width="1.6"'
                f'{" stroke-dasharray=\"2.4 3.2\" stroke-linecap=\"round\"" if not sign else ""}/>')
        glyph = ''
        if sign:
            w = {1: 13, 2: 21, 3: 24}.get(len(sign), 24)
            glyph, _ = placed(AMIRI, sign, w, 17, 20, 21.2, 'var(--mark-on, #fff)' if filled else 'currentColor')
        out[state] = ring + glyph
    return out


def main():
    wm, ratio = wordmark(INK, LAPIS)
    open(os.path.join(OUT, 'wordmark.svg'), 'w', encoding='utf-8').write(wm)
    open(os.path.join(OUT, 'wordmark-reversed.svg'), 'w', encoding='utf-8').write(wordmark(SHEET, LAPIS_HI)[0])
    open(os.path.join(OUT, 'mark.svg'), 'w', encoding='utf-8').write(svg('0 0 64 64', tile(LAPIS, SHEET), 'موثّق'))
    open(os.path.join(OUT, 'mark-ink.svg'), 'w', encoding='utf-8').write(svg('0 0 64 64', tile(INK, SHEET), 'موثّق'))
    open(os.path.join(ROOT, 'b', 'favicon.svg'), 'w', encoding='utf-8').write(svg('0 0 64 64', tile(LAPIS, SHEET, 16), 'موثّق'))
    json.dump(marks(), open(os.path.join(OUT, 'marks.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print('wordmark ratio', round(ratio, 3))


if __name__ == '__main__':
    main()
