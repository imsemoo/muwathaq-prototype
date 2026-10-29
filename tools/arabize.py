"""Arabic only on screen (client, 28 October 2026: «شيل الانجليزي»).

The records keep their sources' original names in research/*.json, so citations stay checkable; this layer
sets what the reader sees in Arabic: publishers and bodies by their Arabic names, the platform's record numbers
with Arabic letters, photographers in Arabic letters, licences by their Arabic titles. It touches text only,
never attributes or links. Official document symbols (ICC-01/18, A/HRC/60/CRP.3, MDE 15/8668/2024) are kept:
they are how a court or a UN body files the document, and changing them would break a citation.
"""
import re

# Longest names first, so «Times of Israel» is matched before «Israel» would be.
NAMES = {
    'IDF Military Advocate General': 'المدعي العسكري العام في الجيش الإسرائيلي',
    'Israeli Military Advocate General': 'المدعي العسكري العام الإسرائيلي',
    'Israeli Ministry of Defense': 'وزارة الدفاع الإسرائيلية',
    'Israeli Southern District Attorney&#x27;s Office': 'النيابة العامة الإسرائيلية في لواء الجنوب',
    "Israeli Southern District Attorney's Office": 'النيابة العامة الإسرائيلية في لواء الجنوب',
    'Israel Police': 'الشرطة الإسرائيلية',
    'US Ambassador to Israel': 'السفير الأمريكي لدى إسرائيل',
    'UN Independent International Commission of Inquiry on the OPT and Israel': 'لجنة التحقيق الدولية المستقلة بشأن الأرض الفلسطينية المحتلة وإسرائيل',
    'UN Independent International Commission of Inquiry': 'لجنة التحقيق الدولية المستقلة التابعة للأمم المتحدة',
    'UN Commission of Inquiry': 'لجنة التحقيق الأممية',
    'UN Human Rights Office': 'مكتب الأمم المتحدة لحقوق الإنسان',
    'UN in Palestine': 'الأمم المتحدة في فلسطين',
    'UN News': 'أخبار الأمم المتحدة',
    'United Nations': 'الأمم المتحدة',
    'OHCHR oPt': 'مكتب المفوضية السامية لحقوق الإنسان في الأرض الفلسطينية المحتلة',
    'OHCHR': 'المفوضية السامية لحقوق الإنسان',
    'OCHA oPt': 'أوتشا في الأرض الفلسطينية المحتلة',
    'OCHA': 'أوتشا',
    'UNRWA': 'الأونروا',
    'UNIFIL': 'اليونيفيل',
    'World Health Organization': 'منظمة الصحة العالمية',
    'WHO': 'منظمة الصحة العالمية',
    'IPC Gaza Strip analysis': 'تحليل التصنيف المرحلي لقطاع غزة',
    'IPC Gaza Strip': 'التصنيف المرحلي: غزة',
    'IPC': 'التصنيف المرحلي المتكامل',
    'International Criminal Court': 'المحكمة الجنائية الدولية',
    'ICC Pre-Trial Chamber I': 'الدائرة التمهيدية الأولى في المحكمة الجنائية الدولية',
    'Pre-Trial Chamber I': 'الدائرة التمهيدية الأولى',
    'Office of the Prosecutor': 'مكتب المدعي العام',
    'Appeals Chamber': 'دائرة الاستئناف',
    'International Court of Justice': 'محكمة العدل الدولية',
    'ICJ Order of 24 May 2024': 'أمر محكمة العدل الدولية في 24 مايو 2024',
    'South Africa v. Israel': 'جنوب أفريقيا ضد إسرائيل',
    'General List No.': 'القائمة العامة رقم',
    'ICJ No.': 'العدل الدولية رقم',
    'Human Rights Watch': 'هيومن رايتس ووتش',
    'Amnesty International': 'منظمة العفو الدولية',
    'Committee to Protect Journalists': 'لجنة حماية الصحفيين',
    'B&#x27;Tselem': 'بتسيلم', "B'Tselem": 'بتسيلم', 'B’Tselem': 'بتسيلم',
    'PHRI': 'أطباء لحقوق الإنسان - إسرائيل',
    'Forensic Architecture': 'فورنزيك آركيتكتشر',
    'Earshot': 'إيرشوت',
    'Airwars': 'إيروورز',
    'TNO': 'المنظمة الهولندية للبحث العلمي التطبيقي',
    'Mediterranea Saving Humans': 'ميديتيرانيا لإنقاذ البشر',
    'WAFA (Palestinian News &amp; Information Agency) in contract with APAimages': 'وكالة الأنباء والمعلومات الفلسطينية (وفا) بالتعاقد مع إيه بي إيه إيميجز',
    'WAFA (Palestinian News & Information Agency) in contract with APAimages': 'وكالة الأنباء والمعلومات الفلسطينية (وفا) بالتعاقد مع إيه بي إيه إيميجز',
    'WAFA': 'وفا',
    'The New York Times': 'نيويورك تايمز', 'New York Times': 'نيويورك تايمز',
    'The Washington Post': 'واشنطن بوست',
    'The Times of Israel': 'تايمز أوف إسرائيل', 'Times of Israel': 'تايمز أوف إسرائيل',
    'The Jerusalem Post': 'جيروزاليم بوست',
    'Jewish Telegraphic Agency': 'وكالة التلغراف اليهودية', 'JTA': 'وكالة التلغراف اليهودية',
    'Al Arabiya English': 'العربية', 'Al Jazeera': 'الجزيرة', 'Al-Monitor': 'المونيتور',
    'Associated Press': 'أسوشيتد برس', 'AP': 'أسوشيتد برس',
    'Reuters': 'رويترز', 'AFP': 'وكالة الصحافة الفرنسية',
    'BBC News': 'بي بي سي نيوز', 'BBC': 'بي بي سي',
    'NBC News': 'إن بي سي نيوز', 'ABC News': 'إيه بي سي نيوز', 'ABC': 'إيه بي سي', 'CNN': 'سي إن إن',
    'VOA': 'صوت أمريكا', 'News4JAX': 'نيوز فور جاكس', 'Yahoo News': 'ياهو نيوز',
    'Haaretz': 'هآرتس', 'Ynetnews': 'واي نت', 'Ynet': 'واي نت',
    'Orient Today': 'أورينت توداي', 'The National': 'ذا ناشونال', 'BusinessDay': 'بزنس داي',
    'The Local Norway': 'ذا لوكال النرويج', 'The Local Spain': 'ذا لوكال إسبانيا',
    'Global Affairs Canada': 'وزارة الشؤون العالمية الكندية', 'Justice Laws Website': 'موقع القوانين الكندي',
    'UK Foreign, Commonwealth &amp; Development Office': 'وزارة الخارجية والكومنولث والتنمية البريطانية',
    'UK Foreign, Commonwealth & Development Office': 'وزارة الخارجية والكومنولث والتنمية البريطانية',
    'UK Government': 'الحكومة البريطانية', 'GOV.UK': 'موقع الحكومة البريطانية',
    'Australian Government Special Adviser': 'المستشار الخاص للحكومة الأسترالية', 'Mark Binskin': 'مارك بينسكين',
    'Australian Minister for Foreign Affairs': 'وزيرة الخارجية الأسترالية',
    'New Zealand Government': 'حكومة نيوزيلندا', 'Beehive': 'موقع الحكومة النيوزيلندية',
    'Government of Norway': 'الحكومة النرويجية', 'regjeringen.no': 'موقع الحكومة النرويجية',
    'Government of the Republic of Slovenia': 'حكومة جمهورية سلوفينيا',
    'Tweede Kamer der Staten-Generaal': 'مجلس النواب الهولندي',
    'Council of the European Union': 'مجلس الاتحاد الأوروبي', 'EUR-Lex': 'بوابة تشريعات الاتحاد الأوروبي',
    'U.S. Department of State': 'وزارة الخارجية الأمريكية', 'Federal Register': 'السجل الفيدرالي الأمريكي', 'GovInfo': 'السجل الحكومي الأمريكي',
    'Special Economic Measures (Extremist Settler Violence) Regulations': 'لائحة التدابير الاقتصادية الخاصة (عنف المستوطنين المتطرفين)',
    'Global Human Rights Sanctions Regulations': 'لائحة العقوبات العالمية لحقوق الإنسان',
    'World Central Kitchen': 'المطبخ المركزي العالمي', 'WCK': 'المطبخ المركزي العالمي',
    'Sayfollah Musallet': 'سيف الله مصلط',
    'GBU-39': 'جي بي يو-39', 'FN MAG': 'إف إن ماغ', 'PRESS': 'صحافة',
    'IDF': 'الجيش الإسرائيلي', 'Canada': 'كندا', 'Australia': 'أستراليا',
    'SIL Open Font License': 'رخصة الخطوط المفتوحة',
}
# photographers, as their names are read in Arabic
AUTHORS = {
    'Jaber Jehad Badwan': 'جابر جهاد بدوان', 'Avi Ohayon / Government Press Office (Israel)': 'آفي أوهايون / مكتب الصحافة الحكومي الإسرائيلي',
    'Ashraf Amra / UNRWA': 'أشرف عمرة / الأونروا', 'Kazem Abu-Khalaf / UNRWA': 'كاظم أبو خلف / الأونروا',
    'U.S. Air Force courtesy photo (DVIDS 8281513, credited to Staff Sgt. Jasmonet Holmes)': 'صورة من سلاح الجو الأمريكي (الرقيب جاسمونيت هولمز)',
    'Yair Dov (יאיר דב)': 'يائير دوف', 'Sgt. 1st Class Malcolm Cohens-Ashley, U.S. Army': 'الرقيب أول مالكوم كوهينز آشلي، الجيش الأمريكي',
    'Cameron Smith / The White House': 'كاميرون سميث / البيت الأبيض', 'Hagai Agmon-Snir': 'حجاي أغمون سنير',
    'MMO:VAS Monoliths (Commons user)': 'مستخدم في ويكيميديا كومنز', 'Shlomo Roded, via PikiWiki - Israel free image collection project': 'شلومو روديد، عبر مشروع بيكي ويكي',
    'Thomas Wolf, www.foto-tw.de': 'توماس وولف', 'Michielverbeek': 'ميخيل فيربيك', 'Shlomi Amsalem / Knesset Archives': 'شلومي أمسالم / أرشيف الكنيست',
    'Pierre Markuse (contains modified Copernicus Sentinel data 2023)': 'بيير ماركوزه (بيانات معدلة من القمر الصناعي سنتينل، 2023)',
    'Mediterranea Saving Humans': 'ميديتيرانيا لإنقاذ البشر',
    'WAFA (Palestinian News & Information Agency) in contract with APAimages': 'وكالة وفا بالتعاقد مع إيه بي إيه إيميجز',
}
LICENCES = {
    'CC BY-SA 4.0': 'المشاع الإبداعي: نسب المصنف، الترخيص بالمثل 4.0', 'CC BY-SA 3.0 IGO': 'المشاع الإبداعي: نسب المصنف، الترخيص بالمثل 3.0 للمنظمات الدولية',
    'CC BY-SA 3.0 DE': 'المشاع الإبداعي: نسب المصنف، الترخيص بالمثل 3.0 (ألمانيا)', 'CC BY-SA 3.0': 'المشاع الإبداعي: نسب المصنف، الترخيص بالمثل 3.0',
    'CC BY 4.0': 'المشاع الإبداعي: نسب المصنف 4.0', 'CC BY 2.5': 'المشاع الإبداعي: نسب المصنف 2.5', 'CC BY 2.0': 'المشاع الإبداعي: نسب المصنف 2.0',
    'CC0': 'ملكية عامة', 'Public domain (US Government work)': 'ملكية عامة (عمل للحكومة الأمريكية)',
}
NAMES.update(AUTHORS)
NAMES.update(LICENCES)
NAMES.update({'ملف PDF': 'الملف الأصلي', 'L&#x27;Orient Today': 'لوريان توداي', "L'Orient Today": 'لوريان توداي',
              'extermination': 'الإبادة', ' (plausible)': '', '1 July – 30 September 2025': '1 يوليو – 30 سبتمبر 2025',
              # sanction instruments: the words become Arabic, the official numbers stay as filed
              'E.O. 14148, sec. 2(hhh); 90 FR 8237': 'الأمر التنفيذي 14148، القسم 2(hhh)؛ السجل الاتحادي 90، ص 8237',
              'E.O. 14115': 'الأمر التنفيذي 14115', 'Kamerstuk 23 432, nr. 569': 'وثائق مجلس النواب الهولندي 23 432، رقم 569',
              ' (Sayfollah Musallet)': '', 'TNO': 'المنظمة الهولندية للبحث العلمي التطبيقي'})
