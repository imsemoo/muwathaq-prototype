"""Page templates for every route. Called by build.py; never hand-edit the built HTML."""
import os
import re

import build as B
import shell as S
from shell import esc, icon, seal, seal_row, knots, ext, mono, date_ar, write, STATUS, VERIF, REGIONS

slug = B.slug


def P(rel, path, title, desc, active, main, **kw):
    write(path, S.page(title, desc, rel, path, active, main, **kw).replace('<body class="', f'<body data-rel="{rel}" class="'))


def nature_short(d):
    n = d.get('nature_ar', '')
    return n.split('—')[0].split(' - ')[0].strip() or B.DOC_CAT.get(d.get('cat'), 'وثيقة')


# ---------- tags for incident and document ----------
def title_cls(text, limit=80):
    return 'tag-title is-long' if len(text) > limit else 'tag-title'


def incident_tag(inc, rel, actions=True):
    st = B.state_of(inc['id'])
    region = REGIONS.get(inc.get('region'), '')
    precise = 'موقع مؤكد' if inc.get('precise') else 'موقع تقريبي'
    toll = inc.get('toll_ar') or '—'
    acts = ''
    if actions:
        acts = (f'<div class="tag-actions"><a class="btn btn-light" href="{rel}incidents/{slug(inc["id"])}.html">افتح الحرز {icon("arrow")}</a>'
                f'<a class="btn btn-ghost" href="{rel}incidents/{slug(inc["id"])}.html#evidence">الأدلة ({len(inc["ev_ids"])})</a></div>')
    conflict = (f'<div><dt>الروايات</dt><dd>{seal_row("rereview", illus=False).replace("يحتاج إلى إعادة مراجعة", "رواية رسمية تعارضها أدلة")}</dd></div>'
                if inc.get('conflict') else '')
    return f'''<article class="tag is-reversed"{B.vt(inc["id"])} aria-label="سجل واقعة">
  <span class="tag-hole" aria-hidden="true"></span>
  <div class="tag-top"><span class="tag-no">{esc(inc["id"])}</span><span class="tag-kind">واقعة · {esc(region)}</span></div>
  <div class="tag-seal" data-cord-from>{S.wax(st)}</div>
  <h1 class="{title_cls(inc["title_ar"])} open-1">{esc(inc["title_ar"])}</h1>
  <p class="tag-by open-1">{icon("cal")} {esc(date_ar(inc["date"]))}{(" — " + esc(date_ar(inc["date_to"]))) if inc.get("date_to") else ""} · {icon("pin")} {esc(inc.get("place_ar", ""))}</p>
  <dl class="fields open-2">
   <div><dt>حالة التحقق</dt><dd>{seal_row(st)}</dd></div>
   <div><dt>دقة الموقع</dt><dd>{precise}{(" — " + esc(inc["loc_note_ar"])) if inc.get("loc_note_ar") else ""}</dd></div>
   <div><dt>نوع الواقعة</dt><dd>{esc("، ".join(inc.get("type_ar", [])) or "—")}</dd></div>
   <div class="wide"><dt>الحصيلة كما وردت</dt><dd class="dd-more">{esc(toll)}</dd></div>
   {conflict}
  </dl>
  {acts}
</article>'''


def doc_tag(d, rel, actions=True):
    acts = ''
    if actions:
        acts = (f'<div class="tag-actions"><a class="btn btn-light" href="{rel}reports/{slug(d["id"])}.html">افتح الحرز {icon("arrow")}</a>'
                f'{ext(d["url"], "الوثيقة الأصلية", "btn btn-ghost") if d.get("url") else ""}</div>')
    return f'''<article class="tag is-reversed"{B.vt(d["id"])} aria-label="وثيقة">
  <span class="tag-hole" aria-hidden="true"></span>
  <div class="tag-top"><span class="tag-no">{esc(d["id"])}</span><span class="tag-kind">وثيقة · {esc(B.DOC_CAT.get(d.get("cat"), ""))}</span></div>
  <div class="tag-seal" data-cord-from>{S.wax("complete")}</div>
  <p class="tag-status open-1">{esc(nature_short(d))}</p>
  <p class="tag-by open-1">{esc(d.get("publisher_ar", ""))} · {esc(date_ar(d.get("date")))}</p>
  <div class="tag-name open-2"><b>{esc(d.get("title_ar", ""))}</b></div>
  <dl class="fields open-3">
   <div><dt>رمز الوثيقة</dt><dd>{mono(d.get("symbol") or "—")}</dd></div>
   <div><dt>سلامة النسخة</dt><dd>{seal_row("complete")}</dd></div>
   <div class="wide"><dt>الطبيعة القانونية</dt><dd class="dd-more">{esc(d.get("nature_ar", ""))}</dd></div>
   {f'<div class="wide"><dt>النطاق الزمني</dt><dd class="dd-more">{esc(d["period_ar"])}</dd></div>' if d.get("period_ar") else ""}
  </dl>
  {acts}
</article>'''


def evidence_tag(ev, rel):
    kind, ic = B.EV_KIND.get(ev.get('type'), ('مادة', 'doc'))
    inc = B.INC_BY_ID[ev['incident']]
    st = B.ev_state(ev)
    return f'''<article class="tag is-reversed"{B.vt(ev["id"])} aria-label="دليل">
  <span class="tag-hole" aria-hidden="true"></span>
  <div class="tag-top"><span class="tag-no">{esc(ev["id"])}</span><span class="tag-kind">دليل · {esc(kind)}</span></div>
  <div class="tag-seal" data-cord-from>{S.wax(st)}</div>
  <h1 class="{title_cls(ev.get("desc_ar", ""))} open-1">{esc(ev.get("desc_ar", ""))}</h1>
  <p class="tag-by open-1">{esc(ev.get("source", ""))} · {esc(date_ar(ev.get("date")))}</p>
  <dl class="fields open-2">
   <div><dt>حالة التحقق</dt><dd>{seal_row(st)}</dd></div>
   <div><dt>الواقعة</dt><dd><a href="{rel}incidents/{slug(inc["id"])}.html">{esc(inc["title_ar"])}</a></dd></div>
   <div><dt>نوع المادة</dt><dd>{esc(kind)}</dd></div>
   <div><dt>المصدر الأصلي</dt><dd>{ext(ev["url"], "فتح المصدر") if ev.get("url") else "—"}</dd></div>
  </dl>
</article>'''


def person_row(p, rel):
    return (f'<li><a class="row row-person" href="{rel}people/{slug(p["id"])}.html" data-cord-to="{p["id"]}"><span class="row-body">'
            f'<span class="tag-kind">{esc(STATUS[p["status"]][0])}</span><h3>{esc(p["name_ar"])}</h3></span><span class="row-end"><span class="mono">{p["id"]}</span></span></a></li>')


def side_list(title, items, dup=False):
    """dup: the body lists the same records, so on narrow screens, where the side falls below the body, it is left out."""
    if not items:
        return ''
    return f'<section class="side-group{" is-dup" if dup else ""}"><h2 class="side-h">{title} <span class="mono">{len(items)}</span></h2><ul class="rows rows-tight">{"".join(items)}</ul></section>'


def toc_of(body):
    """Give every section heading an id and return (body, contents list) for the sticky side."""
    import re as _re
    items, n = [], [0]
    def fix(m):
        attrs, text = m.group(1), m.group(2)
        hid = _re.search(r'id="([^"]+)"', attrs)
        if not hid:
            n[0] += 1
            hid_v = f'sec-{n[0]}'
            attrs = attrs + f' id="{hid_v}"'
        else:
            hid_v = hid.group(1)
        items.append((hid_v, _re.sub('<[^>]+>', '', text)))
        return f'<h2{attrs}>{text}</h2>'
    body = _re.sub(r'<h2( class="h2"[^>]*)>(.*?)</h2>', fix, body)
    toc = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)
    return body, (f'<nav class="toc" aria-label="في هذا الحرز"><p class="side-h">في هذا الحرز</p><ol>{toc}</ol></nav>' if items else '')


def stamp(rec_id, state=None, counts=(), extra=''):
    """The record's label as it stays beside the reader once the tag has scrolled away: number, seal, what it holds."""
    cells = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in counts if v)
    return (f'<div class="stamp"><div class="stamp-top"><span class="mono">{esc(rec_id)}</span>{seal_row(state) if state else ""}</div>'
            f'{extra}{f"<dl class=stamp-counts>{cells}</dl>" if cells else ""}</div>')


