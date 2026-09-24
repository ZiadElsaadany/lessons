# -*- coding: utf-8 -*-
"""يبني html/lesson_3_3.html من قالب lesson_3_1.html (نفس الستايل والسكريبتات) + محتوى الدرس 3-3."""
import re, sys
import os
TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import newsec as N
from house_svg import house
from chat_svg import chat
HOUSE = house()

BASE = os.path.join(os.path.dirname(TOOLS), "")   # فولدر html (أبو فولدر tools)
tpl = open(BASE + "lesson_3_1.html", encoding="utf-8").read()
head = tpl[:tpl.index('<body data-lesson=')]
head = head.replace("<title>الدرس 3-1 — البنية العامة لتطبيقات الويب</title>", "<title>الدرس 3-3 — أساسيات تقنية الواجهة الأمامية</title>")
head = head.replace("الدرس 3-1 (الشرح)", "الدرس 3-3 (الشرح + بنك الأسئلة)")

START, TOTAL = 42, 58

FX = '<span class="fx">للفهم</span>'
FXA = '<span class="fx abs">للفهم</span>'
TQ = '<span class="tq">تقييمات</span>'
L = ["أ", "ب", "ج", "د", "هـ", "و"]
AB = '<span class="ab"></span>'
def num(t): return f'<span class="num">{t}</span>'
def tg(t): return f'<bdi class="tg">&lt;{t}&gt;</bdi>'          # وسم HTML جوه سطر عربي
def en(t): return f'<bdi>{t}</bdi>'                             # كلمة إنجليزي جنب كلمة إنجليزي
def lines(n): return '<div class="wl"><i></i></div>' * n
def blank(w=70): return f'<span class="bl" style="width:{w}pt"></span>'
def opts(items, cols=1):
    return f'<ul class="op c{cols}">' + "".join(f'<li><b>{L[k]}‌</b>{t}</li>' for k, t in enumerate(items)) + '</ul>'
def classify(items, letters=None, w=False):
    ks = letters or [str(k + 1) for k in range(len(items))]
    ab = AB.replace('class="ab"', 'class="ab w"') if w else AB
    return '<ul class="cl">' + "".join(f'<li><span class="k">{ks[k]}</span><span class="t">{t}</span>{ab}</li>' for k, t in enumerate(items)) + '</ul>'
def card(n, title, body, tag=""):
    t = f'<h4><span class="n">{n}</span> · {title}{tag}</h4>' if n else ""
    return f'<div class="qcard split {"cont" if not n else ""}">{t}{body}</div>'
def instr(t): return f'<p class="qi">{t}</p>'
def hint(t, label="عناصر الإجابة"): return f'<div class="hint"><b>{label}</b> {t}</div>'
def cat(title, count): return f'<h2 class="cat kwn">{title}<span class="cnt">{count}</span></h2>'
def cmp_table(heads, rows, badge=False, tall=False):
    th = "".join(f"<th>{x}</th>" for x in heads)
    tr = "".join(f'<tr><td class="k">{r}</td>' + "<td></td>" * (len(heads) - 1) + "</tr>" for r in rows)
    t = f'<table class="cmp{" tall" if tall else ""}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
    return f'<div class="cmpw">{TQ}{t}</div>' if badge else t
MARK6 = '<span class="mk">[<span class="num">6</span> درجات]</span>'

def lk(cls, d, c, cx, cy):
    return f'<svg class="lk {cls}" viewBox="0 0 20 16"><path d="{d}" fill="none" stroke="{c}" stroke-width="1.55" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="2" fill="{c}"/></svg>'

# أيقونات الشكل 3.3.1
def ic_html(c):
    return (f'<svg viewBox="0 0 48 48" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M24 4 40 10v14c0 10-7 17-16 20C15 41 8 34 8 24V10z"/><path d="M19 19l-5 5 5 5M29 19l5 5-5 5M26.5 16.5l-5 15"/></svg>')
def ic_css(c):
    return (f'<svg viewBox="0 0 48 48" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M31 7l9 9-19 19-11 3 3-11z"/><path d="M27 11l9 9"/><path d="M9 43h22"/></svg>')
def ic_js(c):
    return (f'<svg viewBox="0 0 48 48" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M27 4 11 27h12l-3 17 17-25H25z"/></svg>')

# ============================ الشرح ============================
E = []
A = E.append
A('''<div class="band">
  <div class="badge"><span class="l">الدرس</span><span class="n">3-3</span></div>
  <h1>أساسيات تقنية الواجهة الأمامية</h1>
  <div class="who">
    <div class="t"><span class="u">الوحدة الثالثة</span><span class="k">الشرح والمراجعة</span></div>
    <img src="assets/avatar.png" alt="">
  </div>
</div>''')
A(f'''<div class="two">
  <div class="intro">
    <h3>أي صفحة ويب بتفتحها… وراها {num("3")} تقنيات أساسية شغالة مع بعض</h3>
    <div class="body">
      <img class="robot" src="assets/robot.svg" alt="">
      <p><b>HTML</b> بيبني هيكل الصفحة،<br><b>CSS</b> بيتحكم في شكلها وتنسيقها،<br>و<b>JavaScript</b> بيضيف التفاعل والسلوك.</p>
      <p>والواجهة الأمامية <bdi class="nw">(Frontend)</bdi> الحديثة بتستخدم كمان أفكار تساعد الصفحة تبقى أوضح، وتتكيّف مع أحجام الشاشات المختلفة، وتسهّل عملية التطوير.</p>
      <p>في الدرس ده هنفهم دور كل تقنية، وبعدها نشوف <b>HTML الدلالية</b>، و<b>التصميم المتجاوب</b>، و<b>أطر العمل</b>.</p>
    </div>
    <div class="foot"><span class="pill-dark">يلا بينا نبدأ يا صديقي ونشوف كل واحدة بتعمل إيه؟</span></div>
  </div>
  <div class="goals">
    <h3>أهداف التعلم</h3>
    <div class="g"><span class="tag">شرح</span><span class="x">الأدوار المميزة لكل من HTML وCSS وJavaScript في بناء صفحة الويب.</span></div>
    <div class="g"><span class="tag">شرح</span><span class="x">كيف تسهم لغة HTML الدلالية <bdi class="nw">(Semantic HTML)</bdi>، والتصميم المتجاوب، وأطر العمل في تحسين الواجهة الأمامية الحديثة.</span></div>
  </div>
</div>''')
A('<div class="note-box"><span class="tag">للفهم</span>أي جزء عليه علامة «للفهم» هو شرح أو رسم إضافي للتوضيح، ومش مطلوب حفظه كنص من الكتاب.</div>')
A(f'''<div class="map m2">
  <div class="cell c1"><h4><span class="mn">1</span>كيف تُبنى صفحة الويب؟</h4><ul>
    <li><b>HTML</b> — يبني بنية الصفحة ومحتواها الأساسي.</li>
    <li><b>CSS</b> — يحدد مظهر الصفحة وتنسيقها.</li>
    <li><b>JavaScript</b> — يضيف السلوك والتفاعلية.</li></ul></div>
  <div class="cell c3"><h4><span class="mn">2</span>HTML الدلالية — عناصر توضّح وظيفة أجزاء الصفحة</h4><ul>
    <li>مثل: <span class="tags">{tg("header")} {tg("nav")} {tg("main")} {tg("footer")}</span></li></ul>
    <div class="sl">الفوائد:</div><ul>
    <li>تساعد قارئ الشاشة على فهم بنية الصفحة.</li>
    <li>قد تساعد محركات البحث على فهم المحتوى بشكل أفضل.</li></ul>
    <div class="imp"><b>مهم:</b> لا تضمن ترتيبًا أعلى في نتائج البحث.</div></div>
  <div class="hub">كيف تُبنى<br>الواجهة الأمامية؟
    {lk("r1", "M0 14 C7 14 10 3 17 3", "#22375c", 17.5, 3)}
    {lk("r2", "M0 2 C7 2 10 13 17 13", "#e29433", 17.5, 13)}
    {lk("l1", "M20 14 C13 14 10 3 3 3", "#2e4a78", 2.5, 3)}
    {lk("l2", "M20 2 C13 2 10 13 3 13", "#a9670f", 2.5, 13)}
  </div>
  <div class="cell c2"><h4><span class="mn">3</span>كيف تتكيف الصفحة مع الشاشات المختلفة؟</h4><div class="term">التصميم المتجاوب</div><ul>
    <li>يتكيف التخطيط تلقائيًا مع أحجام الشاشات المختلفة.</li>
    <li>يساعد على تحسين سهولة الاستخدام.</li>
    <li>مراعاة الشاشات الصغيرة من بداية التصميم تُسمى أحيانًا: «نهج الأولوية للجوال».</li></ul></div>
  <div class="cell c4"><h4><span class="mn">4</span>كيف تساعد أطر العمل المطور؟</h4><div class="term">أطر العمل</div><ul>
    <li>توفر مسبقًا وظائف ومكونات شائعة الاستخدام.</li>
    <li>تقلل الحاجة إلى كتابة كامل الكود من الصفر.</li>
    <li>تساعد على تطوير تطبيقات الويب بكفاءة أكبر.</li></ul>
    <div class="sl">أمثلة من الدرس: <span class="ex">{en("React")} · {en("Vue")} · {en("Next.js")}</span></div></div>
</div>''')
A('''<div class="iq">
  <div class="q">
    <div class="lab">السؤال الرئيسي — الدرس كله بيجاوب عليه</div>
    <div class="qq">كيف تعمل HTML وCSS وJavaScript معًا لبناء صفحة ويب، وما الذي يجعل الواجهة الأمامية الحديثة ذات معنى وقابلة للتكيف وفعّالة في البناء؟</div>
  </div>
  <div class="idea"><span class="qmark">”</span><b>الفكرة الأساسية:</b> تُبنى صفحة الويب من <b>HTML (البنية)</b>، و<b>CSS (المظهر)</b>، و<b>JavaScript (السلوك)</b>؛ وتضيف الواجهة الأمامية الحديثة <b>HTML الدلالية</b> و<b>التصميم المتجاوب</b> و<b>أطر العمل</b>.</div>
</div>''')

