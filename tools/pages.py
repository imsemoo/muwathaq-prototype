"""Page templates for every route. Called by build.py; never hand-edit the built HTML."""
import os

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
  <h1 class="tag-title open-1">{esc(inc["title_ar"])}</h1>
  <p class="tag-by open-1">{icon("cal")} {esc(date_ar(inc["date"]))}{(" — " + esc(date_ar(inc["date_to"]))) if inc.get("date_to") else ""} · {icon("pin")} {esc(inc.get("place_ar", ""))}</p>
  <dl class="fields open-2">
   <div><dt>حالة التحقق</dt><dd>{seal_row(st)}</dd></div>
   <div><dt>دقة الموقع</dt><dd>{precise}{(" — " + esc(inc["loc_note_ar"])) if inc.get("loc_note_ar") else ""}</dd></div>
   <div><dt>نوع الواقعة</dt><dd>{esc("، ".join(inc.get("type_ar", [])) or "—")}</dd></div>
   <div><dt>الحصيلة كما وردت</dt><dd>{esc(toll)}</dd></div>
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
  <p class="tag-en open-2" lang="en" dir="ltr">{esc(d.get("title_en", ""))}</p>
  <dl class="fields open-3">
   <div><dt>رمز الوثيقة</dt><dd>{mono(d.get("symbol") or "—")}</dd></div>
   <div><dt>الطبيعة القانونية</dt><dd>{esc(d.get("nature_ar", ""))}</dd></div>
   <div><dt>النطاق الزمني</dt><dd>{esc(d.get("period_ar") or "—")}</dd></div>
   <div><dt>سلامة النسخة</dt><dd>{seal_row("complete")}</dd></div>
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
  <h1 class="tag-title open-1">{esc(ev.get("desc_ar", ""))}</h1>
  <p class="tag-by open-1">{esc(ev.get("source", ""))} · {esc(date_ar(ev.get("date")))}</p>
  <dl class="fields open-2">
   <div><dt>حالة التحقق</dt><dd>{seal_row(st)}</dd></div>
   <div><dt>الواقعة</dt><dd><a href="{rel}incidents/{slug(inc["id"])}.html">{esc(inc["title_ar"])}</a></dd></div>
   <div><dt>نوع المادة</dt><dd>{esc(kind)}</dd></div>
   <div><dt>المصدر الأصلي</dt><dd>{ext(ev["url"], "فتح المصدر") if ev.get("url") else "—"}</dd></div>
  </dl>
</article>'''


def side_list(title, items):
    if not items:
        return ''
    return f'<section class="side-group"><h2 class="side-h">{title} <span class="mono">{len(items)}</span></h2><ul class="rows rows-tight">{"".join(items)}</ul></section>'


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
def print_card(ev, rel):
    ph = B.EV_PHOTO.get(ev['id'])
    sz = B.PHOTO_SIZE[ph]
    p = B.PHOTOS[ph]
    inc = B.INC_BY_ID[ev['incident']]
    return f'''<article class="tag print" aria-label="دليل مصوّر">
  <span class="tag-hole" aria-hidden="true"></span>
  <div class="tag-top"><span class="tag-no">{esc(ev["id"])}</span><span class="tag-kind">دليل مصوّر</span></div>
  <div class="tag-seal" data-cord-from>{S.wax(B.ev_state(ev))}</div>
  <img class="print-img" src="{rel}assets/img/photo/{ph}-640.webp" alt="{esc(p.get("alt", ""))}" width="640" height="{round(640 * sz["h"] / sz["w"])}" loading="lazy" decoding="async">
  <p class="print-cap">{esc(p.get("caption_ar", ""))}</p>
  <p class="tag-by">{esc(p.get("author", ""))} · {esc(p.get("license", ""))} · ضمن سجل {esc(inc["id"])}</p>
  <div class="tag-actions"><a class="btn btn-light" href="{rel}evidence/{slug(ev["id"])}.html">افتح الحرز {icon("arrow")}</a><a class="btn btn-ghost" href="{rel}evidence/{slug(ev["id"])}.html#verify">افحص الختم</a></div>
</article>'''


def law_card(r, rel):
    text = (r.get('paraphrase_ar') or r.get('text_ar') or '').splitlines()[0]
    if len(text) > 190:
        text = text[:186].rsplit(' ', 1)[0] + '…'
    return f'''<article class="tag lawcard" aria-label="مادة قانونية">
  <span class="tag-hole" aria-hidden="true"></span>
  <div class="tag-top"><span class="tag-no">{esc(r.get("article_en", ""))}</span><span class="tag-kind">{esc(B.BRANCH.get(r.get("branch"), ""))}</span></div>
  <div class="tag-seal" data-cord-from>{S.wax("complete")}</div>
  <p class="tag-by">{esc(r.get("instrument_ar", ""))}</p>
  <p class="tag-status">{esc(r.get("article_ar", ""))}</p>
  <div class="tag-name"><b>{esc(r.get("title_ar", ""))}</b></div>
  <blockquote class="law-quote">{esc(text)}</blockquote>
  <div class="tag-actions"><a class="btn btn-light" href="{rel}law/{slug(r["id"])}.html">افتح المادة {icon("arrow")}</a></div>