def record(rel, tag, side, below, card=''):
    """One grid for the whole record: the tag and its reading column, and beside them the linked records,
    then a side panel (record stamp, contents, citation) that stays in view to the end."""
    inner = below
    for pre in ('<section class="sec record-body"><div class="wrap read">',):
        if inner.startswith(pre):
            inner = inner[len(pre):]
            inner = inner[:inner.rindex('</div></section>')]
    cite = ''
    if '<div class="cite-box">' in inner:
        k = inner.index('<div class="cite-box">')
        inner, cite = inner[:k], inner[k:]
    inner, toc = toc_of(inner)
    if card:
        toc = (toc.replace('<p class="side-h">', card + '<p class="side-h">', 1) if toc
               else f'<div class="toc">{card}</div>')
    return f'''<section class="record" data-cords>
 <div class="wrap record-grid">
  <div class="record-main"><div data-open>{tag}</div><div class="record-body read">{inner}</div></div>
  <aside class="record-side" aria-label="السجلات المرتبطة">{side}<div class="side-sticky">{toc}{cite}</div></aside>
 </div>
</section>'''


def cite_block(rel, rec_id, text):
    return (f'<div class="cite-box"><p class="xs mute">استشهد بهذا السجل</p><p id="cite-{slug(rec_id)}" class="small">{esc(text)}</p>'
            f'<div class="cite-actions"><button class="btn btn-line btn-sm" type="button" data-copy="cite-{slug(rec_id)}" data-done="نُسخ الاستشهاد.">{icon("doc")} انسخ الاستشهاد</button>'
            f'<button class="btn btn-line btn-sm" type="button" data-copy="url" data-done="نُسخ رابط السجل.">{icon("link")} انسخ الرابط</button>'
            f'<a class="btn btn-line btn-sm" href="{rel}standards.html#correction">طلب تصحيح أو رد</a></div></div>')


# ---------- home ----------
def counted(n, few, many):
    """Arabic counted noun: 3 to 10 take the plural, 11 and up the singular."""
    return few if 3 <= n % 100 <= 10 else many


def register():
    cells = [(len(B.PERSONS), counted(len(B.PERSONS), 'ملفات أشخاص', 'ملف شخص'), 'people/index.html'),
             (len(B.INCIDENTS), counted(len(B.INCIDENTS), 'وقائع', 'واقعة'), 'incidents/index.html'),
             (len(B.EVIDENCE), counted(len(B.EVIDENCE), 'أدلة', 'دليلا'), 'evidence/index.html'),
             (len(B.DOCS), counted(len(B.DOCS), 'وثائق', 'وثيقة'), 'reports/index.html'),
             (len(B.RULES), counted(len(B.RULES), 'قواعد قانونية', 'قاعدة قانونية'), 'law/index.html')]
    return ('<nav class="register" aria-label="ما يحفظه الأرشيف">' +
            ''.join(f'<a href="{href}"><b class="mono">{n}</b> <span>{esc(label)}</span></a>' for n, label, href in cells) + '</nav>')


SILHOUETTE = ('<svg class="sil" viewBox="0 0 120 150" aria-hidden="true"><circle cx="60" cy="54" r="27"/>'
              '<path d="M12 150c0-36 21-60 48-60s48 24 48 60z"/></svg>')


def count_ar(n, one, two, few, many):
    """Arabic counted noun: 1 and 2 have their own forms, 3 to 10 the plural, 11 and up the singular."""
    return {1: one, 2: two}.get(n) or f'{n} {few if 3 <= n % 100 <= 10 else many}'


def person_href(p, rel):
    return f'{rel}people/{p["slug"] if p.get("demo") else slug(p["id"])}.html'


def charge_of(p):
    """The type of charge in a few words: the client's list for real files, the first act for illustrative ones."""
    if p.get('demo'):
        return p['acts'][0]['act_ar'] if p['acts'] else ''
    return B.PICKS.get('charge_ar', {}).get(p['id'], '')


# the stamp's word and its basis line, per legal standing
STAMP = {'convicted': ('مدان', 'حكم قضائي نهائي'), 'warrant': ('مطلوب', 'أمر قبض دولي'),
         'charged': ('متهم', 'لائحة اتهام رسمية'), 'named': ('ورد اسمه', 'في تحقيق أممي موثق'),
         'sanctioned': ('عقوبات', 'قرار حكومي إداري'), 'alleged': ('قيد التحقق', 'ادعاءات لم تراجع')}


def fstamp(p):
    word, basis = STAMP[p['status']]
    lv = STATUS[p['status']][1]
    form = 'is-firm' if lv >= 4 else ('is-charged' if lv == 3 else ('is-open' if lv == 2 else 'is-loose'))
    _, _, main = B.person_status_line(p) if not p.get('demo') else (None, None, {})
    year = (main.get('date') or '')[:4]
    return (f'<span class="fstamp {form}" aria-hidden="true"><b>{esc(word)}</b><small>{esc(basis)}</small>'
            f'{f"<i class=mono>{year}</i>" if year else ""}</span><span class="sr">{esc(STATUS[p["status"]][0])}.</span>')


def fcard(p, rel):
    """A file in the persons database: photo, then legal standing, name, role and the charge; one quiet line
    for the articles the acts engage. The standing label weighs what it means: a warrant or a conviction is
    solid ink, a charge, a naming or a sanction is outlined, an allegation under review is dashed."""
    demo = p.get('demo')
    ph = None if demo else B.photo_of(p['id'])
    if ph:
        sz = B.PHOTO_SIZE[ph]
        pic = (f'<img src="{rel}assets/img/photo/{ph}-640.webp" alt="" width="640" height="{round(640 * sz["h"] / sz["w"])}" '
               f'loading="lazy" decoding="async">')
    else:
        pic = f'{SILHOUETTE}<small>{"ملف تجريبي — لا صورة" if demo else "لا صورة منشورة في الملف"}</small>'
    n = len(p['rule_ids'])
    badge = '<span class="fcard-demo">تجريبي</span>' if demo else ''
    charge = charge_of(p)
    return (f'<a class="fcard{" is-demo" if demo else ""}" href="{person_href(p, rel)}">'
            f'<span class="fcard-ph{"" if ph else " is-empty"}">{pic}{badge}{fstamp(p)}</span>'
            f'<span class="fcard-body">'
            f'<b class="fcard-name">{esc(p["name_ar"])}</b><span class="fcard-role">{esc(p.get("role_ar", ""))}</span>'
            f'{f"<span class=fcard-charge>{esc(charge)}</span>" if charge else ""}</span>'
            f'<span class="fcard-foot"><span>{count_ar(n, "مادة قانونية واحدة", "مادتان قانونيتان", "مواد قانونية", "مادة قانونية")}</span>'
            f'<span class="fcard-open">عرض الملف {icon("arrow")}</span></span></a>')


def fcard_li(p, rel):
    text = ' '.join([p['name_ar'], p.get('name_en', ''), p.get('role_ar', '')] + [x['act_ar'] for x in p['acts']])
    return f'<li data-status="{p["status"]}" data-kind="{"demo" if p.get("demo") else "file"}" data-text="{esc(text)}">{fcard(p, rel)}</li>'


def all_people():
    return B.PERSONS + B.DEMO


def people_filter(persons, legend='الوضع القانوني'):
    opts = [(k, STATUS[k][0], f'<span class="mono">{STATUS[k][1]}/5</span>', sum(p['status'] == k for p in persons))
            for k in STATUS if any(p['status'] == k for p in persons)]
    return facet('status', legend, opts)


def wanted(rel):
    """The banner: the two people the International Criminal Court has issued arrest warrants for."""
    pa, pb = B.P_BY_ID['P-0001'], B.P_BY_ID['P-0002']
    # Gallant had left the ministry two weeks before the warrants were issued
    roles = {'P-0001': pa.get('role_ar', ''), 'P-0002': 'وزير الدفاع الإسرائيلي السابق'}

    def side(p, cls):
        ph = B.photo_of(p['id'])
        sz = B.PHOTO_SIZE[ph]
        return (f'<a class="wanted-face {cls}" href="{rel}people/{slug(p["id"])}.html">'
                f'<img src="{rel}assets/img/photo/{ph}-640.webp" alt="{esc(p["name_ar"])}" width="640" '
                f'height="{round(640 * sz["h"] / sz["w"])}" fetchpriority="high">'
                f'<span class="wanted-cap"><b>{esc(p["name_ar"])}</b><span>{esc(roles[p["id"]])}</span></span></a>')
    st = next(s for s in pa['statuses'] if s.get('type') == 'warrant')
    acts = ''.join(f'<li>{esc(x["act_ar"])}</li>' for x in pa['acts'][:3])
    return f"""<section class="wanted is-reversed" aria-labelledby="wanted-h">
 <div class="wrap wanted-grid">
  {side(pa, 'is-start')}
  <div class="wanted-mid">
   <p class="wanted-by">المحكمة الجنائية الدولية · الدائرة التمهيدية الأولى · <span class="mono">{esc(st.get("doc_symbol", ""))}</span></p>
   <h1 class="wanted-h" id="wanted-h">مطلوبان للعدالة الدولية</h1>
   <p class="wanted-lead">أمران بالقبض صدرا في {esc(date_ar(st["date"]))}، بعد أن وجدت الدائرة أسبابا معقولة للاعتقاد بمسؤوليتهما الجنائية عن:</p>
   <ul class="wanted-acts">{acts}</ul>
   <div class="wanted-knots">{knots("warrant")}</div>
   <p class="wanted-not">{icon("info")}<span>أمر القبض ليس حكما بالإدانة، ويفترض براءة الشخص حتى تثبت إدانته.</span></p>
   <div class="wanted-actions"><a class="btn btn-light" href="{rel}people/{slug(pa["id"])}.html">ملف نتنياهو</a><a class="btn btn-ghost" href="{rel}people/{slug(pb["id"])}.html">ملف غالانت</a>{ext(st["url"], "بيان المحكمة", "btn btn-ghost")}</div>
  </div>
  {side(pb, 'is-end')}
 </div>
</section>"""