# ---- الجزء الأول
A('<div class="part p1"><span>الجزء الأول</span></div>\n<hr class="rule">')
A('<h2 class="sec"><span class="num">1</span><span class="dot">·</span> أدوار HTML وCSS وJavaScript</h2>')
A('<div class="quote"><span class="qmark">”</span>تؤدي التقنيات التالية <b>أدوارًا مختلفة</b> في كثير من صفحات الويب؛ <b>وليس من الضروري أن تستخدم الصفحة الثلاث كلها معًا</b>.<br>يمكن أن تستخدم الصفحة <b>HTML وحده</b>، أو <b>HTML مع CSS وJavaScript</b> بحسب الوظائف التي تحتاج إليها.</div>')
A(f'''<div class="fig keep">
  <div class="tri">
    <div class="tc h"><span class="ic">{ic_html("#22375c")}</span><h4>HTML</h4><div class="rl">البنية</div><p><b>يحدد بنية (هيكل) صفحة الويب</b>. يصف عناصر مثل <b>العناوين والفقرات والصور والروابط</b>.</p><span class="an">هيكل المبنى</span></div>
    <div class="tc c"><span class="ic">{ic_css("#a9670f")}</span><h4>CSS</h4><div class="rl">المظهر</div><p><b>يحدد مظهر صفحة الويب</b> (الألوان، التخطيط، الحجم، الخطوط، إلخ).</p><span class="an">الديكور الداخلي والخارجي</span></div>
    <div class="tc j"><span class="ic">{ic_js("#2e4a78")}</span><h4>JavaScript</h4><div class="rl">السلوك</div><p><b>يضيف السلوك والتفاعلية</b> إلى صفحة الويب. <b>يفعّل الاستجابات عند الضغط على الأزرار وتحديثات جزء فقط من الشاشة</b>.</p><span class="an">الكهرباء والسباكة</span></div>
  </div>
  <div class="cap">الشكل <span class="num">3.3.1</span> — أدوار HTML وCSS وJavaScript</div>
</div>''')
A(f'''<div class="anl keep">
  <div class="hd"><span class="lb">{N.bulb("#e29433")}ببساطة</span><span>التشبيه ده من كتاب المدرسة: صفحة الويب زي بناء بيت.</span></div>
  <div class="row">
    <div class="it"><div class="t"><b>HTML</b><i>=</i><span>هيكل المبنى</span></div><small>العناوين، الفقرات، الصور، الروابط</small></div>
    <div class="it"><div class="t"><b>CSS</b><i>=</i><span>الديكور الداخلي والخارجي</span></div><small>الألوان، التخطيط، الحجم، الخطوط</small></div>
    <div class="it"><div class="t"><b>JavaScript</b><i>=</i><span>أنظمة الكهرباء والسباكة</span></div><small>الاستجابة للأزرار، وتحديث جزء من الشاشة</small></div>
  </div>
  {HOUSE}
  <div class="ft">ومش شرط الصفحة تستخدم التلاتة معًا.</div>
  <div class="sum"><b>HTML</b> يبني، <b>CSS</b> ينسّق، <b>JavaScript</b> يضيف التفاعل.</div>
</div>''')
A(f'''<div class="chx keep">{FXA}
  <div class="hd"><span class="lb">مثال إضافي للتوضيح:</span><span class="tt">واجهة دردشة شبيهة بواتساب</span></div>
  <div class="row">
    <div class="it">{chat("html")}<p><b class="k">HTML</b> يبني بنية الصفحة وعناصرها: اسم الشخص، الرسائل، مربع الكتابة، زر الإرسال.</p></div>
    <div class="it">{chat("css")}<p><b class="k">CSS</b> يحدد شكلها: لون الرسائل، حجم الخط، المسافات، مكان كل عنصر.</p></div>
    <div class="it">{chat("js")}<p><b class="k">JavaScript</b> يضيف التفاعل: عند الضغط على إرسال تظهر الرسالة، وقد يتغير عداد الرسائل أو يظهر تنبيه.</p></div>
  </div>
</div>''')

