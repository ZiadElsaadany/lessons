# -*- coding: utf-8 -*-
"""يبني html/lesson_4_2.html من tools/u4src/lesson_4_2_src.html (تصميمات الدرس الأصلية) على قالب المذكرة — انظر tools/u4conv.py."""
import os, sys
TOOLS = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, TOOLS)
from u4conv import build, recall, exs, terms, recall, exs, terms
START, TOTAL = 2, 99      # الترقيم النهائي للوحدة الرابعة هيتعمل في الآخر

# ربط أسئلة التقييمات بالبنك (اتراجعت سؤال سؤال): رقم = سؤال «اختر» المطابق · نص = سؤال البنك المطابق · "new" · "skip" (مكرر في التقييمات)
OV = {("m", 1): 1, ("m", 2): 5, ("m", 3): 22, ("m", 4): 23, ("m", 5): 16, ("m", 6): 15, ("m", 7): 17,
      ("m", 8): "لا يُعد معلومة مناسبة لإدراجها عند إعداد شخصية", ("m", 9): 19, ("m", 10): 5, ("m", 11): 10, ("m", 12): 19,
      ("m", 13): 4, ("m", 14): 12, ("m", 15): 11, ("m", 16): 21, ("m", 17): 13, ("m", 18): 19, ("m", 19): 7, ("m", 20): 15,
      ("e", 1): "عرّف شخصية المستخدم كما يذكرها الكتاب", ("e", 2): "لماذا يُحدَّد مكان المعلومات", ("e", 3): "new", ("e", 4): "new",
      ("e", 5): "اذكر مبادئ CRAP الأربعة", ("e", 6): "new", ("e", 7): "اذكر مبادئ CRAP الأربعة", ("e", 8): "new", ("e", 9): "skip",
      ("e", 10): "skip", ("e", 11): "اذكر مبادئ CRAP الأربعة", ("e", 12): "اشرح خطوات التصميم المتمحور حول المستخدم", ("e", 13): "skip",
      ("e", 14): "لا يُفضَّل الاعتماد على اللون وحده", ("e", 15): "يجب محاذاة النص العربي", ("e", 16): "يُختبر التصميم مع المستخدمين",
      ("e", 17): "skip", ("e", 18): "new", ("e", 19): "new", ("e", 20): "skip"}

# تعديلات صياغة على نص المصدر (دقة + كلام مدرس طبيعي) — u4conv.Lesson بيتأكد إن كل واحدة لقت مكانها مرة واحدة
SUBS = [
 ('<p class="lead"><b>تلات خطوات</b> مرتبة ورا بعض، والكتاب نفسه ماشي بالترتيب ده: <b>مين ← فين ← واضح إزاي</b>. والرابعة مش خطوة بعديهم — دي <b>الإطار اللي بيحكمهم كلهم</b>: كل قرار يتاخد <b>لصالح مين؟</b></p>',
  '<p class="lead kwn"><span class="tag">للفهم</span><b>للتذكّر</b> — ممكن ترتب أفكار الدرس في دماغك كده: <b>مين؟</b> ← شخصية المستخدم · <b>فين؟</b> ← المخطط الهيكلي · <b>واضح إزاي؟</b> ← مبادئ CRAP · <b>وكل ده من منظور المستخدم</b> ← UCD.</p>'),
 ('<b>طب ليه أصلًا؟</b>', '<b>ليه أصلًا؟</b>'),
 ('الكتاب في نشاط «فكّر كمهندس» بيطلب تدرس النوعين دول بالذات:', 'ونشاط «فكّر كمهندس» في الدرس بيطلب تدرس النوعين دول:'),
 ('<b>فرق بيتسأل عليه:</b> CRAP', '<b>الفرق المهم:</b> CRAP'),
 ('<h2>خلي بالك من العبارات دي — كلمات الكتاب اللي بتفرق في الامتحان</h2>', '<h2>خلي بالك من العبارات دي</h2>'),
 ('— والكتاب مابيقولش «أبيض وأسود»، ومابيقولش إنه التصميم النهائي.', '— مش شرط «أبيض وأسود»، ومش هو التصميم النهائي.'),
 ('الفرق بيتشاف مش بيتحفظ.', 'الفرق بيبان بالعين.'),
]