REVIEW = [('الاستلام', 'يسجل المقال ويصل إشعار للكاتب.'), ('المراجعة التحريرية', 'الوضوح والبنية واللغة.'),
          ('تدقيق الوقائع', 'كل واقعة بمصدرها.'), ('التحكيم القانوني', 'مختص في القانون الدولي.'),
          ('النشر أو الرد', 'ينشر بتاريخه أو يعاد بملاحظات.')]


def review_path():
    return ('<ol class="review-path" aria-label="مراحل نشر المقال">' +
            ''.join(f'<li><b>{esc(x)}</b><span>{esc(y)}</span></li>' for x, y in REVIEW) + '</ol>')


def article_card(x, rel):
    badge = '<span class="fcard-demo">تجريبي</span>' if x.get('demo') else ''
    return (f'<a class="acard" href="{rel}articles/{x["slug"]}.html"><span class="acard-meta"><span>{esc(x["topic_ar"])}</span>'
            f'<span>{esc(date_ar(x["date"]))}</span>{badge}</span>'
            f'<b class="acard-t">{esc(x["title_ar"])}</b><span class="acard-x">{esc(x["dek_ar"])}</span>'
            f'<span class="acard-by">{esc(x["author_ar"])}</span></a>')


def bar_li(r, rel, total):
    n = len(r['p_ids'])
    return (f'<li><a href="{rel}law/{slug(r["id"])}.html"><span class="bar-t"><span class="mono">{esc(B.rule_short(r))}</span> '
            f'{esc(r.get("title_ar", ""))}</span><span class="bar" style="--w:{n / max(1, total):.3f}"><i></i></span>'
            f'<b class="mono">{n}</b></a></li>')


def home():
    rel = ''
    people = all_people()
    pdb = f"""<section class="sec" id="accused" aria-labelledby="accused-h">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2" id="accused-h">الأشخاص المتهمون</h2><p>قاعدة بيانات الأشخاص والملفات القانونية: كل ملف يربط الشخص بالأفعال المنسوبة إليه وبالمواد القانونية التي قد تنطبق عليها، مع حالته القانونية ومصدرها.</p></div><a class="link-arrow" href="people/index.html">كل الملفات {icon("arrow")}</a></div>
  <form class="chips-filter" data-filter="home-people" data-count="home-people-count" data-empty="home-people-empty" aria-label="تصفية الأشخاص حسب الوضع القانوني">{people_filter(people)}</form>
  <p class="count" id="home-people-count" aria-live="polite"></p>
  <ul class="fcards" id="home-people">{"".join(fcard_li(p, rel) for p in people)}</ul>
  <div class="empty" id="home-people-empty" hidden>{seal("not_started", label=False)}<p><b>لا ملفات بهذا الوضع القانوني بعد.</b></p></div>
  <p class="note is-quiet">{icon("info")}<span>الملفات الموسومة «تجريبي» نماذج لا تخص أشخاصا حقيقيين: تعرض كيف يبنى ملف لشخص ظهر في مواد مصورة منشورة ولم تصنفه أي جهة بعد. لا ينشر ملف كهذا إلا بعد التحقق والمراجعة القانونية.</span></p>
 </div>
</section>"""
    docs = sorted(B.DOCS, key=lambda d: d.get('date', ''), reverse=True)
    national = [d for d in docs if d.get('cat') == 'national']
    intl = [d for d in docs if d.get('cat') != 'national']
    if national:
        lists = (f'<div class="two-lists"><div><h3 class="h3 col-h">قرارات وتقارير دولية</h3><ul class="rows">{"".join(B.doc_row(d, rel) for d in intl[:5])}</ul></div>'
                 f'<div><h3 class="h3 col-h">إجراءات قضائية وطنية</h3><ul class="rows">{"".join(B.doc_row(d, rel) for d in national[:5])}</ul></div></div>')
    else:
        lists = f'<ul class="rows">{"".join(B.doc_row(d, rel) for d in intl[:6])}</ul>'
    reports = f"""<section class="sec band-paper" aria-labelledby="reports-h">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2" id="reports-h">التقارير الدولية</h2><p>وثائق قضائية وأممية وحقوقية، وإجراءات قضاء وطني في عدة دول، كل منها بطبيعته القانونية.</p></div><a class="link-arrow" href="reports/index.html">كل التقارير ({len(docs)}) {icon("arrow")}</a></div>
  {lists}
 </div>
</section>"""
    articles = f"""<section class="sec" aria-labelledby="articles-h">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2" id="articles-h">المقالات</h2><p>مقالات في القانون الدولي وجرائم الحرب يكتبها باحثون وكتاب، وتنشر بعد التحكيم والتدقيق.</p></div><a class="btn btn-ink" href="articles/write.html">اكتب مقالا</a></div>
  <ul class="acards">{"".join(f"<li>{article_card(x, rel)}</li>" for x in B.ARTICLES[:3])}</ul>
  <h3 class="h3 path-h">كيف ينشر مقال</h3>
  {review_path()}
 </div>
</section>"""
    tops = sorted([r for r in B.RULES if r['p_ids']], key=lambda r: (-len(r['p_ids']), r['id']))[:6]
    database = f"""<section class="sec band-paper" aria-labelledby="db-h">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2" id="db-h">قاعدة البيانات التفاعلية</h2><p>عدد الأشخاص الموثقة ملفاتهم، وكيف ترتبط الأفعال المنسوبة إليهم بمواد القانون الدولي الإنساني وغيره.</p></div><a class="link-arrow" href="database.html">افتح قاعدة البيانات {icon("arrow")}</a></div>
  {register()}
  <h3 class="h3 col-h">المواد الأكثر ارتباطا بالملفات</h3>
  <ul class="bars">{"".join(bar_li(r, rel, len(B.PERSONS)) for r in tops)}</ul>
 </div>
</section>"""
    method_steps = ['جمع المادة', 'تسجيل المصدر والعهدة', 'الأصالة والسياق', 'المقارنة المستقلة', 'الموقع والزمن', 'توثيق القيود',
                    'المراجعة القانونية', 'حماية الأشخاص', 'قرار النشر', 'التصحيح المستمر']
    strip = ''.join(f'<li class="is-tied"><i></i><span>{s}</span></li>' for s in method_steps)
    method = f"""<section class="sec sec-ink method-strip">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2">منهجية التحقق: عشر خطوات</h2><p>لا ينشر ملف قبل أن يمر بكل خطوة.</p></div><a class="btn btn-light" href="method.html">المنهجية كاملة</a></div>
  <ol class="cord-steps">{strip}</ol>
 </div>
</section>"""
    act = f"""<section class="sec">
 <div class="wrap act-grid">
  <div class="sheet act">
   {seal("in_progress", label=False)}
   <h2 class="h2">أرسل مادة للمراجعة</h2>
   <p>كل مساهمة تفحص وتراجع قانونيا قبل أي نشر.</p>
   <p class="note is-quiet">{icon("shield")}<span>لا ترسل ما يعرضك أو يعرض غيرك للخطر.</span></p>
   <a class="btn btn-ink" href="submit.html">ابدأ الإرسال</a>
  </div>
  <div class="sheet act">
   {seal("complete", label=False)}
   <h2 class="h2">ادعم التوثيق المستقل</h2>
   <p>تمول المساهمات حفظ الأدلة والتحقق والمراجعة القانونية.</p>
   <p class="note is-quiet">{icon("lock")}<span>الدفع غير مفعل في هذا النموذج.</span></p>
   <a class="btn btn-line" href="donate.html">طرق الدعم</a>
  </div>
 </div>
</section>"""
    main = wanted(rel) + pdb + reports + articles + database + method + act
    P(rel, 'index.html', 'موثّق', 'منصة مستقلة لتوثيق الأشخاص المتهمين بجرائم الاحتلال الإسرائيلي، وربط الأفعال المنسوبة إليهم بمواد القانون الدولي.',
      'home', main, body_cls='home')


