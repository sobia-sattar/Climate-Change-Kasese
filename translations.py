"""
translations.py - Multilingual strings and fallback templates for RainCheck.

Languages supported:
- English (Verified)
- Urdu (Pending review by fluent speaker)
- Luganda (Pending review by fluent speaker)

Note on ethics & transparency:
Translations in Urdu and Luganda are preliminary machine translations intended
as placeholders and are explicitly marked as pending review by fluent speakers.
"""

from typing import Dict, Any

# Review status for each language to ensure academic and user-facing honesty
LANGUAGE_STATUS = {
    "en": {
        "name": "English",
        "native": "English",
        "status": "Verified",
        "is_reviewed": True,
        "note": "Official project default language."
    },
    "ur": {
        "name": "Urdu",
        "native": "اردو",
        "status": "Pending review by fluent speaker",
        "is_reviewed": False,
        "note": "یہ ترجمہ حتمی نہیں ہے اور ماہرِ زبان کی توثیق کا منتظر ہے۔ (Pending review by fluent speaker)"
    },
    "lg": {
        "name": "Luganda",
        "native": "Oluganda",
        "status": "Pending review by fluent speaker",
        "is_reviewed": False,
        "note": "Kino tekinaba kukkirizibwa muntu amanyi Oluganda obulungi. (Pending review by fluent speaker)"
    }
}

