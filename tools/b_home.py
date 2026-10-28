"""Direction B, «المتن والحاشية»: the home page and the identity page, on the same real records as direction A.

python tools/b_home.py   (from the project root, after tools/b_brand.py and tools/b_fonts.py)

Every page is a text and its margin. The text (المتن) says what the record says; the margin (الحاشية)
carries, for each numbered sentence, the source it rests on, what kind of source it is, and its date.
A لحق, the copyist's hooked line, runs from the sentence being read to its source. Verification states
are the copyists' collation signs; a person's legal standing is a ruled scale of five, read before the name.
The inner pages are still direction A's; links into them say so in the prototype bar.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402
import shell as S  # noqa: E402
from shell import esc, date_ar, STATUS, KNOTS, REGIONS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'b')
V = 1
A = '../'   # direction A's pages and shared photographs

MARK_SVG = json.load(open(os.path.join(OUT, 'assets', 'brand', 'marks.json'), encoding='utf-8'))
# state -> (sign, name, what it means)
SIGNS = {
    'complete': ('صح', 'مكتمل وفق المنهجية', 'قوبلت المادة بمصادرها وصحت: علامة الناسخ على قراءة متحقق منها.'),
    'specific': ('معا', 'تحقق من عناصر محددة', 'وردت العناصر المحددة في مصدرين مستقلين معا.'),
    'partial': ('كذا', 'تحقق جزئي', 'نقلت كما وردت في مصدرها، ولم تكتمل مقابلتها بغيره.'),
    'in_progress': ('بلغ', 'التحقق جار', 'بلغت المقابلة هذا الموضع، وما بعده قيد المراجعة.'),
    'rereview': ('خ', 'رواية مغايرة', 'في رواية أو نسخة أخرى ما يخالفها، فتعاد مراجعتها.'),
    'not_started': ('', 'لم تقابل بعد', 'سجلت المادة ولم تبدأ مقابلتها.'),
}
ORDER = ['complete', 'specific', 'partial', 'in_progress', 'rereview', 'not_started']


def mark(state, cls='mark', label=False):
    aria = f' role="img" aria-label="{esc(SIGNS[state][1])}"' if label else ' aria-hidden="true"'
    return f'<svg class="{cls} is-{state}" viewBox="0 0 40 40"{aria}><use href="#m-{state}"/></svg>'


def icon(name, cls='icon'):
    return S.icon(name, cls)


def sprite():
    marks = ''.join(f'<symbol id="m-{k}" viewBox="0 0 40 40">{v}</symbol>' for k, v in MARK_SVG.items())
    icons = ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
                    for k, v in S.ICONS.items())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{marks}{icons}</svg>'


def scale(status, compact=False):
    """A person's legal standing: five ruled cells, the current one inked in lapis, the ones after it left open."""
    label, level, _ = STATUS[status]
    cells = ''.join(f'<li class="{"is-now" if i == level else ("is-past" if i < level else "")}"><span>{k}</span></li>'
                    for i, k in enumerate(KNOTS, 1))
    return (f'<div class="scale{" is-compact" if compact else ""}"><ol aria-hidden="true">{cells}</ol>'
            f'<p class="scale-now"><b>{level}</b> من 5 · {esc(KNOTS[level - 1])}</p>'
            f'<span class="sr">المرحلة في المسار القضائي: {esc(label)}، {level} من 5.</span></div>')


def head(title, desc, path, extra=''):
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/naskh.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/kufi.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/b.css?v={V}">
<script>document.documentElement.classList.add('js')</script>
{extra}</head>'''


NAV = [('الأشخاص', 'people/index.html'), ('الوقائع', 'incidents/index.html'), ('الأدلة', 'evidence/index.html'),
       ('التقارير', 'reports/index.html'), ('القانون', 'law/index.html'), ('المنهجية', 'method.html')]


def masthead(active=''):
    nav = ''.join(f'<li><a href="{A}{u}">{t}</a></li>' for t, u in NAV)
    return f'''<div class="proto" id="proto" role="note"><div class="wrap"><p><b>الاتجاه ب: المتن والحاشية.</b> نموذج للمقارنة: الصفحة الرئيسية والهوية فقط، والصفحات الداخلية ما زالت بالاتجاه أ. الوثائق والوقائع حقيقية؛ علامات التحقق توضيحية.</p><a href="../directions.html">قارن الاتجاهين</a></div></div>
