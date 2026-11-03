"""Page shell and the shared components of the الحِرْز world.

Imported by build.py (run from the project root: python tools/build.py). Bump V on any CSS/JS change.
"""
from arabize import arabize, words
import html
import json
import os
import re

import brand

V = 70
BASE_URL = 'https://taktek-dev.github.io/muwathaq-prototype/'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

esc = lambda s: html.escape(str(s or ''), quote=True)

STATUS = {
    'convicted': ('مدان بحكم قضائي', 5, 'صدر حكم نهائي بالإدانة من محكمة مختصة.'),
    'warrant': ('مطلوب بموجب مذكرة توقيف', 4, 'المذكرة ليست حكمًا بالإدانة.'),
    'charged': ('متهم رسميًا', 3, 'الاتهام ليس إدانة، ولم يُفصل فيه قضائيًا.'),
    'named': ('ورد اسمه في تحقيق أو تقرير موثق', 2, 'ورود الاسم في تقرير أو تحقيق ليس اتهامًا قضائيًا.'),
    'sanctioned': ('خاضع لعقوبات حكومية', 2, 'قرار حكومي إداري — ليس اتهامًا قضائيًا ولا حكمًا.'),
    'alleged': ('محل ادعاءات قيد التحقق', 1, 'ادعاءات لم تُستكمل مراجعتها.'),
}
KNOTS = ['ادعاءات', 'تقرير أو إجراء', 'اتهام رسمي', 'مذكرة توقيف', 'حكم إدانة']

VERIF = {
    'not_started': ('لم تبدأ المراجعة', 'none', 'سُجّلت المادة ولم تبدأ مراجعتها.'),
    'in_progress': ('قيد التحقق', 'tied', 'تجري مراجعة المصدر والأصالة والسياق.'),
    'partial': ('تحقق جزئي', 'half', 'تحقق من عناصر جوهرية، وتبقى عناصر غير محسومة.'),
    'specific': ('تحقق من عناصر محددة', 'notch', 'تحقق من عناصر بعينها، مثل الموقع أو التاريخ.'),
    'complete': ('مكتمل وفق المنهجية', 'whole', 'استُكملت خطوات المنهجية؛ لا يعني ذلك ثبوت المسؤولية الجنائية.'),
    'rereview': ('يحتاج إلى إعادة مراجعة', 'crack', 'ظهرت معلومات أو روايات تستدعي إعادة الفحص.'),
}

REGIONS = {'gaza': 'غزة', 'westbank': 'الضفة الغربية', 'jerusalem': 'القدس الشرقية', 'lebanon': 'جنوب لبنان',
           'detention': 'مرافق الاحتجاز', 'opt': 'الأرض الفلسطينية المحتلة', 'general': 'عام'}

MONTHS = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']


def date_ar(iso, short=False):
    if not iso:
        return '—'
    p = str(iso).split('-')
    if len(p) == 1:
        return p[0]
    m = MONTHS[int(p[1]) - 1]
    if len(p) == 2:
        return f'{m} {p[0]}'
    return f'{int(p[2])} {m} {p[0]}'