# ---- الجزء الثاني
A('<div class="part p2"><span>الجزء الثاني</span></div>\n<hr class="rule">')
A('<h2 class="sec"><span class="num">2</span><span class="dot">·</span> HTML الدلالية</h2>')
A('<span class="chip">HTML الدلالي (Semantic HTML)</span>')
A(f'<div class="banner kwn"><b>استخدام عناصر توضح وظيفة أجزاء الصفحة</b>، مثل <b>{tg("header")}</b> في أعلى الصفحة، و<b>{tg("nav")}</b> للتنقل، و<b>{tg("main")}</b> للمحتوى الرئيس، و<b>{tg("footer")}</b> في أسفل الصفحة.</div>')
IC_ACC = '<svg viewBox="0 0 24 24" fill="none" stroke="#2e4a78" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10.2"/><circle cx="12" cy="6.9" r="1.5" fill="#2e4a78" stroke="none"/><path d="M7 10h10M12 10v4.2M12 14.2l-2.6 4.3M12 14.2l2.6 4.3"/></svg>'
IC_SEO = '<svg viewBox="0 0 24 24" fill="none" stroke="#2e4a78" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="10.5" cy="10.5" r="6.8"/><path d="M15.6 15.6 20.5 20.5M7.6 9h5.8M7.6 12.2h4"/></svg>'
A(f'''<div class="bens">
  <div class="bh"><span>فوائده</span></div>
  <div class="br"><i class="s"></i><i class="l"></i><i class="r"></i><i class="a al"></i><i class="a ar"></i></div>
  <div class="bg">
    <div class="bc">
      <div class="bt"><span class="bn">1</span>{IC_ACC}<b>إمكانية الوصول</b></div>
      <div class="be"><bdi class="nw">(Accessibility)</bdi></div>
      <p>يساعد HTML الدلالي <b>قارئ الشاشة على فهم بنية الصفحة والتنقل فيها</b>،</p>
      <div class="bw">مع الحاجة إلى ممارسات وصول أخرى أيضًا.</div>
    </div>
    <div class="bc">
      <div class="bt"><span class="bn">2</span>{IC_SEO}<b>فهم محركات البحث للمحتوى</b></div>
      <div class="be"><bdi class="nw">(Search Engine Optimization – SEO)</bdi></div>
      <p><b>قد يساعد</b> HTML الدلالي محركات البحث على فهم بنية المحتوى بصورة أفضل،</p>
      <div class="bw">لكنه لا يضمن ترتيبًا أعلى.</div>
    </div>
  </div>
</div>''')
A(f'<div class="note-line"><span class="tag">للفهم</span><span class="lead">طب ليه؟</span>العنصر العام زي <b>{tg("div")}</b> <b>ما بيوضّحش وظيفته</b> من اسمه، لكن عنصر زي <b>{tg("nav")}</b> <b>بيوضّح إن الجزء ده مخصّص للتنقل</b>. وده بيساعد <b>قارئات الشاشة</b> على فهم بنية الصفحة بشكل أفضل، <b>وممكن يساعد محركات البحث</b> كمان.</div>')
A('<h2 class="sec"><span class="num">3</span><span class="dot">·</span> التصميم المتجاوب</h2>')
A('<span class="chip">التصميم المتجاوب</span>')
A('<div class="banner"><b>مفهوم تصميمي يُضبط فيه التخطيط تلقائيًا وفقًا لأحجام الشاشات المختلفة</b> مثل أجهزة الكمبيوتر والهواتف الذكية والأجهزة اللوحية. ويساعد الصفحة على <b>التكيف مع أحجام الشاشات المختلفة وتحسين سهولة استخدامها</b>.</div>')
ARL = '<svg viewBox="0 0 20 12" fill="none" stroke="#e29433" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 6H3M8 1 3 6l5 5"/></svg>'
IC_PH = '<svg viewBox="0 0 24 24" fill="none" stroke="#2e4a78" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.3h2"/></svg>'
IC_PEN = '<svg viewBox="0 0 24 24" fill="none" stroke="#2e4a78" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20l1-4L16 5l3 3L8 19l-4 1zM14 7l3 3"/></svg>'
IC_FLAG = '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M3.5 12.2V4.5a1 1 0 0 1 1-1h7.7L21 12.3l-8.7 8.7z"/><circle cx="8" cy="8" r="1.4" fill="#fff" stroke="none"/></svg>'
A(f'''<div class="mf">
  <div class="st"><span class="ic">{IC_PH}</span><p>يستخدم كثير من الناس الويب <b>عبر الهواتف</b>،</p></div>
  <i class="ar">{ARL}</i>
  <div class="st"><span class="ic">{IC_PEN}</span><p>لذلك <b>يراعي المطورون الشاشات الصغيرة منذ بداية التصميم</b>.</p></div>
  <i class="ar">{ARL}</i>
  <div class="st nm"><span class="ic">{IC_FLAG}</span><p>ويسمى ذلك أحيانًا <b>نهج الأولوية للجوال</b>.</p></div>
</div>''')
A(f'''<div class="fig keep" style="position:relative">{FXA}
  <div class="resp">
    <div class="dev pc"><div class="scr"><i class="bar"></i><div class="cols"><i>1</i><i>2</i><i>3</i></div><i class="bar"></i></div><b>كمبيوتر — ثلاثة أعمدة</b></div>
    <div class="go"><svg viewBox="0 0 60 12" fill="none" stroke="#e29433" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M58 6H5" stroke-dasharray="4 3.5"/><path d="M9.5 1.5 4 6l5.5 4.5"/></svg><small>يتكيف</small></div>
    <div class="dev tb"><div class="scr"><i class="bar"></i><div class="cols"><i>1</i><i>2</i></div><div class="cols"><i>3</i></div><i class="bar"></i></div><b>تابلت — عمودان</b></div>
    <div class="go"><svg viewBox="0 0 60 12" fill="none" stroke="#e29433" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M58 6H5" stroke-dasharray="4 3.5"/><path d="M9.5 1.5 4 6l5.5 4.5"/></svg><small>يتكيف</small></div>
    <div class="dev ph"><div class="scr"><i class="bar"></i><i class="blk">1</i><i class="blk">2</i><i class="blk">3</i><i class="bar"></i></div><b>هاتف — عمود واحد</b></div>
  </div>
  <div class="cap">التصميم المتجاوب يعيد تنسيق العرض ليناسب كل حجم شاشة</div>
</div>''')
A(f'<div class="note-line"><span class="tag">للفهم</span><span class="lead">طب ليه؟</span>لأن أحجام الشاشات <b>كتير جدًا</b>، ومش منطقي نعمل نسخة من الصفحة لكل جهاز. بدل كده بنعمل <b>صفحة واحدة</b>، و<b>تخطيطها بيتغير حسب عرض الشاشة</b>.</div>')
A('<h2 class="sec"><span class="num">4</span><span class="dot">·</span> أطر العمل</h2>')
A('<span class="chip">إطار العمل</span>')
A('<div class="banner"><b>بنية توفر مسبقًا وظائف ومكونات شائعة الاستخدام</b>، وذلك <b>لجعل عملية تطوير تطبيقات الويب أكثر كفاءة</b>. وعند استخدام إطار عمل، <b>لا يحتاج المطورون إلى كتابة كامل الكود البرمجي من الصفر</b>، ويمكنهم التطوير بكفاءة أكبر.</div>')
A('''<div class="fw keep">
  <div class="fwh"><span>مكتبات وأطر شائعة لتطوير الويب</span></div>
  <div class="lk"><i class="s"></i><i class="h"></i><i class="a al"></i><i class="a am"></i><i class="a ar"></i></div>
  <div class="fg">
    <div class="fc"><div class="fh"><span class="fn">React</span><span class="ft">مكتبة JavaScript</span></div><p><b>مكتبة JavaScript</b> لبناء واجهات المستخدم من <b>مكونات قابلة لإعادة الاستخدام</b> وتحديثها عند تغير البيانات.</p></div>
    <div class="fc"><div class="fh"><span class="fn">Vue</span></div><p>له <b>بنية بسيطة</b> ويتيح بناء تطبيقات الويب <b>تدريجيًا</b> بدءًا من ميزات صغيرة.</p></div>
    <div class="fc"><div class="fh"><span class="fn">Next.js</span><span class="ft">إطار مبني على React</span></div><p><b>إطار مبني على React</b> لبناء تطبيقات ويب، ويوفر <b>التوجيه</b> وطرقًا مختلفة لعرض الصفحات والعمل <b>على الخادم والعميل</b>.</p></div>
  </div>
  <div class="cap">تساعد المكتبات وأطر العمل على بناء الصفحات من مكوّنات قابلة لإعادة الاستخدام.</div>
</div>''')
A('<div class="note-line"><span class="tag">للفهم</span><span class="lead">ببساطة</span>خُد بالك من فرق صغير الكتاب بيقوله بالنص: <b>React «مكتبة»</b>، و<b>Next.js «إطار مبني على React»</b>. المصطلحين مختلفين: <b>React</b> مكتبة، و<b>Next.js</b> إطار مبني عليها — ركّز في الفرق لأنه ممكن ييجي في سؤال مباشر.</div>')
A('<div class="kidea keep"><div class="kh">الفكرة الرئيسة</div><p>صفحة الويب الحديثة هي <b>تركيبة، وليست تقنية واحدة</b>: <b>HTML</b> يبني بنيتها، و<b>CSS</b> ينسّق مظهرها، و<b>JavaScript</b> يجعلها تفاعلية – بينما تجعل <b>HTML الدلالية</b> و<b>التصميم المتجاوب</b> و<b>أطر العمل</b> بناءها <b>ذا معنى وقابلًا للتكيف وفعّالًا</b>.</p></div>')
A('<div class="big">سؤال على نمط الامتحان — ونموذج إجابته</div>\n<hr class="rule">')
A(f'''<div class="exam keep">
  <div class="hd"><span class="n">1</span><span class="t">سؤال على نمط الامتحان</span><span class="m">[{num("6")} درجات]</span></div>
  <div class="qt">اشرح كيف تساهم كل من HTML وCSS وJavaScript في صفحة مكتبة تعرض قائمة كتب، وتكون منسّقة، وتُصفّي النتائج أثناء كتابة المستخدم.</div>
  <div class="hint"><b>راجع:</b> البنية، المظهر، السلوك.</div>
</div>''')
A('<h3 class="sub">سؤال على نمط الامتحان — إجابة نموذجية</h3>')
A(f'''<div class="box white split">
  <h3>نموذج إجابة مقترح لسؤال الـ{num("6")} درجات{FX}</h3>
  <ol style="counter-reset:n 0"><li><b>HTML — البنية:</b> يحدد <b>هيكل الصفحة</b> — <b>عنوان الصفحة</b>، و<b>قائمة الكتب</b> كعناصر (عناوين وفقرات وصور وروابط)، و<b>مربع البحث</b> نفسه.</li></ol>
  <ol style="counter-reset:n 1"><li><b>CSS — المظهر:</b> يحدد <b>الألوان والتخطيط والحجم والخطوط</b> — فتظهر قائمة الكتب <b>منسّقة</b> ومرتّبة وسهلة القراءة.</li></ol>
  <ol style="counter-reset:n 2"><li><b>JavaScript — السلوك:</b> يضيف <b>التفاعلية</b> — <b>يُصفّي النتائج أثناء كتابة المستخدم</b> و<b>يحدّث جزءًا فقط من الشاشة</b> بدل إعادة تحميل الصفحة كلها.</li></ol>
  <ol style="counter-reset:n 3"><li><b>التعاون بينهم:</b> <b>HTML يحمل المحتوى</b>، و<b>CSS ينسّقه</b>، و<b>JavaScript يجعله يتفاعل ويُحدِّث</b>.</li></ol>
  <ol style="counter-reset:n 4"><li><b>إضافة تستحق الذكر:</b> استخدام <b>HTML الدلالية</b> ({tg("header")} · {tg("nav")} · {tg("main")}) يساعد <b>قارئ الشاشة</b>، و<b>التصميم المتجاوب</b> يجعل الصفحة صالحة على <b>الهاتف</b> كما على الحاسوب.</li></ol>
  <div class="tip"><span class="l">ركّز:</span> التلميح سمّى <b>تلات كلمات</b> — البنية · المظهر · السلوك. اربط <b>كل تقنية بمهمة من مهام صفحة المكتبة نفسها</b> (قائمة الكتب · التنسيق · التصفية أثناء الكتابة)، مش بتعريف عام.</div>
</div>''')
A('<h2 class="sec"><span class="num"></span>إجابة السؤال الرئيسي</h2>')
A('''<div class="mq">
  <div class="lab">السؤال</div>
  <div class="qq">كيف تعمل HTML وCSS وJavaScript معًا لبناء صفحة ويب، وما الذي يجعل الواجهة الأمامية الحديثة ذات معنى وقابلة للتكيف وفعّالة في البناء؟</div>
</div>''')
A('<div class="quote"><span class="qmark">”</span>تستخدم كثير من صفحات الويب <b>HTML لبناء الهيكل</b>، ويمكن أن تضيف <b>CSS للمظهر</b> و<b>JavaScript للتفاعل بحسب الحاجة</b>. ويستخدم <b>HTML الدلالي</b> عناصر توضح وظيفة أجزاء الصفحة، ما <b>يساعد التقنيات المساعدة ومحركات البحث على فهم بنيتها</b>. ويجعل <b>التصميم المتجاوب</b> الصفحة <b>تتكيف مع أحجام الشاشات المختلفة</b>. كما <b>تساعد المكتبات والأطر</b> على بناء الواجهة من <b>مكونات قابلة لإعادة الاستخدام</b> وتقليل بعض العمل المتكرر: فـ<b>React مكتبة</b> لبناء واجهات المستخدم، و<b>Next.js إطار مبني عليها</b> لبناء تطبيقات ويب.</div>')
A('''<div class="terms keep">
  <div class="th"><h3>مصطلحات أساسية</h3><div class="t3"><span><b>HTML</b> – البنية.</span><span><b>CSS</b> – المظهر.</span><span><b>JavaScript</b> – السلوك.</span></div></div>
  <div class="t2">
    <div><b>التصميم المتجاوب</b> – يتكيف التخطيط مع حجم الشاشة.</div>
    <div><b>إطار العمل</b> – وظائف جاهزة لتطوير أكثر كفاءة.</div>
    <div><b>إمكانية الوصول <bdi class="nw">(Accessibility)</bdi></b> – تصميم المحتوى والواجهة بحيث يمكن لأصحاب القدرات والاحتياجات المختلفة استخدامها، بمن فيهم ذوو الإعاقة.</div>
    <div><b><bdi>SEO</bdi> (تحسين محركات البحث)</b> – ممارسات تجعل الصفحة أيسر في الفهرسة والظهور في نتائج البحث.</div>
  </div>
</div>''')
A(f'''<div class="dark keep">
  <h3>الخلاصة في دقيقة</h3>
  <p class="rem"><b>تذكّر:</b> HTML يبني البنية، وCSS ينسّق المظهر، وJavaScript يضيف السلوك – وتجعل HTML الدلالية والتصميم المتجاوب وأطر العمل الواجهة الأمامية الحديثة ذات معنى وقابلة للتكيف وفعّالة.</p>
  <div class="g2">
    <ul>
      <li><b>HTML</b> البنية (هيكل مبنى) · <b>CSS</b> المظهر (الديكور) · <b>JavaScript</b> السلوك (الكهرباء والسباكة).</li>
      <li><b>HTML الدلالية:</b> {en("header")} · {en("nav")} · {en("main")} · {en("footer")} — تساعد <b>قارئ الشاشة</b>، و<b>قد تساعد محركات البحث بدون ضمان ترتيب أعلى</b>.</li>
      <li><b>إطار العمل: وظائف ومكونات جاهزة</b> — تطوير <b>أكثر كفاءة</b> بدون كتابة كل الكود من الصفر.</li>
    </ul>
    <ul>
      <li><b>مش لازم</b> الصفحة تستخدم التلاتة معًا.</li>
      <li><b>التصميم المتجاوب:</b> يُضبط <b>تلقائيًا</b> وفقًا لأحجام الشاشات · و<b>نهج الأولوية للجوال</b> = مراعاة الشاشات الصغيرة من البداية.</li>
      <li><b>أمثلة:</b> <b>React</b> مكتبة · <b>Vue</b> بسيط وتدريجي · <b>Next.js</b> إطار مبني على <b>React</b>.</li>
    </ul>
  </div>
</div>''')
A('''<div class="check keep kwn">
  <h3>اتأكد إنك قادر على</h3>
  <div class="g2">
    <ul>
      <li><span>أعرف <b>دور</b> كل تقنية من التلاتة <b>وتشبيهها</b> في الكتاب.</span></li>
      <li><span>أعرف <b>عناصر HTML الدلالية الأربعة</b> ووظيفة كل واحد.</span></li>
      <li><span>أعرف تعريف <b>التصميم المتجاوب</b> و<b>سبب</b> الحاجة له.</span></li>
      <li><span>مابقولش إن الدلالية <b>تضمن</b> ترتيبًا أعلى في البحث.</span></li>
    </ul>
    <ul>
      <li><span>أقدر أصنّف أي مهمة على <b>HTML</b> ولا <b>CSS</b> ولا <b>JavaScript</b>.</span></li>
      <li><span>أعرف <b>فائدتَي</b> HTML الدلالية <b>وتحفّظ كل واحدة</b>.</span></li>
      <li><span>أعرف تعريف <b>إطار العمل</b> وأفرّق بين <b>مكتبة</b> و<b>إطار</b>.</span></li>
    </ul>
  </div>
</div>''')
A('<div class="endline">أكواد مع زياد — أ/ زياد السعدني · مذكرة البرمجة والذكاء الاصطناعي — تانية ثانوي <span class="num">2026/2027</span> · الوحدة الثالثة — الدرس <span class="num">3-3</span></div>')
A('<div class="pb"></div>')
A('''<div class="band" style="height:55pt;padding-right:12pt">
  <div class="badge"><span class="n">3-3</span></div>
  <h1 style="text-align:right;margin-right:12pt;font-size:14pt">لخّص الدرس بأسلوبك</h1>
</div>''')
A('<div class="instr"><span class="fx fl">للفهم</span>اقفل المذكرة وحاول تلخّص الدرس من غير ما تبصّ: اكتب أهم <b>المصطلحات</b>، و<b>الفكرة الأساسية</b>، و<b>النقطة اللي لسه محتاجة مراجعة</b>. بعد كده افتح المذكرة وقارن اللي كتبته.</div>')
A('<div class="lines">' + '<div></div>' * 24 + '</div>')