<a class="skip" href="#main">تخط إلى المحتوى</a>
<header class="mast">
 <div class="wrap mast-in">
  <a class="brand" href="index.html" aria-label="موثّق، الصفحة الرئيسية"><img src="assets/brand/wordmark.svg" alt="موثّق" width="176" height="79"><span class="brand-en">MUWATHAQ</span></a>
  <nav class="nav" aria-label="الأقسام"><ul>{nav}</ul></nav>
  <form class="find" action="{A}search.html" role="search"><label class="sr" for="mq">ابحث في موثّق</label>{icon("search")}<input id="mq" name="q" type="search" placeholder="اسم، رقم ملف، أو مادة"></form>
  <a class="btn btn-line" href="{A}submit.html">أرسل مادة</a>
  <details class="menu"><summary aria-label="القائمة">{icon("menu")}</summary><div class="menu-in"><form action="{A}search.html" role="search"><label class="sr" for="mq2">ابحث</label><input id="mq2" name="q" type="search" placeholder="ابحث في موثّق"></form><ul>{nav}<li><a href="{A}submit.html">أرسل مادة</a></li><li><a href="identity.html">الهوية البصرية</a></li></ul></div></details>
 </div>
 <div class="rule" aria-hidden="true"></div>
</header>'''


def footer():
    cols = [('قاعدة البيانات', NAV[:5]), ('المنهجية والسياسات', [('كيف نتحقق', 'method.html'), ('المعايير القانونية والأخلاقية', 'standards.html'), ('طلب تصحيح أو رد', 'standards.html#correction')]),
            ('شارك وادعم', [('أرسل مادة للمراجعة', 'submit.html'), ('ادعم التوثيق المستقل', 'donate.html'), ('عن موثّق', 'about.html')])]
    html = ''.join(f'<div><h2>{h}</h2><ul>{"".join(f"<li><a href=\"{A}{u}\">{t}</a></li>" for t, u in items)}</ul></div>' for h, items in cols)
    return f'''<footer class="foot">
 <div class="rule rule-on-ink" aria-hidden="true"></div>
 <div class="wrap foot-grid">
  <div class="foot-brand"><img src="assets/brand/wordmark-reversed.svg" alt="موثّق" width="160" height="72"><p>منصة رقمية مستقلة لتوثيق الوقائع والأدلة المتعلقة بجرائم الاحتلال الإسرائيلي، والتحقق منها، وحفظها، وربطها بالقانون الدولي.</p><p class="foot-motto">كل جملة ومعها سندها.</p></div>
  {html}
  <div><h2>الهوية</h2><ul><li><a href="identity.html">الهوية البصرية للاتجاه ب</a></li><li><a href="../directions.html">قارن الاتجاهين</a></li></ul></div>
 </div>
 <div class="wrap foot-end"><p>© 2026 موثّق MUWATHAQ — نموذج تصميم لا يرسل بيانات إلى أي خادم.</p><p>منصة مستقلة لا تتبع أي محكمة أو منظمة دولية أو جهة حكومية.</p></div>