# ---------- lists ----------
def facet(key, legend, opts):
    """One filter shown as a list of its values with how many records each holds; the counts follow the other filters."""
    total = sum(n for *_, n in opts)
    rows = [('', 'الكل', '', total)] + list(opts)
    items = ''.join(f'<label class="facet-opt"><input type="radio" name="f-{key}" value="{esc(v)}"{" checked" if not v else ""}>'
                    f'<span class="facet-mark" aria-hidden="true">{mark}</span><span class="facet-t">{esc(lab)}</span><span class="facet-n">{n}</span></label>'
                    for v, lab, mark, n in rows)
    return f'<fieldset class="facet" data-key="{key}"><legend class="side-h">{legend}</legend>{items}</fieldset>'


def archive_card(total, noun, rng='', counts=()):
    cells = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in counts if v)
    return (f'<div class="stamp"><div class="stamp-top"><p class="stamp-total"><b>{total}</b> {noun}</p>{f"<span class=mono>{esc(rng)}</span>" if rng else ""}</div>'
            f'{f"<dl class=stamp-counts>{cells}</dl>" if cells else ""}</div>')


def id_range(ids):
    ids = sorted(ids)
    return f'{ids[0]} – {ids[-1]}' if len(ids) > 1 else (ids[0] if ids else '')


def list_page(rel, path, active, title, lead, filters, items_html, list_id, extra='', cls='rows', before='', fac='', card=''):
    """An archive: the records, and beside them a panel that stays in view: what the archive holds,
    the search and filters, and one facet whose counts follow the other filters."""
    cut = filters.index('</div>') + len('</div>')   # the search field comes first; the rest fold on phones
    q, rest = filters[:cut], filters[cut:]
    main = f'''<div class="wrap">{S.crumbs(rel, [(title, None)])}</div>
<section class="list-head"><div class="wrap"><h1 class="h1">{esc(title)}</h1><p class="lead">{lead}</p>{before}</div></section>
<section class="sec list-sec"><div class="wrap list-grid">
 <aside class="list-side" aria-label="تصفية {esc(title)}"><div class="side-sticky" data-lenis-prevent>
  <div class="panel">{card}
   <form class="filters filters-side" data-filter="{list_id}" data-count="{list_id}-count" data-empty="{list_id}-empty" role="search" aria-label="تصفية {esc(title)}">{q}<details class="filt-more" data-filt open><summary>{icon("layers")}<span>التصفية</span><b class="filt-n" data-filt-n hidden></b></summary><div class="filt-in">{rest}{fac}<button class="btn btn-line btn-sm" type="reset">إعادة الضبط</button></div></details></form>
  </div>
 </div></aside>
 <div class="list-main">
  <h2 class="sr">السجلات</h2>
  <p class="count" id="{list_id}-count" aria-live="polite"></p>
  <ul class="{cls}" id="{list_id}">{items_html}</ul>
  <div class="empty" id="{list_id}-empty" hidden>{seal("not_started", label=False)}<p><b>لا توجد سجلات تطابق هذا البحث.</b> غيّر المرشحات أو امسحها.</p></div>
  {extra}
 </div>
</div></section>'''
    P(rel, path, title, lead, active, main)


def q_field(placeholder):
    return f'<div class="field grow"><label for="fq">بحث</label><input class="input" id="fq" data-q type="search" placeholder="{placeholder}"></div>'


def sel(fid, label, key, options):
    opts = ''.join(f'<option value="{esc(v)}">{esc(t)}</option>' for v, t in options)
    return f'<div class="field"><label for="{fid}">{label}</label><select class="select" id="{fid}" data-key="{key}"><option value="">الكل</option>{opts}</select></div>'


def people_pages():
    rel = '../'
    people = all_people()
    items = ''.join(fcard_li(p, rel) for p in people)
    note = (f'<p class="note" style="margin-top:28px">{icon("info")}<span>لا يدرج شخص حقيقي دون مصدر رسمي لوضعه القانوني، ولكل معني حق التصحيح أو الرد. '
            f'الملفات الموسومة «تجريبي» نماذج لا تخص أشخاصا حقيقيين.</span></p>')
    list_page(rel, 'people/index.html', 'people', 'الأشخاص المتهمون',
              'كل ملف يربط الشخص بالأفعال المنسوبة إليه وبالمواد القانونية التي قد تنطبق عليها، مع حالته القانونية ومصدرها.',
              q_field('اسم أو منصب أو فعل'), items, 'people-list', cls='fcards',
              fac=people_filter(people),
              card=archive_card(len(B.PERSONS), 'ملف شخص', id_range([p['id'] for p in B.PERSONS]),
                                (('مواد قانونية', len({r for p in B.PERSONS for r in p['rule_ids']})), ('ملفات تجريبية', len(B.DEMO)))),
              extra=note)
    for p in B.PERSONS:
        person_page(p)
    for p in B.DEMO:
        demo_page(p)


def acts_block(p, rel):
    """Each act in the file, then the articles that may apply to it, each one a link into the law library."""
    items = ''
    for x in p['acts']:
        rules = [B.RULE_BY_ID[r] for r in x['rule_ids'] if r in B.RULE_BY_ID]
        chips = ''.join(f'<a class="rule" href="{rel}law/{slug(r["id"])}.html"><span class="mono">{esc(B.rule_short(r))}</span>'
                        f'<b>{esc(r.get("title_ar", ""))}</b><small>{esc(r.get("instrument_ar", ""))}</small></a>' for r in rules)
        basis = f'<p class="lg-basis">{esc(x["basis_ar"])}</p>' if x.get('basis_ar') else ''
        items += (f'<li class="lg"><h3 class="lg-act">{esc(x["act_ar"])}</h3>{basis}'
                  f'<div class="lg-rules">{chips or "<span class=small>لم تربط بمادة بعد.</span>"}</div></li>')
    return (f'<h2 class="h2" id="acts">الأفعال المنسوبة والمواد القانونية</h2><ol class="sheet legal-list">{items}</ol>'
            f'<p class="note">{icon("scale")}<span>الربط تحليل أولي يبين المواد التي قد تنطبق على كل فعل؛ لا يعني ثبوت الفعل ولا المسؤولية الجنائية.</span></p>')


def media_block(p, rel):
    """Pictures from the incidents a person's file is tied to: places and aftermath, each with its source."""
    figs = []
    for i in p['inc_ids']:
        ph = B.photo_of(i)
        if ph and len(figs) < 4:
            inc = B.INC_BY_ID[i]
            sz = B.PHOTO_SIZE[ph]
            figs.append(f'<li><a href="{rel}incidents/{slug(i)}.html"><img src="{rel}assets/img/photo/{ph}-640.webp" alt="{esc(B.PHOTOS[ph].get("alt", ""))}" '
                        f'width="640" height="{round(640 * sz["h"] / sz["w"])}" loading="lazy" decoding="async"><span>{esc(inc["title_ar"])}</span></a></li>')
    if not figs:
        return ''
    return (f'<h2 class="h2">صور من الوقائع المرتبطة</h2><ul class="media-grid">{"".join(figs)}</ul>'
            f'<p class="note is-quiet">{icon("shield")}<span>صور أماكن وآثار فقط، ولكل صورة مصدرها وترخيصها في سجل الواقعة.</span></p>')


def demo_tag(p, rel):
    acts = ''.join(f'<li><b>{esc(x["act_ar"])}</b></li>' for x in p['acts'])
    return f"""<article class="tag is-reversed is-demo" aria-label="ملف تجريبي">
  <span class="tag-hole" aria-hidden="true"></span>
  <div class="tag-top"><span class="tag-no">{esc(p["id"])}</span><span class="tag-kind">ملف تجريبي</span></div>
  <div class="tag-seal">{S.wax("in_progress")}</div>
  <h1 class="tag-status">{esc(STATUS[p["status"]][0])}</h1>
  <p class="tag-by">رصد أولي من مواد مصورة منشورة — مثال توضيحي</p>
  <div class="tag-who"><span class="tag-face sil-face">{SILHOUETTE}</span><div class="tag-name"><b>{esc(p["name_ar"])}</b><span>{esc(p["role_ar"])}</span></div></div>
  <div style="margin-top:18px">{knots(p["status"])}</div>
  <p class="tag-not">{icon("info")}<span>ملف تجريبي لا يخص شخصا حقيقيا. الادعاء ليس اتهاما ولا إدانة، ويفترض براءة الشخص حتى تثبت إدانته.</span></p>
  <dl class="fields">
   <div><dt>حالة التحقق من الملف</dt><dd>{seal_row("in_progress")}</dd></div>
   <div><dt>مصدر المادة</dt><dd>مقطع منشور على حساب عام (مثال)</dd></div>
   <div class="wide"><dt>الأفعال المنسوبة</dt><dd><ul class="acts">{acts}</ul></dd></div>
  </dl>
</article>"""