</article>'''


def case_section(rel):
    """A real record reconstructed as the reader scrolls: the first account, the evidence that contradicted it,
    what changed after, the rules engaged. Every line comes from INC-0012 and its sources."""
    inc = B.INC_BY_ID.get(B.PICKS.get('home', {}).get('case', 'INC-0012'))
    if not inc:
        return ''
    R = lambda rid: B.RULE_BY_ID.get(rid)
    rules = [r for r in (R('RS-8-2-b-xxiv'), R('RS-8-2-b-iii'), R('GCIV-147')) if r]
    steps = [
        ('in_progress', '23 مارس 2025، فجرا، قرب تل السلطان في رفح',
         'أطلقت النار على سيارة إسعاف للهلال الأحمر الفلسطيني، ثم على قافلة إنقاذ وصلت إليها. قتل 15: ثمانية من الهلال الأحمر، وستة من الدفاع المدني، وموظف في الأونروا، بحسب الأمم المتحدة. ولم يسمح بالوصول إلى الموقع إلا بعد خمسة أيام.',
         'أوتشا وأخبار الأمم المتحدة، 1 أبريل 2025'),
        ('in_progress', 'الرواية الأولى',
         'قال الجيش الإسرائيلي إن المركبات «تقدمت بشكل مريب» دون أضواء أو إشارات طوارئ.',
         'بيانات الجيش كما نقلتها CNN وتايمز أوف إسرائيل'),
        ('rereview', 'الدليل',
         'في هاتف المسعف رفعت رضوان مقطع مدته نحو ست دقائق صوّره من داخل القافلة. نشر في 5 أبريل 2025، ويظهر المركبات تضيء أنوارها وإشاراتها لحظة إطلاق النار.',
         'نيويورك تايمز وCNN، 5 أبريل 2025'),
        ('specific', 'ما تغيّر بعد الدليل',
         'أقر الجيش بأن روايته الأولى غير دقيقة، وخلص تحقيقه في 20 أبريل 2025 إلى «إخفاقات مهنية». وفي 23 فبراير 2026 وثّق تحليل صوتي أعدته Earshot وForensic Architecture 910 طلقات على الأقل خلال أكثر من ساعتين.',
         'CNN وتايمز أوف إسرائيل؛ تقرير Earshot وForensic Architecture'),
        ('specific', 'القواعد التي قد تنطبق',
         'الهجوم على مستعملي الشارات المميزة، والهجوم على موظفي المساعدة الإنسانية، والمخالفات الجسيمة لاتفاقية جنيف الرابعة. يلزم إثبات العلم بالصفة المحمية وقصد الهجوم قبل أي استنتاج.',
         'تحليل بحثي أولي، ليس حكما'),
        ('specific', 'الحرز ما زال مفتوحا',
         'في 19 أغسطس 2026 أعلن الجيش فتح تحقيق جنائي لدى الشرطة العسكرية. كل تحديث يضاف إلى سجل العهدة بتاريخه، ولا تمحى الرواية الأولى.',
         'بحسب ما نقلته الصحافة الإسرائيلية والدولية'),
    ]
    lis = ''.join(f'<li class="case-step{" is-on" if n == 0 else ""}" data-step="{n}"><span class="cs-k" aria-hidden="true">{seal(st, label=False)}</span><div><h3>{esc(h)}</h3><p>{esc(t)}</p><p class="src">{esc(src)}</p></div></li>'
                  for n, (st, h, t, src) in enumerate(steps))
    rule_cards = ''.join(f'<div class="cs-card cs-rule r{n}" data-in="4"><span class="tag-hole" aria-hidden="true"></span><p class="mono">{esc(r.get("article_en", ""))}</p><b>{esc(r.get("title_ar", ""))}</b><small>{esc(r.get("instrument_ar", "").split(" (")[0])}</small></div>'
                         for n, r in enumerate(rules))
    views = ''.join(f'<div class="kd-view cs-view{" is-on" if k == "in_progress" else ""}" data-state-view="{k}">{S.wax(k, cls="wax")}</div>' for k in ('in_progress', 'rereview', 'specific'))
    return f'''<section class="case" data-case aria-labelledby="case-h">
 <div class="case-pin">
  <div class="wrap case-grid">
   <div class="case-text">
    <h2 class="h2" id="case-h">حرز واقعة: كيف تتغير الرواية أمام الدليل</h2>
    <p class="case-lead">سجل حقيقي من الأرشيف، كما يُبنى في موثّق خطوة بخطوة. مرّر لتتابعه.</p>
    <ol class="case-steps">{lis}</ol>
    <a class="link-arrow case-cta" href="{rel}incidents/{slug(inc["id"])}.html">افتح حرز الواقعة كاملا {icon("arrow")}</a>
   </div>
   <div class="case-stage" aria-hidden="true">
    <svg class="cs-cords" viewBox="0 0 100 100" preserveAspectRatio="none"><path class="c0" d="M50 30 Q38 70 26 86"/><path class="c1" d="M50 30 Q52 74 54 90"/><path class="c2" d="M50 30 Q66 70 80 86"/></svg>
    <div class="cs-card cs-inc" data-in="0"><span class="tag-hole" aria-hidden="true"></span><p class="mono">{esc(inc["id"])}</p><b>{esc(inc["title_ar"])}</b><small>{esc(date_ar(inc["date"]))} · {esc(inc.get("place_ar", ""))}</small></div>
    <div class="cs-seal">{views}</div>
    <div class="cs-card cs-off" data-in="1"><p class="cs-lab">{icon("official")} بيان رسمي · الرواية الأولى</p><q>تقدمت المركبات بشكل مريب دون أضواء أو إشارات طوارئ</q></div>
    <div class="cs-seam" data-in="2"></div>
    <div class="cs-card cs-vid" data-in="2"><p class="cs-lab">{icon("video")} مقطع فيديو · 5 أبريل 2025</p><p class="cs-num"><b>6</b> دقائق صوّرت من داخل القافلة</p><q>الأنوار والإشارات مضاءة لحظة إطلاق النار</q></div>
    <div class="cs-card cs-idf" data-in="3"><p class="cs-lab">{icon("doc")} تحقيق الجيش · 20 أبريل 2025</p><q>إخفاقات مهنية</q></div>
    <div class="cs-card cs-fa" data-in="3"><p class="cs-lab">{icon("sat")} تحليل صوتي · 23 فبراير 2026</p><p class="cs-num"><b>910</b> طلقات على الأقل</p><small>Earshot و Forensic Architecture</small></div>
    {rule_cards}
   </div>
  </div>
 </div>
