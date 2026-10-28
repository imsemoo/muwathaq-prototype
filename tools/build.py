"""Build the موثّق prototype from the research files.

python tools/build.py   (from the project root)

Reads research/{persons,incidents,documents,rules}.json, tools/picks.json (photo and state choices made
by hand) and tools/out/photos.json (sizes written by photos.py); writes every page and assets/js/index.js.
Platform-specific verification states and custody logs are illustrative and say so on the page.
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell as S  # noqa: E402
from shell import esc, icon, seal, seal_row, knots, ext, ltr, mono, date_ar, write, STATUS, VERIF, REGIONS  # noqa: E402

ROOT = S.ROOT
R = lambda *p: os.path.join(ROOT, *p)


RES = os.environ.get('MW_RESEARCH') or R('research')


def load(name, default=None):
    p = os.path.join(RES, name)
    if not os.path.exists(p):
        return default if default is not None else []
    data = json.load(open(p, encoding='utf-8'))
    if isinstance(data, dict):   # {meta, <records>} wrappers: take the record list
        data = next((v for v in data.values() if isinstance(v, list)), [])
    return data


PERSONS = load('persons.json')
INCIDENTS = load('incidents.json')
DOCS = load('documents.json')
RULES = load('rules.json')
PICKS = json.load(open(R('tools', 'picks.json'), encoding='utf-8')) if os.path.exists(R('tools', 'picks.json')) else {}
PHOTOS = json.load(open(R('tools', 'photos.json'), encoding='utf-8')) if os.path.exists(R('tools', 'photos.json')) else {}
PHOTO_SIZE = json.load(open(R('tools', 'out', 'photos.json'), encoding='utf-8')) if os.path.exists(R('tools', 'out', 'photos.json')) else {}

# ---------- rules: resolve free-text citations to library ids ----------
ROMAN = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10, 'xi': 11, 'xii': 12,
         'xiii': 13, 'xiv': 14, 'xv': 15, 'xvi': 16, 'xvii': 17, 'xviii': 18, 'xix': 19, 'xx': 20, 'xxi': 21, 'xxii': 22,
         'xxiii': 23, 'xxiv': 24, 'xxv': 25, 'xxvi': 26}


ID_FAMILY = {'RS-': 'rome', 'GEN-': 'gen', 'GCIV-': 'gc4', 'GC4-': 'gc4', 'API-': 'ap1', 'AP1-': 'ap1', 'ICCPR-': 'iccpr',
             'CAT-': 'cat', 'CIHL-': 'cihl'}


def family(text, rid=''):
    for pre, fam in ID_FAMILY.items():
        if rid.startswith(pre):
            return fam
    t = text.lower()
    if re.search(r'geneva convention\s*\(?iv\)?|fourth geneva|\bgc\s*\(?iv\)?\b|gciv|gc4', t):
        return 'gc4'
    if 'rome' in t or t.startswith('rs') or 'icc statute' in t:
        return 'rome'
    if 'additional protocol' in t or re.search(r'\bap\s*i\b', t) or 'api ' in t or 'protocol i' in t:
        return 'ap1'
    if 'geneva convention iv' in t or re.search(r'\bgc\s*iv\b', t) or 'fourth geneva' in t or 'gciv' in t or 'gc4' in t:
        return 'gc4'
    if 'genocide' in t:
        return 'gen'
    if 'iccpr' in t or 'civil and political' in t:
        return 'iccpr'
    if 'torture' in t or re.search(r'\bcat\b', t):
        return 'cat'
    if 'customary' in t or 'rule' in t:
        return 'cihl'
    return ''


def tokens(text, fam=''):
    """Article path of a citation: 'Rome Statute art. 8(2)(b)(xxv)' -> ['8', '2', 'b', '25']."""
    t = text.lower().replace('–', ' ').replace('-', ' ')
    m = re.search(r'(?:\barticles?\b|\barts?\.?|\brule\b)\s*(.*)$', t)
    tail = m.group(1) if m else t
    toks = re.findall(r'[0-9]+|[a-z]+', tail)
    if not m:  # no keyword: drop the instrument's words before the first number (or roman article for genocide)
        while toks and not (toks[0].isdigit() or (fam == 'gen' and toks[0] in ROMAN)):
            toks.pop(0)
    out = []
    for tok in toks:
        if tok in ('para', 'paragraph', 'and', 'of', 'the'):
            continue
        out.append(str(ROMAN[tok]) if tok in ROMAN and len(out) >= 3 else tok)
    return out


RULE_BY_ID = {r['id']: r for r in RULES}
RULE_KEYS = []
for r in RULES:
    fam = family(r.get('instrument_en', ''), r.get('id', ''))
    RULE_KEYS.append((fam, tokens(r.get('article_en', ''), fam), r['id']))


def resolve(text):
    fam = family(text)
    tk = tokens(text, fam)
    best, score = None, 0
    for f, rt, rid in RULE_KEYS:
        if f != fam or not rt:
            continue
        n = 0
        for a, b in zip(rt, tk):
            if a != b:
                break
            n += 1
        if n and n == len(rt) and n > score:
            best, score = rid, n
        elif n and n > score and n == len(tk):
            best, score = rid, n
    return best


# ---------- records ----------
def slug(i):
    return i.lower()


EVIDENCE = []
EV_PHOTO = dict(PICKS.get('ev_photo', {}))
for inc in INCIDENTS:
    inc['ev_ids'] = []
    # documentary photographs we archive ourselves join the record as image evidence
    for x in PICKS.get('extra_ev', {}).get(inc['id'], []):
        if x.get('photo') in PHOTOS:
            ph = PHOTOS[x['photo']]
            inc.setdefault('evidence', []).append({'type': 'image', 'desc_ar': x.get('desc_ar') or ph.get('caption_ar', ''),
                                                   'source': ph.get('author', ''), 'date': ph.get('date', ''), 'url': ph['page_url'],
                                                   '_photo': x['photo']})
    for k, ev in enumerate(inc.get('evidence', [])):
        eid = 'EV-%04d' % (len(EVIDENCE) + 1)
        ev = dict(ev, id=eid, incident=inc['id'], k=k)
        if ev.get('_photo'):
            EV_PHOTO[eid] = ev['_photo']
        EVIDENCE.append(ev)
        inc['ev_ids'].append(eid)
    rule_ids = []
    for L in inc.get('legal', []):
        L['ids'] = [x for x in (resolve(t) for t in L.get('rules', [])) if x]
        rule_ids += L['ids']
    inc['rule_ids'] = list(dict.fromkeys(rule_ids))

INC_BY_ID = {i['id']: i for i in INCIDENTS}
EV_BY_ID = {e['id']: e for e in EVIDENCE}
DOC_BY_ID = {d['id']: d for d in DOCS}
P_BY_ID = {p['id']: p for p in PERSONS}
NAME_TO_P = {}
for p in PERSONS:
    for n in [p.get('name_en', ''), p.get('name_ar', '')]:
        if n:
            NAME_TO_P[n.lower()] = p['id']


def persons_of_incident(inc):
    out = []
    for n in inc.get('persons', []):
        pid = n if n in P_BY_ID else NAME_TO_P.get(str(n).lower())
        if not pid:
            for key, v in NAME_TO_P.items():
                if key and key.split()[-1] in str(n).lower():
                    pid = v
                    break
        if pid and pid not in out:
            out.append(pid)
    return out


for inc in INCIDENTS:
    inc['pids'] = persons_of_incident(inc)
for p in PERSONS:
    p['inc_ids'] = [i['id'] for i in INCIDENTS if p['id'] in i['pids']]
    p['doc_ids'] = [d['id'] for d in DOCS if p['id'] in d.get('persons', [])]
    p['rule_ids'] = list(dict.fromkeys(PICKS.get('person_rules', {}).get(p['id'], [])))
for d in DOCS:
    d['rule_ids'] = list(dict.fromkeys(x for x in (resolve(t) for t in d.get('rules_hint', [])) if x))
    d['inc_ids'] = PICKS.get('doc_incidents', {}).get(d['id'], [])
for r in RULES:
    r['inc_ids'] = [i['id'] for i in INCIDENTS if r['id'] in i['rule_ids']]
    r['doc_ids'] = [d['id'] for d in DOCS if r['id'] in d['rule_ids']]
    r['p_ids'] = [p['id'] for p in PERSONS if r['id'] in p['rule_ids']]

STATES = PICKS.get('states', {})


def state_of(rec_id, default='partial'):
    return STATES.get(rec_id, default)


def ev_state(ev):
    if ev['id'] in STATES:
        return STATES[ev['id']]
    return {'official': 'complete', 'document': 'complete', 'report': 'complete', 'satellite': 'specific',
            'video': 'specific', 'image': 'partial', 'testimony': 'in_progress'}.get(ev.get('type'), 'partial')


def photo_of(rec_id):
    s = PICKS.get('photo', {}).get(rec_id)
    if not s and rec_id in P_BY_ID:
        name = P_BY_ID[rec_id].get('name_en', '').lower()
        s = next((v for k, v in PICKS.get('portrait_by_name', {}).items() if k.lower() in name), None)
    if not s and rec_id in DOC_BY_ID:
        s = PICKS.get('doc_photo_by_cat', {}).get(DOC_BY_ID[rec_id].get('cat'))
    return s if s and s in PHOTOS and s in PHOTO_SIZE else None


def sha(slug_):
    p = R('assets', 'img', 'photo', slug_ + '.webp')
    return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None


EV_KIND = {'video': ('مقطع فيديو', 'video'), 'image': ('صورة', 'image'), 'satellite': ('صور أقمار صناعية', 'sat'),
           'document': ('وثيقة', 'doc'), 'report': ('تقرير', 'doc'), 'testimony': ('شهادة منشورة', 'quote'),
           'official': ('بيان رسمي', 'official')}
EV_LIMIT = {
    'video': 'تاريخ النشر لا يطابق بالضرورة تاريخ التصوير؛ تُطابق معالم المكان بصور مرجعية قبل الاعتماد.',
    'image': 'النسخ المتداولة مضغوطة غالبًا، ما يحدّ من تحليل البيانات الوصفية.',
    'satellite': 'دقة الصور تكشف نطاق الضرر وتوقيته التقريبي، ولا تحدد وحدها سببه أو الجهة المنفذة.',
    'document': 'يلزم التحقق من سلسلة حيازة الوثيقة ومن نسختها الأصلية.',
    'report': 'مصدر ثانوي يعتمد على منهجيته ومصادره الخاصة، ويُقرأ بحدودها.',
    'testimony': 'شهادة فردية تُعزَّز بمصادر مستقلة؛ تُخفى البيانات المعرِّفة.',
    'official': 'يعبّر عن موقف طرف في النزاع، ويُعرض بوصفه رواية لا حقيقة مثبتة.',
}
DOC_CAT = {'icj': 'محكمة العدل الدولية', 'icc': 'المحكمة الجنائية الدولية', 'un_coi': 'لجنة التحقيق الدولية',
           'un_sr': 'المقررون الخاصون', 'un_agency': 'وكالات الأمم المتحدة', 'ngo': 'منظمات حقوقية',
           'journalism': 'تحقيقات صحفية', 'forensic': 'تحقيقات جنائية رقمية', 'ipc': 'الأمن الغذائي (IPC)'}
BRANCH = {'ICL': 'القانون الجنائي الدولي', 'IHL': 'القانون الدولي الإنساني', 'IHRL': 'القانون الدولي لحقوق الإنسان',
          'GENOCIDE': 'اتفاقية منع الإبادة الجماعية', 'RESP': 'قواعد المسؤولية الجنائية', 'CUSTOM': 'القانون الدولي الإنساني العرفي'}


def custody(rec_id, entries, on_ink=False):
    rows = ''.join(f'<tr><th scope="row" class="num">{esc(d)}</th><td>{esc(a)}</td><td>{esc(s)}</td></tr>' for d, a, s in entries)
    return (f'<table class="custody"><caption>سجل العهدة <small>توضيحي في النموذج</small></caption>'
            f'<tbody>{rows}</tbody></table>')


def default_custody(kind):
    if kind == 'person':
        return [('12 أكتوبر 2026', 'تسجيل الملف وربط الوثيقة القضائية الأصلية', 'مسجّل'),
                ('14 أكتوبر 2026', 'مطابقة الحالة القانونية مع بيان الجهة المصدرة', 'مراجَع'),
                ('20 أكتوبر 2026', 'مراجعة قانونية وقرار النشر', 'معتمد للنشر')]
    if kind == 'incident':
        return [('9 أكتوبر 2026', 'تسجيل الواقعة ومصادرها الأولية', 'مسجّلة'),
                ('15 أكتوبر 2026', 'مقارنة الروايات وتوثيق القيود', 'قيد التحقق'),
                ('22 أكتوبر 2026', 'مراجعة قانونية أولية للأفعال محل التحليل', 'مراجَعة')]
    if kind == 'evidence':
        return [('10 أكتوبر 2026', 'حفظ نسخة مرجعية وحساب بصمتها', 'مختومة'),
                ('16 أكتوبر 2026', 'فحص الأصالة والسياق والتاريخ', 'قيد الفحص'),
                ('23 أكتوبر 2026', 'ربط المادة بالواقعة وتوثيق القيود', 'مربوطة')]
    return [('11 أكتوبر 2026', 'حفظ الوثيقة من مصدرها الرسمي', 'محفوظة'),
            ('13 أكتوبر 2026', 'تحديد طبيعتها القانونية ونطاقها', 'مصنّفة'),
            ('21 أكتوبر 2026', 'ربطها بالملفات والوقائع ذات الصلة', 'مربوطة')]


def sources_list(srcs, start=1):
    items = []
    for n, s in enumerate(srcs, start):
        meta = ' · '.join(x for x in [s.get('publisher', ''), date_ar(s.get('date')) if s.get('date') else ''] if x)
        title = esc(s.get('title') or s.get('publisher') or s.get('url'))
        link = ext(s['url'], title) if s.get('url') else title
        items.append(f'<li id="src-{n}"><span class="n">[{n}]</span><span>{link}<small>{esc(meta)}</small></span></li>')
    return f'<ol class="sources">{"".join(items)}</ol>'


def photo_fig(slug_, rel, cls='photo', sizes='(min-width: 1024px) 50vw, 100vw', eager=False):
    p = PHOTOS[slug_]
    sz = PHOTO_SIZE[slug_]
    credit = f'{esc(p.get("author", ""))} · {esc(p.get("license", ""))}'
    load_ = 'eager" fetchpriority="high' if eager else 'lazy'
    return (f'<figure class="{cls}"><img src="{rel}assets/img/photo/{slug_}.webp" '
            f'srcset="{rel}assets/img/photo/{slug_}-640.webp 640w, {rel}assets/img/photo/{slug_}.webp {sz["w"]}w" sizes="{sizes}" '
            f'width="{sz["w"]}" height="{sz["h"]}" alt="{esc(p.get("alt", p.get("caption_ar", "")))}" loading="{load_}" decoding="async">'
            f'<figcaption><b>{esc(p.get("caption_ar", ""))}</b><span>صورة: {ext(p["page_url"], credit)}</span></figcaption></figure>')


def face(slug_, rel, cls='tag-face', w=160):
    if not slug_:
        return ''
    sz = PHOTO_SIZE[slug_]
    p = PHOTOS[slug_]
    return (f'<img class="{cls}" src="{rel}assets/img/photo/{slug_}-240.webp" alt="{esc(p.get("alt", ""))}" '
            f'width="{w}" height="{round(w * sz["h"] / sz["w"])}" decoding="async" title="صورة: {esc(p.get("author", ""))} · {esc(p.get("license", ""))}">')


def face_credit(slug_):
    if not slug_:
        return ''
    p = PHOTOS[slug_]
    return f'<p class="xs mute face-credit">صورة الملف: {ext(p["page_url"], esc(p.get("author", "")) + " · " + esc(p.get("license", "")))}، {esc(date_ar(p.get("date")))}.</p>'


def thumb(slug_, rel):
    if not slug_:
        return f'<span class="row-thumb is-blank" aria-hidden="true">{icon("image")}</span>'
    sz = PHOTO_SIZE[slug_]
    return (f'<span class="row-thumb"><img src="{rel}assets/img/photo/{slug_}-240.webp" alt="" width="240" '
            f'height="{round(240 * sz["h"] / sz["w"])}" loading="lazy" decoding="async"></span>')


def rule_label(rid):
    r = RULE_BY_ID.get(rid)
    if not r:
        return esc(rid)
    return f'<span class="mono">{esc(r.get("article_en", ""))}</span> <b>{esc(r.get("title_ar", ""))}</b>'


def vt(rec_id):
    return f' style="view-transition-name:tag-{slug(rec_id)}"'


# ---------- person ----------
def person_status_line(p):
    label = STATUS[p['status']][0]
    main = next((s for s in p.get('statuses', []) if s.get('type') == p['status']), (p.get('statuses') or [{}])[0])
    by = ' · '.join(x for x in [main.get('body_ar', ''), date_ar(main.get('date'))] if x and x != '—')
    return label, by, main


def person_mini(p, rel, vtn=True):
    label, by, _ = person_status_line(p)
    return (f'<a class="mini" href="{rel}people/{slug(p["id"])}.html"{vt(p["id"]) if vtn else ""}>'
            f'<span class="tag-hole" aria-hidden="true"></span>'
            f'<span class="tag-top"><span class="tag-no">{esc(p["id"])}</span>{seal(state_of(p["id"], "complete"), label=False, cls="seal")}</span>'
            f'<span class="mini-status">{esc(label)}</span>'
            f'<span class="mini-who">{face(photo_of(p["id"]), rel, "mini-face", 96)}<span class="mini-name">{esc(p["name_ar"])}</span></span>'
            f'<span class="mini-meta">{esc(by)}</span>{knots(p["status"], mini=True)}</a>')


def person_tag(p, rel, lead=False, actions=True):
    label, by, main = person_status_line(p)
    st = state_of(p['id'], 'complete')
    # each act is read with its basis (warrant, inquiry finding, sanction); on the table only the first two, the rest in the file
    full = not actions
    crimes_all = p.get('crimes_ar', [])
    def act(c):
        what, _, basis = c.partition(' — ')
        return f'<li><b>{esc(what)}</b>{f"<small>{esc(basis)}</small>" if basis else ""}</li>'
    shown = crimes_all if full else crimes_all[:2]
    more = len(crimes_all) - len(shown)
    more_t = {1: 'وفعل آخر في الملف', 2: 'وفعلان آخران في الملف'}.get(more, f'و{more} أفعال أخرى في الملف')
    crimes = ((f'<ul class="acts">{"".join(act(c) for c in shown)}</ul>' +
               (f'<a class="acts-more" href="{rel}people/{slug(p["id"])}.html#status">{more_t}</a>' if more > 0 else '')) if crimes_all else '—')
    per = p.get('period') or []
    period = (f'{date_ar(per[0])}' if per[0] == per[1] else f'من {date_ar(per[0])} إلى {date_ar(per[1])}') if len(per) == 2 and per[0] else ''
    others = [s for s in p.get('statuses', []) if s is not main] if full else []   # on the table: the file holds the rest
    other = '؛ '.join(f'{s.get("body_ar", "")} ({date_ar(s.get("date"))})' for s in others)
    symbol = main.get('doc_symbol') or '—'
    acts = ''
    if actions:
        acts = (f'<div class="tag-actions"><a class="btn btn-light" href="{rel}people/{slug(p["id"])}.html">افتح الحرز {icon("arrow")}</a>'
                f'{f"<a class=\"btn btn-ghost\" href=\"{rel}people/{slug(p["id"])}.html#incidents\">الوقائع المرتبطة ({len(p['inc_ids'])})</a>" if p["inc_ids"] else ""}</div>')
    return f'''<article class="tag is-reversed"{vt(p["id"])} aria-label="ملف {esc(p["name_ar"])}">
  <span class="tag-hole" aria-hidden="true"></span>
  <div class="tag-top"><span class="tag-no">{esc(p["id"])}</span><span class="tag-kind">ملف شخص</span></div>
  <div class="tag-seal" data-cord-from>{S.wax(st)}</div>
  <p class="tag-status open-1">{esc(label)}</p>
  <p class="tag-by open-1">{esc(by)}</p>
  <div class="tag-who open-2">{face(photo_of(p["id"]), rel)}<div class="tag-name"><b>{esc(p["name_ar"])}</b><span>{esc(p.get("role_ar", ""))}</span></div></div>
  <div class="open-2" style="margin-top:18px">{knots(p["status"])}</div>
  <p class="tag-not open-3">{icon("info")}<span>{esc(STATUS[p["status"]][2])} ويُفترض براءة الشخص حتى تثبت إدانته بحكم قضائي.</span></p>
  <dl class="fields open-3">
   <div><dt>رقم الوثيقة أو الحالة</dt><dd>{mono(symbol)}</dd></div>
   <div><dt>حالة التحقق من الملف</dt><dd>{seal_row(st)}</dd></div>
   {f"<div><dt>الفترة المشمولة</dt><dd>{esc(period)}</dd></div>" if period else ""}
   <div class="wide"><dt>الأفعال الواردة في الوثائق</dt><dd>{crimes}</dd></div>
   {f'<div class="wide"><dt>ورد أيضًا في</dt><dd class="dd-more">{esc(other)}</dd></div>' if other else ""}
  </dl>
  {acts}
</article>'''


# ---------- incident ----------
def date_face(inc):
    d = date_ar(inc['date']).split(' ')
    top = ' '.join(d[:-1]) if len(d) > 1 else d[0]
    return (f'<span class="row-thumb is-blank date-face" aria-hidden="true"><b>{esc(top)}</b>'
            f'<span>{esc(d[-1] if len(d) > 1 else "")}</span></span>')


def inc_mini_row(inc, rel):
    ph = photo_of(inc['id'])
    st = state_of(inc['id'])
    region = REGIONS.get(inc.get('region'), '')
    return (f'<li data-region="{esc(inc.get("region", ""))}" data-state="{st}" data-year="{inc["date"][:4]}" data-text="{esc(inc["title_ar"] + " " + inc.get("place_ar", ""))}">'
            f'<a class="row" href="{rel}incidents/{slug(inc["id"])}.html" data-cord-to="{inc["id"]}">{thumb(ph, rel) if ph else date_face(inc)}'
            f'<span class="row-body"><h3>{esc(inc["title_ar"])}</h3><span class="row-meta"><span>{icon("cal")} {esc(date_ar(inc["date"]))}</span>'
            f'<span>{icon("pin")} {esc(inc.get("place_ar", ""))}</span></span></span>'
            f'<span class="row-end">{seal_row(st, illus=False)}<span class="mono">{esc(inc["id"])}</span></span></a></li>')


def doc_face(d):
    """The few characters printed on a document's dark face: its docket or symbol, else who published it."""
    s = (d.get('symbol') or '').split(';')[0].split(',')[0].replace('General List No.', 'ICJ No.').replace(' analysis', '').strip()
    pub = (d.get('publisher_en') or '').split(' (')[0].strip()
    return s or (pub if 0 < len(pub) <= 24 else d['id'])