DEMO_STEPS = [('التعرف على الشخص', 'بمصادر مستقلة متطابقة، لا بالتشابه.'), ('التحقق من المادة', 'الأصالة والمكان والزمان وأول ظهور.'),
              ('التكييف القانوني', 'المواد التي قد تنطبق وما يلزم إثباته.'), ('المراجعة القانونية', 'مختص يراجع الملف قبل أي قرار.'),
              ('قرار النشر', 'وحق الرد والتصحيح بعده.')]


def demo_page(p):
    rel = '../'
    rules = [B.RULE_BY_ID[r] for r in p['rule_ids'] if r in B.RULE_BY_ID]
    side = side_list('المواد القانونية', [B.rule_row(r, rel) for r in rules])
    steps = ''.join(f'<li><b>{esc(x)}</b><span>{esc(y)}</span></li>' for x, y in DEMO_STEPS)
    below = f"""<section class="sec record-body"><div class="wrap read">
 {acts_block(p, rel)}
 <h2 class="h2">المادة المصورة</h2>
 <div class="media-empty">{icon("video")}<p><b>تعرض هنا المادة بعد التحقق منها</b><span>مع مصدرها وتاريخ أول نشر، وتحذير قبل أي مشهد مؤلم.</span></p></div>
 <h2 class="h2">كيف يكتمل هذا الملف</h2>
 <ol class="review-path">{steps}</ol>
 <h2 class="h2">ما لا ينشر</h2>
 <div class="prose"><p>لا تنشر عناوين السكن أو أرقام الهواتف أو بيانات العائلات، ولا أي معلومة تزيد على ما يلزم لتحديد الشخص في الفعل الموثق. وينشر مصدر المادة بوصفه دليلا.</p></div>
</div></section>"""
    card = stamp(p['id'], 'in_progress', (('الأفعال', len(p['acts'])), ('المواد', len(rules))),
                 f'<p class="stamp-status">{esc(STATUS[p["status"]][0])} <span class="mono">{STATUS[p["status"]][1]}/5</span></p>')
    main = (f'<div class="wrap">{S.crumbs(rel, [("الأشخاص المتهمون", "people/index.html"), (p["name_ar"], None)])}</div>' +
            record(rel, demo_tag(p, rel), side, below, card))
    P(rel, f'people/{p["slug"]}.html', p['name_ar'], 'ملف تجريبي: كيف يبنى ملف لشخص ظهر في مواد مصورة منشورة.', 'people', main)


def person_page(p):
    rel = '../'
    incs = [B.INC_BY_ID[i] for i in p['inc_ids']]
    docs = [B.DOC_BY_ID[d] for d in p['doc_ids']]
    rules = [B.RULE_BY_ID[r] for r in p['rule_ids'] if r in B.RULE_BY_ID]
    side = (side_list('الوقائع', [B.inc_mini_row(i, rel) for i in incs], dup=True) + side_list('الوثائق', [B.doc_row(d, rel) for d in docs]) +
            side_list('القواعد', [B.rule_row(r, rel) for r in rules])) or f'<p class="small mute">لا سجلات مرتبطة بعد.</p>'
    tag = B.person_tag(p, rel, actions=False).replace('<span class="tag-hole" aria-hidden="true"></span>', '<span class="tag-hole" aria-hidden="true"></span>', 1)
    tag = tag.replace('<p class="tag-status', '<h1 class="tag-status', 1).replace('</p>\n  <p class="tag-by', '</h1>\n  <p class="tag-by', 1)
    timeline = ''.join(f'''<li><span class="tl-date num">{esc(date_ar(s.get("date")))}</span><div class="tl-body"><p class="tl-kind">{esc(STATUS.get(s.get("type"), (s.get("type", ""),))[0] if s.get("type") in STATUS else ("قرار إجرائي" if s.get("type") == "procedural" else s.get("type", "")))}</p>
      <h3>{esc(s.get("doc_title_ar") or s.get("doc_title_en", ""))}</h3><p class="small mute">{esc(s.get("body_ar", ""))}{(" · " + mono(s["doc_symbol"])) if s.get("doc_symbol") else ""}</p>
      <p class="small">{esc(s.get("summary_ar", ""))}</p>{ext(s["url"], "الوثيقة الرسمية", "small") if s.get("url") else ""}</div></li>''' for s in sorted(p.get('statuses', []), key=lambda s: s.get('date', '')))
    events = ''.join(f'<li><span class="tl-date num">{esc(date_ar(t.get("date")))}</span><div class="tl-body"><p class="small">{esc(t.get("event_ar", ""))}</p>{ext(t["url"], "المصدر", "xs") if t.get("url") else ""}</div></li>'
                     for t in sorted(p.get('timeline', []), key=lambda t: t.get('date', '')))
    below = f'''<section class="sec record-body"><div class="wrap read">
 {acts_block(p, rel)}
 <h2 class="h2" id="status">الوضع القانوني بالتفصيل</h2>
 <ol class="timeline" data-tie>{timeline}</ol>
 {f'<h2 class="h2">التسلسل الإجرائي</h2><ol class="timeline timeline-quiet">{events}</ol>' if events else ''}
 <h2 class="h2">ما تثبته هذه المصادر وما لا تثبته</h2>
 <div class="prose"><p>{esc(p.get("limits_ar", ""))}</p></div>
 <h2 class="h2" id="incidents">الوقائع المرتبطة</h2>
 {f'<ul class="rows">{"".join(B.inc_mini_row(i, rel) for i in incs)}</ul>' if incs else '<p class="note">' + icon("info") + '<span>لا واقعة مرتبطة بعد؛ يربط الشخص بواقعة فقط بوثيقة رسمية.</span></p>'}
 {media_block(p, rel)}
 <h2 class="h2">المصادر</h2>
 {B.sources_list(p.get("sources", []))}
 {B.face_credit(B.photo_of(p["id"]))}
 <div class="sheet custody-sheet">{B.custody(p["id"], B.default_custody("person"))}</div>
 {cite_block(rel, p["id"], f'موثّق، «{p["name_ar"]}»، ملف {p["id"]}، {STATUS[p["status"]][0]}. اطُّلع عليه في 28 أكتوبر 2026.')}
</div></section>'''
    card = stamp(p['id'], counts=(('الوقائع', len(incs)), ('الوثائق', len(docs)), ('القواعد', len(rules)), ('المصادر', len(p.get('sources', [])))),
                 extra=f'<p class="stamp-status">{esc(STATUS[p["status"]][0])} <span class="mono">{STATUS[p["status"]][1]}/5</span></p>')
    main = f'<div class="wrap">{S.crumbs(rel, [("الأشخاص المتهمون", "people/index.html"), (p["name_ar"], None)])}</div>' + record(rel, tag, side, below, card)
    P(rel, f'people/{slug(p["id"])}.html', p['name_ar'], f'{STATUS[p["status"]][0]} — {p.get("role_ar", "")}', 'people', main)