</section>'''


def home():
    rel = ''
    feat = B.PICKS.get('home', {})
    p0 = B.P_BY_ID.get(feat.get('person', 'P-0001')) or (B.PERSONS[0] if B.PERSONS else None)
    i0 = B.INC_BY_ID.get(feat.get('incident')) or (B.INCIDENTS[0] if B.INCIDENTS else None)
    d0 = B.DOC_BY_ID.get(feat.get('doc')) or (B.DOCS[0] if B.DOCS else None)
    hint_rule = B.PICKS.get('home', {}).get('hint_rule', 'RS-8-2-b-xxv')
    hr = B.RULE_BY_ID.get(hint_rule)
    # the exhibits laid on the table: each a real record, each tied to the lead seal by a cord
    ev_print = next((e for e in B.EVIDENCE if B.EV_PHOTO.get(e['id']) in B.PHOTO_SIZE), None)
    exhibits = []
    if p0:
        exhibits.append(('person', 'ملف شخص', p0['name_ar'], f'people/{slug(p0["id"])}.html', B.person_tag(p0, rel)))
    if i0:
        exhibits.append(('incident', 'واقعة', i0['title_ar'], f'incidents/{slug(i0["id"])}.html',
                         incident_tag(i0, rel).replace('<h1 class="tag-title', '<h2 class="tag-title').replace('</h1>', '</h2>')))
    if d0:
        exhibits.append(('doc', 'وثيقة', d0.get('title_ar', ''), f'reports/{slug(d0["id"])}.html', doc_tag(d0, rel)))
    if ev_print:
        exhibits.append(('print', 'دليل مصوّر', ev_print.get('desc_ar', ''), f'evidence/{slug(ev_print["id"])}.html', print_card(ev_print, rel)))
    if hr:
        exhibits.append(('law', 'مادة قانونية', hr.get('title_ar', ''), f'law/{slug(hr["id"])}.html', law_card(hr, rel)))
    pile = ''
    for n, (k, kind, label, href, body) in enumerate(exhibits):
        if n:
            body = body.replace('class="tag is-reversed"', 'class="tag"', 1)
        pick = '' if n == 0 else f'<a class="ex-pick" href="{href}" data-pick><span class="sr">اعرض على الطاولة: {esc(kind)} — {esc(label)}</span></a>'
        pile += f'<div class="ex" data-slot="{n}" data-kind="{k}" id="ex-{k}"><div class="ex-in">{body}</div>{pick}</div>'
    tabs = ''.join(f'<button type="button" role="tab" aria-selected="{"true" if n == 0 else "false"}" tabindex="{0 if n == 0 else -1}" data-tab="{n}">{kind}</button>'
                   for n, (k, kind, *_r) in enumerate(exhibits))
    hints = [f'<a href="people/{slug(p0["id"])}.html"><span class="mono">{p0["id"]}</span></a>' if p0 else '',
             f'<a href="law/{slug(hr["id"])}.html">{esc(hr["article_ar"])}</a>' if hr else '',
             '<a href="search.html?q=%D8%B1%D9%81%D8%AD">رفح</a>', '<a href="reports/index.html">محكمة العدل الدولية</a>']
    hero = f'''<section class="hero table" data-table>
 <div class="wrap hero-grid">
  <div class="hero-side">
   <h1 class="hero-h" data-lines><span class="ln"><span>كل معلومة هنا حرز:</span></span> <span class="ln"><span>مختومة بمصدرها،</span></span> <span class="ln"><span>ومفتوحة للفحص.</span></span></h1>
   <p class="lead">منصة مستقلة لتوثيق الوقائع والأدلة المتعلقة بجرائم الاحتلال الإسرائيلي، والتحقق من مصادرها، وربطها بالقانون الدولي.</p>
   <form class="find find-hero" role="search" action="search.html" data-find="hero">
    <label class="sr" for="q-hero">ابحث في الملفات والوقائع والوثائق والقواعد</label>
    <input id="q-hero" name="q" type="search" placeholder="ابحث باسم، رقم ملف، أو مادة قانونية" autocomplete="off" role="combobox" aria-expanded="false" aria-controls="ql-hero" aria-autocomplete="list">
    {icon("search")}<button class="btn btn-ink" type="submit">بحث</button>
    <div class="find-list" id="ql-hero" role="listbox" hidden></div>
   </form>
   <p class="hints">جرّب: {" · ".join(h for h in hints if h)}</p>
   <p class="pick-hint">{icon("hand")}<span>على الطاولة {len(exhibits)} أحراز حقيقية مربوطة ببعضها. اضغط أيًا منها ليُفتح أمامك.</span></p>
  </div>
  <div class="hero-stage">
   <div class="seg pile-tabs" role="tablist" aria-label="الأحراز على الطاولة">{tabs}</div>
   <div class="pile" data-pile>
    <canvas class="pile-cords" aria-hidden="true"></canvas>
    {pile}
   </div>
  </div>
 </div>