# ============================ بنك الأسئلة ============================
B = []
A = B.append
A('<div class="pb"></div>')
A('''<div class="band">
  <div class="badge"><span class="l">الدرس</span><span class="n">3-3</span></div>
  <h1>أساسيات تقنية الواجهة الأمامية</h1>
  <div class="who"><div class="t"><span class="u">الوحدة الثالثة</span><span class="k">بنك الأسئلة</span></div><img src="assets/avatar.png" alt=""></div>
</div>''')

# ---- الأسئلة اللي جت في «تقييمات الترم الاول» ص58–62 (المطابقة في taq_map.md)
TQ_MCQ = {1, 2, 3, 8, 9, 15, 16, 17, 20, 21, 22, 29}
TAQ_ESS = [   # الناقصة من البنك، بصياغتها
 ("وضّح كيف يساعد التصميم المتجاوب في تحسين تجربة المستخدم.", 3),
 ("ناقش كيف تسهم CSS في تحسين المظهر البصري للصفحة.", 3),
 ("اذكر مثالًا على عنصر HTML دلالي، واشرح فائدته في تحسين الوصول.", 3),
 ("كيف تُضيف JavaScript التفاعلية إلى صفحة الويب مع مثال عملي؟", 3),
 ("ناقش دور إطار العمل Next.js في تطوير تطبيقات الويب الحديثة.", 3),
]

# ---- أسئلة الكتاب
BOOK = []
BOOK.append(card("01", "المثال المحلول — الجزء الأول",
       instr("ضع علامة ○ إذا كانت العبارة (أ - د) صحيحة أو × إذا كانت خاطئة.")
       + '<ul class="tf">' + "".join(f'<li><b>{L[k]}</b><span class="t">{t}</span><span class="pr">(&nbsp;&nbsp;&nbsp;&nbsp;)</span></li>' for k, t in enumerate([
           "HTML تقنية تحدد بنية (هيكل) صفحة الويب.",
           "CSS تقنية تضيف سلوكًا إلى صفحة الويب.",
           "التصميم المتجاوب مفهوم يُضبط فيه التخطيط تلقائيًا وفقًا لأحجام الشاشات المختلفة.",
           "استخدام إطار عمل يُلغي الحاجة إلى كتابة كل الكود من الصفر ويتيح التطوير بكفاءة."])) + '</ul>'))
BOOK.append(card("02", "المثال المحلول — الجزء الثاني",
       instr("طابق كل دور (1 - 3) مع التقنية الأنسب من الخيارات أدناه (أ - ج).")
       + '<div class="match"><div class="mb"><h5>الأدوار</h5><ol>'
       + "".join(f'<li><span>{t}</span>{AB}</li>' for t in [
           "يحدد بنية صفحة الويب", "يحدد مظهر صفحة الويب", "يضيف السلوك والتفاعلية إلى صفحة الويب"])
       + '</ol></div><div class="mb"><h5>الخيارات</h5>' + opts(["HTML", "CSS", "JavaScript"], 1) + '</div></div>'))
SOL1 = [("أ", "تحدد HTML بنية صفحة الويب. لذلك، ○."), ("ب", "CSS تقنية تحدد مظهر صفحة الويب. أما إضافة السلوك فهي JavaScript. لذلك، ×."), ("ج", "تعريف صحيح للتصميم المتجاوب. لذلك، ○."), ("د", "وصف صحيح لفائدة أطر العمل. لذلك، ○.")]
SOL2 = [("1", "تحديد البنية هو HTML.", "أ"), ("2", "تحديد المظهر هو CSS.", "ب"), ("3", "إضافة السلوك هي JavaScript.", "ج")]
BOOK.append('<div class="qcard sol keep"><h4><span class="ck">✓</span> الحل — المثال المحلول</h4><div class="sg">'
       + '<div><div class="sp">(1)</div>' + "".join(f'<div class="sr"><b>{a}</b><span>{t}</span></div>' for a, t in SOL1) + '</div>'
       + '<div><div class="sp">(2)</div>' + "".join(f'<div class="sr"><b>{a}:</b><span>{t} <i>{c}</i></span></div>' for a, t, c in SOL2) + '</div>'
       + '</div></div>')
BOOK.append(card("03", "تدرّب — أجب عن الأسئلة التالية",
       '<div class="sa">' + "".join(f'<div><span class="k">{k+1}</span><p>{t} {blank(80)}</p></div>' for k, t in enumerate([
           "ما هو الاختصار المكوّن من أربعة أحرف للتقنية التي تحدد بنية (هيكل) صفحة الويب؟",
           "ما هو الاختصار المكوّن من ثلاثة أحرف للتقنية التي تحدد مظهر صفحة الويب (الألوان، التخطيط، الحجم، إلخ)؟",
           "ما هو مصطلح التقنية التي تضيف السلوك والتفاعلية إلى صفحة الويب؟",
           "ما هو مصطلح مفهوم التصميم الذي يُضبط فيه التخطيط تلقائيًا وفقًا لأحجام الشاشات المختلفة؟"])) + '</div>'))