KEY = "ب,أ,أ,ج,ب,ج,ب,ج,ب,ج,د,ب,ب,أ,د,أ,أ,ج,د,د,ب,ج,د,أ,د,أ"
LONG = {   # اختيارات غلط اتطوّلت عشان الإجابة الصح ماتبقاش أطول اختيار
 4: {"اختيار الألوان المناسبة": "اختيار الألوان والخطوط والزخارف المناسبة لذوق كل عضو في الفريق"},
 6: {"تسريع فتح الصفحة": "تسريع فتح الصفحة على الأجهزة الضعيفة والشبكات البطيئة قبل نشر الموقع"},
 7: {"الانتهاء بسرعة أكبر": "الانتهاء بسرعة أكبر والوصول إلى اتفاق نهائي من أول اجتماع للفريق"},
 8: {"يؤخر تسليم المشروع": "يؤخر تسليم المشروع لأنه يضيف خطوة غير ضرورية قبل التصميم البصري"},
 12: {"التكرار": "التكرار في العناوين والأزرار"},
 14: {"تكبير كل النصوص بنفس الدرجة": "تكبير كل النصوص والعناوين بنفس الدرجة حتى تتساوى أهمية جميع العناصر في الصفحة"},
 16: {"ترك مسافات بين العناصر": "ترك مسافات واسعة بين كل العناصر في الصفحة حتى لا تبدو مزدحمة أمام المستخدم"},
 17: {"استخدام لون مميز للأزرار": "استخدام لون مميز للأزرار المهمة وتكبير العنوان الرئيسي في أعلى الصفحة"},
 18: {"تغني عن اختبار الموقع مع المستخدمين": "تغني عن اختبار الموقع مع المستخدمين إذا طُبّقت المبادئ الأربعة كلها بدقة في كل الصفحات"},
 19: {"المخطط الهيكلي": "المخطط الهيكلي بتفاصيل بصرية قليلة"},
 20: {"تنظيم ← اختبار ← فهم ← تصميم": "تنظيم ← اختبار ← فهم ← تصميم ← تكرار الاختبار مرة أخيرة"},
 21: {"استخدام أحدث التقنيات دائمًا": "استخدام أحدث التقنيات والأدوات البرمجية دائمًا في كل صفحات الموقع"},
 22: {"المخطط الهيكلي": "المخطط الهيكلي للصفحة"},
 24: {"التكرار": "التكرار — لأن اللون الأحمر لم يتكرر في كل الصفحات بنفس الطريقة"},
}

def mini(kind, after):
    b = lambda w, c="": f'<i class="bar {c}" style="width:{w}%"></i>'
    if kind == "c":
        body = (b(70, "t") + b(90) + b(80) + '<i class="btn">سجّل</i>') if after else (b(70) + b(90) + b(80) + '<i class="btn dull">سجّل</i>')
    elif kind == "r":
        pages = ['<div class="pg">' + (b(60, "t") if after else b(60, ["t", "t2", "t3"][k])) + b(90) + b(75) + '</div>' for k in range(3)]
        body = '<div class="pgs">' + "".join(pages) + '</div>'
    elif kind == "a":
        offs = [0, 0, 0, 0] if after else [0, 14, 5, 22]
        body = "".join(f'<i class="bar" style="width:{w}%;margin-right:{o}%"></i>' for w, o in zip([70, 85, 60, 78], offs))
    else:
        body = ('<div class="grp"><i class="img"></i>' + b(70, "t") + b(40, "p") + '</div>') if after else \
               ('<i class="img"></i><i class="gap"></i>' + b(70, "t") + '<i class="gap"></i><i class="gap"></i>' + b(40, "p"))
    return f'<div class="mn {"af" if after else "bf"}"><span class="ml">{"بعد" if after else "قبل"}</span><div class="mp">{body}</div></div>'

CR = [("c", "التباين", "يُبرز الأهم", "العنوان والزرار زي باقي النص"),
      ("r", "التكرار", "يوحّد", "كل صفحة عنوانها بشكل مختلف"),
      ("a", "المحاذاة", "ينظّم", "العناصر مبعثرة"),
      ("p", "التقارب", "يجمّع", "صورة المنتج بعيدة عن اسمه وسعره")]
CRAPV = ('<div class="u4v keep crv"><span class="fx abs">للفهم</span><div class="vh">نفس الصفحة — <em>قبل وبعد</em> كل مبدأ من مبادئ CRAP</div><div class="vg" style="grid-template-columns:1fr 1fr">'
         + "".join(f'<div class="vc"><b>{t} <span class="tg">{v}</span></b><div class="ba">{mini(k, False)}<i class="ar">←</i>{mini(k, True)}</div><small>المشكلة قبل: {d}</small></div>' for k, t, v, d in CR)
         + '</div></div>')