</section>'''
    key = ''.join(f'<li data-state="{k}" tabindex="0"{" class=\"is-on\"" if k == "complete" else ""}>{seal(k, label=False)}<span><b>{esc(v[0])}</b><small>{esc(v[2])}</small></span></li>' for k, v in VERIF.items())
    views = ''.join(f'<div class="kd-view{" is-on" if k == "complete" else ""}" data-state-view="{k}">{S.wax(k, cls="wax kd-wax")}</div>' for k in VERIF)
    steps5 = ''.join(f'<li><b>{esc(lab)}</b><span>{esc(d)}</span></li>' for lab, d in [
        ('ادعاءات', 'روايات لم تُستكمل مراجعتها.'), ('تقرير أو إجراء', 'ورود في تحقيق أممي أو تقرير موثق أو قرار عقوبات حكومي.'),
        ('اتهام رسمي', 'لائحة اتهام من جهة ادعاء مختصة.'), ('مذكرة توقيف', 'قرار قضائي بالتوقيف، وليس حكمًا.'), ('حكم إدانة', 'حكم نهائي من محكمة مختصة.')])
    read = f'''<section class="sec">
 <div class="wrap">
  <div class="sheet read-key">
   <div class="read-key-head"><h2 class="h2">كيف تقرأ أي ملف هنا</h2><p class="lead">الختم يقول إلى أي حد تحققنا من المادة، والعُقد تقول أين يقف الشخص في المسار القضائي. المساران منفصلان دائمًا: اكتمال التحقق من مادة لا يعني ثبوت مسؤولية أحد.</p></div>
   <div class="read-key-grid">
    <div><h3 class="h3">أختام التحقق</h3><div class="key-wrap"><div class="key-demo" data-key-demo aria-hidden="true">{views}<p data-key-label>مكتمل وفق المنهجية</p></div><ul class="seal-key">{key}</ul></div></div>
    <div><h3 class="h3">عُقد المسار القضائي</h3><div class="knots-demo">{knots("warrant")}<p class="knots-note">مثال: مذكرة توقيف هي العقدة الرابعة من خمس؛ الحكم لم يصدر.</p></div><ol class="ladder">{steps5}</ol></div>
   </div>
  </div>
 </div>
</section>'''
    incs = sorted(B.INCIDENTS, key=lambda i: i['date'], reverse=True)
    lead_inc = B.INC_BY_ID.get(feat.get('feature_incident')) or next((i for i in incs if B.photo_of(i['id'])), incs[0] if incs else None)
    feature = ''
    if lead_inc:
        ph = B.photo_of(lead_inc['id'])
        feature = f'''<article class="feature">
      {B.photo_fig(ph, rel, sizes="(min-width: 1024px) 46vw, 100vw") if ph else ""}
      <div class="feature-body"><p class="tag-kind"><span class="mono">{lead_inc["id"]}</span> · {esc(REGIONS.get(lead_inc.get("region"), ""))}</p>
      <h3 class="h3"><a href="incidents/{slug(lead_inc["id"])}.html">{esc(lead_inc["title_ar"])}</a></h3>
      <p class="small mute">{esc(date_ar(lead_inc["date"]))} · {esc(lead_inc.get("place_ar", ""))}</p>
      <p class="small">{esc(lead_inc.get("summary_ar", ""))}</p>
      <p>{seal_row(B.state_of(lead_inc["id"]))}</p></div></article>'''
    rows = ''.join(B.inc_mini_row(i, rel) for i in incs if not lead_inc or i['id'] != lead_inc['id'])
    incidents = f'''<section class="sec">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2">وقائع موثقة</h2><p>لكل واقعة سجل مستقل: الروايات، والأدلة وحالة كل منها، والقواعد التي قد تنطبق وما يلزم إثباته.</p></div><a class="link-arrow" href="incidents/index.html">أرشيف الوقائع ({len(B.INCIDENTS)}) {icon("arrow")}</a></div>
  <div class="inc-feature">{feature}<ul class="rows rows-5">{"".join(rows.split("</li>")[i] + "</li>" for i in range(min(5, rows.count("</li>"))))}</ul></div>
 </div>
</section>'''
    minis = ''.join(f'<li>{B.person_mini(p, rel, vtn=p is not p0)}</li>' for p in B.PERSONS)
    people = f'''<section class="sec">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2">ملفات الأشخاص</h2><p>لا يُفتح ملف لشخص إلا بوضع قانوني رسمي قابل للاستشهاد. الحالة وجهتها وتاريخها قبل الاسم.</p></div><a class="link-arrow" href="people/index.html">كل الملفات ({len(B.PERSONS)}) {icon("arrow")}</a></div>
  <ul class="minis">{minis}</ul>
 </div>
</section>'''
    top_docs = sorted(B.DOCS, key=lambda d: d.get('date', ''), reverse=True)[:6]
    # the two lists stand side by side, so they hold the same number of rows
    top_rules = sorted(B.RULES, key=lambda r: len(r['inc_ids']), reverse=True)[:max(3, len(top_docs))]
    law = f'''<section class="sec">
 <div class="wrap two-lists">
  <div><div class="sec-head"><div><h2 class="h2">القواعد الأكثر ارتباطًا بالوقائع</h2><p>نص رسمي، وصياغة موجزة، وما يلزم إثباته قبل أي استنتاج.</p></div><a class="link-arrow" href="law/index.html">مكتبة القواعد {icon("arrow")}</a></div>
   <ul class="rows">{"".join(B.rule_row(r, rel) for r in top_rules)}</ul></div>
  <div><div class="sec-head"><div><h2 class="h2">أحدث الوثائق</h2><p>كل وثيقة بطبيعتها القانونية: أمر قضائي ليس حكمًا، وتقرير حقوقي ليس قرارًا.</p></div><a class="link-arrow" href="reports/index.html">مكتبة الوثائق {icon("arrow")}</a></div>
   <ul class="rows">{"".join(B.doc_row(d, rel) for d in top_docs)}</ul></div>
 </div>
</section>'''
    method_steps = ['جمع المادة', 'تسجيل المصدر والعهدة', 'الأصالة والسياق', 'المقارنة المستقلة', 'الموقع والزمن', 'توثيق القيود',
                    'المراجعة القانونية', 'حماية الأشخاص', 'قرار النشر', 'التصحيح المستمر']
    strip = ''.join(f'<li><i></i><span>{s}</span></li>' for s in method_steps)
    method = f'''<section class="sec sec-ink method-strip">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2">من المادة إلى الحرز: عشر خطوات</h2><p>لا تُختم مادة قبل أن تمر بكل عقدة على هذا الحبل، ولا تُنشر قبل حماية من قد يتعرضون للخطر بسببها.</p></div><a class="btn btn-light" href="method.html">المنهجية كاملة</a></div>
  <ol class="cord-steps">{strip}</ol>
 </div>