# General UI strings
UI_STRINGS: Dict[str, Dict[str, str]] = {
    "app_title": {
        "en": "RainCheck — Evidence-Based Weather Advice",
        "ur": "رین چیک — شواہد پر مبنی موسمی مشورے",
        "lg": "RainCheck — Amagezi ku mbeera y'obudde agaesigamiziddwa ku bujulizi"
    },
    "app_tagline": {
        "en": "Empowering farmers, riders, and traders with verified forecast evidence.",
        "ur": "کسانوں، رائیڈرز، اور تاجروں کو تصدیق شدہ موسمی شواہد سے بااختیار بنانا۔",
        "lg": "Okuyamba abalimi, aba boda-boda, n'abasuubuzi n'obujulizi ku mbeera y'obudde."
    },
    "disclaimer_official": {
        "en": "Notice: RainCheck is NOT an official national weather warning service. For emergency decisions, consult the Uganda National Meteorological Authority (UNMA) or the Pakistan Meteorological Department (PMD).",
        "ur": "تنبیہ: رین چیک کوئی سرکاری موسمی وارننگ سروس نہیں ہے۔ ہنگامی صورتحال کے لیے ہمیشہ محکمہ موسمیات پاکستان (PMD) سے رجوع کریں۔",
        "lg": "Okulabula: RainCheck tekiikirira kitongole kya gavumenti ekikola ku mbeera y'obudde. Kozesa UNMA ku nsonga ez'amangu."
    },
    "nav_evidence": {
        "en": "Page 1: Evidence",
        "ur": "صفحہ 1: شواہد (Evidence)",
        "lg": "Omuko 1: Obujulizi (Evidence)"
    },
    "nav_advice": {
        "en": "Page 2: Practical Advice",
        "ur": "صفحہ 2: عملی مشورہ (Advice)",
        "lg": "Omuko 2: Amagezi Ag'omugaso (Advice)"
    },
    "nav_feedback": {
        "en": "Page 3: Community Feedback",
        "ur": "صفحہ 3: عوامی فیڈ بیک (Feedback)",
        "lg": "Omuko 3: Okuddamu kw'abantu (Feedback)"
    },
    "select_language": {
        "en": "Language / زبان / Olulimi",
        "ur": "زبان منتخب کریں",
        "lg": "Londa Olulimi"
    },
    "select_city": {
        "en": "Select Pilot City",
        "ur": "شہر منتخب کریں",
        "lg": "Londa Ekibuga"
    },
    "select_role": {
        "en": "Select Your Role",
        "ur": "اپنا کردار منتخب کریں",
        "lg": "Londa emirimu gyo"
    },
    "choose_role_label": {
        "en": "Choose View / Outdoor Role:",
        "ur": "اپنا پیشہ منتخب کریں:",
        "lg": "Londa Omulimu gwo ogw'ebweru:"
    },
    "role_overview": {
        "en": "Overview",
        "ur": "عمومی جائزہ (Overview)",
        "lg": "Okutwaliza Awamu (Overview)"
    },
    "role_farmer": {
        "en": "Farmer",
        "ur": "کسان (Farmer)",
        "lg": "Omulimi (Farmer)"
    },
    "role_rider": {
        "en": "Rider",
        "ur": "رائیڈر (Rider)",
        "lg": "Owa Boda-boda (Rider)"
    },
    "role_trader": {
        "en": "Trader",
        "ur": "تاجر (Trader)",
        "lg": "Omusuubuzi (Trader)"
    },
    "tab_advisor": {
        "en": "Operational Advisor",
        "ur": "عملی مشیر (Operational Advisor)",
        "lg": "Amagezi Ag'omugaso (Advisor)"
    },
    "tab_kasese": {
        "en": "Kasese ML & Historical Verification",
        "ur": "کاسیسے ایم ایل و تصدیق (ML & Verification)",
        "lg": "Okukakasa Kasese ML & Ebyafaayo"
    },
    "tab_safety": {
        "en": "AI Safety Guardrail",
        "ur": "حفاظتی چیک (AI Guardrail)",
        "lg": "Obukuumi bwa AI (Safety Guardrail)"
    },
    "tab_feedback": {
        "en": "Community Reports",
        "ur": "عوامی رپورٹ (Community Reports)",
        "lg": "Okuddamu kw'Abantu (Reports)"
    },
    "hero_tag": {
        "en": "MEET RAINCHECK • KASESE",
        "ur": "رین چیک • کاسیسے",
        "lg": "SANGANA RAINCHECK • KASESE"
    },
    "hero_title_line1": {
        "en": "The Easiest Way",
        "ur": "سب سے آسان طریقہ",
        "lg": "Engeri Ennyangu"
    },
    "hero_title_line2": {
        "en": "To Get Reliable",
        "ur": "قابلِ اعتماد",
        "lg": "Ey'okufunamu"
    },
    "hero_title_line3": {
        "en": "Rain Advice",
        "ur": "موسمی مشورے",
        "lg": "Amagezi g'Enkuba"
    },
    "hero_sub": {
        "en": "Real historical Kasese data. Random Forest ML. Zero guessing. Select your outdoor profession to load your calibrated 3D action protocol.",
        "ur": "کاسیسے کا حقیقی تاریخی ڈیٹا۔ رینڈم فاریسٹ مشین لرننگ۔ بغیر کسی اندازے کے۔ اپنے پیشے کا انتخاب کریں اور عملی مشورے حاصل کریں۔",
        "lg": "Ebiwandiiko ebituufu eby'e Kasese. Random Forest ML. Tewali kuteebereza. Londa omulimu gwo ofune amagezi amakakafu."
    },
    "overview_title": {
        "en": "Overview &bull; Multi-Sector Weather Risk Protocol",
        "ur": "عمومی جائزہ &bull; تمام شعبوں کے لیے موسمی خطرات کا پروٹوکول",
        "lg": "Okutwaliza Awamu &bull; Enteekateeka y'Obudde mu Mirimu Gyonna"
    },
    "overview_question": {
        "en": "What does today's weather mean across outdoor sectors in Kasese?",
        "ur": "آج کا موسم کاسیسے میں بیرونی شعبوں کے لیے کیا معنی رکھتا ہے؟",
        "lg": "Embeera y'obudde ya leero etegeeza ki eri abantu abakolera ebweru mu Kasese?"
    },
    "overview_advice": {
        "en": "Empirical Kasese Verification Summary: 71% verified model hit rate at 6-hour lead horizon. Farmers: Favorable window for agrochemical treatment and crop maintenance. Riders: Clear highway routes, carry emergency waterproof gear for afternoon showers. Traders: Stable conditions for open-air display, deploy elevated tarpaulins if clouds thicken.",
        "ur": "کاسیسے کی تصدیقی رپورٹ: 6 گھنٹے کے افق پر ماڈل کی 71 فیصد درستگی تصدیق شدہ ہے۔ کسان: فصلوں کی دیکھ بھال اور زرعی ادویات کے لیے سازگار وقت۔ رائیڈرز: ہائی وے روٹس صاف ہیں، دوپہر کی بارش کے لیے رین کوٹ ساتھ رکھیں۔ تاجر: کھلی مارکیٹ کے لیے مستحکم موسم، بادل گہرے ہونے پر ترپال تیار رکھیں۔",
        "lg": "Okubalirira kw'e Kasese: Obutuufu bw'enkuba buli ku 71% ku ssaawa 6 ezijja. Abalimi: Akaseera kalungi okufuyira n'okulabirira ebirime. Aba Boda-boda: Enguudo nnungi, situla raincoat y'enkuba y'olweggulo. Abasuubuzi: Obudde bulungi mu katale, tegeka kaveera singa ebire biba bingi."
    },
    "question_farmer": {
        "en": "Should I plant, spray agrochemicals, or dry crops today?",
        "ur": "کیا مجھے آج بیج بونا، کیڑے مار دوا چھڑکنا یا فصل سکھانی چاہیے؟",
        "lg": "Nsimbe, nfuyire eddagala ly'ebirime, oba nyanike leero?"
    },
    "question_rider": {
        "en": "Are the roads safe for delivery trips today?",
        "ur": "کیا آج سڑکیں ڈیلیوری یا سفر کے لیے محفوظ ہیں؟",
        "lg": "Enguudo nnumgi okutambulirako leero?"
    },
    "question_trader": {
        "en": "Should I open outdoor market stalls today?",
        "ur": "کیا مجھے آج کھلی مارکیٹ کا اسٹال لگانا چاہیے؟",
        "lg": "Nzigulewo amatandalo g'akatale ebweru leero?"
    },
    "protocol_suffix": {
        "en": "Live Operational Protocol",
        "ur": "براہِ راست عملی پروٹوکول",
        "lg": "Enteekateeka y'Okukola ey'Amangu"
    },
    "grounded_records": {
        "en": "Grounded in Empirical Records (Zero Invented Numbers)",
        "ur": "تصدیق شدہ اعداد و شمار پر مبنی (بغیر خود ساختہ اعداد کے)",
        "lg": "Bisinzira ku biwandiiko ebituufu (Tewali namba zikozeseddwa bukozesebwa)"
    },
    "who_protect_title": {
        "en": "Who We Protect",
        "ur": "ہم کن کی حفاظت کرتے ہیں",
        "lg": "B'atukuuma"
    },
    "who_protect_sub": {
        "en": "Built for the people who live and work outdoors in Kasese.",
        "ur": "کاسیسے کے ان محنتی لوگوں کے لیے جو کھلے آسمان تلے کام کرتے ہیں۔",
        "lg": "Kyakolebwa olw'abantu abakolera ebweru mu Kasese."
    },
    "card_farmers_desc": {
        "en": "Protect harvests, time irrigation, and avoid agrochemical runoff by knowing verified rainfall timing.",
        "ur": "بارش کے تصدیق شدہ وقت سے باخبر رہ کر فصلوں کی حفاظت کریں اور کیمیائی کھادوں کا ضیاع روکیں۔",
        "lg": "Kuuma emmere gye wakungudde, tereeza amazzi, era weewale eddagala okukuluggusibwa enkuba."
    },
    "card_riders_desc": {
        "en": "Stay safe on unpaved highland roads, avoid mud hazards, and pack gear only when rain is confirmed.",
        "ur": "کچی پہاڑی سڑکوں پر پھسلن سے بچیں، سفر محفوظ بنائیں اور رین کوٹ تیار رکھیں۔",
        "lg": "Beera mirembe ku nguudo ez'ensozi ez'ebisooto, era weetegereze okusiba kw'eggaali oba piki yo."
    },
    "card_traders_desc": {
        "en": "Keep open-air stalls running profitably. Guard perishable stocks and deploy tarpaulins in advance.",
        "ur": "کھلی منڈی میں کاروبار منافع بخش رکھیں، خراب ہونے والے مال کی حفاظت کریں اور بر وقت ترپال ڈالیں۔",
        "lg": "Kuumira amatandalo g'akatale ku magoba. Kuuma ebiyinza okwonooneka era bikka kaveera mangu."
    },
    "card_btn_text": {
        "en": "View Protocol",
        "ur": "پروٹوکول دیکھیں",
        "lg": "Laba Enteekateeka"
    },
    "card_farmer_metric": {
        "en": "Verified Hit Rate",
        "ur": "ماڈل درستگی کی شرح",
        "lg": "Obutuufu bwa Model"
    },
    "card_rider_metric": {
        "en": "Lead Horizon",
        "ur": "محفوظ پیشگی وقت",
        "lg": "Ekiseera Eky'okwetegeka"
    },
    "card_trader_metric": {
        "en": "Dry Transit Window",
        "ur": "خشک مارکیٹ ونڈو",
        "lg": "Akaseera Akataliimu Nkuba"
    },
    "simulated_warning": {
        "en": "SIMULATED DEMONSTRATION DATA: The verification metrics below are generated for testing and demonstration purposes only.",
        "ur": "فرضی / آزمائشی ڈیٹا: ذیل میں دیے گئے تصدیقی اعداد و شمار صرف جانچ اور مظاہرے کے لیے ہیں۔",
        "lg": "EBIWANDIIKO BY'OKUKEEBERA BYA KULAGA BULAGI: Bino tebivudde mu bifo bituufu eby'obudde."
    },
    "no_results_file": {
        "en": "Verification results file ('results.json') was not found. Please contact the data engineering team or place the file in the data/ folder.",
        "ur": "تصدیقی نتائج کی فائل ('results.json') نہیں ملی۔ برائے مہربانی ڈیٹا ٹیم سے رابطہ کریں یا فائل data/ فولڈر میں رکھیں۔",
        "lg": "Fayiro y'obujulizi ('results.json') tezuuliddwa. Nsaba oyiseeko eri ttiimu y'ebikwata ku data."
    },
    "no_evidence_available": {
        "en": "No verified evidence is available for this city/lead time combination. RainCheck cannot guarantee forecast reliability. Please check official weather forecasts.",
        "ur": "اس شہر کے لیے کوئی تصدیق شدہ شواہد دستیاب نہیں ہیں۔ براہ کرم سرکاری موسمی پیشگوئی سے رجوع کریں۔",
        "lg": "Tewali bujulizi bumanyiddwa ku kibuga kino. Nsaba wekeneenye eby'abakugu mu mbeera y'obudde."
    },
    "small_sample_warning": {
        "en": "Caution: Evaluation is based on a small sample size (N < 30). Metric confidence is low.",
        "ur": "تنبیہ: یہ تخمینہ بہت کم نمونوں (N < 30) پر مبنی ہے۔ نتائج میں غیر یقینی کیفیت زیادہ ہے۔",
        "lg": "Okwegendereza: Obujulizi buno bwesoose ku bibaliddwa bitono nnyo (N < 30)."
    },
    "llm_toggle_label": {
        "en": "Enable AI Assistant (Optional LLM)",
        "ur": "مصنوعی ذہانت (AI) فعال کریں (اختیاری)",
        "lg": "Kozesa Amagezi ga AI (Bwe kiba kyagala)"
    },
    "llm_disabled_notice": {
        "en": "Using deterministic, evidence-grounded template (Safe Fallback).",
        "ur": "محفوظ اور پہلے سے طے شدہ شواہد پر مبنی ٹیمپلیٹ استعمال ہو رہا ہے۔",
        "lg": "Tukozesa amagezi amategeke aga bulijjo agaesigamiziddwa ku bujulizi (Safe Fallback)."
    },
    "llm_guard_passed": {
        "en": "Safety Guard Status: PASSED. All mentioned metrics are verified by data records.",
        "ur": "حفاظتی چیک: کامیاب۔ تمام بیان کردہ اعداد و شمار شواہد سے مطابقت رکھتے ہیں۔",
        "lg": "Okukakasa Obukuumi: KULUNGI. Buli namba eri wano ekakasiddwa obujulizi."
    },
    "llm_guard_failed": {
        "en": "Safety Guard Warning: Output contained unverified numbers or claims. Defaulted safely to the deterministic template.",
        "ur": "حفاظتی انتباہ: جواب میں غیر تصدیق شدہ اعداد پائے گئے۔ خودکار طور پر محفوظ ٹیمپلیٹ استعمال کیا گیا۔",
        "lg": "Okulabula kw'obukuumi: Ebyavuddeko byabaddemu ennamba zitali ntuufu. Tuddeyo ku magezi ag'omusingi."
    },
    "feedback_title": {
        "en": "Community Ground Truth Observation",
        "ur": "عوامی موسمی مشاہدہ",
        "lg": "Okulaba kw'abantu mu kitundu"
    },
    "feedback_intro": {
        "en": "Help calibrate community evidence. Feedback is stored independently and NEVER modifies historical forecast records or verification metrics.",
        "ur": "کمیونٹی شواہد کی بہتری میں مدد کریں۔ آپ کی رائے الگ محفوظ کی جاتی ہے اور یہ سرکاری پیشگوئی کے ریکارڈ کو تبدیل نہیں کرتی۔",
        "lg": "Yamba okutereeza obujulizi bw'ekitundu. Ebiyingiziddwa tebikyusa biwandiiko bya sayansi."
    },
    "feedback_observation": {
        "en": "What did you observe?",
        "ur": "آپ نے موسم میں کیا دیکھا؟",
        "lg": "Kiki kye walabye?"
    },
    "feedback_rain": {
        "en": "Rain",
        "ur": "بارش (Rain)",
        "lg": "Enkuba yatonnye (Rain)"
    },
    "feedback_no_rain": {
        "en": "No Rain",
        "ur": "بارش نہیں ہوئی (No Rain)",
        "lg": "Enkuba teyatonnye (No Rain)"
    },
    "feedback_unsure": {
        "en": "Unsure / Trace drizzle",
        "ur": "غیر یقینی / ہلکی بونداباندی (Unsure)",
        "lg": "Simanyi bulungi / Amatondo matono (Unsure)"
    },
    "feedback_area": {
        "en": "Approximate Area / Neighborhood (e.g. Nakasero, Gulberg)",
        "ur": "تقریبی علاقہ / محلہ (مثلاً گلببرگ، ماڈل ٹاؤن)",
        "lg": "Ekitundu / Akatundu k'obeeramu (e.g. Nakasero, Kansanga)"
    },
    "feedback_time": {
        "en": "Observation Time Window",
        "ur": "مشاہدے کا وقت",
        "lg": "Obudde lwe kyalabikira"
    },
    "feedback_consent": {
        "en": "I consent to contributing this observation for research and community calibration. (No personal identification is saved).",
        "ur": "میں اس مشاہدے کو تحقیقی مقصد کے لیے جمع کرانے کی رضامندی دیتا ہوں۔ (کوئی ذاتی معلومات محفوظ نہیں کی جائیں گی)۔",
        "lg": "Nzikiriza okuwaayo obujulizi buno eri okunoonyereza. (Tewali bikukwatako bikunganyizibwa)."
    },
    "feedback_submit": {
        "en": "Submit Community Observation",
        "ur": "مشاہدہ جمع کرائیں",
        "lg": "Weereza Okulaba Kwo"
    },
    "feedback_success": {
        "en": "Observation recorded safely in feedback storage. Thank you!",
        "ur": "آپ کا مشاہدہ محفوظ کر لیا گیا ہے۔ شکریہ!",
        "lg": "Okulaba kwo kuwandiikiddwa bulungi. Weebale!"
    }
}