BOOK.append(card("04", "تدرّب — اختيار",
       '<p class="qs"><b>توقّف وفكّر:</b> أي من الفوائد أدناه تتعلق بمظهر الصفحة، وأيها تتعلق بمدى سهولة إيجادها وقراءتها من قبل الآخرين؟</p>' + lines(2)
       + '<div class="qq"><span class="k">1</span><p>من بين الخيارات التالية (أ - د)، اختر الخيار الذي <b>لا يمثّل فائدة مناسبة</b> لاستخدام HTML الدلالية.</p></div>'
       + opts(["يمكن لبرامج قارئ الشاشة فهم بنية الصفحة بشكل صحيح.", "يمكن لمحركات البحث فهم محتوى صفحة الويب بسهولة أكبر.", "تصبح سرعة عرض صفحة الويب أسرع بالضرورة.", "يصبح إيصال المعلومات أسهل للمستخدمين ذوي الإعاقة البصرية."], 1)
       + '<div class="qq"><span class="k">2</span><p>من بين الخيارات التالية (أ - د)، اختر الخيار الذي يصف <b>إطار العمل</b> بأنسب شكل.</p></div>'
       + opts(["لغة لتحديد بنية صفحة الويب", "بنية تجعل تطوير تطبيقات الويب أكثر كفاءة", "تقنية لتشفير البيانات وإرسالها بأمان", "مفهوم تصميمي لدعم أحجام الشاشات المختلفة"], 1)))
BOOK.append(card("05", "سؤال على نمط الامتحان",
       '<p class="qs">اشرح كيف تساهم كل من HTML وCSS وJavaScript في صفحة مكتبة تعرض قائمة كتب، وتكون منسّقة، وتُصفّي النتائج أثناء كتابة المستخدم.</p>'
       + hint("<b>راجع:</b> البنية، المظهر، السلوك.") + lines(6), tag=MARK6 + TQ))
BOOK.append(card("06", "تمارين — اقرأ الفقرة ثم املأ الفراغات",
       f'<p class="para">تستخدم كثير من صفحات الويب (<b>1</b>) {blank(75)} لتحديد البنية، ويمكن أن تستخدم (<b>2</b>) {blank(75)} لتنسيق المظهر، و(<b>3</b>) {blank(75)} لإضافة السلوك والتفاعل. ويسمى تصميم التخطيط ليتكيف مع أحجام الشاشات المختلفة (<b>4</b>) {blank(75)}.</p>'))
BOOK.append(card("07", "تمارين — التقنية المستخدمة · واختيار",
       '<div class="qq"><span class="k">1</span><p>بالنسبة لكل من المهام (1 - 6)، حدد التقنية المستخدمة لتحقيقها: <b>أ</b> HTML، <b>ب</b> CSS، <b>ج</b> JavaScript.</p></div>'
       + classify(["وصف بنية العناوين والفقرات", "تغيير لون النص وحجمه", "تحديث جزء من الشاشة عند الضغط على زر", "وضع الصور والروابط", "تحديد لون خلفية الصفحة بأكملها", "التحقق من صحة المحتويات المُدخلة في نموذج"])
       + '<div class="qq"><span class="k">2</span><p>من بين الخيارات التالية (أ - د)، اختر الخيار الذي يصف <b>بأنسب شكل</b> سبب الحاجة إلى التصميم المتجاوب.</p></div>'
       + opts(["لتحسين سرعة عرض المواقع الإلكترونية", "لأن المواقع الإلكترونية يتم الوصول إليها من أجهزة متنوعة مثل أجهزة الكمبيوتر والهواتف الذكية والأجهزة اللوحية", "لرفع الترتيب في محركات البحث", "لإضافة سلوك إلى صفحات الويب"], 1)))

# ---- اختر
MCQ = [
 ("التقنية التي <b>تحدد بنية</b> صفحة الويب هي:", ["HTML", "CSS", "JavaScript", "JSON"]),
 ("التقنية التي <b>تحدد المظهر</b> (الألوان والتخطيط والخطوط) هي:", ["HTML", "JavaScript", "CSS", "API"]),
 ("التقنية التي <b>تضيف السلوك والتفاعلية</b> هي:", ["HTTPS", "CSS", "HTML", "JavaScript"]),
 ("التشبيه الذي يستخدمه الكتاب لـHTML هو:", ["أثاث المبنى", "الديكور الداخلي والخارجي", "أنظمة الكهرباء والسباكة", "هيكل مبنى"]),
 ("التشبيه الذي يستخدمه الكتاب لـJavaScript هو:", ["أنظمة الكهرباء والسباكة", "هيكل مبنى", "الديكور", "واجهة المبنى"]),
 ("حسب الكتاب، استخدام التقنيات الثلاث معًا:", ["ضروري في كل صفحة", "يتوقف على المتصفح", "ممنوع", "ليس ضروريًا؛ فالصفحة قد تستخدم HTML وحده"]),
 ("«استخدام عناصر توضح وظيفة أجزاء الصفحة» هو:", ["التصميم المتجاوب", "إطار العمل", "HTML الدلالية", "تحسين محركات البحث"]),
 ("العنصر الدلالي المستخدم <b>للتنقل</b> هو:", [tg("header"), tg("nav"), tg("main"), tg("footer")]),
 ("العنصر الدلالي المستخدم <b>للمحتوى الرئيس</b> هو:", [tg("footer"), tg("nav"), tg("main"), tg("header")]),
 ("من فوائد HTML الدلالية:", ["تسريع الإنترنت", "مساعدة قارئ الشاشة على فهم بنية الصفحة والتنقل فيها", "تشفير البيانات", "تقليل حجم الصور"]),
 ("حسب الكتاب، HTML الدلالية بالنسبة لمحركات البحث:", ["تضمن ترتيبًا أعلى", "قد تساعدها على فهم بنية المحتوى، لكنها لا تضمن ترتيبًا أعلى", "تمنعها من الفهرسة", "لا علاقة لها بها"]),
 ("أيٌّ مما يلي <b>ليس</b> فائدة مناسبة لـHTML الدلالية؟", ["أن تصبح سرعة العرض أسرع بالضرورة", "فهم محركات البحث للمحتوى", "فهم قارئ الشاشة لبنية الصفحة", "تيسير إيصال المعلومات لذوي الإعاقة البصرية"]),
 ("«تصميم المحتوى والواجهة بحيث يمكن لأصحاب القدرات والاحتياجات المختلفة استخدامها» هو:", ["تحسين محركات البحث", "إمكانية الوصول", "التصميم المتجاوب", "إطار العمل"]),
 ("«ممارسات تجعل الصفحة أيسر في الفهرسة والظهور في نتائج البحث» هي:", ["SEO", "إمكانية الوصول", "إطار العمل", "JSON"]),
 ("«مفهوم تصميمي يُضبط فيه التخطيط تلقائيًا وفقًا لأحجام الشاشات المختلفة» هو:", ["HTML الدلالية", "التصميم المتجاوب", "إطار العمل", "إمكانية الوصول"]),
 ("سبب الحاجة إلى التصميم المتجاوب هو:", ["رفع الترتيب في محركات البحث", "إضافة سلوك للصفحة", "تسريع عرض المواقع", "الوصول إلى المواقع من أجهزة متنوعة بأحجام شاشات مختلفة"]),
 ("«مراعاة الشاشات الصغيرة منذ بداية التصميم» يسمى أحيانًا:", ["نهج الأولوية للجوال", "نهج انعدام الثقة", "الدفاع في العمق", "التصميم الدلالي"]),
 ("«بنية توفر مسبقًا وظائف ومكونات شائعة الاستخدام» هي:", ["SEO", "HTML الدلالية", "إطار العمل", "إمكانية الوصول"]),
 ("الفائدة الأساسية من إطار العمل هي:", ["تسريع الإنترنت", "تشفير البيانات", "عدم الحاجة إلى كتابة كامل الكود من الصفر والتطوير بكفاءة أكبر", "منع الأخطاء نهائيًا"]),
 ("React — حسب الكتاب — هي:", ["قاعدة بيانات", "بروتوكول اتصال", "صيغة بيانات", "مكتبة JavaScript لبناء واجهات المستخدم من مكونات قابلة لإعادة الاستخدام"]),
 ("Next.js — حسب الكتاب — هو:", ["إطار مبني على React لبناء تطبيقات ويب", "مكتبة مستقلة لا علاقة لها بـReact", "لغة برمجة جديدة", "متصفح ويب"]),
 ("Vue — حسب الكتاب — يتميز بـ:", ["التشفير القوي", "بنية بسيطة وبناء تطبيقات الويب تدريجيًا بدءًا من ميزات صغيرة", "تخزين البيانات", "إدارة الشبكات"]),
 ("«تغيير لون النص وحجمه» مهمة تخصّ:", ["HTML", "JavaScript", "CSS", "SEO"]),
 ("«التحقق من صحة المحتويات المُدخلة في نموذج» مهمة تخصّ:", ["HTML", "CSS", "إطار العمل", "JavaScript"]),
 ("«وضع الصور والروابط» مهمة تخصّ:", ["HTML", "CSS", "JavaScript", "JSON"]),
 ("أيُّ العبارات التالية <b>خطأ</b>؟", ["HTML يحدد بنية الصفحة", "التصميم المتجاوب يضبط التخطيط تلقائيًا", "JavaScript يضيف التفاعلية", "CSS يضيف سلوكًا إلى الصفحة"]),
 ("الفكرة الرئيسة تصف صفحة الويب الحديثة بأنها:", ["تركيبة، وليست تقنية واحدة", "تقنية واحدة متطورة", "ملف نصي بسيط", "برنامج يعمل على الخادم فقط"]),
 ("«تحديث جزء من الشاشة فقط» من قدرات:", ["CSS", "JavaScript", "HTML", "SEO"]),
 # من التقييمات (مش موجود في البنك)
 ('كل ما يلي من عناصر HTML الدلالية (<bdi class="nw">Semantic HTML</bdi>) <b>ما عدا</b>:', [tg("header"), tg("main"), tg("E-mail"), tg("footer")]),
]
assert len(MCQ) == 29