</section>'''
    act = f'''<section class="sec">
 <div class="wrap act-grid">
  <div class="sheet act">
   {seal("in_progress", label=False)}
   <h2 class="h2">أرسل مادة للمراجعة</h2>
   <p>لا ننشر شيئًا تلقائيًا. تمر كل مساهمة بفحص أولي، وتحقق رقمي، ومراجعة قانونية، وإخفاء للبيانات الحساسة قبل أي قرار بالنشر.</p>
   <p class="note is-quiet">{icon("shield")}<span>لا ترسل ما قد يعرّضك أو يعرّض الشهود أو الضحايا للخطر. في هذا النموذج لا تُرسل البيانات إلى أي خادم.</span></p>
   <a class="btn btn-ink" href="submit.html">ابدأ الإرسال</a>
  </div>
  <div class="sheet act">
   {seal("complete", label=False)}
   <h2 class="h2">ادعم التوثيق المستقل</h2>
   <p>تموّل المساهمات حفظ الأدلة، وأدوات التحقق الرقمي والجغرافي، والمراجعة القانونية، وحماية البيانات. تُنشر تقارير الشفافية المالية عند تفعيل التبرعات.</p>
   <p class="note is-quiet">{icon("lock")}<span>بوابة الدفع غير مفعّلة في هذا النموذج، ولا نعرض أرقام تمويل غير حقيقية.</span></p>
   <a class="btn btn-line" href="donate.html">طرق الدعم</a>
  </div>
 </div>
</section>'''
    tpl = f'<template id="intro-tpl">{S.wax("complete", label="موثّق")}<img class="intro-word" src="assets/brand/wordmark-reversed.svg" alt="" width="170" height="111"></template>'
    main = hero + case_section(rel) + read + incidents + people + law + method + act + tpl
    js = ''.join(f'<script src="assets/js/vendor/{f}?v={S.V}" defer></script>' for f in ('gsap.min.js', 'ScrollTrigger.min.js')) + f'<script src="assets/js/home.js?v={S.V}" defer></script>'
    P(rel, 'index.html', 'موثّق', 'منصة مستقلة لتوثيق الوقائع والأدلة المتعلقة بجرائم الاحتلال الإسرائيلي والتحقق منها وربطها بالقانون الدولي.', 'home', main, body_cls='page-home', scripts=js)


# ---------- lists ----------
def list_page(rel, path, active, title, lead, filters, items_html, list_id, extra='', cls='rows', before=''):
    main = f'''<div class="wrap">{S.crumbs(rel, [(title, None)])}</div>
<section class="list-head"><div class="wrap"><h1 class="h1">{esc(title)}</h1><p class="lead">{lead}</p>{before}</div></section>
<section class="sec list-sec"><div class="wrap">
 <form class="filters" data-filter="{list_id}" data-count="{list_id}-count" data-empty="{list_id}-empty" role="search" aria-label="تصفية {esc(title)}">{filters}<button class="btn btn-line btn-sm" type="reset">إعادة الضبط</button></form>
 <p class="count" id="{list_id}-count" aria-live="polite"></p>
 <ul class="{cls}" id="{list_id}">{items_html}</ul>
 <div class="empty" id="{list_id}-empty" hidden>{seal("not_started", label=False)}<p><b>لا توجد سجلات تطابق هذا البحث.</b> غيّر المرشحات أو امسحها.</p></div>
 {extra}