def incidents_pages():
    rel = '../'
    incs = sorted(B.INCIDENTS, key=lambda i: i['date'], reverse=True)
    items = ''.join(B.inc_mini_row(i, rel) for i in incs)
    regions = [(k, REGIONS[k]) for k in REGIONS if any(i.get('region') == k for i in incs)]
    states = [(k, VERIF[k][0]) for k in VERIF if any(B.state_of(i['id']) == k for i in incs)]
    years = sorted({i['date'][:4] for i in incs}, reverse=True)
    # the time rope: one knot per incident on a cord from the first record to today (earliest at the start side)
    import datetime as _dt
    d0 = _dt.date(2023, 10, 1); d1 = _dt.date(2026, 10, 31)
    span = (d1 - d0).days
    def pos(iso):
        y, m, *dd = [int(x) for x in iso.split('-')]
        t = ((_dt.date(y, m, dd[0] if dd else 15) - d0).days) / span
        return max(0.01, min(0.99, t))
    knots_html = ''.join(
        f'<a class="tr-knot" href="{slug(i["id"])}.html" data-id="{i["id"]}" data-label="{esc(date_ar(i["date"]))} — {esc(i["title_ar"])}" '
        f'style="inset-inline-start:{pos(i["date"]) * 100:.2f}%;top:{22 + 36 * pos(i["date"]) * (1 - pos(i["date"])):.1f}px">'
        f'<span class="sr">{esc(date_ar(i["date"]))}: {esc(i["title_ar"])}</span></a>' for i in incs)
    year_marks = ''.join(f'<span class="tr-year" style="inset-inline-start:{pos(f"{y}-01-01") * 100:.2f}%">{y}</span>' for y in (2024, 2025, 2026))
    rope = (f'<div class="timerope" data-timerope><p class="tr-cap">{len(incs)} واقعة على حبل الزمن، من أكتوبر 2023 إلى اليوم. قف على عقدة لترى الواقعة.</p>'
            f'<div class="tr-body"><svg class="tr-line" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 22 Q500 40 1000 22"/></svg>'
            f'{knots_html}{year_marks}<p class="tr-tip" hidden></p></div></div>')
    list_page(rel, 'incidents/index.html', 'incidents', 'أرشيف الوقائع',
              'ما حدث بحسب المصادر، والروايات، والأدلة، والتحليل القانوني لكل واقعة.',
              q_field('عنوان أو مكان') + sel('fr', 'المنطقة', 'region', regions) + sel('fy', 'السنة', 'year', [(y, y) for y in years]),
              items, 'inc-list', before=rope,
              fac=facet('state', 'حالة التحقق', [(k, v, seal(k, label=False), sum(B.state_of(i['id']) == k for i in incs)) for k, v in states]),
              card=archive_card(len(incs), 'سجل واقعة', id_range([i['id'] for i in incs]),
                                (('أدلة', sum(len(i['ev_ids']) for i in incs)), ('مصادر', sum(len(i.get('sources', [])) for i in incs)), ('قواعد', len({r for i in incs for r in i['rule_ids']})))))
    for i in B.INCIDENTS:
        incident_page(i)


def incident_page(inc):
    rel = '../'
    evs = [B.EV_BY_ID[e] for e in inc['ev_ids']]
    rules = [B.RULE_BY_ID[r] for r in inc['rule_ids'] if r in B.RULE_BY_ID]
    persons = [B.P_BY_ID[p] for p in inc['pids']]
    docs = [d for d in B.DOCS if inc['id'] in d['inc_ids']]
    side = (side_list('الأشخاص', [person_row(p, rel) for p in persons]) +
            side_list('الأدلة', [B.ev_row(e, rel) for e in evs], dup=True) + side_list('القواعد', [B.rule_row(r, rel) for r in rules], dup=True) +
            side_list('الوثائق', [B.doc_row(d, rel) for d in docs]))
    ph = B.photo_of(inc['id'])
    accounts = ''
    if inc.get('official_account_ar') or inc.get('findings_ar'):
        accounts = f'''<h2 class="h2">الروايات</h2>
 <div class="accounts{' is-conflict' if inc.get('conflict') else ''}">
  <div class="account"><h3 class="h3">رواية الجهة المعنية</h3><p>{esc(inc.get("official_account_ar") or "لم نعثر على رواية رسمية منشورة.")}</p></div>
  <div class="seam" aria-hidden="true">{seal("rereview" if inc.get("conflict") else "partial", label=False)}</div>
  <div class="account"><h3 class="h3">ما وجدته التحقيقات المستقلة</h3><p>{esc(inc.get("findings_ar") or "—")}</p></div>
 </div>
 {'<p class="note">' + icon("alert") + '<span>الروايتان كما وردتا، وترجيح إحداهما يذكر سببه.</span></p>' if inc.get('conflict') else ''}'''
    # one block per act: the act, the rules it engages, then why and what must be proven side by side
    legal_rows = ''.join(f'''<li class="lg"><h3 class="lg-act">{esc(L.get("act_ar", ""))}</h3>
      <div class="lg-rules">{"".join(f'<a class="rule" href="{rel}law/{slug(r)}.html"><span class="mono">{esc(B.rule_short(B.RULE_BY_ID[r]))}</span><b>{esc(B.RULE_BY_ID[r].get("title_ar", ""))}</b></a>' for r in L.get("ids", []) if r in B.RULE_BY_ID) or esc("، ".join(L.get("rules", [])))}</div>
      <div class="lg-cols"><div><p class="lg-h">لماذا قد تنطبق</p><p>{esc(L.get("why_ar", ""))}</p></div><div><p class="lg-h">ما يلزم إثباته</p><p>{esc(L.get("to_prove_ar", ""))}</p></div></div></li>''' for L in inc.get('legal', []))
    resp = (f'<p>ورد في هذا السجل {"، ".join(esc(p["name_ar"]) for p in persons)} لأن وثيقة رسمية ربطت وضعهم القانوني بالأفعال محل التحليل؛ لا يعني ذلك ثبوت مسؤوليتهم الفردية عن هذه الواقعة بعينها.</p>'
            if persons else '<p>لم يُربط هذا السجل بشخص بعينه. تحديد المسؤولية الفردية يتطلب أدلة على المساهمة الشخصية أو شروط المسؤولية القيادية، وهو خارج نطاق هذا السجل.</p>')
    below = f'''<section class="sec record-body"><div class="wrap read">
 {B.photo_fig(ph, rel, sizes="(min-width: 1024px) 760px, 100vw") if ph else ""}
 <h2 class="h2">ماذا حدث بحسب المصادر</h2>
 <div class="prose"><p>{esc(inc.get("summary_ar", ""))}</p></div>
 {accounts}
 <h2 class="h2" id="evidence">الأدلة ({len(evs)})</h2>
 <ul class="rows">{"".join(B.ev_row(e, rel) for e in evs)}</ul>
 <p class="note">{icon("alert")}<span>التحقق من مادة لا يثبت المسؤولية الفردية لأحد.</span></p>
 <h2 class="h2">التحليل القانوني الأولي</h2>
 <ol class="sheet legal-list">{legal_rows}</ol>
 <p class="note">{icon("scale")}<span>تحليل بحثي أولي، وليس حكما قضائيا.</span></p>
 <h2 class="h2">المسؤولية الفردية</h2>
 <div class="prose">{resp}</div>
 <h2 class="h2">المصادر</h2>
 {B.sources_list(inc.get("sources", []))}
 <div class="sheet custody-sheet">{B.custody(inc["id"], B.default_custody("incident"))}</div>
 {cite_block(rel, inc["id"], f'موثّق، «{inc["title_ar"]}»، سجل واقعة {inc["id"]}، {date_ar(inc["date"])}. اطُّلع عليه في 28 أكتوبر 2026.')}
</div></section>'''
    main = f'<div class="wrap">{S.crumbs(rel, [("أرشيف الوقائع", "incidents/index.html"), (inc["title_ar"], None)])}</div>' + record(rel, incident_tag(inc, rel, actions=False), side, below,
                                                                                                                       stamp(inc['id'], B.state_of(inc['id']), (('الأدلة', len(evs)), ('المصادر', len(inc.get('sources', []))), ('القواعد', len(rules)), ('الأشخاص', len(persons)))))
    P(rel, f'incidents/{slug(inc["id"])}.html', inc['title_ar'], inc.get('summary_ar', '')[:150], 'incidents', main)


def evidence_pages():
    rel = '../'
    items = ''.join(B.ev_row(e, rel) for e in B.EVIDENCE)
    types = [(k, v[0]) for k, v in B.EV_KIND.items() if any(e.get('type') == k for e in B.EVIDENCE)]
    states = [(k, VERIF[k][0]) for k in VERIF if any(B.ev_state(e) == k for e in B.EVIDENCE)]
    list_page(rel, 'evidence/index.html', 'evidence', 'سجل الأدلة',
              'كل مادة بمصدرها وحدودها وحالة التحقق منها، وبصمة تطابقها بنفسك.',
              q_field('وصف أو واقعة') + sel('ft', 'نوع المادة', 'type', types), items, 'ev-list',
              fac=facet('state', 'حالة التحقق', [(k, v, seal(k, label=False), sum(B.ev_state(e) == k for e in B.EVIDENCE)) for k, v in states]),
              card=archive_card(len(B.EVIDENCE), 'مادة', id_range([e['id'] for e in B.EVIDENCE]),
                                (('وقائع', len({e['incident'] for e in B.EVIDENCE})), ('بصمة محفوظة', sum(1 for e in B.EVIDENCE if B.EV_PHOTO.get(e['id']) in B.PHOTO_SIZE)))))
    for e in B.EVIDENCE:
        evidence_page(e)


def lead_of(text, limit=320):
    """The opening of a summary, cut at the end of a sentence."""
    if len(text) <= limit:
        return text
    cut = text.rfind('. ', 0, limit)
    return text[:cut + 1] if cut > 80 else text[:limit].rsplit(' ', 1)[0] + '…'


