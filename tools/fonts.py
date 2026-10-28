"""Self-hosted WOFF2 subsets of the two faces.

python -I tools/fonts.py   (from the project root; sources in research/font-src, gitignored)

Vazirmatn (Saber Rastikerdar, OFL) carries everything Arabic, from the display status lines to the
reading text: picked side by side on the platform's own sentences against Beiruti, Noto Sans Arabic,
Almarai, Mada, Zain, Noto Kufi, Changa, Kufam, Scheherazade and Amiri as the clearest at reading size
and the steadiest at Black weight. Red Hat Mono (Red Hat, OFL) sets only data: reference numbers,
document symbols and file fingerprints, with a slashed zero.
"""
import io
import os
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'research', 'font-src')
OUT = os.path.join(ROOT, 'assets', 'fonts')
os.makedirs(OUT, exist_ok=True)

# Latin + Latin-1 + Extended-A, the transliteration letters Arabic names use, typographic punctuation,
# arrows, multiplication and degree signs.
UNICODES = (
    list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) +
    [0x1E0C, 0x1E0D, 0x1E24, 0x1E25, 0x1E62, 0x1E63, 0x1E6C, 0x1E6D, 0x1E92, 0x1E93, 0x02BE, 0x02BF, 0x02BC,
     0x2009, 0x200A, 0x2010, 0x2011, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026,
     0x2032, 0x2033, 0x2039, 0x203A, 0x20AC, 0x2116, 0x2190, 0x2191, 0x2192, 0x2193,
     0x2197, 0x2212, 0x00D7, 0x00B0, 0x00B7, 0x00BD]
)

ARABIC = list(range(0x0600, 0x0700)) + list(range(0xFB50, 0xFE00)) + list(range(0xFE70, 0xFF00)) + [0x200C, 0x200D, 0x200E, 0x200F]

JOBS = [  # file, out, axis limits, extra unicodes
    ('Vazirmatn[wght].ttf', 'vazirmatn.woff2', {'wght': (400, 900)}, ARABIC),
    ('RedHatMono[wght].ttf', 'redhatmono.woff2', {'wght': (400, 600)}, []),
]


def options():
    o = subset.Options()
    o.flavor = 'woff2'
    o.layout_features = ['*']
    o.name_IDs = ['*']
    o.notdef_outline = True
    o.glyph_names = False
    o.hinting = False
    o.desubroutinize = True
    return o


for src, out, limits, extra in JOBS:
    font = instancer.instantiateVariableFont(TTFont(os.path.join(SRC, src)), limits)
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    font = TTFont(buf)
    sub = subset.Subsetter(options())
    sub.populate(unicodes=UNICODES + extra)
    sub.subset(font)
    font.flavor = 'woff2'
    font.save(os.path.join(OUT, out))
    print(out, os.path.getsize(os.path.join(OUT, out)) // 1024, 'KB')