</div></section>'''
    P(rel, path, title, lead, active, main)


def q_field(placeholder):
    return f'<div class="field grow"><label for="fq">بحث</label><input class="input" id="fq" data-q type="search" placeholder="{placeholder}"></div>'


def sel(fid, label, key, options):
    opts = ''.join(f'<option value="{esc(v)}">{esc(t)}</option>' for v, t in options)
    return f'<div class="field"><label for="{fid}">{label}</label><select class="select" id="{fid}" data-key="{key}"><option value="">الكل</option>{opts}</select></div>'


def people_pages():
    rel = '../'
    items = ''.join(f'<li data-status="{p["status"]}" data-text="{esc(p["name_ar"] + " " + p.get("name_en", "") + " " + p.get("role_ar", ""))}">{B.person_mini(p, rel)}</li>' for p in B.PERSONS)
    statuses = [(k, STATUS[k][0]) for k in STATUS if any(p['status'] == k for p in B.PERSONS)]
    list_page(rel, 'people/index.html', 'people', 'ملفات الأشخاص',
              'ملفات لأشخاص لهم وضع قانوني رسمي قابل للاستشهاد: مذكرة توقيف، أو ورود في تحقيق أممي، أو قرار عقوبات حكومي. الحالة وجهتها وتاريخها تُقرأ قبل الاسم.',
              q_field('اسم أو منصب') + sel('fs', 'الوضع القانوني', 'status', statuses), items, 'people-list', cls='minis',
              extra=f'<p class="note" style="margin-top:28px">{icon("info")}<span>لا يُدرج موثّق شخصًا دون مصدر رسمي لوضعه القانوني، ولا يستخدم أوصافًا تجريمية عامة على البطاقات. لأي شخص معني حق طلب التصحيح أو الرد.</span></p>')
    for p in B.PERSONS:
        person_page(p)


def person_page(p):
    rel = '../'
    incs = [B.INC_BY_ID[i] for i in p['inc_ids']]
    docs = [B.DOC_BY_ID[d] for d in p['doc_ids']]
    rules = [B.RULE_BY_ID[r] for r in p['rule_ids'] if r in B.RULE_BY_ID]
    side = (side_list('الوقائع', [B.inc_mini_row(i, rel) for i in incs]) + side_list('الوثائق', [B.doc_row(d, rel) for d in docs]) +
            side_list('القواعد', [B.rule_row(r, rel) for r in rules])) or f'<p class="small mute">لا سجلات مرتبطة بعد.</p>'
    tag = B.person_tag(p, rel, actions=False).replace('<span class="tag-hole" aria-hidden="true"></span>', '<span class="tag-hole" aria-hidden="true"></span>', 1)
    tag = tag.replace('<p class="tag-status', '<h1 class="tag-status', 1).replace('</p>\n  <p class="tag-by', '</h1>\n  <p class="tag-by', 1)
    timeline = ''.join(f'''<li><span class="tl-date num">{esc(date_ar(s.get("date")))}</span><div class="tl-body"><p class="tl-kind">{esc(STATUS.get(s.get("type"), (s.get("type", ""),))[0] if s.get("type") in STATUS else ("قرار إجرائي" if s.get("type") == "procedural" else s.get("type", "")))}</p>
      <h3>{esc(s.get("doc_title_ar") or s.get("doc_title_en", ""))}</h3><p class="small mute">{esc(s.get("body_ar", ""))}{(" · " + mono(s["doc_symbol"])) if s.get("doc_symbol") else ""}</p>
      <p class="small">{esc(s.get("summary_ar", ""))}</p>{ext(s["url"], "الوثيقة الرسمية", "small") if s.get("url") else ""}</div></li>''' for s in sorted(p.get('statuses', []), key=lambda s: s.get('date', '')))
    events = ''.join(f'<li><span class="tl-date num">{esc(date_ar(t.get("date")))}</span><div class="tl-body"><p class="small">{esc(t.get("event_ar", ""))}</p>{ext(t["url"], "المصدر", "xs") if t.get("url") else ""}</div></li>'
                     for t in sorted(p.get('timeline', []), key=lambda t: t.get('date', '')))
    below = f'''<section class="sec record-body"><div class="wrap read">
 <h2 class="h2" id="status">الوضع القانوني بالتفصيل</h2>
 <ol class="timeline" data-tie>{timeline}</ol>
 {f'<h2 class="h2">التسلسل الإجرائي</h2><ol class="timeline timeline-quiet">{events}</ol>' if events else ''}
 <h2 class="h2">ما تثبته هذه المصادر وما لا تثبته</h2>
 <div class="prose"><p>{esc(p.get("limits_ar", ""))}</p></div>
 <h2 class="h2" id="incidents">الوقائع المرتبطة</h2>
 {f'<ul class="rows">{"".join(B.inc_mini_row(i, rel) for i in incs)}</ul>' if incs else '<p class="note">' + icon("info") + '<span>لم يُربط هذا الملف بواقعة بعينها في النموذج. يُربط الشخص بواقعة فقط إذا ربطته بها وثيقة رسمية.</span></p>'}
 <h2 class="h2">المصادر</h2>
 {B.sources_list(p.get("sources", []))}
 {B.face_credit(B.photo_of(p["id"]))}
 <div class="sheet custody-sheet">{B.custody(p["id"], B.default_custody("person"))}</div>
 {cite_block(rel, p["id"], f'موثّق، «{p["name_ar"]}»، ملف {p["id"]}، {STATUS[p["status"]][0]}. اطُّلع عليه في 28 أكتوبر 2026.')}