</footer>'''


def page(path, title, desc, main, scripts='', extra_head=''):
    html = (head(title, desc, path, extra_head) + f'\n<body>\n{sprite()}\n{masthead()}\n<main id="main">\n{main}\n</main>\n{footer()}\n'
            f'<script src="{A}assets/js/vendor/lenis.min.js" defer></script>\n{scripts}<script src="assets/js/b.js?v={V}" defer></script>\n</body>\n</html>\n')
    html = S.plain(html)
    with open(os.path.join(OUT, path), 'w', encoding='utf-8') as f:
        f.write(html)


# ---------- the home page ----------
def folio():
    """The first viewport: a real file as a text whose every sentence is numbered to its source in the margin."""
    p = B.P_BY_ID['P-0001']
    w = next(s for s in p['statuses'] if s.get('type') == 'warrant')
    coi = next((s for s in p['statuses'] if s.get('type') == 'named'), None)
    per = p.get('period') or []
    crimes = [c.partition(' — ')[0] for c in p.get('crimes_ar', [])]
    glosses = [
        ('complete', 'بيان المحكمة الجنائية الدولية بإصدار أمري القبض', f'{w.get("body_ar", "")} · {date_ar(w.get("date"))} · وثيقة قضائية', w.get('url')),
        ('complete', 'الحالة في دولة فلسطين', f'{w.get("doc_symbol") or "ICC-01/18"} · صفحة الحالة الرسمية لدى المحكمة', 'https://www.icc-cpi.int/palestine'),
        ('specific', 'توصيف الأفعال في قرار الدائرة', 'تطابق في البيان الرسمي وملخص القرار: مصدران مستقلان', w.get('url')),
        ('in_progress', 'الفترة الزمنية المشمولة', 'مقابلة التواريخ بالقرار: بلغت 4 من 5 خطوات', w.get('url')),
    ]
    if coi:
        glosses.append(('complete', 'لجنة التحقيق الدولية المستقلة', f'{coi.get("doc_symbol", "")} · {date_ar(coi.get("date"))} · استنتاج لجنة، وليس اتهاما قضائيا', coi.get('url')))
    claims = [
        f'أصدرت الدائرة التمهيدية الأولى في المحكمة الجنائية الدولية أمر قبض بحقه في {date_ar(w.get("date"))}',
        'ضمن الحالة في دولة فلسطين',
        f'ووجدت أسبابا معقولة للاعتقاد بمسؤوليته عن {crimes[0] if crimes else "جرائم حرب"}، و{crimes[1] if len(crimes) > 1 else ""}',
        f'عن الفترة الممتدة من {date_ar(per[0])} على الأقل حتى {date_ar(per[1])} على الأقل' if len(per) == 2 else 'عن الفترة التي يحددها القرار',
    ]
    if coi:
        claims.append(f'وخلصت لجنة التحقيق الأممية في {date_ar(coi.get("date"))} إلى أن تصريحاته ترقى إلى تحريض مباشر وعلني على الإبادة الجماعية')

    def ref(n):
        return f'<a class="ref" href="#g{n}" data-ref="{n}" aria-describedby="g{n}"><span class="sr">السند </span>{n}</a>'

    text = (f'<p><span class="claim" data-claim="1">{esc(claims[0])}</span> <span class="nw">{ref(1)}،</span> <span class="claim" data-claim="2">{esc(claims[1])}</span> <span class="nw">{ref(2)}.</span></p>'
            f'<p><span class="claim" data-claim="3">{esc(claims[2])}</span> <span class="nw">{ref(3)}،</span> <span class="claim" data-claim="4">{esc(claims[3])}</span> <span class="nw">{ref(4)}.</span></p>')
    if coi:
        text += f'<p><span class="claim" data-claim="5">{esc(claims[4])}</span> <span class="nw">{ref(5)}.</span></p>'
    gl = ''.join(f'''<li class="gloss" id="g{n}" data-gloss="{n}">
      <span class="gloss-n">{n}</span>{mark(st, "mark gloss-mark")}
      <div class="gloss-body"><h3>{f'<a href="{esc(u)}" rel="noopener" target="_blank">{esc(t)}{icon("link")}<span class="sr"> (المصدر، يفتح في نافذة جديدة)</span></a>' if u else esc(t)}</h3><p class="gloss-meta">{esc(m)}</p><p class="gloss-sign"><b>{SIGNS[st][0] or "—"}</b> {esc(SIGNS[st][1])} · توضيحي</p></div>
     </li>''' for n, (st, t, m, u) in enumerate(glosses, 1))
    face = B.face(B.photo_of(p['id']), A, 'file-face', 112)
    total = len(B.PERSONS) + len(B.INCIDENTS) + len(B.EVIDENCE) + len(B.DOCS) + len(B.RULES)
    tries = [('P-0001', f'{A}people/p-0001.html'), ('المادة 8(2)(ب)(25)', f'{A}law/rs-8-2-b-xxv.html'), ('رفح', f'{A}search.html?q=رفح'), ('محكمة العدل الدولية', f'{A}search.html?q=محكمة العدل الدولية')]
    return f'''<section class="folio" data-folio aria-labelledby="hero-h">
 <div class="wrap folio-grid">
  <div class="matn">
   <p class="kicker"><span class="mono">{total}</span> سجلا مسندا · ملفات ووقائع وأدلة ووثائق وقواعد</p>
   <h1 class="display" id="hero-h"><span class="ln"><span>كل جملة هنا</span></span><span class="ln"><span>ومعها سندها.</span></span></h1>
   <p class="lead">منصة مستقلة لتوثيق جرائم الاحتلال الإسرائيلي وتحليلها قانونيا: المتن في الصفحة، ومصدر كل جملة في الحاشية، ودرجة التحقق منه بعلامة.</p>
   <form class="search" action="{A}search.html" role="search"><label class="sr" for="hq">ابحث في الأرشيف</label>{icon("search")}<input id="hq" name="q" type="search" placeholder="ابحث باسم، رقم ملف، أو مادة قانونية"><button class="btn btn-ink" type="submit">بحث</button></form>
   <p class="tries">جرب: {" · ".join(f'<a href="{u}">{esc(t)}</a>' for t, u in tries)}</p>
   <article class="file" aria-label="مثال حي: ملف {esc(p["name_ar"])}">
    <header class="file-head">
     <p class="file-kind"><span class="mono">{p["id"]}</span> · ملف شخص · الوضع القانوني</p>
     <p class="file-status">{esc(STATUS[p["status"]][0])}</p>
     <div class="file-who">{face}<p><b>{esc(p["name_ar"])}</b><span>{esc(p.get("role_ar", ""))}</span></p></div>
     <p class="file-not">{icon("info")}<span>الأمر ليس حكما بالإدانة، ويفترض براءة الشخص حتى تثبت إدانته بحكم قضائي.</span></p>
    </header>
    <div class="file-text">{text}</div>
    <footer class="file-foot"><a href="{A}people/p-0001.html">اقرأ الملف كاملا{icon("arrow")}</a><a href="{A}people/p-0001.html#incidents">الوقائع المرتبطة ({len(p["inc_ids"])})</a><a href="{A}people/p-0001.html#status">المسار القضائي</a></footer>
   </article>
  </div>
  <aside class="hashiya" aria-label="الحاشية: مصدر كل جملة">
   <div class="hashiya-in">
    <h2 class="hashiya-h">الحاشية</h2>
    <p class="hashiya-sub">مصدر كل جملة في المتن، ونوعه، وتاريخه، ودرجة مقابلته.</p>
    <ol class="glosses">{gl}</ol>
    <p class="hashiya-hint">{icon("info")}<span>قف على رقم في المتن أو على حاشية لترى السند الذي تقوم عليه الجملة.</span></p>
   </div>
  </aside>
 </div>
 <svg class="luhaq" aria-hidden="true"><path class="luhaq-line"/><circle class="luhaq-dot" r="3.4"/></svg>
