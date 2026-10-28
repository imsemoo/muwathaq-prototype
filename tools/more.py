"""The fixed pages: method, submit, donate, about, standards, search, identity, sources, 404."""
import build as B
import shell as S
from pages import P, archive_card
from shell import esc, icon, seal, seal_row, knots, ext, mono, VERIF, STATUS, KNOTS

STEPS = [
    ('جمع المادة', 'من مصدر يمكن تحديده، مع تسجيل كيفية الحصول عليها.'),
    ('تسجيل المصدر والعهدة', 'تاريخ الحصول على المادة، ومن سلّمها، ونسخة مرجعية تُحسب بصمتها الرقمية فور حفظها.'),
    ('فحص الأصالة والسياق', 'البيانات الوصفية وآثار التعديل، وأول ظهور للمادة على الإنترنت.'),
    ('المقارنة المستقلة', 'مطابقة المادة بمصدرين مستقلين على الأقل، وتوثيق كل تعارض.'),
    ('التحقق الجغرافي والزمني', 'تحديد الموقع والتاريخ بمطابقة المعالم والظلال وصور الأقمار الصناعية عند الإمكان.'),
    ('توثيق القيود', 'تسجيل الشكوك والثغرات صراحة داخل السجل، لا خارجه.'),
    ('المراجعة القانونية', 'فحص عناصر القاعدة ووجه صلتها بالوقائع من مختصين في القانون الدولي.'),
    ('حماية الأشخاص', 'إخفاء ما قد يعرّض الضحايا أو الشهود أو المساهمين للخطر، وتقريب المواقع الحساسة.'),
    ('قرار النشر', 'اعتماد موثّق بمستوى التحقق، أو الحفظ دون نشر.'),
    ('التصحيح المستمر', 'تحديث السجل عند ظهور أدلة جديدة، وتسجيل كل تغيير في سجل العهدة.'),
]


def method():
    rel = ''
    steps = ''.join(f'<li><span class="k">{n:02d}</span><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>' for n, (t, d) in enumerate(STEPS, 1))
    key = ''.join(f'<li>{seal(k, label=False)}<span><b>{esc(v[0])}</b><small>{esc(v[2])}</small></span></li>' for k, v in VERIF.items())
    ladder = ''.join(f'<li><b>{esc(STATUS[s][0])}</b><span>{esc(STATUS[s][2])}</span></li>' for s in ['alleged', 'named', 'charged', 'warrant', 'convicted'])
    main = f'''<div class="wrap">{S.crumbs(rel, [("كيف نتحقق", None)])}</div>
<section class="list-head"><div class="wrap"><h1 class="h1">كيف نتحقق</h1><p class="lead">التوثيق عملية متعددة المراحل. اكتمال الفحص الرقمي لمادة لا يعني ثبوت كل ادعاء مرتبط بها، ولا نستخدم كلمة «مؤكد» بمعنى ثبوت المسؤولية الجنائية لأي شخص.</p></div></section>
<section class="sec"><div class="wrap method-grid">
 <div class="method-main read"><h2 class="h2">عشر خطوات قبل الختم</h2><ol class="steps" data-tie>{steps}</ol>
 {B.photo_fig(B.PICKS['section']['method'], rel, sizes="(min-width: 1024px) 760px, 100vw") if B.PICKS.get('section', {}).get('method') in B.PHOTO_SIZE else ''}
 <h2 class="h2">ثلاثة فصول لا نخلطها</h2>
 <div class="triad">
  <div><h3 class="h3">الدليل</h3><p>مادة يمكن فحص أصالتها وسياقها: صورة، مقطع، وثيقة، صورة أقمار صناعية.</p></div>
  <div><h3 class="h3">الادعاء</h3><p>رواية لم تثبت بعد، تُنسب إلى قائلها وتُعرض كما وردت.</p></div>
  <div><h3 class="h3">الاستنتاج</h3><p>تحليل نستخلصه من الأدلة، ونذكر حدوده وما يلزم لإثباته.</p></div>
 </div>
 <h2 class="h2">كيف نستخدم التقارير</h2>
 <ol class="prose numbered"><li>نحدد طبيعة الوثيقة: قضائية، أممية، لجنة تحقيق، حقوقية، صحفية، أو رأي بحثي.</li><li>نفحص مصادرها ومنهجيتها ونطاقها الزمني والجغرافي.</li><li>نميّز بين ما تثبته وما ترجّحه وما تنقله عن غيرها.</li><li>نقارن استنتاجاتها بمصادر مستقلة وروايات مغايرة عند وجودها.</li><li>نوثّق حدود الاستدلال بكل وثيقة داخل ملف الواقعة أو الشخص.</li></ol>
 <h2 class="h2" id="illustrative">ما الحقيقي وما التوضيحي في هذا النموذج</h2>
 <div class="sheet two-col-note">
  <div><h3 class="h3">حقيقي ومربوط بأصله</h3><ul class="prose"><li>الوثائق القضائية والأممية والحقوقية، بعناوينها ورموزها وتواريخها.</li><li>الوقائع كما وردت في مصادرها، والروايات منسوبة إلى أصحابها.</li><li>الأوضاع القانونية للأشخاص بجهاتها وتواريخها.</li><li>نصوص المواد القانونية من مصادرها الرسمية.</li><li>الصور بمكانها وتاريخها ومصورها وترخيصها.</li></ul></div>
  <div><h3 class="h3">توضيحي لعرض طريقة العمل</h3><ul class="prose"><li>حالات التحقق الخاصة بالمنصة (الأختام) على السجلات.</li><li>سجلات العهدة وتواريخها.</li><li>أرقام الملفات المرجعية <span class="mono">P-0001</span> و<span class="mono">INC-0001</span>.</li><li>نماذج الإرسال والتصحيح والتبرع: لا ترسل أي بيانات.</li></ul></div>
 </div>
</div>
 <aside class="method-side">
  <div class="sheet"><h2 class="h3">أختام التحقق</h2><p class="small mute">الختم يصف المادة أو الواقعة، لا الأشخاص.</p><ul class="seal-key seal-key-1">{key}</ul></div>
  <div class="sheet"><h2 class="h3">عُقد المسار القضائي</h2><p class="small mute">العقد تصف الوضع القانوني للأشخاص فقط، بجهة وتاريخ.</p>{knots("warrant")}<ol class="ladder">{ladder}</ol></div>
 </aside>
</div></section>
'''
    P(rel, 'method.html', 'كيف نتحقق', 'منهجية التحقق في موثّق: عشر خطوات، وأختام التحقق، وعقد المسار القضائي.', 'method', main)