# ---- أكمل
FILL = [
 f"التقنية التي تحدد بنية (هيكل) صفحة الويب هي {blank()}",
 f"التقنية التي تحدد مظهر صفحة الويب هي {blank()}",
 f"التقنية التي تضيف السلوك والتفاعلية هي {blank()}",
 f"استخدام عناصر توضح وظيفة أجزاء الصفحة يُسمى {blank()}",
 f"العناصر الدلالية الأربعة في الكتاب هي: {tg('header')} و{blank(45)} و{blank(45)} و{tg('footer')}",
 f"المفهوم الذي يُضبط فيه التخطيط تلقائيًا وفقًا لأحجام الشاشات هو {blank()}",
 f"مراعاة الشاشات الصغيرة منذ بداية التصميم يسمى أحيانًا {blank()}",
 f"البنية التي توفر مسبقًا وظائف ومكونات شائعة الاستخدام هي {blank()}",
 f"تصميم المحتوى بحيث يستخدمه أصحاب القدرات المختلفة يُسمى {blank()}",
 f"الممارسات التي تجعل الصفحة أيسر في الفهرسة والظهور في نتائج البحث تُسمى {blank()}",
]

# ---- صح وخطأ
TF = [
 "HTML يحمل محتوى الصفحة مثل العناوين والفقرات والروابط.",
 "JavaScript مسؤول عن ألوان الصفحة وخطوطها.",
 "من الضروري أن تستخدم كل صفحة ويب التقنيات الثلاث معًا.",
 f"{tg('nav')} عنصر دلالي يُستخدم للتنقل.",
 "HTML الدلالية تضمن ترتيبًا أعلى في نتائج محركات البحث.",
 "يساعد HTML الدلالي قارئ الشاشة على فهم بنية الصفحة والتنقل فيها.",
 "غرض التصميم المتجاوب هو تحسين سرعة عرض المواقع.",
 "نهج الأولوية للجوال يراعي الشاشات الصغيرة منذ بداية التصميم.",
 "إطار العمل تقنية لتشفير البيانات وإرسالها بأمان.",
 "React مكتبة JavaScript لبناء واجهات المستخدم.",
 "Next.js إطار مبني على React.",
 "«تحديث جزء فقط من الشاشة» من قدرات CSS.",
]

# ---- علّل
WHY = [
 "لا يصحّ القول إن CSS يضيف سلوكًا إلى صفحة الويب.",
 f"يفهم قارئ الشاشة الصفحة بشكل أفضل عندما تستخدم {tg('header')} و{tg('nav')} و{tg('main')} بدلًا من صناديق عادية.",
 "لا يمكن القول إن HTML الدلالية تضمن ترتيبًا أعلى في نتائج البحث.",
 "لا تكفي HTML الدلالية وحدها لتحقيق إمكانية الوصول.",
 "تحتاج المواقع اليوم إلى تصميم متجاوب.",
 "يراعي المطورون الشاشات الصغيرة منذ بداية التصميم.",
 "يجعل استخدام إطار عمل التطوير أكثر كفاءة.",
 "يُفضَّل فصل HTML وCSS وJavaScript كلٌّ حسب دوره بدل كتابة كل شيء في ملف واحد.",
]
TQ_WHY = {6, 7}

ESS = [
 ("اذكر <b>التقنيات الثلاث</b> ودور كل واحدة <b>وتشبيه الكتاب</b> لها، مع مثال مهمة لكل تقنية.", 3, True),
 ("اشرح <b>فائدتَي HTML الدلالية</b> كما يذكرهما الكتاب، مع <b>التحفّظ</b> المرتبط بكل واحدة.", 3, True),
 ("مدرسة عايزة صفحة لنتائج الامتحانات: فيها جدول درجات، بألوان المدرسة، والنتيجة تظهر من غير إعادة تحميل الصفحة. وزّع المهام على التقنيات الثلاث، واقترح <b>تحسينين</b>: واحدًا للتصميم المتجاوب، وواحدًا لـHTML الدلالية.", 4, False),
]

N_ESS = 2 + len(ESS) + len(TAQ_ESS) + 4   # كارتين + المقالي + التقييمات + (توقّف وفكّر ×2، فكّر وتحدَّ، اختبر فهمك)
N_TQ = len(TQ_MCQ) + len(TQ_WHY) + sum(1 for e in ESS if e[2]) + len(TAQ_ESS) + 4   # + كارت الامتحان (أسئلة الكتاب 05) + تصنيف 02 و04 + جدول المقارنة
stats = [("13", "أسئلة الكتاب"), (str(len(MCQ)), "اختر"), (str(len(FILL)), "أكمل"), (str(len(TF)), "صح وخطأ"), ("9", "تصنيف وقارن"), (str(len(WHY)), "علّل"), (str(N_ESS), "مقالي وأنشطة")]
A('<div class="qstats">' + "".join(f'<div><b class="num">{n}</b><span>{t}</span></div>' for n, t in stats) + f'<div><b class="num">{N_TQ}</b>{TQ}</div></div>')

A(cat("أسئلة الكتاب", stats[0][0]))
for c in BOOK: A(c)

A(cat("اختر الإجابة الصحيحة", str(len(MCQ))))
def mq(j): return f'<div class="mq"><div class="qq"><span class="k">{j+1}</span>{TQ if j+1 in TQ_MCQ else ""}<p>{MCQ[j][0]}</p></div>{opts(MCQ[j][1], 2)}</div>'
for i in range(0, len(MCQ), 2):
    A('<div class="mrow">' + "".join(mq(j) for j in range(i, min(i + 2, len(MCQ)))) + '</div>')

A(cat("أكمل", str(len(FILL))))
for i in range(0, len(FILL), 2):
    A('<div class="frow">' + "".join(f'<div><span class="k">{j+1}</span><p>{FILL[j]}</p></div>' for j in (i, i + 1)) + '</div>')

A(cat("صح وخطأ", str(len(TF))))
for i in range(0, len(TF), 3):
    A('<ul class="tfb">' + "".join(f'<li><span class="k">{j+1}</span><span class="t">{TF[j]}</span><span class="pr">(&nbsp;&nbsp;&nbsp;&nbsp;)</span></li>' for j in range(i, i + 3)) + '</ul>')

A(cat("تصنيف وقارن", "9"))
A(card("01", "بنية ولا مظهر ولا سلوك؟",
       instr("اكتب «ب» للبنية، و«م» للمظهر، و«س» للسلوك.")
       + classify(["عنوان رئيسي وفقرة نصية", "خط الصفحة وحجمه", "عدّاد يزيد عند الضغط على زر", "ترتيب العناصر في أعمدة", "رابط لصفحة أخرى", "تصفية نتائج البحث أثناء الكتابة"])))
A(card("02", "العنصر الدلالي المناسب",
       instr(f"اكتب العنصر المناسب: {tg('header')} · {tg('nav')} · {tg('main')} · {tg('footer')}.")
       + classify(["أعلى الصفحة", "روابط التنقل بين الأقسام", "المحتوى الرئيس للصفحة", "أسفل الصفحة"], w=True), tag=TQ))
A(card("03", "طابق كل مصطلح بتعريفه",
       '<div class="match"><div class="mb"><h5>التعريف</h5><ol>'
       + "".join(f'<li><span>{t}</span>{AB}</li>' for t in [
           "يتكيف التخطيط مع حجم الشاشة", "وظائف جاهزة لتطوير أكثر كفاءة", "عناصر توضح وظيفة أجزاء الصفحة",
           "تصميم يمكّن أصحاب القدرات المختلفة من الاستخدام", "ممارسات تيسّر الفهرسة والظهور في نتائج البحث"])
       + '</ol></div><div class="mb"><h5>المصطلح</h5>' + opts(["إطار العمل", "إمكانية الوصول", "SEO", "التصميم المتجاوب", "HTML الدلالية"], 1) + '</div></div>'))
A(card("04", "مكتبة ولا إطار؟",
       instr("اكتب <b>مكتبة</b> أو <b>إطار</b> أمام كل اسم حسب وصف الكتاب.")
       + classify(["React", "Next.js"], w=True)
       + '<p class="qi" style="margin-top:6pt">اكتب خاصية واحدة لكل منهما كما يذكرها الكتاب:</p>' + lines(2), tag=TQ))
A(card("05", "الفائدة دي لمين؟",
       instr("اكتب <b>«وصول»</b> لو الفائدة تخصّ <b>إمكانية الوصول</b>، أو <b>«بحث»</b> لو تخصّ <b>محركات البحث</b>.")
       + classify(["قارئ الشاشة يفهم بنية الصفحة ويتنقل فيها", "فهم بنية المحتوى بصورة أفضل", "إيصال المعلومات أسهل لذوي الإعاقة البصرية", "تيسير الفهرسة والظهور في النتائج"], w=True)))
A(card("06", "قارن بين HTML وCSS", cmp_table(["وجه المقارنة", "HTML", "CSS"], ["الدور", "تشبيه الكتاب"], tall=True)))
A(card("07", "قارن بين CSS وJavaScript", cmp_table(["وجه المقارنة", "CSS", "JavaScript"], ["الدور", "مثال مهمة"], tall=True)))
A(card("08", "قارن بين إمكانية الوصول وتحسين محركات البحث", cmp_table(["وجه المقارنة", "إمكانية الوصول", "تحسين محركات البحث"], ["المستفيد", "تحفّظ الكتاب"], tall=True)))
A(card("09", "قارن بين التصميم المتجاوب وإطار العمل", cmp_table(["وجه المقارنة", "التصميم المتجاوب", "إطار العمل"], ["ما هو", "المشكلة التي يحلها"], tall=True), tag=TQ))

