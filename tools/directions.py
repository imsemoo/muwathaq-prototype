"""The page the client opens to choose between the two directions: directions.html at the site root.

python tools/directions.py   (from the project root; previews in assets/img/directions/, captured from both home pages)

It is set in neither direction's type or colour, so the comparison is not tilted: system Arabic UI type on white,
each direction's own name in its own face, and each one's real home page as its preview.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import esc, plain  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIRS = [
    {
        'key': 'a', 'letter': 'أ', 'name': 'الحِرْز', 'face': 'A', 'home': 'index.html', 'identity': 'identity.html',
        'thesis': 'كل سجل حرز مختوم ضد العبث، يفض أمام القارئ.',
        'from': 'تحريز الأدلة في الإجراءات الجنائية العربية: لفافة بخيط، وختم بالشمع، وبطاقة عهدة.',
        'inks': [('#15171A', 'الحبر'), ('#EEF0F2', 'الطاولة'), ('#FFFFFF', 'الورق'), ('#B0241C', 'الشمع')],
        'logo': 'assets/brand/wordmark.svg', 'mark': 'assets/brand/mark.svg',
        'built': 'الهوية وكل صفحات الموقع (197 صفحة)',
    },
    {
        'key': 'b', 'letter': 'ب', 'name': 'المتن والحاشية', 'face': 'B', 'home': 'b/index.html', 'identity': 'b/identity.html',
        'thesis': 'كل جملة هنا ومعها سندها في الهامش.',
        'from': 'حواشي المخطوطات العربية وعلامات النساخ (صح، بلغ، معا، خ، كذا)، وهوامش التقارير الحقوقية.',
        'inks': [('#111417', 'الحبر'), ('#E9EDF0', 'الحاشية'), ('#FFFFFF', 'الورق'), ('#2B44B8', 'اللازورد')],
        'logo': 'b/assets/brand/wordmark.svg', 'mark': 'b/assets/brand/mark.svg',
        'built': 'الهوية والصفحة الرئيسية',
    },
]

ROWS = [
    ('الفكرة', 'السجل حرز: يلف ويربط ويختم، ولا يفتح إلا أمام القارئ.', 'الصفحة متن وحاشية: لكل جملة رقم، ولكل رقم سند.'),
    ('الشعار', 'الكلمة بخط فازيرمتن وشدتها بالشمع الأحمر، وختم شمع عليه حرف الثاء.', 'الكلمة بخط النسخ ولحقها يخرج إلى الهامش موقعا بكلمة صح، ومربع صح أبيض على اللازورد.'),
    ('الألوان', 'حبر، وطاولة رمادية باردة، وأحمر الشمع للختم وحده: ختم واحد في كل شاشة.', 'حبر، وحاشية رمادية باردة، ولازورد الناسخ لكل سند وعلامة.'),
    ('الخط', 'فازيرمتن لكل النصوص، وريد هات مونو للبيانات.', 'نسخ للمتن، وكوفي للحاشية والواجهة، وفراجمنت مونو للبيانات.'),
    ('حالة التحقق', 'حالة الختم: مكتمل، نصفي، ثلاث نقاط، مشقوق للمراجعة.', 'علامات النساخ: صح، معا، كذا، بلغ، خ، مع كلمتها الواضحة.'),
    ('الوضع القانوني', 'حبل بخمس عقد من الادعاء إلى الحكم.', 'سلم مسطر بخمس خانات، الحالية باللازورد.'),
    ('الحركة', 'افتتاحية يسقط فيها الشمع ويضغط الختم، وخيوط حقيقية تتدلى وتشد بين السجلات المرتبطة، وحرز واقعة يبنى مع التمرير.',
     'افتتاحية يكتب فيها الناسخ الكلمة ويمد لحقها ويوقعها صح، ومقابلة تشطب فيها الرواية الأولى ولا تمحى، وسند يرسم حلقة حلقة.'),
    ('الإحساس', 'مادي وجليل: غرفة أحراز ومحكمة.', 'علمي وهادئ: صفحة باحث ومكتبة.'),
    ('الخطر', 'قد يقرأ الختم والشمع قراءة حرفية لاسم موثّق، والأحمر يجب أن يبقى للختم وحده.', 'إن صغر الهامش أو خجل قرب من شكل الموسوعات؛ علاماته تحتاج دائما كلمة تشرحها.'),
]


def card(d):
    inks = ''.join(f'<li><span style="background:{h}"></span>{esc(n)}</li>' for h, n in d['inks'])
    return f'''<article class="dir dir-{d["key"]}" aria-labelledby="h-{d["key"]}">
  <a class="shot" href="{d["home"]}"><img src="assets/img/directions/{d["key"]}.webp" alt="الصفحة الرئيسية في الاتجاه {d["letter"]}" width="1200" height="717" loading="eager"></a>
  <div class="dir-body">
   <p class="dir-letter">الاتجاه {d["letter"]}</p>
   <h2 id="h-{d["key"]}" class="dir-name face-{d["face"]}">{d["name"]}</h2>
   <p class="dir-thesis face-{d["face"]}">{esc(d["thesis"])}</p>
   <p class="dir-from">{esc(d["from"])}</p>
   <div class="dir-brand"><img src="{d["logo"]}" alt="شعار الاتجاه {d["letter"]}" height="56"><img class="dir-mark" src="{d["mark"]}" alt="" width="44" height="44"></div>
   <ul class="inks">{inks}</ul>
   <p class="dir-built">المبني الآن: {esc(d["built"])}</p>
   <div class="dir-links"><a class="go" href="{d["home"]}">افتح الصفحة الرئيسية</a><a href="{d["identity"]}">الهوية البصرية</a></div>
  </div>
 </article>'''


def main():
    rows = ''.join(f'<tr><th scope="row">{esc(r)}</th><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for r, a, b in ROWS)
    html = f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>موثّق — اتجاهان للهوية</title>
<meta name="description" content="اتجاهان للهوية البصرية لمنصة موثّق على السجلات الحقيقية نفسها: الحرز، والمتن والحاشية.">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>
@font-face {{ font-family: "A"; src: url("assets/fonts/vazirmatn.woff2") format("woff2"); font-weight: 400 900; font-display: swap; }}
@font-face {{ font-family: "B"; src: url("b/assets/fonts/naskh.woff2") format("woff2"); font-weight: 400 700; font-display: swap; }}
:root {{ --ink: #14171A; --mute: #5A626B; --line: #D8DDE2; --bg: #F3F5F7; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: var(--bg); color: var(--ink); font: 400 16px/1.8 system-ui, "Segoe UI", Tahoma, sans-serif; }}
a {{ color: inherit; }}
a:focus-visible {{ outline: 2px solid var(--ink); outline-offset: 3px; border-radius: 6px; }}
.wrap {{ max-width: 1320px; margin-inline: auto; padding-inline: clamp(16px, 3.4vw, 48px); }}
header {{ padding-block: clamp(32px, 5vw, 64px) clamp(20px, 3vw, 36px); }}
.kick {{ font-size: 14px; font-weight: 700; color: var(--mute); }}
h1 {{ font: 800 clamp(1.875rem, 1.3rem + 2vw, 3rem)/1.35 "A", system-ui, sans-serif; margin-top: 6px; }}
header p.lead {{ max-width: 68ch; margin-top: 10px; font-size: 1.0625rem; color: #343A41; }}
.dirs {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: clamp(16px, 2.4vw, 32px); }}
.dir {{ background: #fff; border-radius: 24px; overflow: hidden; box-shadow: 0 1px 0 rgb(20 23 26 / .05), 0 24px 48px -32px rgb(20 23 26 / .45); display: grid; grid-template-rows: auto 1fr; min-width: 0; }}
.shot {{ display: block; border-bottom: 1px solid var(--line); overflow: hidden; }}
.shot img {{ width: 100%; height: auto; display: block; transition: transform .6s cubic-bezier(.22,.8,.2,1); }}
.shot:hover img {{ transform: scale(1.015); }}
.dir-body {{ display: grid; gap: 10px; align-content: start; padding: clamp(20px, 2.6vw, 32px); }}
.dir-letter {{ font-size: 13px; font-weight: 700; color: var(--mute); }}
.dir-name {{ font-size: clamp(1.75rem, 1.3rem + 1.4vw, 2.5rem); line-height: 1.35; }}
.face-A {{ font-family: "A", system-ui, sans-serif; font-weight: 900; }}
.face-B {{ font-family: "B", serif; font-weight: 700; }}
.dir-thesis {{ font-size: 1.25rem; line-height: 1.7; }}
.dir-thesis.face-A {{ font-weight: 700; }}
.dir-from {{ font-size: 15px; color: var(--mute); }}
.dir-brand {{ display: flex; align-items: center; gap: 18px; padding: 14px 0; border-block: 1px dashed var(--line); margin-top: 6px; }}
.dir-brand img {{ height: 52px; width: auto; }}
.dir-brand .dir-mark {{ height: 44px; width: 44px; }}
.inks {{ list-style: none; display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 13.5px; color: #343A41; }}
.inks li {{ display: flex; align-items: center; gap: 7px; }}
.inks span {{ width: 18px; height: 18px; border-radius: 6px; box-shadow: inset 0 0 0 1px rgb(20 23 26 / .16); }}
.dir-built {{ font-size: 14px; font-weight: 600; }}
.dir-links {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 6px; }}
.dir-links a {{ display: inline-flex; align-items: center; min-height: 46px; padding: 0 18px; border-radius: 14px; font-weight: 700; text-decoration: none; box-shadow: inset 0 0 0 1.5px var(--ink); }}
.dir-links a.go {{ background: var(--ink); color: #fff; }}
.dir-a .dir-links a.go:hover {{ background: #B0241C; box-shadow: none; }}
.dir-b .dir-links a.go:hover {{ background: #2B44B8; box-shadow: none; }}
section.cmp {{ padding-block: clamp(36px, 5vw, 64px); }}
h2.h {{ font: 800 1.5rem/1.5 "A", system-ui, sans-serif; margin-bottom: 14px; }}
.table {{ background: #fff; border-radius: 20px; overflow: hidden; box-shadow: 0 24px 48px -36px rgb(20 23 26 / .4); overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; min-width: 640px; }}
th, td {{ text-align: start; vertical-align: top; padding: 14px 18px; border-top: 1px solid var(--line); font-size: 15px; line-height: 1.8; }}
thead th {{ border-top: 0; font-size: 14px; background: #fff; }}
thead th.ta {{ font-family: "A", sans-serif; font-weight: 900; font-size: 18px; }}
thead th.tb {{ font-family: "B", serif; font-weight: 700; font-size: 19px; }}
tbody th {{ width: 16%; font-weight: 700; white-space: nowrap; color: #343A41; }}
td {{ width: 42%; }}
.foot-note {{ margin-top: 16px; font-size: 14px; color: var(--mute); }}
@media (max-width: 900px) {{ .dirs {{ grid-template-columns: minmax(0, 1fr); }} }}
</style>
</head>
<body>
<header class="wrap">
 <p class="kick">موثّق MUWATHAQ · للاختيار</p>
 <h1>اتجاهان للهوية البصرية</h1>
 <p class="lead">الاتجاهان مبنيان على السجلات الحقيقية نفسها: الأشخاص والوقائع والأدلة والوثائق والقواعد. افتح كل واحد وتنقل فيه، ثم اختر الاتجاه الذي نكمل به كل الصفحات. الاختيار يغير الهوية والإحساس، لا المحتوى ولا المنهجية.</p>
</header>
<main>
 <div class="wrap dirs">{"".join(card(d) for d in DIRS)}</div>
 <section class="cmp wrap" aria-labelledby="cmp-h">
  <h2 class="h" id="cmp-h">مقارنة سريعة</h2>
  <div class="table"><table><thead><tr><th scope="col"><span class="sr" style="position:absolute;clip:rect(0 0 0 0)">البند</span></th><th scope="col" class="ta">أ · الحرز</th><th scope="col" class="tb">ب · المتن والحاشية</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="foot-note">نموذج تصميم: حالات التحقق والعهدة في الاتجاهين توضيحية، والوثائق والوقائع والأوضاع القانونية حقيقية ومنسوبة إلى مصادرها.</p>
 </section>
</main>
</body>
</html>
'''
    open(os.path.join(ROOT, 'directions.html'), 'w', encoding='utf-8').write(plain(html))
    print('directions.html')


if __name__ == '__main__':
    main()