PIPE = ['استلام المادة', 'رقم مرجعي للمساهم', 'فحص أولي للمخاطر', 'التحقق من المصدر والأصالة', 'مراجعة قانونية وحقوقية', 'القرار', 'إخفاء البيانات الحساسة', 'إبلاغ المساهم إن كان آمنًا']
REGION_OPTS = [('gaza', 'غزة'), ('westbank', 'الضفة الغربية'), ('jerusalem', 'القدس الشرقية'), ('lebanon', 'جنوب لبنان'), ('detention', 'مرفق احتجاز'), ('other', 'أخرى')]
TYPE_OPTS = ['استهداف المدنيين', 'هجوم على منشأة طبية', 'عرقلة الإغاثة الإنسانية', 'التهجير القسري', 'هدم أو تدمير ممتلكات', 'الاحتجاز التعسفي أو سوء المعاملة', 'استهداف صحفيين أو عاملين إنسانيين', 'عنف المستوطنين', 'أخرى']


def field(fid, label, control, req=False, help_='', err='', cls=''):
    star = ' <span aria-hidden="true">*</span>' if req else ''
    return (f'<div class="field {cls}"><label for="{fid}">{label}{star}</label>{control}'
            f'{f"<p class=\"help\" id=\"{fid}-h\">{help_}</p>" if help_ else ""}'
            f'<p class="err" id="{fid}-e">{seal("rereview", label=False)}<span>{err}</span></p></div>')