def hook(L):
    if KEY: print("longest:", L.mcq_key(KEY, LONG))
    L.move("مثال من حياتنا", 5, before="سؤال على نمط الامتحان")
    L.move("اتأكد إنك قادر على", 2, before="سؤال على نمط الامتحان")
    L.insert_after("exp", "المخطط الهيكلي هو التصميم بنسخته النهائية",
        recall(["شخصية المستخدم ← مين؟", "المخطط الهيكلي ← فين؟", "CRAP ← واضح إزاي؟"]))
    L.insert_after("exp", "مبادئ تصميم CRAP · كل مبدأ",
        recall(["التباين ← يُبرز", "التكرار ← يوحّد", "المحاذاة ← ينظّم", "التقارب ← يجمّع"]))
    L.insert_before("exp", "توقّف وفكّر (من الكتاب): أي مبدأ يجمع العناصر المرتبطة", CRAPV)
    L.insert_after("exp", "التصميم المتمحور حول المستخدم يدور حول المستخدم الفعلي",
        exs('صفحة نتائج المدرسة: <b>فهم المستخدم</b> (ولي أمر مستعجل بيفتح من الموبايل) ← <b>تنظيم المعلومات</b> (خانة رقم الجلوس فوق خالص) ← '
            '<b>تصميم الحل</b> ← <b>اختبار مع المستخدمين</b> (خمس أولياء أمور جرّبوا ولقوا الزرار صغير) ← <b>تكرار التحسين</b> (كبّرناه واختبرنا تاني).'))
    L.replace("exp", "CRAP = التباين والتكرار والمحاذاة والتقارب", terms([
        ("شخصية المستخدم (Persona)", "تمثيل لنمط من المستخدمين يستند قدر الإمكان إلى بحث أو بيانات عن أهدافهم واحتياجاتهم وسلوكهم وسياق استخدامهم."),
        ("المخطط الهيكلي", "مخطط للتخطيط قبل إضافة أي لون أو زخرفة."),
        ("CRAP", "التباين والتكرار والمحاذاة والتقارب."),
        ("التصميم المتمحور حول المستخدم", "التصميم من منظور المستخدم."),
        ("قابلية الاستخدام", "مدى سهولة استخدام المستخدمين للموقع."),
        ("إمكانية الوصول (Accessibility)", "تصميم المحتوى والواجهة بحيث يمكن لأصحاب القدرات والاحتياجات المختلفة استخدامها، بمن فيهم ذوو الإعاقة.")]))

CSS = """
.crv .vc{text-align:right}
.crv .vc>b{display:flex;align-items:center;gap:6pt}
.crv .vc>b .tg{margin:0}
.crv .ba{display:grid;grid-template-columns:1fr 16pt 1fr;align-items:center;gap:4pt;margin:5pt 0 3pt 0}
.crv .ar{font-style:normal;text-align:center;color:#DA9C3B;font-weight:800}
.crv .mn{position:relative;border-radius:7pt;padding:12pt 6pt 6pt 6pt;background:#fff;border:.75pt solid #E3E7EF;min-height:58pt}
.crv .mn.af{border-color:#BFE3CE;background:#F7FCF9}
.crv .ml{position:absolute;top:2pt;right:5pt;font-size:8pt;font-weight:800;color:#8A93AB}
.crv .mn.af .ml{color:#2e7d5b}
.crv .mp{display:flex;flex-direction:column;align-items:flex-start;gap:3pt}
.crv .bar{display:block;height:4pt;border-radius:2pt;background:#C9D0DD;font-style:normal}
.crv .bar.t{height:7pt;background:#1F2A47}
.crv .bar.t2{height:5pt;background:#DA9C3B}
.crv .bar.t3{height:8pt;background:#8A93AB}
.crv .bar.p{background:#DA9C3B}
.crv .btn{font-style:normal;font-size:8pt;font-weight:800;border-radius:6pt;padding:0 8pt;line-height:13pt;background:#DA9C3B;color:#fff}
.crv .btn.dull{background:#E3E7EF;color:#8A93AB}
.crv .pgs{display:grid;grid-template-columns:repeat(3,1fr);gap:3pt;width:100%}
.crv .pg{display:flex;flex-direction:column;gap:3pt;border:.75pt solid #E3E7EF;border-radius:4pt;padding:3pt}
.crv .img{display:block;width:26pt;height:16pt;border-radius:3pt;background:#DCE3EE;font-style:normal}
.crv .gap{display:block;height:5pt;font-style:normal}
.crv .grp{display:flex;flex-direction:column;gap:3pt;border:.75pt dashed #DA9C3B;border-radius:5pt;padding:4pt;width:80%}
"""

L = build(TOOLS + "/u4src/lesson_4_2_src.html", "4-2", "تصميم المعلومات وتجربة المستخدم للمواقع الإلكترونية", START, TOTAL, "lesson_4_2.html", hook=hook, ov=OV, extra_css=CSS, subs=SUBS)
print("\n".join(L.log)); print("mcq", L.n_mcq, "ess", L.n_ess, "tq", L.n_badges)