A(cat("علّل", str(len(WHY))))
for k, t in enumerate(WHY):
    A(f'<div class="why split"><div class="qq"><span class="k">{k+1}</span>{TQ if k+1 in TQ_WHY else ""}<p>{t}</p></div>{lines(2)}</div>')

# ---- مقالي وأنشطة (من غير عنوان)
A(card("01", "طبّق ما تعلمته — موقع إخباري",
       '<p class="qs">يريد موقع إخباري أن يعمل جيدًا على الهاتف وأن يفهم محرك البحث بنية صفحاته. اذكر <b>اختيارًا في التصميم المتجاوب</b> و<b>اختيارًا في HTML الدلالي</b>، واشرح <b>الفائدة المتوقعة</b> من كل منهما.</p>'
       + hint("<b>اختياران محددان</b> (مش كلام عام) · <b>فائدة لكل واحد</b> · وانتبه: فائدة الدلالية <b>«قد تساعد»</b> محركات البحث ولا <b>تضمن</b> ترتيبًا أعلى.") + lines(5)))
A(card("02", "فكّر كمهندس — ابحث ثم قرر",
       '<p class="qs">يريد نادٍ طلابي صفحة ويب بسيطة تعرض فعالياته، ومنسّقة بألوان النادي، وتحتوي على زر يعرض عدد الأشخاص المسجلين.</p>'
       + '<p class="qs"><b>(1) لاحظ أولًا.</b> افتح صفحة ويب واحدة تستخدمها كثيرًا ولاحظ <b>أمرين فيها يتغيران</b> عند النقر أو الكتابة. ثم وزّع الميزات الثلاث على التقنيات.</p>'
       + cmp_table(["الميزة", "التقنية", "ليه؟"], ["قائمة الفعاليات", "ألوان النادي وتخطيطه", "عدّاد التسجيل الحي"])))
A(card("", "",
       '<p class="qs"><b>(2) اجعلها تصل إلى الجميع.</b> اذكر <b>تغييرًا واحدًا</b> يجعل الصفحة أسهل قراءة على الهاتف (التصميم المتجاوب)، و<b>اختيارًا واحدًا</b> في HTML الدلالية يساعد قارئ الشاشة.</p>' + lines(2)
       + '<p class="qs"><b>(3) قرّر.</b> أوصِ بما إذا كان على النادي فصل HTML وCSS وJavaScript، وقدّم سببين. في أزواج، قارنوا توزيعكم للأدوار واتفقوا معًا على ما يحتاجه عدّاد التسجيل.</p>'
       + '<p class="chx"><span>☐ اكتب كل شيء في ملف واحد</span><span>☐ استخدم HTML وCSS وJavaScript كلًا حسب دوره الصحيح</span></p>' + lines(2)
       + hint("تلميح الكتاب: <b>HTML يحمل المحتوى؛ وCSS ينسّقه؛ وJavaScript يجعله يتفاعل ويُحدِّث.</b> ولاحظ إن السؤال طالب <b>بدليل</b> على إجابتك.")))
for k, (t, n, b) in enumerate(ESS):
    A(f'<div class="why ess split"><div class="qq"><span class="k">{k+3}</span>{TQ if b else ""}<p>{t}</p></div>{lines(n)}</div>')
# أسئلة التقييمات الناقصة — بعد المقالي على طول، والترقيم مكمّل
for k, (t, n) in enumerate(TAQ_ESS, start=3 + len(ESS)):
    A(f'<div class="why split"><div class="qq"><span class="k">{k}</span>{TQ}<p>{t}</p></div>{lines(n)}</div>')
T0 = 3 + len(ESS) + len(TAQ_ESS)
A(f'<div class="why split"><div class="qq"><span class="k">{T0}</span><p><b>توقّف وفكّر:</b> في صفحة تستخدمها كثيرًا، ما هي الأجزاء التي تمثل البنية (HTML)، وما هي التي تمثل الشكل (CSS)، وما الذي يتفاعل معك (JavaScript)؟</p></div>{lines(2)}</div>')
A(f'<div class="why split"><div class="qq"><span class="k">{T0 + 1}</span><p><b>توقّف وفكّر:</b> لماذا يفهم قارئ الشاشة الصفحة بشكل أفضل عندما تستخدم {tg("header")} و{tg("nav")} و{tg("main")} بدلًا من صناديق عادية؟</p></div>{lines(2)}</div>')
A(f'<div class="why split"><div class="qq"><span class="k">{T0 + 2}</span><p><b>فكّر وتحدَّ – تأمّل:</b> من بين البنية والشكل والسلوك، أيها تلاحظه أكثر عندما تكون صفحة الويب سيئة الصنع، ولماذا؟ · <b>وتحدَّ:</b> اذكر موقعًا واحدًا تستخدمه وصف شيئًا واحدًا تقوم به كل من HTML وCSS وJavaScript فيه.</p></div>{lines(3)}</div>')
A(f'<div class="why split"><div class="qq"><span class="k">{T0 + 3}</span><p><b>اختبر فهمك:</b> أجب عن أسئلة هذا البنك <b>دون الرجوع</b> إلى الشرح، ثم راجع إجاباتك.</p></div>{lines(1)}</div>')