def submit():
    rel = ''
    regions = ''.join(f'<option value="{v}">{t}</option>' for v, t in REGION_OPTS)
    types = ''.join(f'<option>{t}</option>' for t in TYPE_OPTS)
    mats = ''.join(f'<label class="check"><input type="checkbox" name="mat" value="{v}" data-review="نوع المادة"> {v}</label>' for v in ['صورة', 'فيديو', 'وثيقة', 'رابط إلكتروني', 'شهادة', 'أخرى'])
    pipe = ''.join(f'<li><i></i><span>{t}</span></li>' for t in PIPE)
    prog = ''.join(f'<li><i></i><span>{t}</span></li>' for t in ['الواقعة', 'المادة', 'السلامة', 'المراجعة'])
    main = f'''<div class="wrap">{S.crumbs(rel, [("أرسل مادة للمراجعة", None)])}</div>
<section class="list-head"><div class="wrap"><h1 class="h1">أرسل مادة للمراجعة</h1><p class="lead">لا تنشر المنصة أي مادة تلقائيًا. تخضع كل مساهمة للمراجعة والتحقق قبل اتخاذ قرار بنشرها أو حفظها دون نشر.</p></div></section>
<section class="sec"><div class="wrap submit-grid">
 <div class="submit-main">
  <p class="note warn">{icon("shield")}<span><b>قبل أن تبدأ:</b> لا ترسل معلومات قد تعرّضك أو تعرّض الشهود أو الضحايا للخطر، ولا تدرج عناوين دقيقة أو وجوهًا يمكن التعرف عليها دون موافقة. هذا النموذج يعمل داخل متصفحك فقط ولا يرسل أي بيانات.</span></p>
  <ol class="progress" data-progress aria-label="مراحل الإرسال">{prog}</ol>
  <form class="sheet wizard" data-wizard="sent" novalidate>
   <fieldset data-step="1"><legend class="h2">الواقعة</legend>
    {field("s-title", "عنوان الواقعة", '<input class="input" id="s-title" name="title" required maxlength="160" data-review="العنوان" aria-describedby="s-title-h s-title-e">', True, "عنوان مختصر ومحايد يصف ما حدث، دون أوصاف تجريمية.", "اكتب عنوانًا وصفيًا للواقعة.")}
    {field("s-desc", "وصف الواقعة ومصدر معرفتك بها", '<textarea class="input" id="s-desc" name="desc" required minlength="30" data-review="الوصف" aria-describedby="s-desc-h s-desc-e"></textarea>', True, "ماذا تعرف، وكيف عرفته، وما الذي لم تتمكن من التحقق منه.", "اكتب وصفًا لا يقل عن 30 حرفًا.")}
    <div class="grid-2">
     {field("s-date", "تاريخ الواقعة أو بدايتها", '<input class="input" id="s-date" name="date" type="date" required data-review="التاريخ" aria-describedby="s-date-e">', True, "", "حدد التاريخ، ولو تقريبيًا.")}
     {field("s-date2", "نهاية الفترة (اختياري)", '<input class="input" id="s-date2" name="date2" type="date">')}
     {field("s-region", "المنطقة", f'<select class="select" id="s-region" name="region" required data-review="المنطقة" aria-describedby="s-region-e"><option value="">اختر</option>{regions}</select>', True, "", "اختر المنطقة.")}
     {field("s-type", "نوع الواقعة", f'<select class="select" id="s-type" name="type" required data-review="نوع الواقعة" aria-describedby="s-type-e"><option value="">اختر</option>{types}</select>', True, "", "اختر نوع الواقعة.")}
    </div>
    {field("s-loc", "الموقع التقريبي إن كان آمنًا", '<input class="input" id="s-loc" name="loc" placeholder="حي أو بلدة، لا عنوانًا دقيقًا" data-review="الموقع">')}
    <div class="wizard-nav"><button class="btn btn-ink" type="button" data-next>التالي: المادة {icon("arrow")}</button></div>
   </fieldset>
   <fieldset data-step="2" hidden><legend class="h2">المادة</legend>
    <div class="field" data-group="mat"><span class="lab">نوع المادة <span aria-hidden="true">*</span></span><div class="checks">{mats}</div><p class="err">{seal("rereview", label=False)}<span>اختر نوع مادة واحدًا على الأقل.</span></p></div>
    <div class="field"><span class="lab">الملفات (تبقى على جهازك في هذا النموذج)</span><label class="drop">{icon("upload")}<span><b>اختر ملفات</b> JPG أو PNG أو PDF أو MP4 أو WEBM، حتى 25 ميغابايت للملف وخمسة ملفات</span><input class="sr" type="file" multiple accept=".jpg,.jpeg,.png,.pdf,.mp4,.webm" data-files="file-list"></label><ul class="file-list" id="file-list"></ul></div>
    {field("s-url", "رابط المصدر الأصلي", '<input class="input ltr-input" id="s-url" name="url" type="url" placeholder="https://" data-review="رابط المصدر" aria-describedby="s-url-e">', False, "", "اكتب رابطًا صحيحًا يبدأ بـ https://")}
    {field("s-how", "كيف حصلت على المادة؟", '<select class="select" id="s-how" name="how" data-review="طريقة الحصول"><option value="">اختر</option><option>صوّرتها بنفسي</option><option>تلقيتها من مصدرها مباشرة</option><option>من منصة تواصل اجتماعي</option><option>من موقع إعلامي أو مؤسسي</option><option>أخرى</option></select>')}
    <div class="wizard-nav"><button class="btn btn-line" type="button" data-back>{icon("prev")} السابق</button><button class="btn btn-ink" type="button" data-next>التالي: السلامة {icon("arrow")}</button></div>
   </fieldset>
   <fieldset data-step="3" hidden><legend class="h2">السلامة والتواصل</legend>
    <div class="field"><span class="lab">هل تتضمن المادة بيانات شخصية أو حساسة؟</span><div class="radios"><label class="check"><input type="radio" name="sens" value="نعم" data-review="بيانات حساسة"> نعم</label><label class="check"><input type="radio" name="sens" value="لا"> لا</label><label class="check"><input type="radio" name="sens" value="غير متأكد" checked> غير متأكد</label></div></div>
    <div class="field"><span class="lab">هل توافق على أن نتواصل معك عند الحاجة؟</span><div class="radios"><label class="check"><input type="radio" name="contact" value="yes"> نعم</label><label class="check"><input type="radio" name="contact" value="no" checked> لا</label></div></div>
    <div id="contact-field" hidden>{field("s-contact", "وسيلة تواصل آمنة", '<input class="input" id="s-contact" name="contactv" placeholder="بريد مشفّر أو تطبيق آمن">', False, "الاسم الحقيقي غير مطلوب.")}</div>
    <div class="wizard-nav"><button class="btn btn-line" type="button" data-back>{icon("prev")} السابق</button><button class="btn btn-ink" type="button" data-next>التالي: المراجعة {icon("arrow")}</button></div>
   </fieldset>
   <fieldset data-step="review" hidden><legend class="h2">راجع قبل الإرسال</legend>
    <dl class="fields review" data-review-out></dl>
    <div class="field"><label class="check"><input type="checkbox" id="s-decl" required> أقرّ بأن المعلومات صحيحة بحسب علمي، وأنني لم أعدّل المواد بما يغيّر مضمونها. <span aria-hidden="true">*</span></label><p class="err">{seal("rereview", label=False)}<span>هذا الإقرار مطلوب.</span></p></div>
    <div class="field"><label class="check"><input type="checkbox" id="s-priv" required> أوافق على <a href="standards.html#privacy">سياسة الخصوصية</a> وشروط الإرسال. <span aria-hidden="true">*</span></label><p class="err">{seal("rereview", label=False)}<span>الموافقة مطلوبة.</span></p></div>
    <div class="wizard-nav"><button class="btn btn-line" type="button" data-back>{icon("prev")} السابق</button><button class="btn btn-ink" type="submit">إرسال للمراجعة (تجريبي)</button></div>
   </fieldset>
  </form>
  <div class="sheet sent" id="sent" hidden tabindex="-1">
   <div class="sent-seal">{seal("in_progress", wax=True, label=False)}</div>
   <h2 class="h2">سُجّلت مساهمتك في هذا المتصفح</h2>
   <p>رقمك المرجعي: <span class="mono ref" data-ref></span></p>
   <p class="small mute">في المنصة الفعلية تُستلم المادة عبر قناة مشفّرة وتظهر حالتها بهذا الرقم. هنا لم يُرسل شيء إلى أي خادم ولم يُحفظ بعد إغلاق الصفحة.</p>
   <ol class="cord-steps cord-steps-light">{"".join(f'<li class="{"is-now" if n == 0 else ""}"><i></i><span>{t}</span></li>' for n, t in enumerate(["مستلمة", "قيد الفحص الأولي", "قيد التحقق الرقمي", "قيد المراجعة القانونية", "القرار"]))}</ol>
   <a class="btn btn-line" href="index.html">العودة إلى الرئيسية</a>
  </div>
 </div>
 <aside class="submit-side">
  <div class="sheet"><h2 class="h3">مسار كل مساهمة</h2><ol class="cord-steps cord-steps-v">{pipe}</ol>
   <p class="small mute">القرار: النشر، أو طلب معلومات إضافية، أو الرفض، أو الحفظ دون نشر.</p></div>
  <div class="sheet"><h2 class="h3">في المنصة الفعلية</h2><ul class="ticks small"><li>تشفير أثناء النقل والتخزين</li><li>فحص الملفات من البرمجيات الضارة</li><li>فصل الأصول عن نسخ النشر</li><li>سجل لكل وصول وتعديل</li><li>صلاحيات متدرجة للمراجعين</li><li>حق سحب المساهمة أو حذف البيانات</li></ul></div>
 </aside>
</div></section>'''
    P(rel, 'submit.html', 'أرسل مادة للمراجعة', 'أرسل واقعة أو دليلًا لمراجعة فريق موثّق. لا شيء يُنشر تلقائيًا.', 'submit', main)