def evidence_page(ev):
    rel = '../'
    inc = B.INC_BY_ID[ev['incident']]
    kind, _ = B.EV_KIND.get(ev.get('type'), ('مادة', 'doc'))
    ph = B.EV_PHOTO.get(ev['id'])
    ph = ph if ph in B.PHOTO_SIZE else None
    h = B.sha(ph) if ph else None
    rules = [B.RULE_BY_ID[r] for r in inc['rule_ids'] if r in B.RULE_BY_ID]
    siblings = [B.EV_BY_ID[e] for e in inc['ev_ids'] if e != ev['id']]
    docs = [d for d in B.DOCS if inc['id'] in d['inc_ids']]
    side = side_list('الواقعة', [B.inc_mini_row(inc, rel)]) + side_list('القواعد ذات الصلة', [B.rule_row(r, rel) for r in rules[:4]])
    verify = ''
    if h:
        verify = f'''<h2 class="h2" id="verify">افحص سلامة الختم بنفسك</h2>
 <div class="verify" data-verify="{h}">
  <div class="verify-seal" data-verify-seal><svg class="seal is-wax" viewBox="0 0 40 40" aria-hidden="true"><use href="#s-whole"/></svg></div>
  <div class="verify-body">
   <p>حُفظت من هذه المادة نسخة مرجعية على المنصة، وسُجّلت بصمتها الرقمية. نزّل النسخة، ثم أفلتها هنا أو اخترها، وتُحسب بصمتها على جهازك دون رفعها إلى أي مكان.</p>
   <dl class="fields"><div><dt>البصمة الرقمية المسجلة</dt><dd><span class="mono hash">{h}</span></dd></div></dl>
   <div class="verify-actions"><a class="btn btn-line btn-sm" href="{rel}assets/img/photo/{ph}.webp" download>{icon("download")} نزّل النسخة المحفوظة</a>
   <button class="btn btn-line btn-sm" type="button" data-copy="{h}" data-done="نُسخت البصمة.">{icon("doc")} انسخ البصمة</button></div>
   <label class="drop">{icon("upload")}<span><b>أفلت الملف هنا</b> أو اضغط لاختياره</span><input type="file" class="sr"></label>
   <p class="verify-out" data-verify-out aria-live="polite"></p>
  </div>
 </div>'''
    below = f'''<section class="sec record-body"><div class="wrap read">
 {B.photo_fig(ph, rel, sizes="(min-width: 1024px) 760px, 100vw") if ph else ""}
 <h2 class="h2">السياق</h2>
 <div class="prose"><p>المادة من سجل <a href="{rel}incidents/{slug(inc["id"])}.html">«{esc(inc["title_ar"])}»</a>، {esc(inc.get("place_ar", ""))}، {esc(date_ar(inc["date"]))}.</p>
 <p>{esc(lead_of(inc.get("summary_ar", "")))}</p></div>
 <h2 class="h2">القيود المعروفة</h2>
 <div class="prose"><p>{esc(B.EV_LIMIT.get(ev.get("type"), "تُذكر قيود المادة عند مراجعتها."))}</p></div>
 {verify}
 {f'<h2 class="h2">أدلة أخرى في السجل نفسه ({len(siblings)})</h2><ul class="rows">{"".join(B.ev_row(e, rel) for e in siblings)}</ul>' if siblings else ""}
 {f'<h2 class="h2">وثائق تتناول الواقعة ({len(docs)})</h2><ul class="rows">{"".join(B.doc_row(d, rel) for d in docs)}</ul>' if docs else ""}
 <div class="sheet custody-sheet">{B.custody(ev["id"], B.default_custody("evidence")).replace("سجل العهدة", "سلسلة الحيازة")}</div>
 {cite_block(rel, ev["id"], f'موثّق، «{ev.get("desc_ar", "")}»، دليل {ev["id"]} ضمن سجل {inc["id"]}. اطُّلع عليه في 28 أكتوبر 2026.')}
</div></section>'''
    main = f'<div class="wrap">{S.crumbs(rel, [("سجل الأدلة", "evidence/index.html"), (ev["id"], None)])}</div>' + record(rel, evidence_tag(ev, rel), side, below,
                                                                                                                stamp(ev['id'], B.ev_state(ev), (('القواعد', len(rules)),), f'<p class="stamp-status">{esc(kind)} · ضمن {esc(inc["id"])}</p>'))
    P(rel, f'evidence/{slug(ev["id"])}.html', f'{kind}: {ev.get("desc_ar", "")}'[:90], ev.get('desc_ar', ''), 'evidence', main)


def reports_pages():
    rel = '../'
    docs = sorted(B.DOCS, key=lambda d: d.get('date', ''), reverse=True)
    cats = [(k, v) for k, v in B.DOC_CAT.items() if any(d.get('cat') == k for d in docs)]
    years = sorted({d.get('date', '')[:4] for d in docs}, reverse=True)
    list_page(rel, 'reports/index.html', 'reports', 'التقارير والوثائق',
              'وثائق قضائية وأممية وحقوقية، كل منها بطبيعته القانونية.',
              q_field('عنوان أو جهة') + sel('fy', 'السنة', 'year', [(y, y) for y in years]),
              ''.join(B.doc_row(d, rel) for d in docs), 'doc-list',
              fac=facet('cat', 'نوع الجهة', [(k, v, '', sum(d.get('cat') == k for d in docs)) for k, v in cats]),
              card=archive_card(len(docs), 'وثيقة', id_range([d['id'] for d in docs]),
                                (('جهات', len({d.get('publisher_ar') for d in docs})), ('وقائع مرتبطة', len({i for d in docs for i in d['inc_ids']})))))
    for d in B.DOCS:
        report_page(d)


def report_page(d):
    rel = '../'
    persons = [B.P_BY_ID[p] for p in d.get('persons', []) if p in B.P_BY_ID]
    rules = [B.RULE_BY_ID[r] for r in d['rule_ids'] if r in B.RULE_BY_ID]
    incs = [B.INC_BY_ID[i] for i in d['inc_ids'] if i in B.INC_BY_ID]
    side = (side_list('الأشخاص', [person_row(p, rel) for p in persons]) +
            side_list('الوقائع', [B.inc_mini_row(i, rel) for i in incs]) + side_list('القواعد', [B.rule_row(r, rel) for r in rules]))
    findings = ''.join(f'<li>{esc(f)}</li>' for f in d.get('findings_ar', []))
    tag = doc_tag(d, rel, actions=False).replace('<p class="tag-status', '<h1 class="tag-status', 1).replace('</p>\n  <p class="tag-by', '</h1>\n  <p class="tag-by', 1)
    links = ' '.join(x for x in [ext(d['url'], 'النص الرسمي', 'btn btn-line btn-sm') if d.get('url') else '',
                                 ext(d['url_ar'], 'النسخة العربية', 'btn btn-line btn-sm') if d.get('url_ar') else ''] if x)
    ph = B.photo_of(d['id'])
    below = f'''<section class="sec record-body"><div class="wrap read">
 {B.photo_fig(ph, rel, sizes="(min-width: 1024px) 760px, 100vw") if ph else ""}
 <h2 class="h2">ماذا تقول الوثيقة</h2>
 <div class="prose"><p>{esc(d.get("summary_ar", ""))}</p>{f"<ul>{findings}</ul>" if findings else ""}</div>
 <div class="link-row">{links}</div>
 {('<p class="note">' + icon("alert") + '<span>بعض عناصر هذا السجل، كالتاريخ، تقوم على مصدر واحد غير رسمي؛ يراجع قبل الاعتماد عليه.</span></p>') if d.get('uncertain') else ''}
 {'' if d.get('url_ar') else '<p class="note is-quiet">' + icon("doc") + '<span>النص الكامل بالعربية يضاف بعد اعتماد ترجمة مراجعة؛ حتى ذلك الحين يرجع إلى النص الرسمي.</span></p>'}
 {('<h2 class="h2">المصادر</h2><ol class="sources">' + ''.join(f'<li><span class="n">[{n}]</span><span>{ext(s["url"], esc(s.get("publisher", "")))}<small>{esc(date_ar(s.get("date")))}</small></span></li>' for n, s in enumerate(d['sources_extra'], 1)) + '</ol>') if d.get('sources_extra') else ''}
 <h2 class="h2">كيف تُقرأ هذه الوثيقة</h2>
 <p class="note">{icon("scale")}<span>{esc(d.get("nature_ar", ""))}. نميز بين ما تثبته الوثيقة وما ترجحه وما تنقله.</span></p>
 <div class="sheet custody-sheet">{B.custody(d["id"], B.default_custody("doc"))}</div>
 {cite_block(rel, d["id"], f'{d.get("publisher_ar", "")}، «{d.get("title_ar", "")}»، {date_ar(d.get("date"))}{"، " + d["symbol"] if d.get("symbol") else ""}. محفوظة في موثّق برقم {d["id"]}.')}
</div></section>'''
    card = stamp(d['id'], None, (('الوقائع', len(incs)), ('الأشخاص', len(persons)), ('القواعد', len(rules))), f'<p class="stamp-status">{esc(B.DOC_CAT.get(d.get("cat"), ""))}</p>')
    main = f'<div class="wrap">{S.crumbs(rel, [("التقارير والوثائق", "reports/index.html"), (d.get("title_ar", ""), None)])}</div>' + record(rel, tag, side, below, card)
    P(rel, f'reports/{slug(d["id"])}.html', d.get('title_ar', ''), d.get('summary_ar', '')[:150], 'reports', main)