def doc_row(d, rel):
    return (f'<li data-cat="{esc(d.get("cat", ""))}" data-year="{d.get("date", "")[:4]}" data-text="{esc(d.get("title_ar", "") + " " + d.get("title_en", "") + " " + d.get("publisher_ar", ""))}">'
            f'<a class="row row-doc" href="{rel}reports/{slug(d["id"])}.html" data-cord-to="{d["id"]}">'
            f'<span class="row-thumb is-blank doc-face" aria-hidden="true"><span class="mono">{esc(doc_face(d))}</span></span>'
            f'<span class="row-body"><span class="tag-kind">{esc(DOC_CAT.get(d.get("cat"), ""))}</span><h3>{esc(d.get("title_ar", ""))}</h3>'
            f'<span class="row-meta"><span>{esc(d.get("publisher_ar", ""))}</span><span>{esc(date_ar(d.get("date")))}</span></span></span>'
            f'<span class="row-end"><span class="nature">{esc(d.get("nature_ar", ""))}</span><span class="mono">{esc(d["id"])}</span></span></a></li>')


def rule_short(r):
    a = r.get('article_ar', '')
    for pre in ('المادتان ', 'المادة ', 'القاعدة '):
        if a.startswith(pre):
            return ('قاعدة ' if pre == 'القاعدة ' else 'م ') + a[len(pre):]
    return a