</div></section>'''
    card = stamp(p['id'], counts=(('الوقائع', len(incs)), ('الوثائق', len(docs)), ('القواعد', len(rules)), ('المصادر', len(p.get('sources', [])))),
                 extra=f'<p class="stamp-status">{esc(STATUS[p["status"]][0])} <span class="mono">{STATUS[p["status"]][1]}/5</span></p>')
    main = f'<div class="wrap">{S.crumbs(rel, [("ملفات الأشخاص", "people/index.html"), (p["name_ar"], None)])}</div>' + record(rel, tag, side, below, card)
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
    years = ''.join(f'<span class="tr-year" style="inset-inline-start:{pos(f"{y}-01-01") * 100:.2f}%">{y}</span>' for y in (2024, 2025, 2026))
    rope = (f'<div class="timerope" data-timerope><p class="tr-cap">{len(incs)} واقعة على حبل الزمن، من أكتوبر 2023 إلى اليوم. قف على عقدة لترى الواقعة.</p>'
            f'<div class="tr-body"><svg class="tr-line" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 22 Q500 40 1000 22"/></svg>'
            f'{knots_html}{years}<p class="tr-tip" hidden></p></div></div>')
    list_page(rel, 'incidents/index.html', 'incidents', 'أرشيف الوقائع',
              'لكل واقعة سجل مستقل يفصل بين ما حدث بحسب المصادر، والروايات المتعارضة، والأدلة وحالة كل منها، والتحليل القانوني. التحقق من الواقعة منفصل عن تحديد المسؤولية الفردية.',
              q_field('عنوان أو مكان') + sel('fr', 'المنطقة', 'region', regions) + sel('fv', 'حالة التحقق', 'state', states) + sel('fy', 'السنة', 'year', [(y, y) for y in years]),
              items, 'inc-list', before=rope)
    for i in B.INCIDENTS:
        incident_page(i)


def incident_page(inc):
    rel = '../'
    evs = [B.EV_BY_ID[e] for e in inc['ev_ids']]
    rules = [B.RULE_BY_ID[r] for r in inc['rule_ids'] if r in B.RULE_BY_ID]
    persons = [B.P_BY_ID[p] for p in inc['pids']]
    docs = [B.DOC_BY_ID[d] for d in B.PICKS.get('incident_docs', {}).get(inc['id'], []) if d in B.DOC_BY_ID]
    side = (side_list('الأشخاص', [f'<li><a class="row row-person" href="{rel}people/{slug(p["id"])}.html" data-cord-to="{p["id"]}"><span class="row-body"><span class="tag-kind">{esc(STATUS[p["status"]][0])}</span><h3>{esc(p["name_ar"])}</h3></span><span class="row-end"><span class="mono">{p["id"]}</span></span></a></li>' for p in persons]) +
            side_list('الأدلة', [B.ev_row(e, rel) for e in evs]) + side_list('القواعد', [B.rule_row(r, rel) for r in rules]) +
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
 {'<p class="note">' + icon("alert") + '<span>نعرض الروايتين كما وردتا ومصدر كل منهما؛ ترجيح رواية على أخرى يُذكر سببه صراحة ولا يُفترض.</span></p>' if inc.get('conflict') else ''}'''
    # one block per act: the act, the rules it engages, then why and what must be proven side by side
    legal_rows = ''.join(f'''<li class="lg"><h3 class="lg-act">{esc(L.get("act_ar", ""))}</h3>
      <div class="lg-rules">{"".join(f'<a class="rule" href="{rel}law/{slug(r)}.html"><span class="mono">{esc(B.RULE_BY_ID[r].get("article_en", ""))}</span><b>{esc(B.RULE_BY_ID[r].get("title_ar", ""))}</b></a>' for r in L.get("ids", []) if r in B.RULE_BY_ID) or esc("، ".join(L.get("rules", [])))}</div>
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
 <p class="note">{icon("alert")}<span>التحقق من أصالة مادة وسياقها منفصل عن الاستنتاج القانوني؛ ارتباط صورة أو مقطع بمكان أو حادثة لا يثبت المسؤولية الفردية لأي شخص.</span></p>
 <h2 class="h2">التحليل القانوني الأولي</h2>
 <ol class="sheet legal-list">{legal_rows}</ol>
 <p class="note">{icon("scale")}<span>تحليل بحثي أولي يربط الوقائع بالقواعد، وليس حكمًا قضائيًا ولا تقريرًا نهائيًا للمسؤولية الجنائية.</span></p>
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
              'كل مادة مرتبطة بواقعة لها سجل: نوعها ومصدرها وسياقها وحدودها وحالة التحقق منها. للمواد المحفوظة على المنصة بصمة رقمية تستطيع مطابقتها بنفسك.',
              q_field('وصف أو واقعة') + sel('ft', 'نوع المادة', 'type', types) + sel('fv', 'حالة التحقق', 'state', states), items, 'ev-list')
    for e in B.EVIDENCE:
        evidence_page(e)


def evidence_page(ev):
    rel = '../'
    inc = B.INC_BY_ID[ev['incident']]
    kind, _ = B.EV_KIND.get(ev.get('type'), ('مادة', 'doc'))
    ph = B.EV_PHOTO.get(ev['id'])
    ph = ph if ph in B.PHOTO_SIZE else None
    h = B.sha(ph) if ph else None
    rules = [B.RULE_BY_ID[r] for r in inc['rule_ids'] if r in B.RULE_BY_ID]
    side = side_list('الواقعة', [B.inc_mini_row(inc, rel)]) + side_list('القواعد ذات الصلة', [B.rule_row(r, rel) for r in rules[:4]])
    verify = ''
    if h:
        verify = f'''<h2 class="h2" id="verify">افحص سلامة الختم بنفسك</h2>
 <div class="verify" data-verify="{h}">
  <div class="verify-seal" data-verify-seal><svg class="seal is-wax" viewBox="0 0 40 40" aria-hidden="true"><use href="#s-whole"/></svg></div>
  <div class="verify-body">
   <p>حُفظت من هذه المادة نسخة مرجعية على المنصة، وسُجّلت بصمتها الرقمية. نزّل النسخة، ثم أفلتها هنا أو اخترها، وتُحسب بصمتها على جهازك دون رفعها إلى أي مكان.</p>
   <dl class="fields"><div><dt>البصمة المسجّلة (SHA-256)</dt><dd><span class="mono hash">{h}</span></dd></div></dl>
   <div class="verify-actions"><a class="btn btn-line btn-sm" href="{rel}assets/img/photo/{ph}.webp" download>{icon("download")} نزّل النسخة المحفوظة</a>
   <button class="btn btn-line btn-sm" type="button" data-copy="{h}" data-done="نُسخت البصمة.">{icon("doc")} انسخ البصمة</button></div>
   <label class="drop">{icon("upload")}<span><b>أفلت الملف هنا</b> أو اضغط لاختياره</span><input type="file" class="sr"></label>
   <p class="verify-out" data-verify-out aria-live="polite"></p>
  </div>
 </div>'''
    below = f'''<section class="sec record-body"><div class="wrap read">
 {B.photo_fig(ph, rel, sizes="(min-width: 1024px) 760px, 100vw") if ph else ""}
 <h2 class="h2">السياق</h2>
 <div class="prose"><p>{esc(ev.get("desc_ar", ""))}. المصدر: {esc(ev.get("source", ""))}، {esc(date_ar(ev.get("date")))}. ترتبط المادة بسجل «{esc(inc["title_ar"])}».</p></div>
 <h2 class="h2">القيود المعروفة</h2>
 <div class="prose"><p>{esc(B.EV_LIMIT.get(ev.get("type"), "تُذكر قيود المادة عند مراجعتها."))}</p></div>
 {verify}
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
              'مكتبة للوثائق القضائية والأممية والحقوقية، كل منها موسوم بطبيعته القانونية: التقرير الحقوقي ليس مذكرة توقيف، ومذكرة التوقيف ليست حكمًا نهائيًا، والتدابير المؤقتة تخص مسؤولية الدولة لا الأفراد.',
              q_field('عنوان أو جهة') + sel('fc', 'نوع الجهة', 'cat', cats) + sel('fy', 'السنة', 'year', [(y, y) for y in years]),
              ''.join(B.doc_row(d, rel) for d in docs), 'doc-list')
    for d in B.DOCS:
        report_page(d)