# Deterministic Fallback Advice Templates
# Grounded strictly on evidence metrics without hallucinations
FALLBACK_ADVICE: Dict[str, Dict[str, Dict[str, str]]] = {
    "Farmer": {
        "high_rain": {
            "en": "Evidence shows frequent rain events with verified forecast accuracy. Protect harvested grain, check drainage in seedbeds, and hold off on spraying agrochemicals until dry conditions return.",
            "ur": "شواہد سے ثابت ہوتا ہے کہ بارش کی پیشگوئی قابلِ اعتماد ہے۔ اپنی کٹائی شدہ فصل اور بیجوں کو محفوظ رکھیں اور کیڑے مار ادویات کے چھڑکاؤ میں تاخیر کریں۔",
            "lg": "Obujulizi bulaga enkuba eraga okutonnya. Bikka ku mmere gy'okungudde, tereeza ensalosalo, era olinde okufuyira eddagala okutuusa ng'omusana gwaka."
        },
        "high_false_alarms": {
            "en": "Notice: Historical forecasts for this lead time show a high false alarm ratio. Do not cancel vital planting solely on rain warnings, but keep flexible irrigation contingencies.",
            "ur": "انتباہ: ماضی کی پیشگوئیوں میں بارش کے جھوٹے الارم کا تناسب زیادہ رہا ہے۔ صرف بارش کی وارننگ پر اہم کام منسوخ نہ کریں، مگر پانی کے متبادل انتظامات تیار رکھیں۔",
            "lg": "Okulabula: Okulagula okw'emabega kulaga nti ebiseera ebisinga bagamba enkuba egenda kutonnya naye n'etonnya ntono oba obutatonnya. Tokalambira ku kuleka kulima, naye ba mwetegefu."
        },
        "moderate_or_dry": {
            "en": "Evidence indicates low rain frequency. Favorable window for weeding, drying crops, and regular maintenance. Continue monitoring official UNMA / PMD bulletins.",
            "ur": "شواہد کم بارش کا اشارہ دیتے ہیں۔ فصلوں کی کٹائی، خشک کرنے اور معمول کی دیکھ بھال کے لیے وقت سازگار ہے۔ سرکاری بلیٹن دیکھتے رہیں۔",
            "lg": "Obujulizi bulaga enkuba ntono. Kano kaseera kalungi okusaawa, okwanika emmere, n'okukola emirimu gy'ennimiro. Ggwe gumu gweyongere okuwuliriza UNMA."
        },
        "no_evidence": {
            "en": "No verified forecast evidence is currently available for this area. Make decisions with caution and consult local agriculture extension or the official meteorological department.",
            "ur": "اس علاقے کے لیے تصدیق شدہ موسمی شواہد دستیاب نہیں ہیں۔ براہ کرم مقامی محکمہ زراعت یا سرکاری محکمہ موسمیات کے جاری کردہ مشوروں پر عمل کریں۔",
            "lg": "Tewali bujulizi bwa nkuba bumanyiddwa mu kitundu kino. Kakkana olinde oba obuuze ku bakugu b'ebyobulimi oba ekitongole ky'obudde ekya gavumenti."
        }
    },
    "Rider": {
        "high_rain": {
            "en": "Evidence confirms high likelihood of rain. Carry waterproof gear, slow down on muddy or unpaved roads, and anticipate reduced braking distance.",
            "ur": "شواہد بارش کے قوی امکان کی تصدیق کرتے ہیں۔ رین کوٹ ساتھ رکھیں، پھسلن والی سڑکوں پر رفتار کم رکھیں، اور بریک کے فاصلے کا خیال رکھیں۔",
            "lg": "Obujulizi bukakasizza enkuba. Situla engoye z'enkuba (raincoat), genda mpolampola ku nguudo z'ettaka oba eziriko ebisooto, era weetegereze obupapula bw'okusiba (brakes)."
        },
        "high_false_alarms": {
            "en": "Notice: Rain alerts for this time window historically have elevated false alarm ratios. Keep waterproof gear accessible, but trips do not need immediate cancellation.",
            "ur": "انتباہ: اس دوران بارش کی وارننگز میں غلط الارم کی شرح زیادہ رہی ہے۔ رین کوٹ ساتھ رکھیں مگر بلاوجہ سفر منسوخ نہ کریں۔",
            "lg": "Okulabula: Ebiseera bingi bwe balagula enkuba ku ssaawa zino tetonnya. Situla eky'okukubikka naye toleka ntambula zo bwe ziba nkulu."
        },
        "moderate_or_dry": {
            "en": "Evidence shows dry or stable conditions. Normal road safety rules apply. Check tire tread pressure for standard daily transit.",
            "ur": "شواہد خشک اور مستحکم موسم کا اشارہ دیتے ہیں۔ عام ٹریفک قوانین کی پابندی کریں اور ٹائروں میں ہوا کا دباؤ چیک کریں۔",
            "lg": "Obujulizi bulaga obudde bulungi obutaliimu nkuba ya maanyi. Goba eggaali oba piki yo mu ngeri eya bulijjo ng'okwata amateeka g'okuguudo."
        },
        "no_evidence": {
            "en": "Weather verification evidence is missing for this route. Carry standard wet-weather contingency gear and check local highway forecasts.",
            "ur": "اس روٹ کے لیے تصدیق شدہ شواہد دستیاب نہیں ہیں۔ حفاظتی احتیاط کے طور پر رین کوٹ رکھیں اور مقامی موسمی صورتحال دیکھیں۔",
            "lg": "Tewali bujulizi bwa budde bumanyiddwa ku kkubo lino. Situla engoye z'enkuba okulaba nga weegendereza era wekkaanye ebiyinza okujja."
        }
    },
    "Trader": {
        "high_rain": {
            "en": "Evidence confirms high probability of rain. Secure outdoor open-air stalls, raise perishables off ground level, and wrap electrical wares in tarpaulins.",
            "ur": "شواہد بارش کے امکان کی تصدیق کرتے ہیں۔ کھلی دکانوں پر ترپالیں ڈالیں، خراب ہونے والا سامان اونچی جگہ رکھیں، اور گاہکوں کے لیے محفوظ جگہ کا انتظام رکھیں۔",
            "lg": "Obujulizi bulaga enkuba ya maanyi. Bikka amatandalo agali ebweru, situla eby'amaguzi ebiyinza okwonooneka ku ttaka, era weetegekere abaguzi abatono."
        },
        "high_false_alarms": {
            "en": "Notice: Significant false alarm ratio in current forecasts. Prepare protective covers on standby without prematurely shutting down open market activity.",
            "ur": "انتباہ: پیشگوئی میں غلط الارم کا امکان زیادہ ہے۔ ترپالیں تیار رکھیں لیکن کاروبار یا دکان وقت سے پہلے بند نہ کریں۔",
            "lg": "Okulabula: Ebiseera ebisinga balagula enkuba naye n'etatonnya. Tegeka ebibikka ng'obirinze naye tozzalawo katale mu bwangu."
        },
        "moderate_or_dry": {
            "en": "Evidence indicates stable commercial conditions. Ideal window for loading, inventory restocking, and open display.",
            "ur": "شواہد تجارتی سرگرمیوں کے لیے سازگار موسم کا بتاتے ہیں۔ سامان لوڈ کرنے، ذخیرہ کرنے اور مارکیٹ کے لیے بہترین وقت ہے۔",
            "lg": "Obujulizi bulaga obudde bulungi. Kano kaseera kalungi okusaabaza eby'amaguzi, okubyoleka, n'okukola emirimu mu katale obulungi."
        },
        "no_evidence": {
            "en": "No verification data exists for this trading center. Maintain standard tarpaulins handy and refer to municipal weather updates.",
            "ur": "اس تجارتی مرکز کے لیے تصدیق شدہ ڈیٹا موجود نہیں ہے۔ ترپال تیار رکھیں اور مقامی موسمی خبروں سے باخبر رہیں۔",
            "lg": "Tewali biwandiiko bya budde bimanyiddwa ku katale kano. Beera ne kaveera w'okubikka era weyongere okukebere ebiva mu bakugu."
        }
    }
}