def rule_row(r, rel):
    n = len(r['inc_ids'])
    return (f'<li data-branch="{esc(r.get("branch", ""))}" data-text="{esc(r.get("title_ar", "") + " " + r.get("article_ar", "") + " " + r.get("article_en", ""))}">'
            f'<a class="row row-rule" href="{rel}law/{slug(r["id"])}.html" data-cord-to="{r["id"]}">'
            f'<span class="row-thumb rule-face" aria-hidden="true"><span>{esc(rule_short(r))}</span></span>'
            f'<span class="row-body"><span class="tag-kind">{esc(r.get("instrument_ar", ""))}</span><h3>{esc(r.get("title_ar", ""))}</h3>'
            f'<span class="row-meta"><span>{esc(r.get("article_ar", ""))}</span><span class="mono">{esc(r.get("article_en", ""))}</span></span></span>'
            f'<span class="row-end"><span class="small"><b>{n}</b> {"واقعة مرتبطة" if n == 1 else "وقائع مرتبطة"}</span></span></a></li>')


def ev_row(ev, rel):
    kind, ic = EV_KIND.get(ev.get('type'), ('مادة', 'doc'))
    inc = INC_BY_ID[ev['incident']]
    st = ev_state(ev)
    ph = EV_PHOTO.get(ev['id'])
    ph = ph if ph in PHOTO_SIZE else None
    return (f'<li data-type="{esc(ev.get("type", ""))}" data-state="{st}" data-text="{esc(ev.get("desc_ar", "") + " " + inc["title_ar"])}">'
            f'<a class="row" href="{rel}evidence/{slug(ev["id"])}.html" data-cord-to="{ev["id"]}">'
            f'{thumb(ph, rel) if ph else f"<span class=\"row-thumb is-blank\" aria-hidden=\"true\">{icon(ic)}</span>"}'
            f'<span class="row-body"><span class="tag-kind">{esc(kind)} · {esc(ev.get("source", ""))}</span><h3>{esc(ev.get("desc_ar", ""))}</h3>'
            f'<span class="row-meta"><span>{esc(inc["title_ar"])}</span><span>{esc(date_ar(ev.get("date")))}</span></span></span>'
            f'<span class="row-end">{seal_row(st, illus=False)}<span class="mono">{esc(ev["id"])}</span></span></a></li>')