</section>'''


def signs_section():
    demo_state = 'specific'
    rows = ''.join(f'''<li data-sign="{k}" tabindex="0"{" class=\"is-on\"" if k == demo_state else ""}>{mark(k, "mark")}<div><b>{SIGNS[k][0] or "—"}<span> · {esc(SIGNS[k][1])}</span></b><p>{esc(SIGNS[k][2])}</p></div></li>''' for k in ORDER)
    views = ''.join(f'<span class="demo-mark{" is-on" if k == demo_state else ""}" data-sign-view="{k}">{mark(k, "mark mark-xl")}</span>' for k in ORDER)
    return f'''<section class="sec signs" aria-labelledby="signs-h">
 <div class="wrap signs-grid">
  <div class="signs-matn">
   <p class="eyebrow">كيف تقرأ أي سجل هنا</p>
   <h2 class="h2" id="signs-h">علامات النساخ: إلى أي حد قابلنا المادة</h2>
   <p class="lead-sm">في المخطوطات العربية كان الناسخ يقابل نسخته بالأصل، ويكتب في الهامش علامة لكل موضع: صح إذا صح، وبلغ حيث بلغت المقابلة، وخ إذا خالفتها نسخة أخرى. نستعير العلامات نفسها لنقول بدقة إلى أي حد تحققنا من كل مادة، بعلامة مرسومة وكلمة واضحة، لا بلون.</p>
   <div class="signs-demo" aria-hidden="true">
    <p class="demo-line">قتل 15 من المسعفين وعناصر الدفاع المدني وموظف أممي قرب تل السلطان في رفح <span class="ref is-on">1</span></p>
    <div class="demo-gloss">{views}<p data-sign-label>{esc(SIGNS[demo_state][0])} · {esc(SIGNS[demo_state][1])}</p></div>
   </div>
   <p class="note">{icon("alert")}<span>التحقق من المادة شيء، والوضع القانوني للشخص شيء آخر: علامة صح على دليل لا تعني ثبوت مسؤولية أحد.</span></p>
  </div>
  <ol class="signs-list">{rows}</ol>
 </div>