def donate():
    rel = ''
    amts = ''.join(f'<label class="amt"><input type="radio" name="amount" value="{a}"{" checked" if a == "25" else ""}><span>{a}<small>دولار</small></span></label>' for a in ['10', '25', '50', '100'])
    uses = [('layers', 'تطوير المنصة وصيانتها', 'البنية التقنية والاستضافة الآمنة والتطوير المستمر.'),
            ('search', 'أدوات التحقق الرقمي والجغرافي', 'تحليل الصور والمقاطع وتحديد الموقع والزمن.'),
            ('scale', 'البحث القانوني', 'المراجعة القانونية وإعداد التقارير التحليلية الدورية.'),
            ('lock', 'حماية البيانات', 'تأمين الأدلة وحماية هويات المساهمين والشهود.')]
    uses_html = ''.join(f'<li>{icon(i)}<div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>' for i, t, d in uses)
    main = f'''<div class="wrap">{S.crumbs(rel, [("ادعم التوثيق المستقل", None)])}</div>
<section class="list-head"><div class="wrap"><h1 class="h1">ادعم التوثيق المستقل</h1><p class="lead">مساهمتك تحفظ الأدلة من الحذف والعبث، وتموّل التحقق الرقمي والمراجعة القانونية، وتبقي المعرفة الموثقة متاحة للباحثين والمؤسسات.</p></div></section>
<section class="sec"><div class="wrap donate-grid">
 <div>
  <h2 class="h2">إلى أين تذهب المساهمات</h2>
  <ul class="uses">{uses_html}</ul>
  <div class="sheet transparency"><h2 class="h3">الشفافية المالية</h2><p>ستُنشر تقارير الشفافية وأوجه الإنفاق هنا بعد تفعيل التبرعات. لا نعرض أهدافًا أو مبالغ أو أعداد مساهمين قبل أن تكون حقيقية.</p>
   <dl class="fields"><div><dt>هدف التمويل</dt><dd>يُحدَّد لاحقًا</dd></div><div><dt>ما جُمع فعليًا</dt><dd>—</dd></div><div><dt>الميزانية التقديرية للسنة الأولى</dt><dd>35,000 دولار أمريكي (من وثيقة المشروع، قابلة للتعديل)</dd></div><div><dt>مصادر التمويل المخططة</dt><dd>منح وشراكات واشتراكات مؤسسية وخدمات بحث</dd></div></dl></div>
 </div>
 <form class="sheet donate-form" data-donate="don-out" novalidate>
  <h2 class="h3">تبرّع</h2>
  <div class="seg seg-radio" role="radiogroup" aria-label="نوع التبرع"><label><input type="radio" name="freq" value="once" checked><span>لمرة واحدة</span></label><label><input type="radio" name="freq" value="monthly"><span>شهريًا</span></label></div>
  <fieldset class="amts"><legend class="lab">المبلغ</legend>{amts}<label class="amt"><input type="radio" name="amount" value="other"><span>مبلغ آخر</span></label></fieldset>
  <div class="field" hidden><label for="d-custom">المبلغ بالدولار</label><input class="input ltr-input" id="d-custom" type="number" min="1" step="1" inputmode="numeric"></div>
  <div class="grid-2">{field("d-name", "الاسم (اختياري)", '<input class="input" id="d-name" autocomplete="name">')}{field("d-email", "البريد (اختياري)", '<input class="input ltr-input" id="d-email" type="email" autocomplete="email">', False, "", "اكتب بريدًا صحيحًا.")}</div>
  <label class="check"><input type="checkbox"> لا تُظهر اسمي في قوائم الشكر العامة إن وُجدت.</label>
  <button class="btn btn-ink btn-block" type="submit" data-donate-btn>متابعة التبرع</button>
  <p class="xs mute">{icon("lock")} بوابة الدفع غير مفعّلة في هذا النموذج. لا نجمع بيانات بطاقات داخل الصفحة؛ يُربط الزر لاحقًا ببوابة دفع معتمدة.</p>
  <div class="note" id="don-out" hidden tabindex="-1">{seal("in_progress", label=False)}<span><b>لم يُحصَّل أي مبلغ.</b> في المنصة الفعلية ينقلك هذا الزر إلى بوابة الدفع الآمنة.</span></div>
 </form>
</div></section>'''
    P(rel, 'donate.html', 'ادعم التوثيق المستقل', 'ادعم موثّق: حفظ الأدلة والتحقق الرقمي والمراجعة القانونية.', 'donate', main)