EXTRA_CSS = """
/* ---------- إضافات الدرس 3-3 ---------- */
.banner{text-wrap:pretty}
.intro .body p+p{margin-top:4pt}
.map .cell li{text-wrap:pretty}
.map.m2 .cell h4{display:flex;align-items:flex-start;gap:5pt;line-height:1.4;margin-bottom:2pt}
.map.m2 .cell h4 .mn{flex:none;display:inline-flex;align-items:center;justify-content:center;width:13pt;height:13pt;border-radius:50%;background:var(--navy2);color:#fff;font-size:7.8pt;font-weight:800;margin-top:1.5pt}
.map.m2 .cell .term{display:inline-block;font-weight:800;font-size:8.6pt;color:var(--gold2);background:#fbf6e8;border:.75pt solid #eee0b8;border-radius:6pt;padding:0 7pt;line-height:13pt;margin:0 0 3pt 0}
.map.m2 .cell .sl{font-weight:700;font-size:8.6pt;color:var(--navy2);line-height:13pt;margin:2pt 0 1pt 0}
.map.m2 .cell .sl .ex{font-weight:600;color:var(--text)}
.map.m2 .cell .imp{font-size:8.9pt;line-height:14pt;color:var(--text);margin-top:3pt;padding-top:3pt;border-top:.75pt dashed #e3e9f1}
.map.m2 .cell .imp b{color:var(--gold2);font-weight:800}
.map.m2{grid-template-columns:1fr 104pt 1fr;column-gap:15pt}
.map.m2 .hub{font-size:10.4pt;padding:6pt 6pt}
.map.m2 .cell .tags{white-space:nowrap}
.map.m2 .cell .tags bdi{display:inline-block;margin-left:3pt;font-size:8.2pt}
bdi.tg{font-weight:700}
.nw{white-space:nowrap}
.anl{background:#fff;border:.75pt solid #eee0b8;border-radius:9pt;padding:7pt 11pt 9pt 11pt;margin:0 0 8pt 0}
.anl .hd{display:flex;align-items:center;gap:8pt;font-size:9.8pt;color:var(--text2);line-height:1.4;margin-bottom:6pt}
.anl .lb{display:inline-flex;align-items:center;gap:4pt;font-weight:800;font-size:10.4pt;color:var(--gold2)}
.anl .lb svg{width:15pt;height:15pt}
.anl .row{display:grid;grid-template-columns:.85fr 1.05fr 1.2fr;gap:7pt}
.anl .it{display:flex;flex-direction:column;align-items:center;gap:2pt;background:#fff;border:.75pt solid #eee0b8;border-radius:7pt;padding:5pt 7pt;line-height:1.3;text-align:center}
.anl .it .t{display:flex;align-items:center;gap:5pt}
.anl .it b{font-weight:800;font-size:9.6pt;color:var(--navy)}
.anl .it i{font-style:normal;font-weight:700;font-size:9.6pt;color:var(--muted)}
.anl .it span{font-weight:700;font-size:9.4pt;color:var(--gold2);white-space:nowrap}
.anl .it small{font-size:8.2pt;color:var(--muted);line-height:1.35}
.anl .house{display:block;width:100%;height:auto;margin:0 0 2pt 0}
.anl .ft{margin-top:4pt;font-size:9.6pt;line-height:1.4;color:var(--text2);text-align:center}
.anl .sum{margin-top:6pt;background:var(--navy);color:#fff;border-radius:7pt;padding:4pt 10pt;text-align:center;font-weight:700;font-size:10.4pt;line-height:1.5}
.anl .sum b{color:#ffd08a;font-weight:800}
.chx{position:relative;background:#fff;border:.75pt solid var(--line);border-radius:9pt;padding:8pt 11pt 8pt 11pt;margin:0 0 8pt 0}
.chx .hd{display:flex;align-items:center;gap:5pt;font-size:9.8pt;color:var(--text2);line-height:1.4;margin-bottom:6pt}
.chx .lb{font-weight:800;font-size:10.4pt;color:var(--gold2)}
.chx .tt{font-weight:800;font-size:10.4pt;color:var(--navy)}
.chx .row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10pt}
.chx .it{display:flex;flex-direction:column;align-items:center;gap:5pt}
.chx .chat{display:block;width:112pt;height:auto}
.chx p{font-size:9pt;line-height:13pt;color:var(--text);text-align:center;text-wrap:pretty}
.chx .k{display:inline-block;font-weight:800;font-size:8.6pt;color:#fff;background:var(--navy);border-radius:6pt;padding:0 6pt;line-height:12.5pt;margin-left:3pt}
.bens{position:relative;margin:9pt 0 9pt 0}
.bens .bh{display:flex;justify-content:center}
.bens .bh span{background:var(--navy);color:#fff;font-weight:800;font-size:10.5pt;line-height:17pt;padding:0 16pt;border-radius:9pt}
.bens .br{position:relative;height:17pt}
.bens .br i{position:absolute;display:block}
.bens .br .s{top:0;left:calc(50% - .75pt);width:1.5pt;height:5.5pt;background:#e29433}
.bens .br .l,.bens .br .r{top:4.75pt;width:calc(25% + 2.25pt);height:8pt;border-top:1.5pt solid #e29433}
.bens .br .l{left:calc(25% - 2.25pt);border-left:1.5pt solid #e29433;border-top-left-radius:7pt}
.bens .br .r{right:calc(25% - 2.25pt);border-right:1.5pt solid #e29433;border-top-right-radius:7pt}
.bens .br .a{top:12pt;width:0;height:0;border-left:4pt solid transparent;border-right:4pt solid transparent;border-top:5pt solid #e29433}
.bens .br .al{left:calc(25% - 5.5pt)}
.bens .br .ar{right:calc(25% - 5.5pt)}
.bens .bg{display:grid;grid-template-columns:1fr 1fr;gap:9pt}
.bens .bc{background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:8pt;padding:7pt 10pt 8pt 10pt;display:flex;flex-direction:column;gap:3pt}
.bens .bt{display:flex;align-items:center;gap:5pt;font-size:10.6pt;line-height:15pt}
.bens .bt b{color:var(--navy);font-weight:800}
.bens .bn{flex:none;width:15pt;height:15pt;border-radius:50%;background:var(--navy);color:#fff;font-size:8.6pt;font-weight:800;display:inline-flex;align-items:center;justify-content:center;line-height:1}
.bens .bt svg{width:14pt;height:14pt;flex:none}
.bens .be{font-size:8.4pt;font-weight:700;color:var(--gold2);line-height:12pt}
.bens p{font-size:10pt;line-height:15.5pt;color:var(--text);margin:0;flex:1}
.bens p b{color:var(--navy2)}
.bens .bw{display:flex;align-items:center;gap:5pt;background:#fff;border:.75pt solid #dde5ef;border-right:3pt solid #e29433;border-radius:5pt;padding:2.5pt 7pt;font-size:9.4pt;line-height:13.5pt;font-weight:700;color:var(--navy)}
.bens .bw::before{content:'!';flex:none;width:11pt;height:11pt;border-radius:50%;background:#e29433;color:#fff;font-size:8pt;font-weight:800;display:inline-flex;align-items:center;justify-content:center;line-height:1}
.quote .enx{font-size:8.6pt;font-weight:700;color:var(--gold2)}
.cmpw{position:relative}
.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:9pt}
.tri .tc{display:flex;flex-direction:column;align-items:center;text-align:center;border:.75pt solid #dde5ef;border-radius:10pt;padding:9pt 9pt 8pt 9pt;background:#f5f7fb}
.tri .tc.c{background:#fbf6e8;border-color:#eee0b8}
.tri .ic svg{width:30pt;height:30pt;display:block}
.tri h4{margin:4pt 0 0 0;font-weight:800;font-size:12pt;color:var(--navy);line-height:1.3}
.tri .rl{font-weight:800;font-size:10.4pt;color:var(--gold2);line-height:1.4;margin-bottom:3pt}
.tri p{flex:1;font-size:9.4pt;line-height:14.4pt;color:var(--text)}
.tri p b{color:var(--navy2)}
.tri .an{margin-top:6pt;font-weight:800;font-size:8.8pt;color:var(--gold2);background:#fff;border:.75pt solid #eee0b8;border-radius:7pt;padding:0 8pt;line-height:14pt}
.resp{display:flex;align-items:flex-end;justify-content:center;gap:10pt;padding:2pt 0 0 0}
.resp .dev{display:flex;flex-direction:column;align-items:center;gap:6pt}
.resp .dev b{font-weight:800;font-size:9.6pt;color:var(--navy)}
.resp .scr{border:1.6pt solid #b9c7da;border-radius:7pt;background:#fff;display:flex;flex-direction:column;gap:5pt;padding:6pt}
.resp .pc .scr{width:150pt;height:84pt}
.resp .tb .scr{width:78pt;height:98pt;border-radius:8pt}
.resp .ph .scr{width:48pt;height:98pt;border-radius:9pt}
.resp .bar{display:block;height:7pt;border-radius:3pt;background:#e6edf6}
.resp .cols{flex:1;display:flex;gap:5pt}
.resp .cols i,.resp .blk{flex:1;display:flex;align-items:center;justify-content:center;border-radius:3pt;background:#fff;border:1pt solid #e29433;font-style:normal;font-weight:800;font-size:9pt;color:#a9670f;line-height:1}
.resp .go{display:flex;flex-direction:column;align-items:center;gap:2pt;align-self:center;margin-bottom:16pt}
.resp .go svg{width:30pt;height:10pt}
.resp .go small{font-size:8.4pt;color:var(--muted)}
.mf{display:grid;grid-template-columns:1fr 16pt 1fr 16pt 1fr;align-items:stretch;margin:9pt 0 9pt 0}
.mf .st{background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:8pt;padding:7pt 9pt 8pt 9pt;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4pt;text-align:center}
.mf .st p{font-size:9.8pt;line-height:15pt;color:var(--text);margin:0}
.mf .st p b{color:var(--navy2)}
.mf .ic{width:22pt;height:22pt;border-radius:50%;background:#fff;border:.75pt solid #dde5ef;display:flex;align-items:center;justify-content:center}
.mf .ic svg{width:13pt;height:13pt}
.mf .st.nm{background:#22375c;border-color:#22375c}
.mf .nm p{color:#fff}
.mf .nm p b{color:#ffd08a}
.mf .nm .ic{background:#e29433;border-color:#e29433}
.mf .ar{display:flex;align-items:center;justify-content:center}
.mf .ar svg{width:13pt;height:9pt}
.fw{margin:9pt 0 9pt 0}
.fw .fwh{display:flex;justify-content:center}
.fw .fwh span{background:#22375c;color:#fff;font-weight:800;font-size:10.5pt;line-height:17pt;padding:0 16pt;border-radius:9pt}
.fw .lk{position:relative;height:17pt}
.fw .lk i{position:absolute;display:block}
.fw .lk .s{top:0;left:calc(50% - .75pt);width:1.5pt;height:12.5pt;background:#e29433}
.fw .lk .h{top:4.75pt;left:calc(16.667% - 3.75pt);right:calc(16.667% - 3.75pt);height:8pt;border-top:1.5pt solid #e29433;border-left:1.5pt solid #e29433;border-right:1.5pt solid #e29433;border-radius:7pt 7pt 0 0}
.fw .lk .a{top:12pt;width:0;height:0;border-left:4pt solid transparent;border-right:4pt solid transparent;border-top:5pt solid #e29433}
.fw .lk .al{left:calc(16.667% - 7pt)}
.fw .lk .ar{right:calc(16.667% - 7pt)}
.fw .lk .am{left:calc(50% - 4pt)}
.fw .fg{display:grid;grid-template-columns:1fr 1fr 1fr;gap:9pt}
.fw .fc{background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:8pt;padding:7pt 9pt 8pt 9pt}
.fw .fh{display:flex;align-items:center;justify-content:space-between;gap:6pt;margin-bottom:4pt;padding-bottom:4pt;border-bottom:.75pt solid #dde5ef}
.fw .fn{font-weight:800;font-size:12pt;line-height:16pt;color:var(--navy);direction:ltr}
.fw .ft{font-size:8pt;font-weight:700;color:#a9670f;background:#fff;border:.75pt solid #e29433;border-radius:6pt;padding:0 6pt;line-height:12.5pt;white-space:nowrap}
.fw p{font-size:9.8pt;line-height:15pt;color:var(--text);margin:0}
.fw p b{color:var(--navy2)}
.fw .cap{margin-top:6pt;padding-top:4pt;border-top:.75pt dashed #dde5ef;text-align:center;font-size:8.8pt;line-height:13pt;color:var(--muted)}
/* 3-3: «اتأكد» أضيق سنة عشان يلحق آخر صفحة شرح بعد إضافة «مصطلحات أساسية» و«تذكّر» */
.check{padding:7pt 13pt 5pt 13pt}
.check .g2{margin-top:5pt}
.check li{margin-bottom:4pt}
"""

body = (f'<body data-lesson="الدرس 3-3 — أساسيات تقنية الواجهة الأمامية" data-start="{START}" data-total="{TOTAL}">\n<main class="flow">\n'
        + "\n".join(E) + "\n\n<!-- ===================== بنك الأسئلة ===================== -->\n" + "\n".join(B)
        + "\n</main>\n</body>\n</html>\n")
out = head.replace("</style>", EXTRA_CSS + "</style>", 1) + body
out = out.replace("(el.firstElementChild && el.firstElementChild.tagName === 'H4')", "(el.firstElementChild && /^H[34]$/.test(el.firstElementChild.tagName))")
open(BASE + "lesson_3_3.html", "w", encoding="utf-8").write(out)
print("written", len(out), "| mcq", len(MCQ), "| ess", N_ESS, "| tq", N_TQ)