</section>'''


def leaf(p):
    label, by, main = B.person_status_line(p)
    face = B.face(B.photo_of(p['id']), A, 'leaf-face', 72)
    return f'''<li><a class="leaf" href="{A}people/{B.slug(p["id"])}.html">
   <span class="leaf-top"><span class="mono">{p["id"]}</span>{mark(B.state_of(p["id"], "complete"), "mark mark-sm")}</span>
   <span class="leaf-status">{esc(label)}</span>
   <span class="leaf-who">{face}<span><b>{esc(p["name_ar"])}</b><small>{esc(p.get("role_ar", ""))}</small></span></span>
   {scale(p["status"], compact=True)}
   <span class="leaf-src">{esc(by)}</span>
  </a></li>'''


def people_section():
    leaves = ''.join(leaf(p) for p in B.PERSONS)
    leaves += (f'<li><a class="leaf leaf-note" href="{A}people/index.html"><span class="leaf-status">كيف يفتح ملف</span>'
               f'<span class="leaf-src">بوضع قانوني رسمي قابل للاستشهاد فقط: أمر قبض، أو اتهام، أو ورود في تحقيق أممي، أو قرار عقوبات حكومي.</span>'
               f'<span class="link-arrow">كل الملفات ({len(B.PERSONS)}){icon("arrow")}</span></a></li>')
    return f'''<section class="sec" aria-labelledby="people-h">
 <div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">الوضع القانوني قبل الاسم</p><h2 class="h2" id="people-h">ملفات الأشخاص</h2><p>لا يفتح ملف إلا بوضع قانوني رسمي، ويقرأ على سلم من خمس درجات: الدرجة الحالية بالأزرق، وما بعدها مفتوح لم يصدر.</p></div><a class="link-arrow" href="{A}people/index.html">كل الملفات ({len(B.PERSONS)}){icon("arrow")}</a></div>
  <ul class="leaves">{leaves}</ul>
 </div>
</section>'''


def line(inc):
    st = B.state_of(inc['id'])
    return f'''<li><a class="line" href="{A}incidents/{B.slug(inc["id"])}.html">
   <span class="line-matn"><span class="line-date mono">{esc(inc["date"])}</span><b>{esc(inc["title_ar"])}</b><small>{esc(inc.get("place_ar", ""))}</small></span>
   <span class="line-gloss">{mark(st, "mark mark-sm")}<span><b>{SIGNS[st][0] or "—"} · {esc(SIGNS[st][1])}</b><small>{len(inc["ev_ids"])} أدلة · {len(inc.get("sources", []))} مصادر · <span class="mono">{inc["id"]}</span></small></span></span>
  </a></li>'''


def incidents_section():
    incs = sorted(B.INCIDENTS, key=lambda i: i['date'], reverse=True)
    lead = B.INC_BY_ID.get(B.PICKS.get('home', {}).get('feature_incident')) or incs[0]
    ph = B.photo_of(lead['id'])
    rows = ''.join(line(i) for i in [i for i in incs if i is not lead][:6])
    st = B.state_of(lead['id'])
    return f'''<section class="sec" aria-labelledby="inc-h">
 <div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">المتن ما حدث بحسب المصادر، والحاشية ما يسنده</p><h2 class="h2" id="inc-h">وقائع موثقة</h2><p>لكل واقعة سجل مستقل: الروايات المتعارضة، والأدلة ودرجة مقابلة كل منها، والقواعد التي قد تنطبق وما يلزم إثباته.</p></div><a class="link-arrow" href="{A}incidents/index.html">أرشيف الوقائع ({len(B.INCIDENTS)}){icon("arrow")}</a></div>
  <div class="inc-grid">
   <article class="feature">
    {B.photo_fig(ph, A, "photo", "(min-width: 1024px) 44vw, 100vw") if ph else ""}
    <div class="feature-matn"><p class="line-date mono">{esc(lead["date"])} · {esc(REGIONS.get(lead.get("region"), ""))}</p>
     <h3><a href="{A}incidents/{B.slug(lead["id"])}.html">{esc(lead["title_ar"])}</a></h3>
     <p>{esc(lead.get("summary_ar", ""))}</p></div>
    <p class="feature-gloss">{mark(st, "mark mark-sm")}<span><b>{SIGNS[st][0]} · {esc(SIGNS[st][1])}</b> · توضيحي · {len(lead["ev_ids"])} أدلة · {len(lead.get("sources", []))} مصادر</span></p>
   </article>
   <ol class="lines">{rows}</ol>
  </div>
 </div>