def about():
    rel = ''
    targets = [('واقعة موثقة', '500'), ('ملف تمت مراجعته', '300'), ('تقرير تحليلي على الأقل', '6'), ('مؤسسة مستفيدة على الأقل', '5'), ('من الملفات المنشورة بسجل تحقق مكتمل', '90%')]
    trows = ''.join(f'<tr><th scope="row" class="num">{v}</th><td>{esc(t)}</td><td>مستهدف</td></tr>' for t, v in targets)
    main = f'''<div class="wrap">{S.crumbs(rel, [("عن موثّق", None)])}</div>
<section class="list-head"><div class="wrap"><h1 class="h1">عن موثّق</h1><p class="lead">بنية رقمية للتوثيق والتحليل القانوني، تحفظ الأدلة المتعلقة بجرائم الاحتلال الإسرائيلي، وتتحقق منها، وتربطها بالقانون الدولي، دعمًا للبحث الحقوقي والمساءلة وحقوق الضحايا.</p></div></section>
<section class="sec"><div class="wrap doc-grid"><div class="read">
 <div class="prose">
  {B.photo_fig(B.PICKS['section']['about'], rel, sizes="(min-width: 1024px) 760px, 100vw") if B.PICKS.get('section', {}).get('about') in B.PHOTO_SIZE else ''}
  <h2>لماذا موثّق</h2><p>الأدلة الرقمية على الجرائم متفرقة، ومعرّضة للحذف والتلاعب، ويصعب التحقق من مصادرها وسياقها. يجمع موثّق في منصة واحدة التوثيق الرقمي والتحقق من الأدلة والتحليل الجغرافي وربط الوقائع بالنصوص القانونية الدولية.</p>
  <h2>لمن</h2><p>منظمات حقوق الإنسان، والمحامون، والباحثون، والصحفيون الاستقصائيون، والمؤسسات الأكاديمية والحقوقية، والجمهور المهتم بالعدالة.</p>
  <h2>الاستقلالية</h2><p>منصة مستقلة لا تتبع أي محكمة أو منظمة دولية أو جهة حكومية، ولا تعلن شراكة غير مثبتة. نعلن منهجيتنا ومصادر تمويلنا، ونفصل بين التوثيق والتحليل والاستنتاج، ونحترم الضمانات القانونية لجميع الأطراف.</p>
  <h2>الهدف الأوسع</h2><p>تعزيز العدالة والمساءلة وسيادة القانون، بما يتوافق مع الهدف 16 من أهداف التنمية المستدامة.</p>
 </div>
 </div>
 <aside class="doc-side"><div class="side-sticky">
  <div class="sheet"><h2 class="h3">مستهدفات السنة الأولى</h2><table class="custody"><caption>من وثيقة المشروع، وليست نتائج محققة <small>تُربط بقاعدة البيانات عند التشغيل</small></caption><tbody>{trows}</tbody></table></div>
  <p class="note">{icon("info")}<span>مدة التنفيذ اثنا عشر شهرًا تشمل التأسيس والتطوير والتوثيق التجريبي والإطلاق والتقييم. الشركاء المستهدفون: منظمات حقوقية وجامعات وخبراء قانونيون ومختصو أدلة رقمية وأمن سيبراني.</span></p>
 </div></aside>
</div></section>'''
    P(rel, 'about.html', 'عن موثّق', 'موثّق: منصة مستقلة للتوثيق الرقمي والتحليل القانوني.', 'about', main)


POLICIES = [
    ('accusation', 'الفرق بين الاتهام والإدانة', 'الإدانة لا تثبت إلا بحكم قضائي من محكمة مختصة. مذكرة التوقيف والاتهام الرسمي والورود في تقرير مراحل أو مصادر مختلفة لا تعني الإدانة، ويُفترض براءة الشخص حتى تثبت إدانته.'),
    ('evidence', 'الأدلة والادعاءات والاستنتاجات', 'الدليل مادة يمكن فحص أصالتها وسياقها، والادعاء رواية لم تثبت بعد، والاستنتاج تحليل نستخلصه من الأدلة. نميّز بين الثلاثة صراحة في كل سجل.'),
    ('limits', 'حدود التحليل القانوني', 'التحليل في المنصة بحثي أولي، لا يحل محل التحقيق الجنائي أو القرار القضائي، ولا يحدد المسؤولية الجنائية لأي شخص.'),
    ('corrections', 'سياسة تصحيح الأخطاء', 'نصحح الأخطاء فور التحقق منها، ونسجل التصحيح في سجل العهدة بتاريخه وطبيعته دون إخفاء الصيغة السابقة إلا لأسباب تتعلق بالسلامة.'),
    ('conflict', 'التعامل مع المصادر المتعارضة', 'نعرض الروايات المتعارضة الجوهرية، بما فيها البيانات الرسمية للأطراف، ونوضح أسباب ترجيح رواية على أخرى إن وُجد ترجيح.'),
    ('privacy', 'حماية البيانات والضحايا والشهود', 'نقلل البيانات المجمّعة، ونخفي المعلومات المعرِّفة، ولا ننشر إحداثيات قد تكشف أماكن الضحايا أو الشهود، ولا ننشر شهادات إلا بموافقة أصحابها، ولا ننشر صورًا للجثث أو الدماء.'),
    ('reply', 'طلب التصحيح وحق الرد', 'يحق لأي شخص أو جهة معنية تقديم طلب تصحيح أو رد. يراجع الطلب فريق مختص، ولا يؤدي تلقائيًا إلى حذف المادة ولا إلى رفض الطلب.'),
    ('removal', 'معايير إزالة المحتوى', 'قد يُزال محتوى أو يُقيَّد عند وجود أسباب قانونية أو أمنية موثقة، مثل تعريض شخص للخطر أو ثبوت عدم صحة المادة.'),
    ('pending', 'المواد قيد التحقق', 'المواد الموسومة «قيد التحقق» لم تستكمل مراجعتها، ولا ينبغي الاستناد إليها كحقائق نهائية.'),
]