def law_pages():
    rel = '../'
    branches = [(k, v) for k, v in B.BRANCH.items() if any(r.get('branch') == k for r in B.RULES)]
    list_page(rel, 'law/index.html', 'law', 'مكتبة القواعد القانونية',
              'النص الرسمي لكل مادة، وصياغة موجزة، وما يلزم إثباته.',
              q_field('مادة أو موضوع'), ''.join(B.rule_row(r, rel) for r in B.RULES), 'rule-list',
              fac=facet('branch', 'فرع القانون', [(k, v, '', sum(r.get('branch') == k for r in B.RULES)) for k, v in branches]),
              card=archive_card(len(B.RULES), 'مادة وقاعدة', counts=(('صكوك', len({r.get('instrument_ar') for r in B.RULES})), ('مرتبطة بوقائع', sum(1 for r in B.RULES if r['inc_ids'])))))
    for r in B.RULES:
        rule_page(r)


NO_AR = 'لا يوجد نص عربي رسمي لهذه المادة؛ النص ذو الحجية بلغة الاتفاقية الأصلية، والصياغة أعلاه للإيضاح.'


def rule_page(r):
    rel = '../'
    incs = [B.INC_BY_ID[i] for i in r['inc_ids']]
    docs = [B.DOC_BY_ID[d] for d in r['doc_ids']]
    persons = [B.P_BY_ID[p] for p in r['p_ids']]
    prove = []
    for i in incs:
        for L in i.get('legal', []):
            if r['id'] in L.get('ids', []) and L.get('to_prove_ar'):
                prove.append((i, L['to_prove_ar']))
    # other articles of the same instrument, for moving along the text (not a link between records, so no cord)
    kin = [x for x in B.RULES if x.get('instrument_ar') == r.get('instrument_ar') and x['id'] != r['id']]
    side = (side_list('الأشخاص', [person_row(p, rel) for p in persons], dup=not incs) + side_list('الوقائع', [B.inc_mini_row(i, rel) for i in incs], dup=True) +
            side_list('الوثائق', [B.doc_row(d, rel) for d in docs]) + side_list('من الصك نفسه', [B.rule_row(x, rel).replace(f' data-cord-to="{x["id"]}"', '') for x in kin[:5]]))
    tag = f'''<article class="tag is-reversed"{B.vt(r["id"])} aria-label="قاعدة قانونية">
  <span class="tag-hole" aria-hidden="true"></span>
  <div class="tag-top"><span class="tag-no">{esc(B.rule_short(r))}</span><span class="tag-kind">{esc(B.BRANCH.get(r.get("branch"), ""))}</span></div>
  <div class="tag-seal" data-cord-from>{S.wax("complete")}</div>
  <p class="tag-by open-1">{esc(r.get("instrument_ar", ""))}</p>
  <h1 class="tag-status open-1">{esc(r.get("article_ar", ""))}</h1>
  <div class="tag-name open-2"><b>{esc(r.get("title_ar", ""))}</b></div>
  <p class="tag-not open-3{" is-long" if len(r.get("applies_note_ar") or "") > 160 else ""}">{S.icon("info")}<span>{esc(r.get("applies_note_ar") or "يُرجع دائمًا إلى النص الرسمي؛ الصياغة الموجزة هنا للإيضاح.")}</span></p>
</article>'''
    chapeau = f'<p class="chapeau">{esc(r["chapeau_ar"])}</p>' if r.get('chapeau_ar') else ''
    body = ''.join(f'<p>{esc(line)}</p>' for line in (r.get('text_ar') or '').splitlines() if line.strip())
    defin = (f'<p class="definition"><b>{esc(r.get("definition_ref_ar") or "تعريف مرتبط")}:</b> {esc(r["definition_ar"])}</p>' if r.get('definition_ar') else '')
    text = (f'<blockquote class="official">{chapeau}{body}{defin}<footer>{esc(r.get("instrument_ar", ""))}، {esc(r.get("article_ar_official") or r.get("article_ar", ""))} — النص الرسمي. {esc(re.sub(r"\s*\([^()]*[A-Za-z][^()]*\)", "", r.get("text_source", "")))}</footer></blockquote>'
            if r.get('text_ar') else (f'<blockquote class="official"><p>{esc(r.get("paraphrase_ar", ""))}</p><footer>{esc(r.get("instrument_ar", ""))}، {esc(r.get("article_ar", ""))} — صياغة موجزة؛ لا يوجد نص عربي رسمي لهذه المادة، والنص الرسمي بلغتي الاتفاقية الأصليتين.</footer></blockquote>' if r.get('text_en') else '') + f'<p class="note">{icon("info")}<span>{esc(NO_AR if re.search("[a-z]_[a-z]", r.get("note") or "") else (r.get("note") or "لم يدرج النص الرسمي العربي في هذا النموذج؛ راجع الرابط الرسمي."))}</span></p>')
    prove_html = ''.join(f'<li><a href="{rel}incidents/{slug(i["id"])}.html">{esc(i["title_ar"])}</a><p class="small">{esc(t)}</p></li>' for i, t in prove)
    below = f'''<section class="sec record-body"><div class="wrap read">
 <h2 class="h2">النص</h2>
 {text}
 <div class="link-row">{ext(r["url"], "النص الرسمي", "btn btn-line btn-sm") if r.get("url") else ""} {ext(r["url_en"], "النص بلغته الأصلية", "btn btn-line btn-sm") if r.get("url_en") else ""}</div>
 <h2 class="h2">بصياغة موجزة</h2>
 <div class="prose"><p>{esc(r.get("paraphrase_ar", ""))}</p></div>
 {f'<h2 class="h2">ما يلزم إثباته في الوقائع المرتبطة</h2><ul class="prove">{prove_html}</ul>' if prove_html else ''}
 {f'<h2 class="h2">الوقائع المرتبطة ({len(incs)})</h2><ul class="rows">{"".join(B.inc_mini_row(i, rel) for i in incs)}</ul>' if incs else ''}
 {f'<h2 class="h2">الأشخاص المرتبطون ({len(persons)})</h2><p class="small mute">ربطت وثيقة رسمية وضعهم القانوني بهذه المادة؛ الربط لا يعني ثبوت المسؤولية.</p><ul class="rows">{"".join(person_row(p, rel).replace(f' data-cord-to="{p["id"]}"', '') for p in persons)}</ul>' if persons else ''}
 {'' if incs or persons else '<h2 class="h2">الوقائع المرتبطة</h2><p class="small mute">لا وقائع مرتبطة بهذه المادة في النموذج بعد.</p>'}
{cite_block(rel, r["id"], f'{r.get("instrument_ar", "")}، {r.get("article_ar_official") or r.get("article_ar", "")}: «{r.get("title_ar", "")}». في مكتبة قواعد موثّق.')}
</div></section>'''
    card = stamp(B.rule_short(r), None, (('الوقائع', len(incs)), ('الوثائق', len(docs)), ('الأشخاص', len(persons))), f'<p class="stamp-status">{esc(B.BRANCH.get(r.get("branch"), ""))}</p>')
    main = f'<div class="wrap">{S.crumbs(rel, [("مكتبة القواعد", "law/index.html"), (r.get("article_ar", ""), None)])}</div>' + record(rel, tag, side, below, card)
    P(rel, f'law/{slug(r["id"])}.html', f'{r.get("article_ar", "")}: {r.get("title_ar", "")}', r.get('paraphrase_ar', ''), 'law', main)


def build():
    n = B.write_json_index()
    home()
    people_pages()
    incidents_pages()
    evidence_pages()
    reports_pages()
    law_pages()
    import more
    more.build()
    print('index', n, '| persons', len(B.PERSONS), 'incidents', len(B.INCIDENTS), 'evidence', len(B.EVIDENCE),
          'docs', len(B.DOCS), 'rules', len(B.RULES))