</section>'''


def isnad_section():
    steps = [('جمع المادة', 'من مصدر يمكن تحديده، مع تسجيل كيفية الحصول عليها.'), ('تسجيل المصدر والعهدة', 'من حصل عليها، ومتى، وبصمتها الرقمية.'),
             ('الأصالة والسياق', 'هل هي ما تقول إنها هي، وأين نشرت أولا.'), ('المقارنة المستقلة', 'مقابلتها بمصدر آخر لا يعتمد عليها.'),
             ('الموقع والزمن', 'تحديد المكان والتاريخ بأدوات مفتوحة.'), ('توثيق القيود', 'ما لا تثبته المادة يكتب بجانبها.'),
             ('المراجعة القانونية', 'ربطها بقاعدة وما يلزم إثباته.'), ('حماية الأشخاص', 'لا ينشر ما يعرض شاهدا أو ضحية للخطر.'),
             ('قرار النشر', 'بتوقيع مراجعين، وبتاريخ.'), ('التصحيح المستمر', 'كل تصحيح يكتب في الحاشية ولا يمحى.')]
    items = ''.join(f'<li><span class="isnad-n">{n}</span><div><b>{esc(t)}</b><p>{esc(d)}</p></div></li>' for n, (t, d) in enumerate(steps, 1))
    return f'''<section class="sec sec-lapis" aria-labelledby="isnad-h">
 <div class="wrap isnad-grid">
  <div><p class="eyebrow">السند</p><h2 class="h2" id="isnad-h">لكل سجل سند من عشر حلقات</h2>
   <p>كما يروى الخبر عن فلان عن فلان حتى مصدره، يروى كل سجل في موثّق عن حلقاته: لا تنشر مادة قبل أن يكتمل سندها، وكل حلقة مكتوبة في سجل العهدة بتاريخها.</p>
   <a class="btn btn-light" href="{A}method.html">المنهجية كاملة{icon("arrow")}</a></div>
  <ol class="isnad">{items}</ol>
 </div>
</section>'''


def library_section():
    docs = sorted(B.DOCS, key=lambda d: d.get('date', ''), reverse=True)[:6]
    rules = sorted(B.RULES, key=lambda r: len(r['inc_ids']), reverse=True)[:7]   # a rule entry runs a little shorter than a document's
    d_items = ''.join(f'''<li><a href="{A}reports/{B.slug(d["id"])}.html"><span class="ref-n mono">{d["id"]}</span><span><b>{esc(d.get("title_ar", ""))}</b>
      <small>{esc(d.get("publisher_ar", ""))} · {esc(date_ar(d.get("date")))}{(" · <span class=mono>" + esc(B.doc_face(d)) + "</span>") if d.get("symbol") else ""}</small>
      <em>{esc(d.get("nature_ar", "").split("—")[0].strip())}</em></span></a></li>''' for d in docs)
    r_items = ''.join(f'''<li><a href="{A}law/{B.slug(r["id"])}.html"><span class="ref-n mono">{esc(r.get("article_en", ""))}</span><span><b>{esc(r.get("title_ar", ""))}</b>
      <small>{esc(r.get("instrument_ar", ""))} · {esc(r.get("article_ar", ""))}</small><em>{len(r["inc_ids"])} {"واقعة مرتبطة" if len(r["inc_ids"]) == 1 else "وقائع مرتبطة"}</em></span></a></li>''' for r in rules)
    return f'''<section class="sec" aria-labelledby="lib-h">
 <div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">المراجع</p><h2 class="h2" id="lib-h">الوثائق والقواعد التي يستند إليها المتن</h2><p>كل وثيقة بطبيعتها القانونية، وكل قاعدة بنصها الرسمي: الأمر القضائي ليس حكما، والتقرير الحقوقي ليس قرارا.</p></div></div>
  <div class="lib-grid">
   <div><h3 class="lib-h">أحدث الوثائق <a href="{A}reports/index.html">المكتبة ({len(B.DOCS)}){icon("arrow")}</a></h3><ol class="refs">{d_items}</ol></div>
   <div><h3 class="lib-h">القواعد الأكثر ارتباطا بالوقائع <a href="{A}law/index.html">مكتبة القواعد ({len(B.RULES)}){icon("arrow")}</a></h3><ol class="refs">{r_items}</ol></div>
  </div>
 </div>
</section>'''


def act_section():
    return f'''<section class="sec" aria-labelledby="act-h">
 <div class="wrap act-grid">
  <div class="act"><p class="eyebrow">شارك</p><h2 class="h3" id="act-h">أرسل مادة للمراجعة</h2><p>لا ننشر شيئا تلقائيا: تمر كل مساهمة بالحلقات العشر، وتخفى البيانات الحساسة قبل أي قرار بالنشر.</p>
   <p class="note">{icon("shield")}<span>لا ترسل ما قد يعرضك أو يعرض غيرك للخطر. هذا النموذج لا يرسل البيانات إلى أي خادم.</span></p><a class="btn btn-ink" href="{A}submit.html">ابدأ الإرسال</a></div>
  <div class="act"><p class="eyebrow">ادعم</p><h2 class="h3">ادعم التوثيق المستقل</h2><p>تمول المساهمات حفظ الأدلة، وأدوات التحقق الرقمي والجغرافي، والمراجعة القانونية، وحماية البيانات.</p>
   <p class="note">{icon("lock")}<span>بوابة الدفع غير مفعلة في هذا النموذج، ولا تعرض أرقام تمويل غير حقيقية.</span></p><a class="btn btn-line" href="{A}donate.html">طرق الدعم</a></div>
 </div>