def standards():
    rel = ''
    acc = ''.join(f'<details class="acc" id="{k}"{" open" if n == 0 else ""}><summary>{esc(t)}{icon("down")}</summary><div class="acc-body"><p>{esc(b)}</p></div></details>' for n, (k, t, b) in enumerate(POLICIES))
    main = f'''<div class="wrap">{S.crumbs(rel, [("المعايير القانونية والأخلاقية", None)])}</div>
<section class="list-head"><div class="wrap"><h1 class="h1">المعايير القانونية والأخلاقية</h1><p class="lead">القواعد التي تحكم كل سجل في موثّق، وكيف تطلب تصحيحًا أو ردًا على معلومة منشورة.</p></div></section>
<section class="sec"><div class="wrap standards-grid">
 <div>{acc}<p class="xs mute" style="margin-top:18px">آخر تحديث للسياسات: 28 أكتوبر 2026 — نسخة تحتاج مراجعة قانونية قبل الاعتماد.</p></div>
 <form class="sheet" id="correction" data-simple-form="corr-out" data-done="سُجّل طلب التصحيح في هذا المتصفح فقط." novalidate>
  <h2 class="h3">طلب تصحيح أو رد</h2>
  <p class="small mute">للأشخاص أو الجهات المعنية بمعلومة منشورة.</p>
  {field("c-ref", "رقم الملف أو الواقعة", '<input class="input ltr-input" id="c-ref" required placeholder="P-0001 أو INC-0001" aria-describedby="c-ref-e">', True, "", "اكتب رقمًا مرجعيًا.")}
  {field("c-type", "نوع الطلب", '<select class="select" id="c-type" required aria-describedby="c-type-e"><option value="">اختر</option><option>تصحيح معلومة</option><option>حق الرد</option><option>إزالة لأسباب أمنية</option><option>تحديث حالة قانونية</option></select>', True, "", "اختر نوع الطلب.")}
  {field("c-who", "صفة مقدم الطلب", '<select class="select" id="c-who"><option>الشخص المعني</option><option>ممثل قانوني</option><option>جهة رسمية</option><option>أخرى</option></select>')}
  {field("c-body", "التفاصيل والمستندات المرجعية", '<textarea class="input" id="c-body" required minlength="20" aria-describedby="c-body-e"></textarea>', True, "", "اكتب تفاصيل الطلب.")}
  {field("c-contact", "وسيلة تواصل", '<input class="input" id="c-contact" placeholder="بريد إلكتروني أو وسيلة آمنة">')}
  <button class="btn btn-ink btn-block" type="submit">إرسال الطلب (تجريبي)</button>
  <div class="note" id="corr-out" hidden tabindex="-1">{seal("in_progress", label=False)}<span><b>سُجّل الطلب برقم <span class="mono" data-ref></span>.</b> لم يُرسل إلى أي جهة؛ في المنصة الفعلية يراجعه فريق مختص.</span></div>
 </form>
</div></section>'''
    P(rel, 'standards.html', 'المعايير القانونية والأخلاقية', 'معايير موثّق وسياساته، وطلب التصحيح أو الرد.', 'standards', main)


def search():
    rel = ''
    types = [('person', 'ملفات الأشخاص', len(B.PERSONS)), ('incident', 'الوقائع', len(B.INCIDENTS)), ('evidence', 'الأدلة', len(B.EVIDENCE)),
             ('report', 'التقارير والوثائق', len(B.DOCS)), ('rule', 'القواعد القانونية', len(B.RULES)), ('page', 'صفحات', 0)]
    total = sum(n for *_, n in types)
    opts = ''.join(f'<label class="facet-opt"><input type="radio" name="q-type" value="{k}"{" checked" if not k else ""}>'
                   f'<span class="facet-mark" aria-hidden="true"></span><span class="facet-t">{esc(v)}</span><span class="facet-n" data-total-of="{k}">{n or ""}</span></label>'
                   for k, v, n in [('', 'الكل', total)] + types)
    tries = ['رفح', 'مذكرة توقيف', 'الهلال الأحمر', 'هند رجب', 'ICC-01/18', 'المادة 8', 'سلوان', 'المجاعة']
    recent = sorted([(i['date'], B.inc_mini_row(i, rel)) for i in B.INCIDENTS] + [(d.get('date', ''), B.doc_row(d, rel)) for d in B.DOCS], reverse=True)[:6]
    main = f'''<div class="wrap">{S.crumbs(rel, [("البحث", None)])}</div>
<section class="list-head"><div class="wrap"><h1 class="h1">البحث في موثّق</h1>
 <form class="search-page" role="search" onsubmit="return false"><div class="field grow"><label for="q-page">كلمة البحث</label><input class="input input-lg" id="q-page" type="search" placeholder="اسم، رقم ملف، واقعة، جهة، أو مادة قانونية" autofocus></div></form></div></section>
<section class="sec list-sec"><div class="wrap list-grid">
 <aside class="list-side" aria-label="نطاق البحث"><div class="side-sticky" data-lenis-prevent>
  <div class="panel">{archive_card(total, 'مدخلا في فهرس البحث')}
   <fieldset class="facet" id="q-types"><legend class="side-h">النوع</legend>{opts}</fieldset>
   <p class="small mute search-tip">من أي صفحة: اضغط <kbd>/</kbd> لتبدأ البحث، والأسهم للتنقل بين النتائج.</p>
  </div>
 </div></aside>
 <div class="list-main">
  <p class="count" id="results-count" aria-live="polite"></p>
  <ul class="rows" id="results" hidden></ul>
  <div id="search-start">
   <h2 class="side-h">جرّب</h2>
   <div class="tries">{''.join(f'<button class="btn btn-line btn-sm" type="button" data-try="{esc(q)}">{esc(q)}</button>' for q in tries)}</div>
   <h2 class="side-h">أحدث ما أضيف إلى الأرشيف</h2>
   <ul class="rows">{''.join(r for _, r in recent)}</ul>
  </div>
 </div>
</div></section>'''
    P(rel, 'search.html', 'البحث', 'ابحث في ملفات الأشخاص والوقائع والأدلة والوثائق والقواعد.', 'search', main)