# ---------- icons: one stroke family, 24 px grid ----------
ICONS = {
    'search': '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'close': '<path d="M6 6l12 12M18 6L6 18"/>',
    'next': '<path d="M14 6l-6 6 6 6"/>',
    'prev': '<path d="M10 6l6 6-6 6"/>',
    'arrow': '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    'down': '<path d="M6 9l6 6 6-6"/>',
    'info': '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.8v.2"/>',
    'alert': '<path d="M12 4l9 16H3z"/><path d="M12 10v4.5M12 17.3v.2"/>',
    'pin': '<path d="M12 21s-6.5-5.9-6.5-11a6.5 6.5 0 0 1 13 0c0 5.1-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    'cal': '<rect x="4" y="5.5" width="16" height="14.5" rx="3"/><path d="M4 10h16M9 3.5v4M15 3.5v4"/>',
    'doc': '<path d="M14 3.5H7.5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V8z"/><path d="M14 3.5V8h4.5M9 13h6M9 16.5h4"/>',
    'scale': '<path d="M12 4v16M7 20h10M5 8h14M5 8l-2.5 6a3 3 0 0 0 5 0zM19 8l-2.5 6a3 3 0 0 0 5 0z"/>',
    'user': '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20c.8-3.7 3.8-5.6 7.5-5.6s6.7 1.9 7.5 5.6"/>',
    'image': '<rect x="3.5" y="5" width="17" height="14" rx="3"/><circle cx="9" cy="10" r="1.8"/><path d="M20.5 16l-5-5-8.5 8"/>',
    'video': '<rect x="3.5" y="6" width="12" height="12" rx="3"/><path d="M15.5 10.5l5-3v9l-5-3"/>',
    'sat': '<path d="M4 20l4-4M10.5 6.5l7 7M8 9l4-4 7 7-4 4z"/><path d="M5 14a5 5 0 0 0 5 5"/>',
    'quote': '<path d="M10 7H6a2 2 0 0 0-2 2v3h5v5H4M20 7h-4a2 2 0 0 0-2 2v3h5v5h-5"/>',
    'official': '<path d="M4 9.5L12 5l8 4.5M5.5 10v7.5M9.5 10v7.5M14.5 10v7.5M18.5 10v7.5M4 20h16"/>',
    'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    'lock': '<rect x="5" y="10.5" width="14" height="10" rx="3"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
    'upload': '<path d="M12 15.5V4.5M7.5 9L12 4.5 16.5 9M4.5 15v2.5a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V15"/>',
    'download': '<path d="M12 4.5v11M7.5 11L12 15.5 16.5 11M4.5 15v2.5a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V15"/>',
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'layers': '<path d="M12 4l8.5 4.5L12 13 3.5 8.5z"/><path d="M3.5 12.5L12 17l8.5-4.5M3.5 16.5L12 21l8.5-4.5"/>',
    'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    'shield': '<path d="M12 3.5l7 2.6v5.6c0 4.4-3 7.7-7 8.8-4-1.1-7-4.4-7-8.8V6.1z"/>',
    'pen': '<path d="M4.5 19.5l1.1-4.3L15.9 4.9a2.1 2.1 0 0 1 3 3L8.6 18.2z"/><path d="M13.9 6.9l3 3M12 19.5h7.5"/>',
    'inbox': '<path d="M4 13.5l2.1-6.6A2.2 2.2 0 0 1 8.2 5.4h7.6a2.2 2.2 0 0 1 2.1 1.5l2.1 6.6V18a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><path d="M4 13.5h4.6l1.3 2.4h4.2l1.3-2.4H20"/>',
    'refresh': '<path d="M19.5 12a7.5 7.5 0 1 1-2.4-5.5"/><path d="M19.5 4.5v4.2h-4.2"/>',
    'hand': '<path d="M8 12.5V6.8a1.5 1.5 0 0 1 3 0V11M11 10V5.5a1.5 1.5 0 0 1 3 0V10M14 10V6.5a1.5 1.5 0 0 1 3 0v6.8c0 4-2.6 6.7-6.2 6.7-2.2 0-3.6-.9-4.9-2.7L3.8 13a1.5 1.5 0 0 1 2.4-1.8L8 13.5"/>',
}