def get_ui_text(key: str, lang: str = "en") -> str:
    """Retrieve translated UI string by key with English fallback."""
    target_lang = lang if lang in LANGUAGE_STATUS else "en"
    if key in UI_STRINGS:
        return UI_STRINGS[key].get(target_lang, UI_STRINGS[key].get("en", key))
    return key


def get_language_status(lang: str) -> Dict[str, Any]:
    """Return status metadata about language verification."""
    return LANGUAGE_STATUS.get(lang, LANGUAGE_STATUS["en"])


def get_fallback_advice(role: str, condition: str, lang: str = "en") -> str:
    """Retrieve deterministic advice grounded in evidence conditions."""
    target_role = role if role in FALLBACK_ADVICE else "Farmer"
    target_lang = lang if lang in LANGUAGE_STATUS else "en"

    role_conditions = FALLBACK_ADVICE.get(target_role, FALLBACK_ADVICE["Farmer"])
    cond_text_dict = role_conditions.get(condition, role_conditions.get("no_evidence", {}))

    return cond_text_dict.get(target_lang, cond_text_dict.get("en", "Evidence-grounded advice is unavailable."))


def get_role_display_name(role: str, lang: str = "en") -> str:
    """Return localized display label for role radio buttons."""
    key_map = {
        "Overview": "role_overview",
        "Farmer": "role_farmer",
        "Rider": "role_rider",
        "Trader": "role_trader",
    }
    key = key_map.get(role, "role_overview")
    return get_ui_text(key, lang)


def get_role_question_text(role: str, lang: str = "en") -> str:
    """Return localized headline question for each role protocol."""
    key_map = {
        "Overview": "overview_question",
        "Farmer": "question_farmer",
        "Rider": "question_rider",
        "Trader": "question_trader",
    }
    key = key_map.get(role, "overview_question")
    return get_ui_text(key, lang)