def identity():
    rel = ''
    key = ''.join(f'<li>{seal(k, label=False)}<span><b>{esc(v[0])}</b><small>{esc(v[2])}</small></span></li>' for k, v in VERIF.items())
    sw = [('الحبر', '#15171A', 'النص وكل ما يُرسم؛ والبطاقة الرئيسية في كل صفحة تُطبع به مقلوبة.'),
          ('الطاولة', '#EEF0F2', 'أرضية الصفحات: طاولة الأحراز الباردة.'),
          ('الورق', '#FFFFFF', 'البطاقات والأوراق وعمود القراءة.'),
          ('الشمع', '#B0241C', 'الختم وحده: ختم أحمر واحد في كل شاشة، ولا يُستعمل للزينة.'),
          ('الخيط', '#6B737C', 'الخيوط بين السجلات المرتبطة فعلًا، والعناصر غير النصية.'),
          ('الرمادي الثانوي', '#5A626B', 'النص الثانوي بتباين لا يقل عن 4.5:1 على الورق والطاولة.')]
    swatches = ''.join(f'<li><span class="sw" style="background:{h}"></span><b>{esc(n)}</b><span class="mono">{h}</span><small>{esc(d)}</small></li>' for n, h, d in sw)
    main = f'''<div class="wrap">{S.crumbs(rel, [("الهوية البصرية", None)])}</div>
<section class="list-head"><div class="wrap"><h1 class="h1">الهوية البصرية: الحِرْز</h1><p class="lead">في الإجراءات الجنائية العربية يُحرَّز الدليل: يُلف ويُربط بخيط ويُختم بالشمع، فلا يُفتح إلا أمام المحكمة. موثّق يعامل كل معلومة بهذه الطريقة: مربوطة بمصدرها، ومختومة ضد العبث، ومفتوحة أمام القارئ.</p></div></section>
<section class="sec"><div class="wrap id-grid">
 <div class="id-col">
 <div class="sheet id-logo"><h2 class="h2">الشعار</h2>
  <div class="id-lock"><img class="m" src="assets/brand/mark.svg" alt="" width="96" height="96"><img class="w" src="assets/brand/wordmark.svg" alt="موثّق" height="84" width="129"></div>
  <div class="id-lock is-ink"><img class="m" src="assets/brand/mark.svg" alt="" width="72" height="72"><img class="w" src="assets/brand/wordmark-reversed.svg" alt="موثّق" height="64" width="98"></div>
  <div class="prose"><p>الختم يحمل حرف الثاء، أوسط حروف الجذر «و ث ق»: أن تربط الشيء فلا يفلت، ومنه الوثيقة والثقة والموثّق. نقاطه الثلاث مستديرة كقطرات الشمع، وتُقرأ أيضًا كالمصادر الثلاثة المستقلة التي تُطابق بها المعلومة.</p>
  <p>والكلمة مرسومة من خط فازيرمتن الأسود، بنقاط مستديرة وزوايا ملينة، وشدّتها وحدها بلون الشمع: الشدّة علامة التشديد، أي الربط المحكم.</p></div>
 </div>
 <div class="sheet"><h2 class="h2">الألوان: ثلاثة أحبار</h2><ul class="swatches">{swatches}</ul></div>
 </div>
 <div class="id-col">
 <div class="sheet"><h2 class="h2">الأختام: حالة التحقق علامة لا لون</h2><ul class="seal-key">{key}</ul></div>
 <div class="sheet"><h2 class="h2">العُقد: الوضع القانوني للأشخاص</h2>{knots("warrant")}<p class="small" style="margin-top:14px">خمس عقد على حبل واحد من الادعاء إلى الحكم. تُعقد العقدة بجهة وتاريخ، وتبقى العقد التالية ظاهرة مفتوحة حتى لا تُقرأ مذكرة توقيف كأنها حكم.</p></div>
 <div class="sheet"><h2 class="h2">صوت الكتابة</h2>
  <ul class="ticks small"><li>نسند ولا نجزم: «خلصت اللجنة إلى…»، «وجدت الدائرة أسبابًا معقولة للاعتقاد…».</li><li>الحالة القانونية وجهتها وتاريخها قبل الاسم، دائمًا.</li><li>لا أوصاف تجريمية عامة على البطاقات، ولا كلمة «مؤكد» بمعنى ثبوت المسؤولية.</li><li>كل رقم بمصدره كما ورد، وكل رواية منسوبة إلى صاحبها.</li><li>لا تشكيل في العناوين والواجهة، إلا في اسم موثّق والنصوص الرسمية المقتبسة.</li></ul>
 </div>
 <div class="sheet"><h2 class="h2">ما لا نفعله</h2>
  <ul class="ticks small"><li>ختم أحمر ثانٍ في الشاشة نفسها.</li><li>بادجات ملونة للحالات: الحالة علامة مرسومة.</li><li>خيط بين سجلين غير مرتبطين فعلًا.</li><li>صور جثث أو دماء أو وجوه ضحايا دون موافقة.</li><li>أرضيات بيج أو ورق دافئ، أو توهج وزجاج للزينة.</li></ul>
 </div>
 </div>
 <div class="sheet id-type id-wide"><h2 class="h2">الخط</h2><div class="id-type-in"><div class="id-type-spec">
  <p class="display">مطلوب بموجب مذكرة توقيف</p>
  <p class="h1">الوقائع المرتبطة والتحليل القانوني</p>
  <p class="prose">نص القراءة بخط فازيرمتن 18 بكسل وارتفاع سطر 2.0: أصدرت الدائرة التمهيدية الأولى مذكرة توقيف، والمذكرة ليست حكمًا بالإدانة.</p>
  <p class="small mute">البيانات وحدها بخط ريد هات مونو: <span class="mono">P-0001 · ICC-01/18 · SHA-256 3f9a…</span></p>
  </div><table class="custody"><tbody><tr><th>عرض الحالة</th><td>60 بكسل · 900 · سطر 1.4</td></tr><tr><th>عنوان الصفحة</th><td>44 بكسل · 800 · سطر 1.45</td></tr><tr><th>عنوان القسم</th><td>32 بكسل · 800 · سطر 1.5</td></tr><tr><th>القراءة</th><td>18 بكسل · 400 · سطر 2.0 · 68 حرفًا</td></tr><tr><th>الواجهة</th><td>16 بكسل · 400–700 · سطر 1.75</td></tr></tbody></table>
 </div></div>
 <div class="sheet id-motion"><h2 class="h2">الحركة: لحظة واحدة متكررة</h2>
  <p class="small">للهوية حركة واحدة أصيلة: الختم يُضغط والخيط يُشد. لا مؤثرات متفرقة، ولا حركة تخفي المحتوى، وكلها تتوقف عند تفضيل تقليل الحركة.</p>
  <ul class="motion-list">
   <li><div class="demo" data-demo="press"><svg class="seal is-wax" viewBox="0 0 40 40" aria-hidden="true"><use href="#s-whole"/></svg></div><div><h3>ضغطة الختم</h3><p class="small mute">640 مللي ثانية، منحنى ارتداد خفيف؛ عند فتح سجل أو اكتمال فحص.</p><button class="btn btn-line btn-sm" type="button" data-replay="press">أعد الحركة</button></div></li>
   <li><div class="demo demo-cord" data-demo="cord"><svg viewBox="0 0 160 60" aria-hidden="true"><path d="M8 14 Q80 70 152 14"/></svg></div><div><h3>شدّ الخيط</h3><p class="small mute">240 مللي ثانية؛ خيط واحد يشتد حين تقف على السجل المرتبط.</p><button class="btn btn-line btn-sm" type="button" data-replay="cord">شدّ الخيط</button></div></li>
   <li><div class="demo" data-demo="open"><span class="demo-tag"><span class="tag-hole" aria-hidden="true"></span><b>P-0001</b></span></div><div><h3>فتح الحرز</h3><p class="small mute">البطاقة ترتفع 14 بكسل وتظهر، ثم الختم، ثم السطور بتتابع 80 مللي ثانية.</p><button class="btn btn-line btn-sm" type="button" data-replay="open">افتح الحرز</button></div></li>
  </ul>
 </div>
 <div class="sheet"><h2 class="h2">البطاقة والخيط</h2><div class="id-tag">{B.person_mini(B.PERSONS[0], rel, vtn=False) if B.PERSONS else ""}</div><p class="small" style="margin-top:14px">كل سجل بطاقة حرز بثقب يمر منه الخيط. الخيط يُرسم فقط بين سجلات مرتبطة فعلًا، ويشتد خيط واحد في كل مرة حين تقف على السجل المرتبط.</p></div>
</div></section>'''
    P(rel, 'identity.html', 'الهوية البصرية', 'هوية موثّق البصرية: الحرز، الختم، الخيط، والأحبار الثلاثة.', 'identity', main)