def report_page(d):
    rel = '../'
    persons = [B.P_BY_ID[p] for p in d.get('persons', []) if p in B.P_BY_ID]
    rules = [B.RULE_BY_ID[r] for r in d['rule_ids'] if r in B.RULE_BY_ID]
    incs = [B.INC_BY_ID[i] for i in d['inc_ids'] if i in B.INC_BY_ID]
    side = (side_list('الأشخاص', [f'<li><a class="row row-person" href="{rel}people/{slug(p["id"])}.html" data-cord-to="{p["id"]}"><span class="row-body"><span class="tag-kind">{esc(STATUS[p["status"]][0])}</span><h3>{esc(p["name_ar"])}</h3></span><span class="row-end"><span class="mono">{p["id"]}</span></span></a></li>' for p in persons]) +
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
 <h2 class="h2">كيف تُقرأ هذه الوثيقة</h2>
 <p class="note">{icon("scale")}<span>{esc(d.get("nature_ar", ""))}. لا ننقل محتوى الوثائق آليًا إلى قائمة حقائق؛ نميّز بين ما تثبته، وما ترجّحه، وما تنقله عن غيرها، ونوثّق حدود الاستدلال بها داخل كل ملف.</span></p>
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
              'النصوص الرسمية للمواد التي تُربط بها الوقائع، مع صياغة موجزة. الربط بمادة تحليل بحثي أولي يوضح وجه الصلة وما يلزم إثباته، ولا يفترض انطباقها لمجرد التشابه.',
              q_field('مادة أو موضوع') + sel('fb', 'الفرع', 'branch', branches), ''.join(B.rule_row(r, rel) for r in B.RULES), 'rule-list')
    for r in B.RULES:
        rule_page(r)


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
    side = (side_list('الوقائع', [B.inc_mini_row(i, rel) for i in incs]) + side_list('الوثائق', [B.doc_row(d, rel) for d in docs]) +
            side_list('من الصك نفسه', [B.rule_row(x, rel).replace(f' data-cord-to="{x["id"]}"', '') for x in kin[:5]]))
    tag = f'''<article class="tag is-reversed"{B.vt(r["id"])} aria-label="قاعدة قانونية">
  <span class="tag-hole" aria-hidden="true"></span>
  <div class="tag-top"><span class="tag-no">{esc(r.get("article_en", r["id"]))}</span><span class="tag-kind">{esc(B.BRANCH.get(r.get("branch"), ""))}</span></div>
  <div class="tag-seal" data-cord-from>{S.wax("complete")}</div>
  <p class="tag-by open-1">{esc(r.get("instrument_ar", ""))}</p>
  <h1 class="tag-status open-1">{esc(r.get("article_ar", ""))}</h1>
  <div class="tag-name open-2"><b>{esc(r.get("title_ar", ""))}</b></div>
  <p class="tag-not open-3">{S.icon("info")}<span>{esc(r.get("applies_note_ar") or "يُرجع دائمًا إلى النص الرسمي؛ الصياغة الموجزة هنا للإيضاح.")}</span></p>
</article>'''
    chapeau = f'<p class="chapeau">{esc(r["chapeau_ar"])}</p>' if r.get('chapeau_ar') else ''
    body = ''.join(f'<p>{esc(line)}</p>' for line in (r.get('text_ar') or '').splitlines() if line.strip())
    defin = (f'<p class="definition"><b>{esc(r.get("definition_ref_ar") or "تعريف مرتبط")}:</b> {esc(r["definition_ar"])}</p>' if r.get('definition_ar') else '')
    text = (f'<blockquote class="official">{chapeau}{body}{defin}<footer>{esc(r.get("instrument_ar", ""))}، {esc(r.get("article_ar_official") or r.get("article_ar", ""))} — النص الرسمي. {esc(r.get("text_source", ""))}</footer></blockquote>'
            if r.get('text_ar') else (f'<blockquote class="official" lang="en" dir="ltr"><p>{esc(r["text_en"])}</p><footer>{esc(r.get("instrument_en", ""))}, {esc(r.get("article_en", ""))} — official English text; no authentic Arabic version exists.</footer></blockquote>' if r.get('text_en') else '') + f'<p class="note">{icon("info")}<span>{esc(r.get("note") or "لم يُدرج النص الرسمي العربي في هذا النموذج؛ راجع الرابط الرسمي.")}</span></p>')
    prove_html = ''.join(f'<li><a href="{rel}incidents/{slug(i["id"])}.html">{esc(i["title_ar"])}</a><p class="small">{esc(t)}</p></li>' for i, t in prove)
    below = f'''<section class="sec record-body"><div class="wrap read">
 <h2 class="h2">النص</h2>
 {text}
 <div class="link-row">{ext(r["url"], "النص الرسمي", "btn btn-line btn-sm") if r.get("url") else ""} {ext(r["url_en"], "English", "btn btn-line btn-sm") if r.get("url_en") else ""}</div>
 <h2 class="h2">بصياغة موجزة</h2>
 <div class="prose"><p>{esc(r.get("paraphrase_ar", ""))}</p></div>
 {f'<h2 class="h2">ما يلزم إثباته في الوقائع المرتبطة</h2><ul class="prove">{prove_html}</ul>' if prove_html else ''}
 <h2 class="h2">الوقائع المرتبطة ({len(incs)})</h2>
 {f'<ul class="rows">{"".join(B.inc_mini_row(i, rel) for i in incs)}</ul>' if incs else '<p class="small mute">لا وقائع مرتبطة بهذه المادة في النموذج.</p>'}
{cite_block(rel, r["id"], f'{r.get("instrument_ar", "")}، {r.get("article_ar_official") or r.get("article_ar", "")}: «{r.get("title_ar", "")}». في مكتبة قواعد موثّق برقم {r["id"]}.')}
</div></section>'''
    card = stamp(r.get('article_en') or r['id'], None, (('الوقائع', len(incs)), ('الوثائق', len(docs)), ('الأشخاص', len(persons))), f'<p class="stamp-status">{esc(B.BRANCH.get(r.get("branch"), ""))}</p>')
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