def icon(name, cls='icon'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-{name}"/></svg>'


# ---------- seals: the sprite ----------
def seal_sprite():
    edge = brand.wax_edge(20, 20, 16.5, lobes=12, amp=0.045, steps=120)
    mark_dots = brand.dots(20, 20, 16.5, style='fill:var(--seal-on,#fff)')
    rim = f'<circle cx="20" cy="20" r="{brand.RING * 16.5:.2f}" fill="none" style="stroke:var(--seal-on,#fff)" stroke-opacity=".38" stroke-width=".9"/>'
    syms = {
        'none': '<circle cx="20" cy="20" r="15.2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="3.1 3.3" stroke-linecap="round"/>',
        'tied': (f'<path d="{edge}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-opacity=".55"/>'
                 '<path d="M1.5 24.2C7.5 21.2 12.5 20.6 16.4 20.6M23.6 20.6C27.5 20.6 32.5 21.2 38.5 24.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
                 '<path d="M16.4 20.6C16.4 16.6 23.6 16.6 23.6 20.6C23.6 24.4 16.4 24.4 16.4 20.6Z" fill="none" stroke="currentColor" stroke-width="1.8"/>'),
        'half': (f'<clipPath id="sc-half"><rect x="20" y="0" width="20" height="40"/></clipPath>'
                 f'<path d="{edge}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
                 f'<path d="{edge}" fill="currentColor" clip-path="url(#sc-half)"/>'),
        'notch': (f'<path d="{edge}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
                  f'{brand.dots(20, 20, 14.5, "currentColor")}'),   # the mark's dots on an open seal: some elements, not the whole
        'whole': f'<path d="{edge}" fill="currentColor"/>{rim}{mark_dots}',
        'crack': (f'<clipPath id="sc-a"><path d="M0 0H21L17.5 12L23 19.5L16.5 27L20.5 40H0Z"/></clipPath>'
                  f'<clipPath id="sc-b"><path d="M21 0H40V40H20.5L16.5 27L23 19.5L17.5 12Z"/></clipPath>'
                  f'<g clip-path="url(#sc-a)"><path d="{edge}" fill="currentColor" transform="translate(-1.4 .6) rotate(-4 20 20)"/></g>'
                  f'<g clip-path="url(#sc-b)"><path d="{edge}" fill="currentColor" transform="translate(1.4 -.4) rotate(3 20 20)"/></g>'
                  '<path d="M20.6 3.5L17.4 12.2L22.6 19.6L16.6 26.9L19.8 36.5" fill="none" style="stroke:var(--seal-on,#fff)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'),
    }
    out = ''.join(f'<symbol id="s-{k}" viewBox="0 0 40 40">{v}</symbol>' for k, v in syms.items())
    out += ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>{out}</defs></svg>'


_WAX_N = [0]


def wax(state='complete', cls='wax', label=''):
    """The lead seal as material: a domed wax disc lit from the top start corner, the mark's three dots pressed into it
    (shadow on the lit edge, highlight on the far edge), a pressed rim. Half, cracked and whole states
    keep the seal grammar; the other states fall back to the drawn symbol."""
    shape = VERIF[state][1]
    if shape not in ('whole', 'half', 'crack'):
        return seal(state, wax=True, cls='seal ' + cls)
    _WAX_N[0] += 1
    n = _WAX_N[0]
    edge = brand.wax_edge(60, 60, 54, lobes=12, amp=0.035, seed=1.3, steps=160)
    def pressed(fill, dx=0, dy=0, op=1):
        return f'<g opacity="{op}">{brand.dots(60, 60, 52, fill, dx=dx, dy=dy)}</g>'
    relief = pressed('#5E0F0B', -1.1, -1.1, .7) + pressed('#E7705F', 1.0, 1.0, .55) + pressed('#9C1F18')
    ring = brand.RING * 52
    rim = (f'<circle cx="60" cy="60" r="{ring:.1f}" fill="none" stroke="#6A110D" stroke-opacity=".55" stroke-width="2.2"/>'
           f'<circle cx="60.8" cy="60.8" r="{ring:.1f}" fill="none" stroke="#E7705F" stroke-opacity=".35" stroke-width="1.2"/>')
    body = (f'<path d="{edge}" fill="url(#wx-d{n})"/>'
            f'<path d="{edge}" fill="none" stroke="#5E0F0B" stroke-opacity=".35" stroke-width="1.4"/>'
            f'{rim}{relief}'
            f'<ellipse cx="42" cy="34" rx="15" ry="7" fill="#fff" opacity=".18" transform="rotate(-32 42 34)" filter="url(#wx-g{n})"/>')
    clip = ''
    if shape == 'half':
        clip = f'<clipPath id="wx-c{n}"><rect x="60" y="0" width="60" height="120"/></clipPath>'
        body = (f'<path d="{edge}" fill="none" stroke="currentColor" stroke-width="2" stroke-opacity=".6"/>'
                f'<g clip-path="url(#wx-c{n})">{body}</g>')
    elif shape == 'crack':
        clip = (f'<clipPath id="wx-a{n}"><path d="M0 0H63L53 36L69 58L50 82L61 120H0Z"/></clipPath>'
                f'<clipPath id="wx-b{n}"><path d="M63 0H120V120H61L50 82L69 58L53 36Z"/></clipPath>')
        body = (f'<g clip-path="url(#wx-a{n})"><g transform="translate(-3 1.5) rotate(-4 60 60)">{body}</g></g>'
                f'<g clip-path="url(#wx-b{n})"><g transform="translate(3 -1) rotate(3 60 60)">{body}</g></g>')
    defs = (f'<defs><radialGradient id="wx-d{n}" cx="36%" cy="30%" r="78%">'
            '<stop offset="0" stop-color="#E25546"/><stop offset=".38" stop-color="#B8271E"/>'
            '<stop offset=".78" stop-color="#8F1A14"/><stop offset="1" stop-color="#6A110D"/></radialGradient>'
            f'<filter id="wx-g{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>{clip}</defs>')
    aria = f' role="img" aria-label="{esc(label or VERIF[state][0])}"'
    return f'<svg class="{cls}" viewBox="0 0 120 120"{aria}>{defs}{body}</svg>'


def seal(state, wax=False, cls='seal', label=True):
    name, shape, _ = VERIF[state]
    aria = f' role="img" aria-label="{esc(name)}"' if label else ' aria-hidden="true"'
    return f'<svg class="{cls}{" is-wax" if wax else ""}" viewBox="0 0 40 40"{aria}><use href="#s-{shape}"/></svg>'


def seal_row(state, wax=False, illus=True):
    name = VERIF[state][0]
    note = ' <span class="illus">· توضيحي</span>' if illus else ''
    return f'<span class="seal-row">{seal(state, wax, label=False)}<span>{esc(name)}{note}</span></span>'


def knots(status, mini=False):
    label, level, desc = STATUS[status]
    items = []
    for i, k in enumerate(KNOTS, 1):
        cls = 'is-now' if i == level else ('is-tied' if i < level else '')
        items.append(f'<li class="{cls}"><i></i><span>{k}</span></li>')
    sr = f'<span class="sr">المرحلة الحالية في المسار القضائي: {esc(label)}، {level} من 5.</span>'
    return f'<div class="knots-wrap">{sr}<ol class="knots" aria-hidden="true">{"".join(items)}</ol></div>'


def ext(url, text, cls=''):
    return f'<a class="ext {cls}" href="{esc(url)}" rel="noopener" target="_blank">{text}</a>'


def ltr(s):
    return f'<bdi class="ltr">{esc(s)}</bdi>'


def mono(s):
    return f'<span class="mono">{esc(s)}</span>'


# ---------- shell ----------
NAV = [('people', 'الأشخاص', 'people/index.html'), ('reports', 'التقارير', 'reports/index.html'),
       ('law', 'القانون', 'law/index.html'), ('articles', 'المقالات', 'articles/index.html'),
       ('database', 'قاعدة البيانات', 'database.html'), ('incidents', 'الوقائع', 'incidents/index.html'),
       ('evidence', 'الأدلة', 'evidence/index.html'), ('method', 'المنهجية', 'method.html')]


def head(title, desc, rel, path, extra=''):
    # link previews read these attributes; the text layer does not reach them. A description cut inside
    # a parenthesis loses the cut fragment.
    title, desc = words(title), re.sub(r'\s*\([^)]*$', '', words(desc))
    full = f'{title} | موثّق' if title != 'موثّق' else 'موثّق | منصة التوثيق الرقمي والتحليل القانوني'
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ar_AR">
<link rel="canonical" href="{BASE_URL}{path}">
<link rel="icon" href="{rel}favicon.svg?v={V}" type="image/svg+xml">
<link rel="preload" href="{rel}assets/fonts/vazirmatn.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{rel}assets/css/site.css?v={V}">
<script>document.documentElement.classList.add('js')</script>
<script type="speculationrules">{{"prefetch":[{{"where":{{"href_matches":"*.html"}},"eagerness":"moderate"}}]}}</script>
{extra}</head>'''


def masthead(rel, active):
    nav = ''.join(f'<li><a href="{rel}{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
                  for key, label, href in NAV)
    return f'''<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<div class="proto" id="proto" role="note"><div class="wrap">{icon('info')}<span><b>نموذج تصميم.</b> الوثائق والوقائع حقيقية، وحالات التحقق والعهدة توضيحية. <a href="{rel}method.html#illustrative">التفاصيل</a></span><button type="button" data-dismiss="proto" aria-label="إخفاء التنبيه">{icon('close')}</button></div></div>
<header class="mast" id="mast">
 <div class="wrap">
  <a class="brand" href="{rel}index.html" aria-label="موثّق — الرئيسية"><img class="mark" src="{rel}assets/brand/mark.svg?v={V}" alt="" width="40" height="40"><img class="word" src="{rel}assets/brand/wordmark.svg" alt="موثّق" width="55" height="36"></a>
  <nav aria-label="الأقسام"><ul class="nav" id="nav"><li class="mob-only">{find(rel, 'menu')}</li>{nav}<li class="mob-only"><a href="{rel}submit.html">أرسل مادة للمراجعة</a></li><li class="mob-only"><a href="{rel}donate.html">ادعم التوثيق</a></li><li class="mob-only"><a href="{rel}about.html">عن موثّق</a></li><li class="mob-only"><a href="{rel}standards.html">المعايير والسياسات</a></li></ul></nav>
  <div class="mast-end">
   {find(rel, 'mast')}
   <a class="btn btn-wax btn-sm desk-only" href="{rel}submit.html">أرسل مادة</a>
   <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="القائمة">{icon('menu')}</button>
  </div>
 </div>
</header>'''


def find(rel, where):
    return f'''<form class="find" role="search" action="{rel}search.html" data-find="{where}">
    <label class="sr" for="q-{where}">ابحث في المنصة</label>
    <input id="q-{where}" name="q" type="search" placeholder="ابحث باسم، رقم ملف، أو مادة" autocomplete="off" role="combobox" aria-expanded="false" aria-controls="ql-{where}" aria-autocomplete="list">
    {icon('search')}<kbd>/</kbd>
    <div class="find-list" id="ql-{where}" role="listbox" hidden></div>
   </form>'''


def footer(rel):
    return f'''<footer class="foot">
 <div class="wrap">
  <div class="foot-seal">
   <img class="foot-wax" src="{rel}assets/brand/mark.svg?v={V}" alt="" width="72" height="72">
   <div class="foot-say"><p class="foot-motto">التوثيق الدقيق أساس المساءلة.</p><p>لا ينشر ملف قبل أن يمر بعشر خطوات تحقق. <a href="{rel}method.html">كيف نتحقق</a></p></div>
   <div class="foot-cta"><a class="btn btn-wax" href="{rel}submit.html">{icon("upload")} أرسل مادة</a><a class="btn btn-ghost" href="{rel}donate.html">ادعم التوثيق</a></div>
  </div>
  <div class="foot-grid">
   <div class="foot-brand">
    <a class="brand" href="{rel}index.html" aria-label="موثّق — الرئيسية"><img class="mark" src="{rel}assets/brand/mark.svg?v={V}" alt="" width="40" height="40"><img class="word" src="{rel}assets/brand/wordmark-reversed.svg" alt="موثّق" width="55" height="36"></a>
    <p>منصة مستقلة لتوثيق جرائم الاحتلال الإسرائيلي وربطها بالقانون الدولي.</p>
    <p class="foot-ind">{icon("shield")}<span>لا تتبع أي محكمة أو منظمة دولية أو جهة حكومية.</span></p>
   </div>
   <div><h2>{icon("layers")}قاعدة البيانات</h2><ul><li><a href="{rel}people/index.html">ملفات الأشخاص</a></li><li><a href="{rel}incidents/index.html">أرشيف الوقائع</a></li><li><a href="{rel}evidence/index.html">سجل الأدلة</a></li><li><a href="{rel}reports/index.html">التقارير والوثائق</a></li><li><a href="{rel}law/index.html">مكتبة القواعد القانونية</a></li></ul></div>
   <div><h2>{icon("scale")}المنهجية والسياسات</h2><ul><li><a href="{rel}method.html">كيف نتحقق</a></li><li><a href="{rel}standards.html">المعايير القانونية والأخلاقية</a></li><li><a href="{rel}standards.html#correction">طلب تصحيح أو رد</a></li><li><a href="{rel}identity.html">الهوية البصرية</a></li><li><a href="{rel}sources.html">المصادر وحقوق الصور</a></li></ul></div>
   <div><h2>{icon("hand")}شارك وادعم</h2><ul><li><a href="{rel}submit.html">أرسل مادة للمراجعة</a></li><li><a href="{rel}donate.html">ادعم التوثيق المستقل</a></li><li><a href="{rel}articles/write.html">اكتب مقالا</a></li><li><a href="{rel}about.html">عن موثّق</a></li><li><a href="{rel}search.html">البحث في المنصة</a></li></ul></div>
  </div>
  <div class="foot-cord" aria-hidden="true"><i></i><img src="{rel}assets/brand/mark.svg?v={V}" alt="" width="26" height="26"><i></i></div>
  <div class="foot-bottom"><span>© 2026 موثّق — نموذج تصميم لا يرسل بيانات إلى أي خادم.</span><a class="foot-top" href="#main">العودة إلى الأعلى <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" style="transform:rotate(180deg)"><use href="#i-down"/></svg></a></div>
 </div>
</footer>
<div class="toasts" id="toasts" aria-live="polite"></div>'''


HARAKAT = re.compile('[ً-ْ]')
KEEP = re.compile(r'(<blockquote class="official">.*?</blockquote>|موثّق)', re.S)


def plain(html_):
    """No diacritics in headlines or copy (house rule); the brand name and quoted official texts keep theirs."""
    parts = KEEP.split(html_)
    return arabize(''.join(p if i % 2 else HARAKAT.sub('', p) for i, p in enumerate(parts)))


def eager_top(main, n=6):
    """The first images in the body are on or near the first screen; they are not left to lazy loading."""
    for _ in range(n):
        main = main.replace('loading="lazy"', 'loading="eager"', 1)
    return main


def page(title, desc, rel, path, active, main, extra_head='', body_cls='', scripts=''):
    main = eager_top(main)
    return plain(head(title, desc, rel, path, extra_head) +
            f'\n<body class="{body_cls}">\n{seal_sprite()}\n{masthead(rel, active)}\n<main id="main">\n{main}\n</main>\n{footer(rel)}\n'
            f'<script src="{rel}assets/js/index.js?v={V}"></script>\n{scripts}<script src="{rel}assets/js/site.js?v={V}" defer></script>\n<script src="{rel}assets/js/world.js?v={V}" defer></script>\n</body>\n</html>\n')


def crumbs(rel, items):
    li = [f'<li><a href="{rel}index.html">الرئيسية</a></li>']
    for label, href in items:
        li.append(f'<li><a href="{rel}{href}">{esc(label)}</a></li>' if href else f'<li aria-current="page">{esc(label)}</li>')
    return f'<nav aria-label="مسار الصفحة"><ol class="crumbs">{"".join(li)}</ol></nav>'


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8', newline='\n').write(text)


def json_js(name, obj):
    return f'window.{name}=' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + ';\n'