KIND = {'un': 'أممي', 'media': 'صحفي', 'forensic': 'تحقيق جنائي رقمي', 'ngo': 'حقوقي', 'official': 'رسمي', 'court': 'قضائي', 'gov': 'حكومي', 'academic': 'أكاديمي'}
# the platform's own record numbers, with Arabic letters: شخص، واقعة، دليل، وثيقة
IDS = {'INC': 'و', 'EV': 'د', 'R': 'ث', 'P': 'ش'}
_ID = re.compile(r'\b(INC|EV|R|P)-(\d{4})\b')
_VIA = re.compile(r'\s*(?<![A-Za-z])via(?![A-Za-z])\s*')
_GBU = re.compile(r'\bGBU-(\d+)')
_EU = re.compile(r'\(EU\) (\d{4}/\d+), Annex I, entry (\d+)')   # an EU sanctions listing: regulation, annex, entry
_AND = re.compile(r'(?<=[؀-ۿ])\s+(?:&amp;|&)\s+(?=[؀-ۿ])')   # «إيرشوت & فورنزيك» -> «إيرشوت وفورنزيك»
_NAMES = re.compile(r'(?<![A-Za-z])(?:' + '|'.join(re.escape(k) for k in sorted(NAMES, key=len, reverse=True)) + r')(?![A-Za-z])')


def rec_id(s):
    """P-0001 -> ش-0001, kept apart from the surrounding text so it reads as one number."""
    # isolated right-to-left (RLI … PDI), so the letter reads first even inside a left-to-right data span
    return _ID.sub(lambda m: f'⁧{IDS[m.group(1)]}-{m.group(2)}⁩', s)


def words(s):
    s = _NAMES.sub(lambda m: NAMES[m.group(0)], s)
    s = _VIA.sub(' عبر ', s)
    s = _GBU.sub(lambda m: f'جي بي يو-{m.group(1)}', s)
    s = _EU.sub(lambda m: f'اللائحة الأوروبية {m.group(1)}، الملحق الأول، البند {m.group(2)}', s)
    s = _AND.sub(' و', s)
    return rec_id(s)


def licence(s):
    return LICENCES.get(s, s)


def author(s):
    return AUTHORS.get(s, words(s))


_SKIP = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', re.S)


def arabize(html):
    """Arabic names and record numbers in every text node; tags, attributes, scripts and styles untouched."""
    parts = _SKIP.split(html)
    return ''.join(p if i % 2 else words(p) for i, p in enumerate(parts))