</section>'''


def home():
    main = folio() + signs_section() + people_section() + incidents_section() + isnad_section() + library_section() + act_section()
    page('index.html', 'موثّق — كل جملة ومعها سندها (الاتجاه ب)',
         'موثّق منصة مستقلة لتوثيق الوقائع والأدلة المتعلقة بجرائم الاحتلال الإسرائيلي: المتن في الصفحة، ومصدره في الحاشية.', main)


def identity():
    inks = [('الحبر', '#111417', 'المتن وكل ما يقرأ؛ والقاعدة الثقيلة في التجديل.'), ('الحاشية', '#E9EDF0', 'أرضية الهامش وخانات السند، باردة لا دافئة.'),
            ('الورق', '#FFFFFF', 'الصفحة وعمود القراءة.'), ('اللازورد', '#2B44B8', 'حبر الناسخ: كل سند وعلامة ولحق، ولا شيء غيرها. الملف الرئيسي وحده يطبع أبيض عليه.')]
    sw = ''.join(f'<li><span class="sw" style="background:{h}"></span><b>{esc(n)}</b><span class="mono">{h}</span><small>{esc(d)}</small></li>' for n, h, d in inks)
    keys = ''.join(f'<li>{mark(k, "mark")}<div><b>{SIGNS[k][0] or "—"}<span> · {esc(SIGNS[k][1])}</span></b><p>{esc(SIGNS[k][2])}</p></div></li>' for k in ORDER)
    eg = B.P_BY_ID['P-0001']
    logo = (f'<div class="id-sheet"><h2 class="h2">الشعار</h2>'
            f'<div class="id-lock"><img src="assets/brand/wordmark.svg" alt="موثّق" width="352" height="157"></div>'
            f'<div class="id-lock is-ink"><img src="assets/brand/wordmark-reversed.svg" alt="موثّق" width="264" height="118"><img class="id-tile" src="assets/brand/mark.svg" alt="" width="72" height="72"></div>'
            f'<p class="lead-sm">في المخطوطات العربية إذا سقطت كلمة من الناسخ كتبها في الهامش، ومد إليها من موضعها في السطر خطا معقوفا اسمه اللحق، ثم ختم الإضافة بكلمة صح: أي قوبلت وصحت. '
            f'هذا هو شعار موثّق: الكلمة بخط النسخ، ولحقها يخرج منها إلى الهامش، وفي طرفه صح باللازورد. ومربع الأيقونة هو صح وحدها، علامة القراءة المتحقق منها.</p></div>')
    colors = (f'<div class="id-sheet"><h2 class="h2">الألوان: ثلاثة أحبار</h2><ul class="swatches">{sw}</ul>'
              f'<p class="note">{icon("info")}<span>لا أحمر ولا ألوان للحالات: الحالة علامة مرسومة وكلمة، واللازورد للسند وحده.</span></p></div>')
    signs = f'<div class="id-sheet"><h2 class="h2">علامات النساخ بدل البادجات</h2><ol class="signs-list">{keys}</ol></div>'
    ladder = (f'<div class="id-sheet"><h2 class="h2">سلم الوضع القانوني</h2>{scale(eg["status"])}'
              f'<p class="small-p">خمس خانات مسطرة من الادعاء إلى الحكم: الخانة الحالية باللازورد، وما قبلها مخطط، وما بعدها مفتوح لم يصدر، فلا يقرأ أمر القبض كأنه حكم.</p>'
              f'<ul class="id-scales">{"".join(f"<li><b>{esc(STATUS[s][0])}</b>{scale(s, compact=True)}</li>" for s in ("charged", "sanctioned"))}</ul></div>')
    rows = [('عنوان الصفحة', 'نسخ 700 · 56 بكسل · سطر 1.38'), ('عنوان القسم', 'نسخ 700 · 40 بكسل · سطر 1.5'), ('الوضع القانوني', 'نسخ 700 · 36 بكسل · سطر 1.45'),
            ('القراءة', 'نسخ 400 · 19 بكسل · سطر 2.05'), ('الحاشية', 'كوفي 400–700 · 13–15 بكسل · سطر 1.7'), ('البيانات', 'Fragment Mono · 12–13 بكسل')]
    table = ''.join(f'<tr><th>{a_}</th><td>{b_}</td></tr>' for a_, b_ in rows)
    typ = (f'<div class="id-sheet id-wide id-type"><h2 class="h2">الخط: نسخ للمتن، كوفي للحاشية</h2><div class="id-type-in"><div class="id-spec">'
           f'<p class="display">كل جملة هنا ومعها سندها.</p>'
           f'<p class="lead-sm">نص القراءة بخط Noto Naskh Arabic بحجم 19 بكسل وارتفاع سطر 2.05، وعرض لا يتجاوز 62 حرفا: أصدرت الدائرة التمهيدية الأولى أمر قبض، والأمر ليس حكما بالإدانة.</p>'
           f'<p class="id-kufi">الحاشية والواجهة بخط Noto Kufi Arabic: بيان المحكمة الجنائية الدولية · 21 نوفمبر 2024 · وثيقة قضائية</p>'
           f'<p class="small-p">البيانات وحدها بخط Fragment Mono: <span class="mono">P-0001 · ICC-01/18 · A/HRC/60/CRP.3</span></p></div>'
           f'<table class="id-scale"><tbody>{table}</tbody></table></div></div>')
    motion = (f'<div class="id-sheet id-motion"><h2 class="h2">الحركة: اللحق يكتب</h2>'
              f'<p class="lead-sm">حركة واحدة أصيلة: الجملة التي تقرؤها يغمرها اللازورد كحبر يجف، ثم يخط اللحق منها إلى سندها في الحاشية. لا شيء يتحرك للزينة، وكلها تتوقف عند تفضيل تقليل الحركة.</p>'
              f'<div class="id-demo" data-demo><p><span class="claim" data-demo-claim>ووجدت الدائرة أسبابا معقولة للاعتقاد بمسؤوليته</span> <span class="ref" data-demo-ref>3</span></p>'
              f'<svg class="id-demo-line" aria-hidden="true"><path/></svg>'
              f'<div class="id-demo-gloss">{mark("specific", "mark")}<span><b>معا · تحقق من عناصر محددة</b><small>تطابق في البيان الرسمي وملخص القرار</small></span></div></div>'
              f'<button class="btn btn-line" type="button" data-replay>أعد الحركة</button></div>')
    ticks = ['نسند ولا نجزم: «خلصت اللجنة إلى…»، «وجدت الدائرة أسبابا معقولة للاعتقاد…».', 'الوضع القانوني وجهته وتاريخه قبل الاسم، دائما.',
             'لكل جملة في المتن رقم، ولكل رقم سند في الحاشية؛ الجملة بلا سند لا تنشر.', 'علامة النساخ تكتب دائما ومعها كلمتها الواضحة.',
             'لا ألوان للحالات، ولا أحمر، ولا أختام أو شمع: هذا اتجاه آخر.', 'لا صور جثث أو دماء، ولا أرضيات بيج أو ورق مصفر.']
    voice = f'<div class="id-sheet"><h2 class="h2">صوت الكتابة وما لا نفعله</h2><ul class="ticks">{"".join(f"<li>{esc(x)}</li>" for x in ticks)}</ul></div>'
    main = (f'<section class="id-head"><div class="wrap"><p class="eyebrow">الاتجاه ب</p><h1 class="display">الهوية البصرية: المتن والحاشية</h1>'
            f'<p class="lead">كل صفحة في موثّق متن وحاشيته: المتن يقول ما يقوله السجل، والحاشية تحمل لكل جملة مرقمة سندها ونوعه وتاريخه ودرجة مقابلته. '
            f'الاتجاه مأخوذ من حواشي المخطوطات العربية وعلامات النساخ، ومن هوامش التقارير الحقوقية.</p></div></section>'
            f'<section class="sec id-sec"><div class="wrap id-grid"><div class="id-col">{logo}{ladder}</div><div class="id-col">{signs}{colors}</div>{typ}{motion}{voice}</div></section>')
    page('identity.html', 'الهوية البصرية: المتن والحاشية — موثّق (الاتجاه ب)', 'هوية موثّق في الاتجاه ب: المتن والحاشية، اللحق، علامات النساخ، والأحبار الثلاثة.', main)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    home()
    identity()
    print('b/index.html, b/identity.html')