def sources():
    rel = ''
    used = sorted({s for s in list(B.PICKS.get('photo', {}).values()) + list(B.EV_PHOTO.values()) + list(B.PICKS.get('section', {}).values()) if s in B.PHOTO_SIZE})
    rows = ''.join(f'<tr><th scope="row"><span class="mono">{esc(s)}</span></th><td>{esc(B.PHOTOS[s].get("caption_ar", ""))}</td><td>{ext(B.PHOTOS[s]["page_url"], esc(B.PHOTOS[s].get("author", "")))}</td><td>{esc(B.PHOTOS[s].get("license", ""))}</td></tr>' for s in used)
    main = f'''<div class="wrap">{S.crumbs(rel, [("المصادر وحقوق الصور", None)])}</div>
<section class="list-head"><div class="wrap"><h1 class="h1">المصادر وحقوق الصور</h1><p class="lead">كل وثيقة وواقعة في هذا النموذج مربوطة بمصدرها داخل سجلها. هنا حقوق الصور والخطوط، وما هو توضيحي.</p></div></section>
<section class="sec"><div class="wrap doc-grid"><div class="read">
 <h2 class="h2">الصور ({len(used)})</h2>
 <p class="small mute">من ويكيميديا كومنز بتراخيصها المذكورة، بمكانها وتاريخها الحقيقيين. لا نعرض صورًا للجثث أو الدماء. الصور مصغّرة الحجم دون تعديل في محتواها.</p>
 <div class="sheet table-wrap"><table class="legal credits"><thead><tr><th>الملف</th><th>ما تظهره</th><th>المصور</th><th>الترخيص</th></tr></thead><tbody>{rows}</tbody></table></div>
 </div>
 <aside class="doc-side"><div class="side-sticky">
  <div class="sheet"><h2 class="h3">ما هو توضيحي</h2><p class="small">حالات التحقق الخاصة بالمنصة، وسجلات العهدة وتواريخها، والأرقام المرجعية، ونماذج الإرسال والتبرع. التفاصيل في <a href="method.html#illustrative">صفحة المنهجية</a>.</p></div>
  <div class="sheet"><h2 class="h3">الخطوط</h2><p class="small">فازيرمتن (صابر راستي كردار) وريد هات مونو (ريد هات)، برخصة SIL Open Font License، ومستضافان من المنصة نفسها.</p></div>
 </div></aside>
</div></section>'''
    P(rel, 'sources.html', 'المصادر وحقوق الصور', 'مصادر موثّق وحقوق الصور والخطوط.', 'sources', main)


def not_found():
    base = '/muwathaq-prototype/'
    main = f'''<section class="sec lost" data-loose><div class="wrap lost-grid"><div class="lost-in">
 <h1 class="h1">لا يوجد حرز بهذا الرقم</h1>
 <p class="lead">ربما نُقل السجل أو كُتب الرابط بخطأ. ابحث برقم الملف أو الاسم، أو ابدأ من أحد الأقسام.</p>
 {S.find(base, "lost")}
 <p class="link-row"><a class="btn btn-line btn-sm" href="{base}people/index.html">ملفات الأشخاص</a><a class="btn btn-line btn-sm" href="{base}incidents/index.html">أرشيف الوقائع</a><a class="btn btn-line btn-sm" href="{base}index.html">الرئيسية</a></p>
</div><div class="lost-rope" aria-hidden="true"><canvas></canvas><div class="loose-seal">{seal("not_started", label=False)}</div></div></div></section>'''
    P(base, '404.html', 'غير موجود', 'الصفحة غير موجودة.', '', main)


def build():
    method()
    submit()
    donate()
    about()
    standards()
    search()
    identity()
    sources()
    not_found()