def write_json_index():
    idx = []
    for p in PERSONS:
        idx.append({'type': 'person', 'id': p['id'], 'title': p['name_ar'], 'sub': STATUS[p['status']][0] + ' · ' + p.get('role_ar', ''),
                    'url': f'people/{slug(p["id"])}.html', 'k': p.get('name_en', '') + ' ' + ' '.join(p.get('crimes_ar', [])), 'seal': VERIF[state_of(p['id'], 'complete')][1]})
    for i in INCIDENTS:
        idx.append({'type': 'incident', 'id': i['id'], 'title': i['title_ar'], 'sub': date_ar(i['date']) + ' · ' + i.get('place_ar', ''),
                    'url': f'incidents/{slug(i["id"])}.html', 'k': ' '.join(i.get('type_ar', [])) + ' ' + REGIONS.get(i.get('region'), ''), 'seal': VERIF[state_of(i['id'])][1]})
    for e in EVIDENCE:
        idx.append({'type': 'evidence', 'id': e['id'], 'title': e.get('desc_ar', ''), 'sub': EV_KIND.get(e.get('type'), ('',))[0] + ' · ' + e.get('source', ''),
                    'url': f'evidence/{slug(e["id"])}.html', 'k': INC_BY_ID[e['incident']]['title_ar'], 'seal': VERIF[ev_state(e)][1]})
    for d in DOCS:
        idx.append({'type': 'report', 'id': d['id'], 'title': d.get('title_ar', ''), 'sub': d.get('publisher_ar', '') + ' · ' + date_ar(d.get('date')),
                    'url': f'reports/{slug(d["id"])}.html', 'k': ' '.join([d.get('title_en', ''), d.get('symbol', '') or '', d.get('nature_ar', '')]), 'seal': 'whole'})
    for r in RULES:
        idx.append({'type': 'rule', 'id': r.get('article_en', r['id']), 'title': r.get('title_ar', ''), 'sub': r.get('instrument_ar', '') + ' · ' + r.get('article_ar', ''),
                    'url': f'law/{slug(r["id"])}.html', 'k': r.get('article_ar', '') + ' ' + r.get('paraphrase_ar', ''), 'seal': 'whole'})
    for t, u, k in [('كيف نتحقق', 'method.html', 'منهجية التحقق الأختام'), ('أرسل مادة للمراجعة', 'submit.html', 'ساهم أضف واقعة دليل'),
                    ('ادعم التوثيق المستقل', 'donate.html', 'تبرع'), ('عن موثّق', 'about.html', 'الرؤية الرسالة'),
                    ('المعايير القانونية والأخلاقية', 'standards.html', 'تصحيح رد خصوصية'), ('الهوية البصرية', 'identity.html', 'شعار ألوان خط')]:
        idx.append({'type': 'page', 'id': '', 'title': t, 'sub': '', 'url': u, 'k': k, 'seal': 'whole'})
    open(R('assets', 'js', 'index.js'), 'w', encoding='utf-8').write(S.json_js('MW_INDEX', idx))
    return len(idx)


if __name__ == '__main__':
    import pages  # noqa: E402  (page templates live in pages.py)
    pages.build()
