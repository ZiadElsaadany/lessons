# -*- coding: utf-8 -*-
"""يبني html/lesson_2_2.html من قالب lesson_3_1.html (نفس الستايل والسكريبتات) + محتوى الدرس 2-2."""
import re, sys
import os
TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import newsec as N

BASE = os.path.join(os.path.dirname(TOOLS), "")   # فولدر html (أبو فولدر tools)
tpl = open(BASE + "lesson_3_1.html", encoding="utf-8").read()
head = tpl[:tpl.index('<body data-lesson=')]
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fxflag import FLAG_CSS, group_html, strip_style
head = strip_style(head)
head = head.replace("<title>الدرس 3-1 — البنية العامة لتطبيقات الويب</title>", "<title>الدرس 2-2 — تصميم أمان الشبكات</title>")
head = head.replace("الدرس 3-1 (الشرح)", "الدرس 2-2 (الشرح + بنك الأسئلة)")

START, TOTAL = 22, 99      # الترقيم النهائي للوحدة التانية هيتعمل في الآخر
TITLE = "تصميم أمان الشبكات"

FX = '<span class="fx">للفهم</span>'
FXA = '<span class="fx abs">للفهم</span>'
TQ = '<span class="tq">تقييمات</span>'
L = ["أ", "ب", "ج", "د", "هـ", "و"]
AB = '<span class="ab"></span>'
def num(t): return f'<span class="num">{t}</span>'
def en(t): return f'<bdi>{t}</bdi>'                             # كلمة إنجليزي جنب كلمة إنجليزي
def nw(t): return f'<bdi class="nw">{t}</bdi>'                  # إنجليزي لازم يفضل في سطر واحد
def lines(n): return '<div class="wl"><i></i></div>' * n
def blank(w=70): return f'<span class="bl" style="width:{w}pt"></span>'
def opts(items, cols=1):
    return f'<ul class="op c{cols}">' + "".join(f'<li><b>{L[k]}‌</b><span>{t}</span></li>' if 'bdi' in t else f'<li><b>{L[k]}‌</b>{t}</li>' for k, t in enumerate(items)) + '</ul>'
def classify(items, letters=None, w=False):
    ks = letters or [str(k + 1) for k in range(len(items))]
    ab = AB.replace('class="ab"', 'class="ab w"') if w else AB
    return '<ul class="cl">' + "".join(f'<li><span class="k">{ks[k]}</span><span class="t">{t}</span>{ab}</li>' for k, t in enumerate(items)) + '</ul>'
def card(n, title, body, tag=""):
    t = f'<h4><span class="n">{n}</span><span class="tt">·&nbsp;{title}</span>{tag}</h4>' if n else ""
    return f'<div class="qcard split {"cont" if not n else ""}">{t}{body}</div>'
def instr(t): return f'<p class="qi">{t}</p>'
def hint(t, label="عناصر الإجابة"): return f'<div class="hint"><b>{label}</b> {t}</div>'
def cat(title, count): return f'<h2 class="cat kwn">{title}<span class="cnt">{count}</span></h2>'
def cmp_table(heads, rows, badge=False, tall=False):
    th = "".join(f"<th>{x}</th>" for x in heads)
    tr = "".join(f'<tr><td class="k">{r}</td>' + "<td></td>" * (len(heads) - 1) + "</tr>" for r in rows)
    t = f'<table class="cmp{" tall" if tall else ""}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
    return f'<div class="cmpw">{TQ}{t}</div>' if badge else t
def qq(k, t, tag=""): return f'<div class="qq"><span class="k">{k}</span>{tag}<p>{t}</p></div>'
MARK6 = '<span class="mk">[<span class="num">6</span> درجات]</span>'

def lk(cls, d, c, cx, cy):
    return f'<svg class="lk {cls}" viewBox="0 0 20 16"><path d="{d}" fill="none" stroke="{c}" stroke-width="1.55" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="2" fill="{c}"/></svg>'

# ---------------- أيقونات الدرس ----------------
def _ic(c, body, vb="0 0 24 24", sw="1.8"):
    return f'<svg viewBox="{vb}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
def ic_lock(c): return _ic(c, f'<rect x="4.5" y="10.5" width="15" height="10.5" rx="2.2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><circle cx="12" cy="15.7" r="1.3" fill="{c}" stroke="none"/>')
def ic_sign(c): return _ic(c, '<path d="M3 18.5c2.2-7 4.2-8.6 5.4-4.2 1 3.8 2.6 4.6 4.6-.6"/><path d="M3 21.3h18"/><path d="M17.6 3.6l2.8 2.8-3.4 3.4-2.8-2.8z"/>')
def ic_cert(c): return _ic(c, '<rect x="2.8" y="3.5" width="18.4" height="12.5" rx="2"/><path d="M6.6 7.8h7.4M6.6 11h4.4"/><circle cx="16.2" cy="15.6" r="2.9" fill="#fff"/><path d="M14.6 18.1l-.9 3.5 2.5-1.3 2.5 1.3-.9-3.5"/>')
def ic_2dev(c): return _ic(c, f'<rect x="2.5" y="7" width="8.5" height="11.5" rx="1.7"/><path d="M5 10h3.5"/><rect x="13" y="3" width="8.5" height="18" rx="1.9"/><path d="M15.6 6h3.3"/><circle cx="17.25" cy="17.6" r=".85" fill="{c}" stroke="none"/>')
def ic_q(c): return _ic(c, f'<circle cx="12" cy="12" r="9.4"/><path d="M9.4 9.4a2.7 2.7 0 1 1 3.8 2.5c-.8.4-1.2 1-1.2 1.9v.5"/><circle cx="12" cy="17.2" r="1" fill="{c}" stroke="none"/>')
def ic_phone(c): return _ic(c, '<rect x="6.3" y="2.4" width="11.4" height="19.2" rx="2.4"/><rect x="9" y="6.2" width="6" height="5" rx="1"/><path d="M10 17.6h4"/>')
def ic_finger(c): return _ic(c, '<path d="M5.2 15.5c.4-1.3.6-2.7.6-4.2a6.2 6.2 0 0 1 12.4 0c0 2.6-.3 5-1 7.2"/><path d="M8.7 18.8c.8-2.3 1.1-4.8 1.1-7.3a2.2 2.2 0 0 1 4.4 0c0 3.3-.4 6.3-1.3 9"/><path d="M12 11.6c0 3.4-.4 6.6-1.4 9.4"/><path d="M4 7.8A9 9 0 0 1 20 7.8"/>')
def ic_key(c): return _ic(c, '<circle cx="7.5" cy="12" r="4.3"/><path d="M11.8 12H21.5M18.5 12v3.2M21 12v2.4"/>')

def ic_wall(c): return _ic(c, '<rect x="2.5" y="4" width="19" height="16" rx="1.5"/><path d="M2.5 9.3h19M2.5 14.7h19M8 4v5.3M16 4v5.3M12 9.3v5.4M5 14.7V20M19 14.7V20M12 14.7V20"/>')
def ic_tunnel(c): return _ic(c, '<path d="M2.5 16V11a9.5 7 0 0 1 19 0v5"/><path d="M6.5 16v-4.2a5.5 4 0 0 1 11 0V16"/><path d="M2 16h20"/>')
def ic_server(c): return _ic(c, f'<rect x="3.5" y="3.5" width="17" height="7" rx="1.6"/><rect x="3.5" y="13.5" width="17" height="7" rx="1.6"/><circle cx="7.3" cy="7" r=".9" fill="{c}" stroke="none"/><circle cx="7.3" cy="17" r=".9" fill="{c}" stroke="none"/><path d="M11 7h6M11 17h6"/>')
def ic_globe(c): return _ic(c, '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9M12 3c-2.6 2.6-3.8 5.6-3.8 9s1.2 6.4 3.8 9"/>')
def ic_user(c): return _ic(c, '<circle cx="12" cy="8" r="3.6"/><path d="M5 20c.8-4 3.6-6.3 7-6.3s6.2 2.3 7 6.3"/>')
def ic_laptop(c): return _ic(c, '<rect x="4.5" y="5" width="15" height="10" rx="1.4"/><path d="M2.5 18.5h19"/>')
def ic_db(c): return _ic(c, '<ellipse cx="12" cy="6" rx="7" ry="2.8"/><path d="M5 6v12c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8V6M5 12c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8"/>')
def ic_shield(c): return _ic(c, '<path d="M12 2.8 19.5 6v5.5c0 4.6-3.2 8.3-7.5 9.7-4.3-1.4-7.5-5.1-7.5-9.7V6z"/><path d="m8.8 12 2.2 2.2 4.3-4.4"/>')
def ic_mail(c): return _ic(c, '<rect x="3" y="5.5" width="18" height="13" rx="1.8"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>')
def ic_home(c): return _ic(c, '<path d="M3.5 11 12 4l8.5 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>')
def ic_building(c): return _ic(c, '<rect x="4.5" y="3.5" width="15" height="17" rx="1.2"/><path d="M8 7.5h2M14 7.5h2M8 11h2M14 11h2M8 14.5h2M14 14.5h2M10.5 20.5v-3h3v3"/>')
def ic_wifi(c): return _ic(c, f'<path d="M2.5 9a14 14 0 0 1 19 0M5.5 12.3a9.5 9.5 0 0 1 13 0M8.6 15.5a5 5 0 0 1 6.8 0"/><circle cx="12" cy="18.8" r="1" fill="{c}" stroke="none"/>')
def ic_bug(c): return _ic(c, '<rect x="7.5" y="8" width="9" height="12" rx="4.5"/><path d="M9.5 8a2.5 2.5 0 0 1 5 0M4 11h3.5M16.5 11H20M4 16h3.5M16.5 16H20M7 5.5 9 7.5M17 5.5l-2 2"/>')
def ic_eye(c): return _ic(c, '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>')
def ic_idc(c): return _ic(c, '<rect x="2.5" y="5" width="19" height="14" rx="2"/><circle cx="8.5" cy="11" r="2.3"/><path d="M5 16c.6-1.6 1.9-2.4 3.5-2.4S11.4 14.4 12 16M14.5 10h4M14.5 13.5h3"/>')
def ic_perm(c): return _ic(c, '<rect x="4.5" y="10.5" width="15" height="10.5" rx="2.2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><path d="m9.3 15.6 1.9 1.9 3.6-3.7"/>')
def ic_clock(c): return _ic(c, '<circle cx="12" cy="12" r="9"/><path d="M12 7.2V12l3.2 2"/>')
def ic_x(c): return _ic(c, '<path d="M6 6l12 12M18 6 6 18"/>', sw="2.4")
def ic_ok(c): return _ic(c, '<path d="M5 12.5 10 17 19 7"/>', sw="2.4")
def ic_cloud(c): return _ic(c, '<path d="M7 18.5h10.5a4 4 0 0 0 .4-8 6 6 0 0 0-11.6 1.3A3.4 3.4 0 0 0 7 18.5z"/>')
def ic_bank(c): return _ic(c, '<path d="M3 9.5 12 4l9 5.5z"/><path d="M5.5 10v7.5M9.8 10v7.5M14.2 10v7.5M18.5 10v7.5M3 20.5h18"/>')
ARR = '<svg viewBox="0 0 44 12" fill="none" stroke="#e29433" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M42 6H5"/><path d="M10 1.5 4 6l6 4.5"/></svg>'
def recall(items):
    return ('<div class="rcl keep"><span class="rl">ثبّت الصفحة في 10 ثواني</span><div class="rc">'
            + '<i>·</i>'.join(f'<span>{t}</span>' for t in items) + '</div></div>')
def exs(t): return f'<div class="exs">{FXA}<span class="eh">مثال للتبسيط:</span>{t}</div>'

# ============================ الشرح ============================
E = []
A = E.append
A(f'''<div class="band">
  <div class="badge"><span class="l">الدرس</span><span class="n">2-2</span></div>
  <h1>{TITLE}</h1>
  <div class="who">
    <div class="t"><span class="u">الوحدة الثانية</span><span class="k">الشرح والمراجعة</span></div>
    <img src="assets/avatar.png" alt="">
  </div>
</div>''')
A(f'''<div class="two">
  <div class="intro">
    <h3>لو الحرامي عدّى الباب .. يبقى خلاص؟</h3>
    <div class="body">
      <img class="robot" src="assets/robot.svg" alt="">
      <p>في الدرس اللي فات <b>(2-1)</b> اتكلمنا عن حماية <b>الاتصال والحسابات</b> بالتشفير والمصادقة. الدرس ده بيوسّع الحماية لـ<b>تصميم الشبكة نفسها</b> — يعني إزاي مؤسسة ترتّب شبكتها.</p>
      <p>والفكرة الأساسية: <b>ما نعتمدش على وسيلة واحدة</b>. لو طبقة فشلت، تفضل فيه طبقات تانية تساعد على <b>تقليل الخطر والحد من أثر الاختراق</b> — وده اسمه <b>الدفاع في العمق</b>.</p>
      <p>وهنتعرّف كمان على <b>نهج انعدام الثقة</b>: الجهاز أو المستخدم <b>مايتوثقش فيه تلقائيًا</b> لمجرد إنه جوّه الشبكة — لازم يتفحص <b>الهوية والصلاحيات والسياق</b> عند الوصول.</p>
    </div>
    <div class="foot"><span class="pill-dark">نبدأ من جدار الحماية</span></div>
  </div>
  <div class="goals">
    <h3>أهداف التعلم</h3>
    <div class="g"><span class="tag">اشرح</span><span class="x">أدوار جدار الحماية، و{en("VPN")}، و{en("DMZ")}، وضوابط الأجهزة الطرفية في حماية الشبكة.</span></div>
    <div class="g"><span class="tag">اشرح</span><span class="x">لماذا يوفر الدفاع في العمق حماية أقوى من الاعتماد على إجراء أمني واحد.</span></div>
    <div class="g"><span class="tag">قيّم</span><span class="x">تصميمًا أمنيًا لشبكة، وبرر اختيار الضوابط المناسبة وفق الأصول والتهديدات.</span></div>
  </div>
</div>''')
A('<div class="note-box"><span class="tag">للفهم</span>أي جزء عليه علامة «للفهم» هو شرح أو رسم إضافي للتوضيح، ومش مطلوب حفظه كنص من الكتاب.</div>')
A(f'''<div class="map m2">
  <div class="cell c1"><h4><span class="mn">1</span>الضوابط الأربعة</h4><ul>
    <li><b>جدار الحماية</b> — يسمح بحركة المرور أو يمنعها وفق قواعد.</li>
    <li><b>{nw("VPN")}</b> — اتصال خاص عبر شبكة عامة.</li>
    <li><b>{nw("DMZ")}</b> — الخوادم المواجهة للجمهور منفصلة عن الداخل.</li>
    <li><b>الأجهزة الطرفية</b> — مكافحة فيروسات وتحديث النظام.</li></ul></div>
  <div class="cell c3"><h4><span class="mn">2</span>الدفاع في العمق</h4><ul>
    <li>طبقات متعددة من الضوابط الأمنية.</li>
    <li>لو فشلت طبقة، تساعد الطبقات الأخرى على تقليل الخطر والحد من الأثر.</li></ul></div>
  <div class="hub">تصميم أمان<br>الشبكات
    {lk("r1", "M0 14 C7 14 10 3 17 3", "#22375c", 17.5, 3)}
    {lk("r2", "M0 2 C7 2 10 13 17 13", "#e29433", 17.5, 13)}
    {lk("l1", "M20 14 C13 14 10 3 3 3", "#2e4a78", 2.5, 3)}
    {lk("l2", "M20 2 C13 2 10 13 3 13", "#a9670f", 2.5, 13)}
  </div>
  <div class="cell c2"><h4><span class="mn">3</span>الطبقات الأربع</h4><ul>
    <li>مدخل الشبكة — جدار الحماية</li>
    <li>مسار الاتصال — {nw("VPN")}</li>
    <li>وضع الخوادم — {nw("DMZ")}</li>
    <li>الأجهزة الطرفية — مكافحة الفيروسات والتحديث</li></ul></div>
  <div class="cell c4"><h4><span class="mn">4</span>نهج انعدام الثقة</h4><ul>
    <li>لا ثقة تلقائية لمجرد الوجود داخل الشبكة.</li>
    <li>تُفحص الهوية والصلاحيات والسياق عند الوصول.</li>
    <li>حماية المحيط الأمني وحدها لم تعد كافية.</li></ul></div>
</div>''')
A('''<div class="iq">
  <div class="q">
    <div class="lab">السؤال الرئيسي — الدرس كله بيجاوب عليه</div>
    <div class="qq">كيف يمكن لمؤسسة أن تصمم شبكتها بحيث، حتى لو تم اختراق أحد الدفاعات، يظل النظام محميًا؟</div>
  </div>
  <div class="idea"><span class="qmark">”</span><b>الفكرة الأساسية:</b> يأتي أمان الشبكات القوي من <b>تكديس الإجراءات</b> – جدار الحماية، والشبكة الافتراضية الخاصة، والمنطقة المعزولة، وحماية الأجهزة الطرفية – ومن <b>التحقق من كل عملية وصول</b> (نهج انعدام الثقة)، <b>وليس من حاجز واحد</b>.</div>
</div>''')

# ---- الجزء الأول
A('<div class="part p1"><span>الجزء الأول</span></div>\n<hr class="rule">')
A('<div class="quote kwn"><span class="qmark">”</span>تحتفظ شبكات المؤسسات ببيانات وخدمات مهمة قد يحاول مهاجم الوصول إليها. <b>ولا تكفي وسيلة حماية واحدة؛ فإذا فشلت، قد تتعرض موارد أخرى للخطر</b>. لذلك يُستخدم <b>الدفاع في العمق</b>، فتعمل <b>طبقات متعددة</b> على تقليل احتمال الاختراق والحد من أثره.</div>')
A(exs('هنمشي في الدرس كله على <b>بنك</b> عنده: <b>موقع إلكتروني</b> لأي عميل · <b>قاعدة بيانات حسابات العملاء</b> (سرية) · <b>موظفين بيشتغلوا من البيت</b> · و<b>فروع</b> في مدن تانية. وهنشوف كل إجراء بيحمي إيه فيهم.'))

A('<h2 class="sec"><span class="num">1</span><span class="dot">·</span> دور جدران الحماية</h2>')
A('<span class="chip">جدار الحماية</span>')
A('<div class="banner kwn"><b>نظام أو برنامج يراقب حركة مرور الشبكة ويسمح بها أو يمنعها وفق قواعد أمنية</b>. وقد يوجد <b>عند حدود الشبكة أو بين أجزائها أو على جهاز مضيف</b>. <span class="bx">مثال: السماح بالوصول إلى خادم الويب مع منع الوصول الخارجي المباشر إلى قاعدة البيانات.</span></div>')
FWR = [("globe", "زائر من الإنترنت", "server", "خادم الويب", True), ("globe", "زائر من الإنترنت", "db", "قاعدة البيانات مباشرة", False)]
ICF = {"globe": ic_globe, "server": ic_server, "db": ic_db}
A(f'''<div class="fwx keep">
  <div class="fig fwr">{FXA}<div class="fwh">مثال الكتاب كقواعد</div>'''
  + "".join(f'<div class="fr {"ok" if ok else "no"}"><span class="a">{ICF[i1]("#22375c")}<b>{t1}</b></span><i class="w">{ic_wall("#a9670f")}</i><span class="a">{ICF[i2]("#22375c")}<b>{t2}</b></span><span class="st">{ic_ok("#fff") if ok else ic_x("#fff")}{"مسموح" if ok else "ممنوع"}</span></div>' for i1, t1, i2, t2, ok in FWR)
  + '''<div class="fwp"><span class="pl">ممكن يكون فين؟</span><span>عند حدود الشبكة</span><span>بين أجزائها</span><span>على جهاز مضيف</span></div></div>
  <div class="im"><img src="assets/u2/l22_firewall.jpg" alt=""><div class="icap">يسمح جدار الحماية بمرور البيانات أو يمنعها وفقًا لقواعد محددة.</div></div>
</div>''')
A('<div class="note-line"><span class="tag">للفهم</span><span class="lead">ببساطة</span>اعتبره <b>بوّاب بقائمة</b>: كل اتصال جاي أو رايح بيتقاس على <b>قواعد محددة مسبقًا</b> — مسموح ولا ممنوع. وخُد بالك: الكتاب قال إنه ممكن يكون <b>مش بس على حدود الشبكة</b> — كمان <b>بين أجزائها</b> أو <b>على جهاز واحد</b>.</div>')
A(exs('جدار حماية على حدود شبكة البنك: <b>يسمح</b> لأي عميل يفتح موقع البنك، و<b>يمنع</b> أي اتصال من برّه يحاول يوصل لقاعدة بيانات الحسابات <b>مباشرة</b>.'))

A(f'<h2 class="sec"><span class="num">2</span><span class="dot">·</span> الشبكة الافتراضية الخاصة {nw("(VPN)")}</h2>')
A(f'<span class="chip">الشبكة الافتراضية الخاصة {nw("(VPN - Virtual Private Network)")}</span>')
A('<div class="banner kwn"><b>اتصال أو شبكة منطقية خاصة عبر شبكة عامة مثل الإنترنت</b>، تستخدم <b>عادةً التشفير وتقنيات النفق</b> لحماية البيانات بين الطرفين.</div>')
A(f'''<div class="sf">
  <div class="quote"><span class="qmark">”</span><b>الاستخدامات الرئيسية للشبكة الافتراضية الخاصة:</b><br>① <b>العمل عن بُعد</b>... الاتصال بأمان بشبكة المؤسسة من المنزل أو أثناء التنقل.<br>② <b>ربط الفروع</b>... ربط المكاتب في مواقع مختلفة بأمان.<br>ونظرًا لأن <b>محتوى الاتصال يُشفَّر</b> عند استخدام الشبكة الافتراضية الخاصة، <b>تقل مخاطر التنصت</b> حتى عند استخدام شبكة {nw("Wi-Fi")} عامة.</div>
  <div class="im"><img src="assets/u2/l22_vpn.jpg" alt=""><div class="icap">تنقل الشبكة الافتراضية الخاصة {en("(VPN)")} البيانات بأمان عبر شبكة غير موثوقة.</div></div>
</div>''')
def tun(a_ic, a_t, b_ic, b_t):
    return (f'<div class="tn"><span class="e">{a_ic("#22375c")}<b>{a_t}</b></span><span class="tb"><i></i><em>{ic_lock("#a9670f")}نفق مشفّر عبر الإنترنت</em><i></i></span><span class="e">{b_ic("#22375c")}<b>{b_t}</b></span></div>')
A(f'''<div class="fig vpu keep">{FXA}
  <div class="vu2">
    <div class="vc"><h5><span class="cn">1</span>العمل عن بُعد</h5>{tun(ic_home, "موظف في البيت", ic_building, "شبكة المؤسسة")}</div>
    <div class="vc"><h5><span class="cn">2</span>ربط الفروع</h5>{tun(ic_building, "فرع في مدينة تانية", ic_building, "المقر الرئيسي")}</div>
  </div>
  <div class="vw">
    <div class="vb"><span class="vl">{ic_wifi("#a33a30")}<span>على {nw("Wi-Fi")} عامة من غير {nw("VPN")}</span></span><p>محتوى الاتصال ممكن يتعرّض <b>للتنصت</b></p></div>
    <div class="vb g"><span class="vl">{ic_wifi("#2e7d5b")}<span>على {nw("Wi-Fi")} عامة مع {nw("VPN")}</span></span><p>المحتوى <b>مشفّر</b> ← <b>تقل</b> مخاطر التنصت</p></div>
  </div>
  <div class="cap">الاستخدامين الرئيسيين — والفرق على شبكة عامة. (الكتاب قال «تقل» مش «تنعدم».)</div>
</div>''')
A(exs(f'موظف البنك بيشتغل <b>من البيت</b>، وفرع البنك في مدينة تانية <b>بيتوصل بالمقر</b> — الاتنين عبر {nw("VPN")}، فبيانات العملاء بتعدّي الإنترنت <b>مشفّرة</b> جوّه نفق. ولو الموظف اتوصل من <b>واي فاي كافيه</b>، اللي بيتنصت على الشبكة <b>مايقدرش يقرا</b> المحتوى.'))

A(f'<h2 class="sec"><span class="num">3</span><span class="dot">·</span> المنطقة المعزولة {nw("(DMZ – Demilitarized Zone)")}</h2>')
A(f'<span class="chip">المنطقة المعزولة {nw("(DMZ)")}</span>')
A('<div class="banner kwn">منطقة تُوضع فيها <b>الخوادم المعرَّضة للشبكة الخارجية</b> (خوادم الويب، خوادم البريد، إلخ) <b>بشكل منفصل عن الشبكة الداخلية</b>.</div>')
A('<div class="quote"><span class="qmark">”</span>يساعد فصل الخوادم العامة في منطقة معزولة على <b>تقليل احتمال وصول الهجوم منها إلى الشبكة الداخلية</b> إذا تعرض أحدها للاختراق.</div>')
def dnode(icf, t): return f'<div class="dn">{icf("#22375c")}<span>{t}</span></div>'
A(f'''<div class="fig dmz keep">
  <div class="dzh">تكوين شبكة المنطقة المعزولة {en("(DMZ)")}</div>
  <div class="dz">
    <div class="zc ext"><h5>الشبكة الخارجية<small>(الإنترنت)</small></h5>{dnode(ic_globe, "الإنترنت")}<div class="dr">{dnode(ic_user, "المستخدمون")}{dnode(ic_bug, "مهاجم")}</div></div>
    <div class="fw"><i>{ic_wall("#fff")}</i><span>جدار الحماية</span></div>
    <div class="zc dmzz"><h5>{en("DMZ")}<small>(المنطقة المعزولة)</small></h5><div class="dr">{dnode(ic_server, "خادم الويب")}{dnode(ic_mail, "خادم البريد الإلكتروني")}</div><div class="zx"><b>الخوادم المعرَّضة للإنترنت</b><small>(منفصلة عن الشبكة الداخلية)</small></div></div>
    <div class="fw"><i>{ic_wall("#fff")}</i><span>جدار الحماية</span></div>
    <div class="zc int"><h5>الشبكة الداخلية<small>(المنظمة)</small></h5><div class="dr">{dnode(ic_laptop, "جهاز الكمبيوتر الشخصي")}{dnode(ic_db, "خادم قاعدة بيانات")}</div><div class="zx s"><b>بيانات سرية</b></div></div>
  </div>
  <div class="dzf">إذا تمت مهاجمة خادم عام، فإن الشبكة الداخلية لا تزال محمية.</div>
  <div class="cap">تكوين شبكة المنطقة المعزولة {en("(DMZ)")}</div>
</div>''')
A(f'<div class="note-line"><span class="tag">للفهم</span><span class="lead">خُد بالك</span>تعريف الكتاب بيقول إن {nw("DMZ")} بتساعد على <b>«تقليل احتمال»</b> وصول الهجوم للشبكة الداخلية — مش <b>«تمنعه»</b>. والفرق ده بيتحوّل لسؤال صح وخطأ. وكمان: {nw("DMZ")} <b>مش</b> نظام بيعرّض <b>جميع</b> الخوادم للخارج — بس الخوادم <b>المواجهة للجمهور</b>.</div>')
A(exs(f'<b>موقع البنك</b> و<b>خادم البريد</b> في {nw("DMZ")}، و<b>قاعدة بيانات الحسابات</b> جوّه الشبكة الداخلية. لو حد اخترق موقع البنك، <b>يقل احتمال</b> إن الهجوم يعدّي منه للحسابات.'))
def lb(n): return f'<span class="lbn">{num(str(n))}</span>'
A(f'''<div class="fig bnk keep">{FXA}<div class="dyh">البنك كله على بعضه — كل إجراء واقف فين؟ <b>(والرقم = رقم الطبقة اللي هتيجي في القسم 4)</b></div>
  <div class="dz">
    <div class="zc ext"><h5>الإنترنت</h5><div class="dr">{dnode(ic_user, "عميل")}{dnode(ic_bug, "مهاجم")}</div><div class="dr">{dnode(ic_home, "موظف في البيت")}{dnode(ic_building, "فرع البنك")}</div></div>
    <div class="fw">{lb(1)}<i>{ic_wall("#fff")}</i><span>جدار الحماية</span></div>
    <div class="zc dmzz">{lb(3)}<h5>{en("DMZ")}</h5><div class="dr">{dnode(ic_server, "موقع البنك")}{dnode(ic_mail, "خادم البريد")}</div><div class="zx"><b>اللي الجمهور بيوصله</b></div></div>
    <div class="fw">{lb(1)}<i>{ic_wall("#fff")}</i><span>جدار الحماية</span></div>
    <div class="zc int"><h5>الشبكة الداخلية</h5><div class="dr">{dnode(ic_db, "حسابات العملاء")}</div><div class="dr"><div class="dn ep">{lb(4)}{ic_laptop("#22375c")}<span>أجهزة الموظفين</span><small>مكافحة فيروسات + تحديث</small></div></div></div>
  </div>
  <div class="vtn">{lb(2)}<span class="e">{ic_home("#22375c")}موظف في البيت · {ic_building("#22375c")}الفرع</span><span class="tb"><i></i><em>{ic_lock("#a9670f")}نفق {nw("VPN")} مشفّر عبر الإنترنت</em><i></i></span><span class="e">{ic_db("#22375c")}الشبكة الداخلية</span></div>
  <div class="cap">مثال توضيحي مبسّط على بنك — كل إجراء بيحمي حاجة مختلفة، ومع بعض بيعملوا طبقات.</div>
</div>''')
A(recall(["جدار حماية ← قواعد", f"{nw('VPN')} ← نفق مشفّر", f"{nw('DMZ')} ← الخوادم العامة"]))

# ---- الجزء الثاني
A('<div class="part p2"><span>الجزء الثاني</span></div>\n<hr class="rule">')
A(f'<h2 class="sec"><span class="num">4</span><span class="dot">·</span> الدفاع في العمق {nw("(Defense in Depth)")}</h2>')
A('<span class="chip">الدفاع في العمق</span>')
A('<div class="banner kwn"><b>استخدام طبقات متعددة من الضوابط الأمنية</b>، بحيث <b>تساعد طبقات أخرى على تقليل الخطر والحد من أثر الاختراق إذا فشلت إحدى الطبقات</b>.</div>')
A('<figure class="bimg keep"><img src="assets/u2/l22_depth.jpg" alt=""><figcaption class="icap">إذا فشلت طبقة حماية، تبقى طبقات أخرى تقلل الخطر.</figcaption></figure>')
A('<div class="quote kwn">في أمان الشبكات، يتم <b>الجمع بين عدة إجراءات</b> على النحو التالي.</div>')
LAY = [("الطبقة 1: مدخل الشبكة", "منع الاتصال غير المصرح به باستخدام جدار الحماية"),
       ("الطبقة 2: مسار الاتصال", "تشفير الاتصال باستخدام الشبكة الافتراضية الخاصة"),
       ("الطبقة 3: وضع الخوادم", f"فصل الخوادم المواجهة للجمهور عن الشبكة الداخلية باستخدام المنطقة المعزولة {en('(DMZ)')}"),
       ("الطبقة 4: الأجهزة الطرفية", "تثبيت برنامج مكافحة الفيروسات والحفاظ على تحديث نظام التشغيل")]
A('<table class="t lyt keep"><thead><tr><th style="width:150pt">الطبقة</th><th>أمثلة على الإجراءات</th></tr></thead><tbody>'
  + "".join(f'<tr><td class="k">{a}</td><td>{b}</td></tr>' for a, b in LAY) + '</tbody></table>')
FAIL = [(ic_wall, "مدخل الشبكة", "المهاجم عدّى جدار الحماية ووصل لموقع البنك", ic_server, f"{nw('DMZ')} بتقلل احتمال إنه يوصل منه للشبكة الداخلية"),
        (ic_bug, "الأجهزة الطرفية", "موظف فتح ملف مصاب على جهازه", ic_shield, "مكافحة الفيروسات والتحديثات على الجهاز بتقلل الخطر"),
        (ic_wifi, "مسار الاتصال", f"موظف اتوصل من {nw('Wi-Fi')} عامة وحد بيتنصت", ic_lock, f"{nw('VPN')} بيشفّر المحتوى فتقل مخاطر التنصت")]
A(f'<div class="fig flx keep">{FXA}<div class="dyh">طب لو حاجة فشلت؟ — الطبقات التانية لسه شغالة</div>'
  + '<div class="flc"><span>اللي حصل</span><span></span><span>اللي لسه بيقلل الخطر</span></div>'
  + "".join(f'<div class="flr"><div class="f1">{a("#a33a30")}<p>{t}</p></div><i class="lar">{ARR}</i><div class="f2">{b("#2e7d5b")}<p>{u}</p></div></div>' for a, _, t, b, u in FAIL)
  + '<div class="cap">أمثلة للتوضيح على بنك — والكتاب بيقول «تقلل» مش «تمنع منعًا مطلقًا».</div></div>')
A('<div class="note-line"><span class="tag">للفهم</span><span class="lead">طب ليه؟</span>ليه الطبقات أحسن من حاجز واحد؟ دي <b>بالظبط</b> إجابة سؤال نمط الامتحان في الدرس. لو عندك <b>حاجز واحد</b> وفشل، <b>الطريق مفتوح</b>. لكن لو الإجراءات <b>مكدّسة</b>، فشل طبقة <b>مابيوصّلش المهاجم للهدف على طول</b>: الطبقات التانية بتساعد على <b>تقليل الخطر والحد من أثر الاختراق</b>.</div>')
A(recall(["مدخل الشبكة", "مسار الاتصال", "وضع الخوادم", "الأجهزة الطرفية"]))

# ---- الجزء الثالث
A('<div class="part p3"><span>الجزء الثالث</span></div>\n<hr class="rule">')
A('<h2 class="sec"><span class="num">5</span><span class="dot">·</span> مفهوم نهج انعدام الثقة</h2>')
A(f'<span class="chip">نهج انعدام الثقة {nw("(Zero Trust)")}</span>')
A('<div class="banner kwn">نهج أمني <b>لا يمنح الثقة تلقائيًا لمستخدم أو جهاز لمجرد وجوده داخل الشبكة أو ملكيته للمؤسسة</b>. <b>تُفحص الهوية والصلاحيات والسياق</b> عند طلب الوصول إلى الموارد وفق سياسة المؤسسة.</div>')
A('<div class="quote"><span class="qmark">”</span>صُمم أمان الشبكات التقليدي بشكل أساسي حول <b>حماية المحيط الأمني</b>، بناءً على فرضية أن <b>"داخل شبكة المؤسسة آمن، وخارجها خطر"</b>. ومع ذلك، مع انتشار <b>الخدمات السحابية والعمل عن بُعد</b>، أصبحت الحدود بين "الداخل" و"الخارج" <b>غير واضحة</b>، وأصبحت التصاميم التي تحمي المحيط الأمني فقط <b>غير كافية</b>.</div>')
def pm(icf, t, cls=""): return f'<div class="pm {cls}">{icf("#22375c" if cls != "out" else "#a9670f")}<span>{t}</span></div>'
A(f'''<div class="fig per keep">{FXA}<div class="dyh">ليه المحيط الأمني وحده مبقاش كفاية؟</div>
  <div class="pr2">
    <div class="pc"><h5>زمان — المحيط الأمني</h5>
      <div class="pw"><span class="pt">سور = المحيط الأمني</span>{pm(ic_user, "الموظفين")}{pm(ic_laptop, "الأجهزة")}{pm(ic_db, "البيانات")}</div>
      <div class="po">{pm(ic_globe, "الإنترنت", "out")}</div>
      <p><b>جوّه السور = آمن</b> · <b>برّه = خطر</b> — والحماية كلها عند السور.</p></div>
    <i class="lar">{ARR}</i>
    <div class="pc now"><h5>دلوقتي — السحابة والعمل عن بُعد</h5>
      <div class="pw dash"><span class="pt">السور لسه موجود</span>{pm(ic_user, "موظفين في المكتب")}{pm(ic_laptop, "أجهزة")}</div>
      <div class="po">{pm(ic_cloud, "خدمات وبيانات على السحابة", "out")}{pm(ic_home, "موظف من البيت", "out")}</div>
      <p>حاجات مهمة بقت <b>برّه السور</b> ← الحدود بين «الداخل» و«الخارج» <b>غير واضحة</b> ← حماية المحيط بس <b>غير كافية</b>.</p></div>
  </div>
  <div class="cap">تبسيط لكلام الكتاب: «مع انتشار الخدمات السحابية والعمل عن بُعد، أصبحت الحدود بين الداخل والخارج غير واضحة».</div>
</div>''')
A('<div class="note-line"><span class="tag">للفهم</span><span class="lead">ببساطة</span>زمان الثقة كانت بتتحدد بـ<b>مكانك</b>: لو إنت جوّه الشبكة يبقى إنت كويس. دلوقتي الثقة بتتحدد بـ<b>هويتك وصلاحياتك وسياق الطلب</b> — <b>كل مرة</b>. عشان كده: السحابة برّه، والموظف بيشتغل من بيته — فمبقاش فيه «جوّه» و«برّه» واضحين.</div>')
def zp(icf, t, lock=False): return f'<div class="zp">{icf("#22375c")}<span>{t}</span>{("<i>" + ic_lock("#fff") + "</i>") if lock else ""}</div>'
A(f'''<div class="fig ztf keep">
  <div class="dzh">المقارنة بين الثقة الصفرية و الأمان التقليدي</div>
  <div class="zt2">
    <div class="zs zero"><h5>الثقة الصفرية</h5>
      <div class="zb"><div class="zl">لا يوجد حاجز داخلي / خارجي</div>
        <div class="zr">{zp(ic_laptop, "الجهاز", True)}{zp(ic_user, "المستخدم الخارجي", True)}{zp(ic_user, "المستخدم الداخلي", True)}</div>
        <div class="zv">▼ تحقق من كل وصول ▼</div>
        <div class="zr">{zp(ic_building, "التطبيق")}{zp(ic_db, "البيانات")}</div></div></div>
    <div class="zs trad"><h5>الأمان التقليدي</h5>
      <div class="zb o"><div class="zl">الخارجي<small>غير موثوق</small></div><div class="zr">{zp(ic_laptop, "الجهاز")}{zp(ic_user, "المستخدم الخارجي")}</div></div>
      <div class="zfw">جدار الحماية</div>
      <div class="zb i"><div class="zl">الداخلي<small>موثوق (بدون تحقق)</small></div><div class="zr">{zp(ic_db, "البيانات")}{zp(ic_laptop, "جهاز الكمبيوتر الشخصي")}{zp(ic_user, "المستخدم")}</div></div></div>
  </div>
  <div class="dzf">مع تلاشي الخط الفاصل بين "الداخلي/الخارجي" بسبب الحوسبة السحابية والعمل عن بُعد، يتم التحقق من كل وصول.</div>
  <div class="cap">الأمان التقليدي مقابل نهج انعدام الثقة</div>
</div>''')
ZC = [(ic_idc, "الهوية", "مين اللي بيطلب؟", "موظف مسجّل في البنك بحسابه"),
      (ic_perm, "الصلاحيات", "مسموح له بإيه؟", "حسابات عملاء فرعه بس — مش كل الحسابات"),
      (ic_clock, "السياق", "من أي جهاز؟ إمتى؟ منين؟", "جهاز البنك المعروف، في وقت الشغل")]
A(f'<div class="fig ztc keep">{FXA}<div class="dyh">موظف قاعد <b>جوّه</b> مبنى البنك وعلى شبكته، وطلب يفتح حساب عميل — هل ده كفاية؟</div>'
  + '<div class="zc3">' + "".join(f'<div><span class="zi">{f("#22375c")}</span><h5>{t}</h5><small>{q}</small><p><em>مثال للتبسيط:</em> {x}</p></div>' for f, t, q, x in ZC) + '</div>'
  + '<div class="zcf"><b>الأمان التقليدي:</b> جوّه الشبكة ← موثوق من غير تحقق · <b>نهج انعدام الثقة:</b> مفيش ثقة تلقائية ← يتفحص كل وصول وفق سياسة المؤسسة</div></div>')
A(recall(["الهوية", "الصلاحيات", "السياق"]))

A('<div class="kidea keep"><div class="kh">الفكرة الرئيسة</div><p>يكون أمان الشبكة في أقوى حالاته عندما <b>تُكدَّس الإجراءات في طبقات متعددة (الدفاع في العمق)</b> ولا <b>يُمنح أي وصول ثقة تلقائيًا (نهج انعدام الثقة)</b>، بحيث يصبح <b>من غير المرجح</b> أن يؤدي خرق واحد إلى كشف النظام بأكمله.</p></div>')

# ---- سؤال على نمط الامتحان
A('<div class="big">سؤال على نمط الامتحان — ونموذج إجابته</div>\n<hr class="rule">')
A(f'''<div class="exam keep">
  <div class="hd"><span class="n">1</span><span class="t">سؤال على نمط الامتحان</span><span class="m">[{num("6")} درجات]</span></div>
  <div class="qt">اشرح لماذا يحمي تكديس عدة إجراءات أمنية في طبقات (الدفاع في العمق) المؤسسة بشكل أفضل من الاعتماد على جدار الحماية وحده.</div>
  <div class="hint"><b>استعن بـ:</b> ما يحدث إذا تم اختراق أحد الإجراءات.</div>
</div>''')
A('<h3 class="sub">سؤال على نمط الامتحان — إجابة نموذجية</h3>')
MODEL = [
    "<b>المشكلة في الحاجز الواحد:</b> لا تكفي وسيلة حماية واحدة؛ فإذا فشلت، قد تتعرض موارد أخرى للخطر – يعني اختراق جدار الحماية وحده ممكن يفتح الطريق للشبكة كلها.",
    "<b>الفكرة البديلة – الدفاع في العمق:</b> استخدام طبقات متعددة من الضوابط الأمنية.",
    f"<b>الطبقات الأربع:</b> مدخل الشبكة (جدار الحماية) · مسار الاتصال {en('(VPN)')} · وضع الخوادم {en('(DMZ)')} · الأجهزة الطرفية (مكافحة الفيروسات وتحديث نظام التشغيل).",
    f"<b>ماذا لو اختُرق أحد الإجراءات؟</b> تساعد طبقات أخرى على تقليل الخطر والحد من أثر الاختراق – مثال: لو اتهاجم خادم عام في {en('DMZ')}، يقل احتمال امتداد الهجوم للشبكة الداخلية.",
    "<b>ومع الطبقات – نهج انعدام الثقة:</b> لا تُمنح الثقة تلقائيًا لمستخدم أو جهاز لمجرد وجوده داخل الشبكة، بل تُفحص الهوية والصلاحيات والسياق.",
    "<b>الخلاصة:</b> يصبح من غير المرجح أن يؤدي خرق واحد إلى كشف النظام بأكمله.",
]
A('<div class="box white split"><h3>نموذج إجابة مقترح لسؤال الـ' + num("6") + ' درجات</h3>'
  + "".join(f'<ol style="counter-reset:n {k}"><li>{t}</li></ol>' for k, t in enumerate(MODEL))
  + '<div class="tip"><span class="l">ركّز:</span> التلميح سأل عن <b>ما يحدث إذا تم اختراق أحد الإجراءات</b> – فخلّي في إجابتك <b>مثال واضح لفشل إحدى وسائل الحماية</b>، مع توضيح <b>دور الطبقات الأخرى</b> في تقليل أثره. واذكر إن الطبقات <b>تقلل</b> الخطر ولا تمنعه منعًا مطلقًا.</div></div>')

A('<h2 class="sec"><span class="num"></span>إجابة السؤال الرئيسي</h2>')
A('''<div class="mq">
  <div class="lab">السؤال</div>
  <div class="qq">كيف يمكن لمؤسسة أن تصمم شبكتها بحيث، حتى لو تم اختراق أحد الدفاعات، يظل النظام محميًا؟</div>
</div>''')
A('<div class="quote"><span class="qmark">”</span>تناول السؤال الرئيسي تصميم شبكة لا يؤدي فيها فشل وسيلة واحدة إلى كشف النظام كله. <b>يراقب جدار الحماية حركة الشبكة</b>، و<b>تحمي الشبكة الافتراضية الخاصة الاتصال البعيد</b>، و<b>تفصل المنطقة المعزولة الخوادم العامة عن الشبكة الداخلية</b>، و<b>تحمي ضوابط الأجهزة الطرفية كل جهاز</b>. ومع السحابة والعمل عن بُعد، أصبح <b>الاعتماد على موقع المستخدم داخل الشبكة أقل فاعلية دليلًا على الثقة</b>؛ لذلك <b>لا يمنح نهج انعدام الثقة ثقة تلقائية</b>، بل يطلب التحقق المناسب من الهوية والصلاحيات عند الوصول. تعمل هذه الطبقات معًا <b>لتقليل الخطر والحد من أثر الاختراق</b>.</div>')
A('<div class="note-line"><span class="tag">للفهم</span><span class="lead">طب ليه؟</span><b>لو السؤال ده جالك في الامتحان</b> الإجابة القوية بتعمل 3 حاجات: <b>(1)</b> تذكر <b>دور كل ضابط</b> من الأربعة · <b>(2)</b> توضّح ليه <b>المحيط الأمني وحده</b> مبقاش كفاية (السحابة والعمل عن بُعد) · <b>(3)</b> تقفل بإن الطبقات <b>بتقلل الخطر وبتحدّ من الأثر</b> — مش ضمان مطلق.</div>')
A('''<div class="terms keep">
  <div class="th"><h3>مصطلحات أساسية</h3></div>
  <div class="t2">
    <div><b>جدار الحماية</b> – يسمح بالاتصال أو يمنعه عند نقطة دخول/خروج الشبكة استنادًا إلى قواعد محددة مسبقًا.</div>
    <div><b>المنطقة المعزولة (DMZ)</b> – منطقة للخوادم المواجهة للجمهور، منفصلة عن الشبكة الداخلية.</div>
    <div><b>الدفاع في العمق</b> – تكديس الإجراءات الأمنية في طبقات متعددة.</div>
    <div><b>نهج انعدام الثقة</b> – التحقق من كل عملية وصول.</div>
    <div class="full"><b>المحيط الأمني</b> – الحدود التقليدية التي تفترض أن "الداخل آمن"، والتي طمستها الخدمات السحابية والعمل عن بُعد.</div>
  </div>
</div>''')
A(f'''<div class="box cream keep">
  <h3>خلي بالك من العبارات دي</h3>
  <ul>
    <li>جدار الحماية <b>«قد يوجد عند حدود الشبكة أو بين أجزائها أو على جهاز مضيف»</b> – مش بس على الحدود.</li>
    <li>{nw("VPN")} <b>«تستخدم عادةً التشفير وتقنيات النفق»</b> – «عادةً».</li>
    <li>{nw("DMZ")} تساعد على <b>«تقليل احتمال»</b> وصول الهجوم للداخل – مش «تمنعه»، ومش نظام يعرّض <b>جميع</b> الخوادم.</li>
    <li>الدفاع في العمق: <b>«تساعد طبقات أخرى على تقليل الخطر والحد من أثر الاختراق»</b>.</li>
    <li>الفكرة الرئيسة: <b>«من غير المرجح»</b> أن يؤدي خرق واحد إلى كشف النظام بأكمله – مش «مستحيل».</li>
    <li>انعدام الثقة: تُفحص <b>«الهوية والصلاحيات والسياق»</b> <b>«وفق سياسة المؤسسة»</b>.</li>
  </ul>
</div>''')
A(f'''<div class="box plain keep">
  <h3>مثال من حياتنا{FX}</h3>
  <p>تخيّل مدرسة عندها <b>موقع إلكتروني</b> الناس بتدخله من برّه، و<b>سيرفر درجات</b> فيه بيانات كل الطلبة، و<b>مدرسين بيشتغلوا من البيت</b>. لو حطّينا الموقع جوّه الشبكة الداخلية جنب سيرفر الدرجات – أي ثغرة في الموقع ممكن تبقى <b>باب مفتوح</b> على الدرجات.</p>
  <p>التصميم الأحسن: الموقع في <b>{nw("DMZ")}</b>، وسيرفر الدرجات <b>جوّه</b>، و<b>جدار حماية</b> بينهم، والمدرسين بيدخلوا من البيت عبر <b>{nw("VPN")}</b>، وأجهزتهم عليها <b>مكافحة فيروسات ونظام محدّث</b>. وبعد كل ده: <b>كل طلب وصول للدرجات بيتفحص</b> – مش لأن الجهاز جوّه الشبكة يبقى ماشي.</p>
  <p><b>وبرضه:</b> ده <b>بيقلل</b> الخطر. الكتاب بيقول <b>«من غير المرجح»</b> إن خرق واحد يكشف النظام كله – مش «مستحيل».</p>
</div>''')
A(f'''<div class="dark keep">
  <h3>الخلاصة في دقيقة</h3>
  <p class="rem"><b>تذكّر:</b> كدّس دفاعاتك – جدار الحماية، والشبكة الافتراضية الخاصة، والمنطقة المعزولة، والأجهزة الطرفية – وتحقق من كل عملية وصول (نهج انعدام الثقة). عندها يصبح من غير المرجح أن يؤدي خرق واحد إلى كشف الشبكة بأكملها.</p>
  <div class="g2">
    <ul>
      <li><b>جدار الحماية:</b> يراقب حركة المرور ويسمح بها أو يمنعها <b>وفق قواعد</b> – عند الحدود أو بين الأجزاء أو على جهاز.</li>
      <li><b>{nw("DMZ")}:</b> تفصل الخوادم المواجهة للجمهور عن الشبكة الداخلية، <b>فتقل احتمالية</b> انتقال الهجوم للداخل لو اتخترق خادم عام.</li>
      <li><b>الدفاع في العمق:</b> لو فشلت طبقة، الباقي <b>يقلل الخطر ويحدّ من الأثر</b>.</li>
    </ul>
    <ul>
      <li><b>{nw("VPN")}:</b> اتصال خاص عبر شبكة عامة بالتشفير وتقنيات النفق – <b>العمل عن بُعد وربط الفروع</b>، وتقليل التنصت على {nw("Wi-Fi")} عامة.</li>
      <li><b>الطبقات الأربع:</b> مدخل الشبكة · مسار الاتصال · وضع الخوادم · الأجهزة الطرفية.</li>
      <li><b>انعدام الثقة:</b> لا ثقة تلقائية بسبب الموقع – <b>الهوية والصلاحيات والسياق</b> عند كل وصول.</li>
    </ul>
  </div>
</div>''')
A('''<div class="check keep kwn">
  <h3>اتأكد إنك قادر على</h3>
  <div class="g2">
    <ul>
      <li><span>أعرف تعريف <b>جدار الحماية</b> و<b>أين قد يوجد</b>.</span></li>
      <li><span>أعرف تعريف <b>DMZ</b> و<b>الفايدة</b> منها بالظبط.</span></li>
      <li><span>أقدر أشرح <b>ليه الطبقات أقوى من حاجز واحد</b> بسيناريو فشل.</span></li>
      <li><span>أعرف إن الطبقات <b>تقلل</b> الخطر – والكتاب قال «<b>من غير المرجح</b>» مش «مستحيل».</span></li>
    </ul>
    <ul>
      <li><span>أعرف تعريف <b>VPN</b> و<b>استخدامَيها</b>، وليه بتقلل التنصت على شبكة عامة.</span></li>
      <li><span>أقدر أذكر <b>الطبقات الأربع</b> و<b>مثال إجراء</b> في كل طبقة.</span></li>
      <li><span>أعرف <b>نهج انعدام الثقة</b> وليه <b>المحيط الأمني</b> وحده مبقاش كافي.</span></li>
    </ul>
  </div>
</div>''')
A('<div class="endline">أكواد مع زياد — أ/ زياد السعدني · مذكرة البرمجة والذكاء الاصطناعي — تانية ثانوي <span class="num">2026/2027</span> · الوحدة الثانية — الدرس <span class="num">2-2</span></div>')
A('<div class="pb"></div>')
A('''<div class="band" style="height:55pt;padding-right:12pt">
  <div class="badge"><span class="n">2-2</span></div>
  <h1 style="text-align:right;margin-right:12pt;font-size:14pt">لخّص الدرس بأسلوبك</h1>
</div>''')
A('<div class="instr"><span class="fx fl">للفهم</span>اقفل المذكرة وحاول تلخّص الدرس من غير ما تبصّ: اكتب أهم <b>المصطلحات</b>، و<b>الفكرة الأساسية</b>، و<b>النقطة اللي لسه محتاجة مراجعة</b>. بعد كده افتح المذكرة وقارن اللي كتبته.</div>')
A('<div class="lines">' + '<div></div>' * 24 + '</div>')


# ============================ بنك الأسئلة ============================
B = []
A = B.append
A('<div class="pb"></div>')
A(f'''<div class="band">
  <div class="badge"><span class="l">الدرس</span><span class="n">2-2</span></div>
  <h1>{TITLE}</h1>
  <div class="who"><div class="t"><span class="u">الوحدة الثانية</span><span class="k">بنك الأسئلة</span></div><img src="assets/avatar.png" alt=""></div>
</div>''')

# ---- أسئلة الكتاب
BOOK = []
BOOK.append(card("01", "المثال المحلول — الجزء الأول",
       instr("ضع علامة ○ أمام كل عبارة (أ - د) إذا كانت صحيحة، أو علامة × إذا كانت خاطئة.")
       + '<ul class="tf">' + "".join(f'<li><b>{L[k]}</b><span class="t">{t}</span><span class="pr">(&nbsp;&nbsp;&nbsp;&nbsp;)</span></li>' for k, t in enumerate([
           "يسمح جدار الحماية بالاتصال أو يمنعه استنادًا إلى قواعد محددة مسبقًا.",
           f"يمكن أن يقلل استخدام الشبكة الافتراضية الخاصة من مخاطر التنصت حتى على شبكة {nw('Wi-Fi')} عامة.",
           "المنطقة المعزولة نظام يعرّض جميع الخوادم للخارج.",
           "الدفاع في العمق هو مفهوم تكديس عدة إجراءات أمنية في طبقات متعددة."])) + '</ul>'))
BOOK.append(card("02", "المثال المحلول — الجزء الثاني",
       instr("طابق كل وصف (أ - ج) بأنسب مصطلح من الخيارات التالية (أ - ج).")
       + '<div class="match"><div class="mb"><h5>الوصف</h5><ol class="la">'
       + "".join(f'<li><b>{L[k]}</b><span>{t}</span>{AB}</li>' for k, t in enumerate([
           "تقنية تنشئ خطًا خاصًا افتراضيًا مشفرًا عبر الإنترنت للاتصال الآمن من موقع بعيد",
           "منطقة تُوضع فيها الخوادم المعرَّضة للخارج بشكل منفصل عن الشبكة الداخلية",
           "نظام يسمح بالاتصال أو يمنعه استنادًا إلى قواعد محددة مسبقًا"]))
       + '</ol></div><div class="mb"><h5>الخيارات</h5>' + opts(["جدار الحماية", "الشبكة الافتراضية الخاصة", "المنطقة المعزولة"], 1) + '</div></div>'))
SOL1 = [("أ", "يتحكم جدار الحماية في الاتصال استنادًا إلى القواعد. لذلك، ○."),
        ("ب", f"تشفّر الشبكة الافتراضية الخاصة الاتصال، مما يقلل من مخاطر التنصت على شبكة {nw('Wi-Fi')} العامة. لذلك، ○."),
        ("ج", "المنطقة المعزولة هي منطقة توضع فيها الخوادم المواجهة للجمهور بشكل منفصل عن الشبكة الداخلية، وليست نظامًا يعرّض جميع الخوادم. لذلك، ×."),
        ("د", "تعريف صحيح للدفاع في العمق. لذلك، ○.")]
SOL2 = [("أ", "الخط الخاص الافتراضي المشفر هو الشبكة الافتراضية الخاصة.", "ب"), ("ب", "منطقة تُعزل فيها الخوادم المواجهة للجمهور هي المنطقة المعزولة.", "ج"), ("ج", "نظام يسمح بالاتصال أو يمنعه هو جدار الحماية.", "أ")]
BOOK.append('<div class="qcard sol keep"><h4><span class="ck">✓</span> الحل — المثال المحلول</h4><div class="sg">'
       + '<div><div class="sp">(1)</div>' + "".join(f'<div class="sr"><b>{a}</b><span>{t}</span></div>' for a, t in SOL1) + '</div>'
       + '<div><div class="sp">(2)</div>' + "".join(f'<div class="sr"><b>{a}:</b><span>{t} <i>{c}</i></span></div>' for a, t, c in SOL2) + '</div>'
       + '</div></div>')
BOOK.append(card("03", "تدرّب — أجب عن الأسئلة التالية",
       qq(1, f"ما المصطلح الذي يصف نظامًا أو برنامجًا يراقب حركة مرور الشبكة ويسمح بها أو يمنعها وفق قواعد أمنية؟ {blank(110)}")
       + qq(2, f"ما الاختصار الذي يصف اتصالًا منطقيًا خاصًا يحمي البيانات عبر شبكة عامة؟ {blank(90)}")
       + qq(3, f"ما الاختصار المكوّن من ثلاثة أحرف للمنطقة التي تُوضع فيها الخوادم المعرَّضة للخارج بشكل منفصل عن الشبكة الداخلية؟ {blank(90)}")
       + qq(4, f"ما المصطلح الذي يُطلق على مفهوم تكديس عدة إجراءات أمنية؟ {blank(110)}")))
BOOK.append(card("04", "تدرّب — اختيار · والطبقات",
       qq(1, "من بين الخيارات التالية (أ - د)، اختر الخيار الذي <b>لا يمثل استخدامًا مناسبًا</b> للشبكة الافتراضية الخاصة.")
       + opts(["الاتصال بأمان من المنزل بشبكة المؤسسة", "ربط المكاتب في مواقع مختلفة بأمان", "الحذف التلقائي للملفات المصابة بالفيروسات", f"تشفير محتوى الاتصال على شبكة {nw('Wi-Fi')} العامة"], 1)
       + qq(2, "لكل إجراء أمني (أ - د)، بيّن أي طبقة من طبقات الدفاع المتعدد (أ - د) ينتمي إليها: <b>أ</b> مدخل الشبكة، <b>ب</b> مسار الاتصال، <b>ج</b> وضع الخوادم، <b>د</b> الأجهزة الطرفية.")
       + classify(["منع الاتصال غير المصرح به باستخدام جدار الحماية", "تشفير الاتصال باستخدام الشبكة الافتراضية الخاصة", "تثبيت برنامج مكافحة الفيروسات",
                   f"فصل الخوادم المواجهة للجمهور عن الشبكة الداخلية باستخدام المنطقة المعزولة {en('(DMZ)')}"], letters=L[:4])))
BOOK.append(card("05", "سؤال على نمط الامتحان",
       '<p class="qs">اشرح لماذا يحمي تكديس عدة إجراءات أمنية في طبقات (الدفاع في العمق) المؤسسة بشكل أفضل من الاعتماد على جدار الحماية وحده.</p>'
       + hint("<b>استعن بـ:</b> ما يحدث إذا تم اختراق أحد الإجراءات.") + lines(6), tag=MARK6 + TQ))
BOOK.append(card("06", "تمارين — اقرأ الفقرة ثم املأ الفراغات",
       instr("اقرأ الفقرة التالية وأجب عن السؤال.")
       + '<p class="qs rd">لحماية شبكة مؤسسة، تُستخدم طبقات متعددة. يراقب ( <b>أ</b> ) حركة الشبكة ويسمح بها أو يمنعها وفق قواعد. وتوضع الخوادم العامة في ( <b>ب</b> ) منفصلة عن الشبكة الداخلية. ويُحمى الاتصال البعيد عبر ( <b>ج</b> ). ويسمى استخدام طبقات متعددة من الضوابط الأمنية ( <b>د</b> ).</p>'
       + qq(1, "املأ الفراغات (أ) - (د).")
       + classify(["", "", "", ""], letters=L[:4], w=True)))
BOOK.append(card("07", "تمارين — اختيار",
       qq(1, f"من بين الخيارات التالية (أ - د)، اختر السبب الأنسب لاستخدام منطقة معزولة {en('(DMZ)')}.")
       + opts(["لتحسين سرعة الاتصال.", "لتعريض جميع الخوادم للخارج.", "لمنع الضرر عن الشبكة الداخلية حتى لو تعرض خادم مواجه للجمهور للهجوم.", "للكشف عن الفيروسات وإزالتها تلقائيًا."], 1)
       + qq(2, "من بين الخيارات التالية (أ - د)، اختر الخيار الذي يصف مفهوم نهج انعدام الثقة بأنسب طريقة.")
       + opts(["الوصول من داخل شبكة المؤسسة آمن، لذا فإن التحقق غير ضروري.", "جدار الحماية وحده كافٍ لحماية الشبكة.",
               "لا تُمنح الثقة تلقائيًا بناءً على موقع المستخدم أو الجهاز، ويُتحقق من كل طلب وصول وفق الهوية والصلاحيات والسياق.", "يحتاج فقط الوصول من الخارج إلى المراقبة."], 1)))
BOOK_N = 1 + 1 + 4 + 2 + 1 + 1 + 2   # 01 + 02 + أسئلة 03 + أسئلة 04 + 05 + 06 + أسئلة 07

# ---- اختر (الإجابة الصح أول اختيار قبل rebalance)
MCQ = [
 ("«نظام أو برنامج يراقب حركة مرور الشبكة ويسمح بها أو يمنعها وفق قواعد أمنية» هو:", ["نهج انعدام الثقة", "الشبكة الافتراضية الخاصة", "المنطقة المعزولة", "جدار الحماية"]),
 ("حسب الكتاب، قد يوجد جدار الحماية:", ["داخل قاعدة البيانات فقط", "عند حدود الشبكة فقط ولا يوجد في أي مكان آخر داخلها", "عند حدود الشبكة أو بين أجزائها أو على جهاز مضيف", "على الخادم العام فقط"]),
 ("مثال الكتاب على قاعدة في جدار الحماية:", ["حذف الملفات المصابة بالفيروسات تلقائيًا من جميع أجهزة الموظفين والخوادم داخل الشبكة الداخلية", "السماح بالوصول إلى خادم الويب مع منع الوصول الخارجي المباشر إلى قاعدة البيانات", "تشفير كلمات المرور المخزنة", "ربط الفروع ببعضها"]),
 ("«اتصال أو شبكة منطقية خاصة عبر شبكة عامة مثل الإنترنت» هو:", ["المنطقة المعزولة", "جدار الحماية", "الشبكة الافتراضية الخاصة", "المحيط الأمني حول شبكة المؤسسة"]),
 ("تستخدم الشبكة الافتراضية الخاصة <b>عادةً</b>:", ["التشفير وتقنيات النفق", "مكافحة الفيروسات", "بصمة الإصبع", "قواعد جدار الحماية المحددة مسبقًا"]),
 ("الاستخدامان الرئيسيان للشبكة الافتراضية الخاصة هما:", ["إدارة كلمات المرور وتوليدها", "حذف الفيروسات وتحديث النظام", "فصل الخوادم وتسريع التصفح", "العمل عن بُعد وربط الفروع"]),
 (f"لماذا تقل مخاطر التنصت عند استخدام {nw('VPN')} على {nw('Wi-Fi')} عامة؟", ["لأن الشبكة تُغلق", "لأن سرعة الاتصال بالإنترنت تزيد كثيرًا", "لأن محتوى الاتصال يُشفَّر", "لأن الجهاز يُحدَّث"]),
 ("«منطقة تُوضع فيها الخوادم المعرَّضة للشبكة الخارجية بشكل منفصل عن الشبكة الداخلية» هي:", ["المحيط الأمني", "المنطقة المعزولة", "الشبكة الافتراضية الخاصة", "الدفاع في العمق"]),
 (f"من أمثلة الخوادم التي تُوضع في {nw('DMZ')}:", ["خوادم الويب وخوادم البريد", "خادم قاعدة بيانات الموظفين", "أجهزة الموظفين", "جدار الحماية"]),
 (f"في شكل تكوين {nw('DMZ')}، يقع <b>خادم قاعدة البيانات</b> في:", ["خارج جداري الحماية", "المنطقة المعزولة", "الشبكة الخارجية", "الشبكة الداخلية"]),
 ("«استخدام طبقات متعددة من الضوابط الأمنية» هو:", ["المحيط الأمني", "نهج انعدام الثقة", "الدفاع في العمق", "المنطقة المعزولة"]),
 ("إذا فشلت إحدى طبقات الحماية، فإن الطبقات الأخرى:", ["تتوقف عن العمل", "تساعد على تقليل الخطر والحد من أثر الاختراق", "تمنع أي اختراق آخر منعًا مطلقًا ولا يبقى أي خطر على الشبكة", "تحذف البيانات"]),
 ("الطبقة الأولى «مدخل الشبكة» يمثّلها إجراء:", ["منع الاتصال غير المصرح به بجدار الحماية", f"تشفير الاتصال بـ{nw('VPN')}", f"فصل الخوادم بـ{nw('DMZ')}", "تثبيت برنامج مكافحة الفيروسات على جميع أجهزة الموظفين"]),
 ("طبقة «مسار الاتصال» يمثّلها إجراء:", ["تثبيت مكافحة الفيروسات على أجهزة الموظفين", f"تشفير الاتصال باستخدام {nw('VPN')}", "فصل الخوادم العامة", "تحديث نظام التشغيل"]),
 ("طبقة «وضع الخوادم» يمثّلها إجراء:", ["تشفير الاتصال", "منع الاتصال غير المصرح به من الإنترنت إلى الشبكة باستخدام جدار الحماية", "تحديث نظام التشغيل", f"فصل الخوادم المواجهة للجمهور عن الشبكة الداخلية بـ{nw('DMZ')}"]),
 ("طبقة «الأجهزة الطرفية» يمثّلها إجراء:", ["فصل الخوادم", "تثبيت مكافحة الفيروسات وتحديث نظام التشغيل", "ربط الفروع", "إنشاء قواعد جدار الحماية على حدود الشبكة ومراقبة حركة المرور"]),
 ("«نهج أمني لا يمنح الثقة تلقائيًا لمستخدم أو جهاز لمجرد وجوده داخل الشبكة» هو:", ["الدفاع في العمق", "المحيط الأمني للمؤسسة", "نهج انعدام الثقة", "جدار الحماية"]),
 ("في نهج انعدام الثقة، ما الذي يُفحص عند طلب الوصول؟", ["عدد المستخدمين", "سرعة الشبكة", "نوع المتصفح ونظام التشغيل المستخدم فقط", "الهوية والصلاحيات والسياق"]),
 ("الفرضية التي بُني عليها الأمان التقليدي هي:", ["«الخوادم العامة تُعزل»", "«كل وصول يجب التحقق منه»", "«الطبقات المتعددة أفضل دائمًا من الحاجز الواحد»", "«داخل شبكة المؤسسة آمن، وخارجها خطر»"]),
 ("ما الذي جعل حدود «الداخل» و«الخارج» غير واضحة؟", ["الخدمات السحابية والعمل عن بُعد", "زيادة سرعة الإنترنت وانخفاض أسعار الأجهزة", "انتشار كلمات المرور", f"استخدام {nw('DMZ')}"]),
 ("«الحدود التقليدية التي تفترض أن الداخل آمن» تسمى:", ["المنطقة المعزولة", "المحيط الأمني", "النفق", "الطبقة الرابعة"]),
 ("مع انتشار الخدمات السحابية والعمل عن بُعد، أصبحت التصاميم التي تحمي المحيط الأمني فقط:", ["غير كافية", "كافية تمامًا", "أسرع من غيرها", "بديلًا عن جدار الحماية"]),
 ("حسب الفكرة الرئيسة، أمان الشبكة يكون في أقوى حالاته عندما:", ["تُغلق الشبكة عن الإنترنت", "يُستخدم جدار حماية واحد قوي جدًا عند حدود الشبكة يمنع كل الهجمات", "تُكدَّس الإجراءات في طبقات ولا يُمنح أي وصول ثقة تلقائيًا", "تُشفَّر كلمات المرور فقط"]),
 ("الفكرة الرئيسة تقول إن الخرق الواحد يصبح:", ["مستحيلًا تمامًا مهما كانت قوة المهاجم وأدواته", "من غير المرجح أن يكشف النظام بأكمله", "أسرع في الانتشار", "بلا أثر إطلاقًا"]),
 (f"وضع خادم ويب عام داخل الشبكة الداخلية بدل {nw('DMZ')} يزيد خطر:", ["وصول الهجوم من الخادم إلى الشبكة الداخلية", "بطء تحميل صفحات الموقع على الأجهزة المحمولة للمستخدمين", "نسيان كلمات المرور", "انقطاع الكهرباء"]),
 ("حسب الكتاب، الاعتماد على موقع المستخدم داخل الشبكة أصبح:", ["أقل فاعلية دليلًا على الثقة", "الدليل الوحيد على الثقة", "بديلًا عن جدار الحماية", f"شرطًا لاستخدام {nw('VPN')}"]),
 ("سبب عدم كفاية وسيلة حماية واحدة – حسب الكتاب – هو أنه:", ["تبطئ الشبكة", "تكلفتها عالية", "إذا فشلت، قد تتعرض موارد أخرى للخطر", "تحتاج تدريبًا طويلًا ومكلفًا لكل الموظفين في المؤسسة"]),
 ("الفرضية التي يعتمد عليها نهج انعدام الثقة في تأمين موارد المؤسسة هي:", ["تشفير رسائل البريد الإلكتروني فقط دون الاهتمام بصلاحيات الوصول للبيانات", "اعتبار كل جهاز أو مستخدم داخل شبكة المؤسسة موثوقًا تمامًا بشكل تلقائي", "الاعتماد المطلق على المحيط الأمني الخارجي وعدم فحص التطبيقات الداخلية", "عدم منح الثقة تلقائيًا لمستخدم أو جهاز لمجرد وجوده داخل الشبكة أو ملكيته للمؤسسة، وفحص الهوية والسياق"]),
]
assert len(MCQ) == 28
TQ_MCQ = {1, 4, 6, 8, 11, 13, 16, 17, 21, 28}

# ---- أكمل
FILL = [
 f"النظام الذي يراقب حركة مرور الشبكة ويسمح بها أو يمنعها وفق قواعد أمنية هو {blank()}",
 f"الاتصال أو الشبكة المنطقية الخاصة عبر شبكة عامة هي {blank()}",
 f"المنطقة التي تُوضع فيها الخوادم المعرَّضة للخارج منفصلة عن الشبكة الداخلية هي {blank()}",
 f"تكديس الإجراءات الأمنية في طبقات متعددة يسمى {blank()}",
 f"النهج الذي لا يمنح الثقة تلقائيًا لمستخدم أو جهاز داخل الشبكة هو {blank()}",
 f"الحدود التقليدية التي تفترض أن «الداخل آمن» تسمى {blank()}",
 f"تستخدم الشبكة الافتراضية الخاصة عادةً التشفير و{blank()}",
 f"الاستخدامان الرئيسيان للشبكة الافتراضية الخاصة هما {blank(60)} و{blank(60)}",
 f"الطبقة الأولى في الدفاع في العمق هي {blank()}",
 f"الطبقة الرابعة في الدفاع في العمق هي {blank()}",
 f"في نهج انعدام الثقة تُفحص الهوية و{blank(55)} و{blank(55)} عند طلب الوصول",
 f"ما جعل الحدود بين «الداخل» و«الخارج» غير واضحة هو انتشار {blank(60)} و{blank(60)}",
]

# ---- صح وخطأ (من غير عبارات المثال المحلول)
TF = [
 "جدار الحماية يوجد عند حدود الشبكة فقط.",
 "تستخدم الشبكة الافتراضية الخاصة عادةً التشفير وتقنيات النفق لحماية البيانات بين الطرفين.",
 "من استخدامات الشبكة الافتراضية الخاصة الحذف التلقائي للملفات المصابة.",
 "يساعد فصل الخوادم العامة في منطقة معزولة على تقليل احتمال وصول الهجوم إلى الشبكة الداخلية.",
 "تثبيت مكافحة الفيروسات وتحديث نظام التشغيل ينتميان إلى طبقة مدخل الشبكة.",
 "في نهج انعدام الثقة تُفحص الهوية والصلاحيات والسياق عند طلب الوصول إلى الموارد.",
 "الوصول من داخل شبكة المؤسسة آمن، لذا فإن التحقق غير ضروري.",
 "مع انتشار السحابة والعمل عن بُعد، أصبحت التصاميم التي تحمي المحيط الأمني فقط غير كافية.",
 "في الأمان التقليدي، يُعد خارج شبكة المؤسسة آمنًا وداخلها خطرًا.",
 "من أمثلة قواعد جدار الحماية السماح بالوصول إلى خادم الويب مع منع الوصول الخارجي المباشر إلى قاعدة البيانات.",
 "تكديس الطبقات يمنع الاختراق منعًا مطلقًا.",
 "لا تكفي وسيلة حماية واحدة؛ فإذا فشلت قد تتعرض موارد أخرى للخطر.",
]

# ---- علّل
WHY = [
 "لا تكفي وسيلة حماية واحدة لحماية شبكة مؤسسة.",
 f"يُنصح باستخدام الشبكة الافتراضية الخاصة عند العمل من شبكة {nw('Wi-Fi')} عامة.",
 "لم تعد التصاميم التي تحمي المحيط الأمني وحده كافية.",
 "لا تُمنح الثقة لجهاز لمجرد أنه مملوك للمؤسسة أو موجود داخل الشبكة.",
 f"تظل طبقة الأجهزة الطرفية ضرورية رغم وجود جدار الحماية و{nw('VPN')} و{nw('DMZ')}.",
 f"يقول الكتاب إن {nw('DMZ')} «تساعد على تقليل احتمال» وصول الهجوم للداخل ولا يقول «تمنعه».",
 "تُعد قاعدة «السماح بالوصول إلى خادم الويب مع منع الوصول الخارجي المباشر إلى قاعدة البيانات» قاعدة جيدة.",
 "يجمع الكتاب بين الدفاع في العمق ونهج انعدام الثقة في الفكرة الرئيسة بدل الاكتفاء بواحد منهما.",
]
TQ_WHY = {1, 2, 3}

# ---- مقالي المذكرة (بعد الكارتين 01 و02) — (نص السؤال، عدد السطور، تقييمات؟)
ESS = [
 ("اذكر <b>الطبقات الأربع</b> للدفاع في العمق، ومثال إجراء واحد في كل طبقة، وما الذي تحميه.", 4, True),
 ("وضّح الفرق بين <b>الأمان التقليدي القائم على المحيط الأمني</b> و<b>نهج انعدام الثقة</b>، ولماذا تغيّر النهج.", 3, True),
 (f"مدرسة عندها موقع إلكتروني عام وسيرفر درجات ومدرسون يعملون من المنزل. اقترح <b>تصميمًا أمنيًا</b> يوضّح مكان كل خادم والإجراء المستخدم في كل طبقة، ثم حدّد <b>خطرًا واحدًا</b> يظل قائمًا.", 4, False),
]
TAQ_ESS = [   # أسئلة التقييمات الناقصة من البنك، بصياغتها (تصليح بسيط مكتوب في التقرير)
 ("وضّح الدور الأساسي لجدار الحماية (Firewall) في أمان الشبكات، واذكر مثالًا على كيفية تحكمه في حركة المرور وحماية قواعد البيانات.", 3),
 ("اذكر المقصود بـ«الشبكة الافتراضية الخاصة (VPN)» واثنين من استخداماتها الرئيسية، وبيّن كيف تحمي البيانات المنقولة عبر شبكات Wi-Fi العامة من التنصت.", 3),
 ("اشرح كيف تحمي «المنطقة المعزولة (DMZ)» شبكة المؤسسة الداخلية عند تعرض أحد خوادم الويب العامة للاختراق الهجومي الخارجي.", 3),
 ("وضّح كيف يساهم تطبيق «نهج انعدام الثقة (Zero Trust)» في التحقق من كل عملية وصول بناءً على الهوية والصلاحيات والسياق.", 3),
 ("اشرح كيف يتكامل كل من جدار الحماية، والشبكة الافتراضية الخاصة، والمنطقة المعزولة، وضوابط الأجهزة الطرفية لتشكيل استراتيجية «دفاع في العمق» متكاملة.", 4),
]

CLS_N = 9
N_ESS = 2 + len(ESS) + len(TAQ_ESS) + 3   # كارتين + المقالي + التقييمات + (توقّف وفكّر، فكّر وتحدَّ، اختبر فهمك)
N_TQ = len(TQ_MCQ) + len(TQ_WHY) + sum(1 for e in ESS if e[2]) + len(TAQ_ESS) + 1 + 1 + 1   # + كارت الكتاب 05 + جدول المقارنة 09 + توقّف وفكّر
stats = [(str(BOOK_N), "أسئلة الكتاب"), (str(len(MCQ)), "اختر"), (str(len(FILL)), "أكمل"), (str(len(TF)), "صح وخطأ"), (str(CLS_N), "تصنيف وقارن"), (str(len(WHY)), "علّل"), (str(N_ESS), "مقالي وأنشطة")]
A('<div class="qstats">' + "".join(f'<div><b class="num">{n}</b><span>{t}</span></div>' for n, t in stats) + f'<div><b class="num">{N_TQ}</b>{TQ}</div></div>')

A(cat("أسئلة الكتاب", stats[0][0]))
for c in BOOK: A(c)

A(cat("اختر الإجابة الصحيحة", str(len(MCQ))))
def mq(j): return f'<div class="mq"><div class="qq"><span class="k">{j+1}</span>{TQ if j+1 in TQ_MCQ else ""}<p>{MCQ[j][0]}</p></div>{opts(MCQ[j][1], 1 if max(len(o) for o in MCQ[j][1]) > 60 else 2)}</div>'
for i in range(0, len(MCQ), 2):
    A('<div class="mrow">' + "".join(mq(j) for j in range(i, min(i + 2, len(MCQ)))) + '</div>')

A(cat("أكمل", str(len(FILL))))
A(hint("اكتب المصطلح كامل وصحيح الإملاء. ولو المصطلح ليه اختصار إنجليزي، اكتبه جنبه كطريقة تساعدك تثبّت المصطلح.", label="ملحوظة").replace('class="hint"', 'class="hint kwn"', 1))
for i in range(0, len(FILL), 2):
    A('<div class="frow">' + "".join(f'<div><span class="k">{j+1}</span><p>{FILL[j]}</p></div>' for j in (i, i + 1)) + '</div>')

A(cat("صح وخطأ", str(len(TF))))
for i in range(0, len(TF), 3):
    A('<ul class="tfb">' + "".join(f'<li><span class="k">{j+1}</span><span class="t">{TF[j]}</span><span class="pr">(&nbsp;&nbsp;&nbsp;&nbsp;)</span></li>' for j in range(i, i + 3)) + '</ul>')

A(cat("تصنيف وقارن", str(CLS_N)))
A(card("01", "الإجراء ده في أنهي طبقة؟",
       instr(f"اكتب رقم الطبقة: <b>{num('1')}</b> مدخل الشبكة · <b>{num('2')}</b> مسار الاتصال · <b>{num('3')}</b> وضع الخوادم · <b>{num('4')}</b> الأجهزة الطرفية.")
       + classify(["قاعدة تمنع الوصول الخارجي المباشر لقاعدة البيانات", "تحديث نظام التشغيل على أجهزة الموظفين", "ربط فرعين بأمان عبر الإنترنت",
                   "وضع خادم البريد في منطقة منفصلة", "تشفير اتصال موظف يعمل من المنزل"])))
A(card("02", "طابق كل تعريف بالمصطلح",
       '<div class="match"><div class="mb"><h5>التعريف</h5><ol>'
       + "".join(f'<li><span>{t}</span>{AB}</li>' for t in [
           "منطقة للخوادم المواجهة للجمهور منفصلة عن الداخل", "التحقق من كل عملية وصول دون ثقة تلقائية",
           "يسمح بالاتصال أو يمنعه وفق قواعد محددة مسبقًا", "تكديس الإجراءات الأمنية في طبقات متعددة", "اتصال خاص مشفّر عبر شبكة عامة"])
       + '</ol></div><div class="mb"><h5>المصطلح</h5>' + opts(["جدار الحماية", "الشبكة الافتراضية الخاصة", "المنطقة المعزولة", "الدفاع في العمق", "نهج انعدام الثقة"], 1) + '</div></div>'))
A(card("03", "الخادم ده مكانه فين؟",
       instr("اكتب <b>د</b> لو مكانه <b>الشبكة الداخلية</b>، و<b>ع</b> لو مكانه <b>المنطقة المعزولة</b>.")
       + classify(["خادم الويب العام للمدرسة", "قاعدة بيانات درجات الطلاب", "خادم البريد الإلكتروني المواجه للجمهور", "ملفات شؤون الموظفين السرية"])))
A(card("04", "التهديد والإجراء",
       instr(f"اكتب الإجراء الأنسب: <b>جدار الحماية</b> · <b>{nw('VPN')}</b> · <b>{nw('DMZ')}</b> · <b>ضوابط الأجهزة الطرفية</b>.")
       + classify([f"موظف يتصل بشبكة المؤسسة من كافيه على {nw('Wi-Fi')} عامة", "محاولة اتصال غير مصرح به من الخارج بقاعدة البيانات",
                   "اختراق خادم الويب العام قد يمتد للشبكة الداخلية", "ملف مصاب فُتح على جهاز موظف"], w=True)))
A(card("05", "الدفاع في العمق ولا انعدام الثقة؟",
       instr("اكتب <b>ع</b> لو الوصف عن <b>الدفاع في العمق</b>، و<b>ث</b> لو عن <b>نهج انعدام الثقة</b>.")
       + classify(["لو فشلت طبقة، الباقي يقلل الخطر", "لا ثقة بسبب الموقع داخل الشبكة", "تُفحص الهوية والصلاحيات والسياق", "تكديس الإجراءات في أربع طبقات"])))
A(card("06", f"قارن بين جدار الحماية والمنطقة المعزولة {en('(DMZ)')}", cmp_table(["وجه المقارنة", "جدار الحماية", f"المنطقة المعزولة {en('(DMZ)')}"], ["النوع", "الوظيفة"], tall=True)))
A(card("07", "قارن بين الشبكة الافتراضية الخاصة وضوابط الأجهزة الطرفية", cmp_table(["وجه المقارنة", "الشبكة الافتراضية الخاصة", "ضوابط الأجهزة الطرفية"], ["الطبقة", "ما الذي تحميه"], tall=True)))
A(card("08", "قارن بين الدفاع في العمق ونهج انعدام الثقة", cmp_table(["وجه المقارنة", "الدفاع في العمق", "نهج انعدام الثقة"], ["الفكرة", "المشكلة التي يعالجها"], tall=True)))
A(card("09", "قارن بين الأمان التقليدي ونهج انعدام الثقة", cmp_table(["وجه المقارنة", "الأمان التقليدي (المحيط)", "نهج انعدام الثقة"], ["أساس منح الثقة", "لماذا تغيّر"], tall=True), tag=TQ))

A(cat("علّل", str(len(WHY))))
for k, t in enumerate(WHY):
    A(f'<div class="why split"><div class="qq"><span class="k">{k+1}</span>{TQ if k+1 in TQ_WHY else ""}<p>{t}</p></div>{lines(2)}</div>')

# ---- مقالي وأنشطة (من غير عنوان)
A(card("01", "طبّق ما تعلمته — سجلات المستشفى على السحابة",
       '<p class="qs">ينقل مستشفى سجلات مرضاه إلى خدمة سحابية ويسمح للأطباء بالوصول إليها من المنزل. باستخدام نهج انعدام الثقة والدفاع في العمق، <b>اقترح إجراءين</b> ينبغي تطبيقهما <b>وبيّن أين يساعد كل منهما</b>، ثم <b>حدّد خطرًا واحدًا قد يظل قائمًا</b>.</p>'
       + hint("<b>إجراءان بالاسم</b> · <b>أين</b> يساعد كل واحد بالتحديد · <b>خطر يظل قائمًا</b> – لأن الطبقات <b>تقلل</b> الخطر ولا تمنعه منعًا مطلقًا.") + lines(5)))
A(card("02", "فكّر كمهندس — ابحث ثم قرر",
       '<p class="qs">تقوم شركة في مدينتك بإعداد شبكة مكتبها. لديها <b>موقع إلكتروني عام</b>، و<b>موظفون يعملون من المنزل</b>، و<b>بيانات عملاء سرية</b>. أنت تقدم المشورة بشأن تصميم الأمان.</p>'
       + '<p class="qs"><b>(1) اجمع البيانات.</b> اذكر أصول الشركة الثلاثة (الموقع الإلكتروني العام، الموظفون عن بُعد، قاعدة بيانات العملاء) والتهديد الرئيسي لكل منها.</p>'
       + cmp_table(["الأصل", "التهديد الرئيسي"], ["الموقع الإلكتروني العام", "الموظفون عن بُعد", "قاعدة بيانات العملاء"])
       + '<p class="qs"><b>(2) اربط وحلّل.</b> اربط كل أصل أو تهديد في هذه الشركة بطبقة الحماية الأكثر ارتباطًا به (مدخل الشبكة، مسار الاتصال، وضع الخوادم، الأجهزة الطرفية). ثم اختر طبقة واحدة يكون فشلها شديد الأثر في هذا السيناريو، وفسّر لماذا لا تكفي وحدها.</p>' + lines(3)))
A(card("", "",
       '<p class="qs"><b>(3) قرّر.</b> أوصِ بتصميم وقدّم سببين يوضحان لماذا يكون التكديس أكثر أمانًا من جدار حماية واحد. <b>في أزواج</b>، قارنا تصميماتكما واتفقا معًا على أقوى سبب قبل تدوينه.</p>'
       + f'<p class="chx"><span>☐ جدار حماية فقط</span><span>☐ تصميم متعدد الطبقات (جدار حماية + شبكة افتراضية خاصة + المنطقة المعزولة {en("(DMZ)")} + أجهزة طرفية) يتحقق أيضًا من كل عملية وصول (نهج انعدام الثقة)</span></p>'
       + '<p class="qs"><b>قدّم دليلًا على إجابتك.</b></p>' + lines(3)
       + hint("تلميح الكتاب: <b>ضع الخادم العام في المنطقة المعزولة لتقليل احتمال وصول المهاجم إلى الشبكة الداخلية إذا اختُرق الخادم، ولا تعتمد على العزل وحده.</b> ولاحظ إن السؤال طالب <b>بدليل</b> على إجابتك.")))
for k, (t, n, b) in enumerate(ESS):
    A(f'<div class="why ess split"><div class="qq"><span class="k">{k+3}</span>{TQ if b else ""}<p>{t}</p></div>{lines(n)}</div>')
for k, (t, n) in enumerate(TAQ_ESS, start=3 + len(ESS)):
    for a in ["(Firewall)", "(VPN)", "(DMZ)", "(Zero Trust)"]: t = t.replace(a, en(a))
    t = t.replace("Wi-Fi", nw("Wi-Fi"))
    A(f'<div class="why split"><div class="qq"><span class="k">{k}</span>{TQ}<p>{t}</p></div>{lines(n)}</div>')
T0 = 3 + len(ESS) + len(TAQ_ESS)
A(f'<div class="why split"><div class="qq"><span class="k">{T0}</span>{TQ}<p><b>توقّف وفكّر:</b> لماذا يكون وضع خادم ويب عام في المنطقة المعزولة {en("(DMZ)")} أكثر أمانًا من وضعه داخل الشبكة الداخلية؟</p></div>{lines(2)}</div>')
A(f'<div class="why split"><div class="qq"><span class="k">{T0 + 1}</span><p><b>فكّر وتحدَّ – تأمّل:</b> ما الطبقة الدفاعية التي تعتقد أنها الأسهل على المهاجم لتجاوزها، ولماذا؟ · <b>وتحدَّ:</b> اقترح إجراءً واحدًا يمكن لشركة صغيرة إضافته بجانب جدار الحماية، وتهديدًا واحدًا سيظل غير مزال.</p></div>{lines(3)}</div>')
A(f'<div class="why split"><div class="qq"><span class="k">{T0 + 2}</span><p><b>اختبر فهمك:</b> أجب عن أسئلة هذا البنك <b>دون الرجوع</b> إلى الشرح، ثم راجع إجاباتك.</p></div>{lines(1)}</div>')
assert T0 + 2 == N_ESS

EXTRA_CSS = """
/* ---------- إضافات الدرس 2-2 (مبنية على 2-1) ---------- */
.banner{text-wrap:pretty}
.quote,.note-line,.box p,.box li,.stg p,.hf .hs p{text-wrap:pretty}
.intro .body p+p{margin-top:4pt}
.map .cell li{text-wrap:pretty}
.map.m2 .cell h4{display:flex;align-items:flex-start;gap:5pt;line-height:1.4;margin-bottom:2pt}
.map.m2 .cell h4 .mn{flex:none;display:inline-flex;align-items:center;justify-content:center;width:13pt;height:13pt;border-radius:50%;background:var(--navy2);color:#fff;font-size:7.8pt;font-weight:800;margin-top:1.5pt}
.map.m2{grid-template-columns:1fr 104pt 1fr;column-gap:15pt}
.map.m2 .hub{font-size:10.4pt;padding:6pt 6pt}
.nw{white-space:nowrap}
.box.plain{background:#f5f7fb;border-color:#dde5ef} .box.plain h3{color:var(--navy)}
.box.plain p{text-wrap:pretty}
.cmpw{position:relative}
/* مراحل اتصال HTTPS (جدول الكتاب ككروت) */
.stg{display:flex;flex-direction:column;gap:6pt;margin:0 0 4pt 0}
.stg .sh{display:grid;grid-template-columns:1fr 112pt;gap:10pt;padding:0 11pt 0 11pt;font-weight:700;font-size:8.6pt;color:var(--muted);line-height:1.3}
.stg .sh span:first-child{padding-right:30pt}
.stg .sh span:last-child{text-align:center}
.stg .sc{display:grid;grid-template-columns:20pt 1fr 112pt;align-items:center;gap:10pt;background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:9pt;padding:7pt 11pt}
.stg .sn{width:20pt;height:20pt;border-radius:50%;background:#e29433;color:#fff;font-weight:800;font-size:10.5pt;display:flex;align-items:center;justify-content:center;line-height:1}
.stg h4{margin:0 0 1pt 0;font-weight:800;font-size:10.6pt;color:var(--navy);line-height:1.4}
.stg p{font-size:9.7pt;line-height:15pt;color:var(--text2)}
.stg p b{color:var(--navy2)}
.stg .mc{align-self:stretch;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2pt;text-align:center;background:#fff;border:.75pt solid #dde5ef;border-radius:8pt;padding:4pt 6pt}
.stg .mc svg{width:22pt;height:22pt}
.stg .mc b{font-size:9.6pt;font-weight:800;line-height:1.35}
.stg .mc.pk b{color:#2e4a78} .stg .mc.sy b{color:#a9670f}
.stg .mc.sy{background:#fbf6e8;border-color:#eee0b8}
/* شكل الكتاب: تدفق اتصال HTTPS */
.hf{padding-top:9pt}
.hf .hfh{display:flex;justify-content:space-between}
.hf .nd{width:150pt;border-radius:8pt;text-align:center;padding:4pt 6pt 5pt 6pt;line-height:1.3}
.hf .nd b{display:block;font-weight:800;font-size:11pt}
.hf .nd small{display:block;font-size:8.2pt;font-weight:600}
.hf .nd.b{background:#fff;border:1.2pt solid #22375c} .hf .nd.b b{color:var(--navy)} .hf .nd.b small{color:var(--muted)}
.hf .nd.s{background:#22375c;border:1.2pt solid #22375c} .hf .nd.s b{color:#fff} .hf .nd.s small{color:#c9d6e6}
.hf .hfb{position:relative;padding:8pt 0 6pt 0}
.hf .hfb::before,.hf .hfb::after{content:'';position:absolute;top:0;bottom:0;width:0;border-left:1.2pt dashed #b9c6d8}
.hf .hfb::before{right:75pt} .hf .hfb::after{left:75pt}
.hf .hs{margin:0 75pt;position:relative}
.hf .hs+.hs{margin-top:9pt}
.hf .hs .pl{display:flex;justify-content:center;margin-bottom:4pt}
.hf .hs .pl span{display:inline-flex;align-items:center;gap:5pt;background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:9pt;padding:0 10pt 0 8pt;font-weight:800;font-size:9.4pt;line-height:17pt;color:var(--navy)}
.hf .hs .pl i{font-style:normal;flex:none;width:13pt;height:13pt;border-radius:50%;background:#e29433;color:#fff;font-size:8pt;display:inline-flex;align-items:center;justify-content:center;line-height:1}
.hf .ar{position:relative;height:10pt}
.hf .ar::before{content:'';position:absolute;left:0;right:0;top:4.2pt;border-top:1.6pt solid #22375c}
.hf .ar i{position:absolute;top:0;width:0;height:0;border-top:5pt solid transparent;border-bottom:5pt solid transparent}
.hf .ar .hr{right:-1pt;border-left:9pt solid #22375c}
.hf .ar .hl{left:-1pt;border-right:9pt solid #22375c}
.hf .ar.g::before{border-top-color:#e29433} .hf .ar.g .hr{border-left-color:#e29433} .hf .ar.g .hl{border-right-color:#e29433}
.hf .hs p{text-align:center;font-size:9.3pt;line-height:14pt;color:var(--text2);margin-top:3pt;padding:0 6pt}
.hf .hff{background:#eef2f8;border-radius:7pt;text-align:center;font-size:8.8pt;line-height:13.5pt;color:var(--text2);padding:3pt 10pt}
.hf .hff b{color:var(--navy2)}
/* صورة من الكتاب جنب نص */
.sf{display:grid;grid-template-columns:1fr 200pt;gap:12pt;align-items:center;margin:0 0 9pt 0}
.sf .quote{margin:0}
.im{background:#fff;border:.75pt solid #dde5ef;border-radius:9pt;padding:5pt 5pt 0 5pt}
.im img{display:block;width:100%;height:auto;border-radius:6pt}
.im .icap{margin:4pt 2pt 4pt 2pt;text-wrap:pretty}
/* المفتاح العام × المتماثل */
.kp .kg{display:grid;grid-template-columns:1fr 1fr;gap:10pt}
.kp .kc{display:flex;align-items:center;gap:10pt;border-radius:9pt;padding:8pt 11pt;border:.75pt solid #dde5ef;background:#f5f7fb}
.kp .kc.sy{background:#fbf6e8;border-color:#eee0b8}
.kp .kc .ic{flex:none;display:flex;flex-direction:column;align-items:center;gap:1pt;width:38pt}
.kp .kc .ic svg{width:34pt;height:17pt}
.kp .kt{flex:1}
.kp h4{margin:0 0 2pt 0;font-weight:800;font-size:11pt;color:var(--navy);line-height:1.35}
.kp .kc.sy h4{color:#a9670f}
.kp p{font-size:9.4pt;line-height:14.2pt;color:var(--text2)}
.kp .tg{flex:none;font-weight:800;font-size:8.6pt;border-radius:7pt;padding:0 8pt;line-height:15pt;background:#fff;border:.75pt solid #dde5ef;color:#2e4a78}
.kp .kc.sy .tg{border-color:#eee0b8;color:#a9670f}
/* فئات عوامل المصادقة */
.fac .fg3{display:grid;grid-template-columns:repeat(3,1fr);gap:9pt}
.fac .fc{display:flex;flex-direction:column;align-items:center;text-align:center;background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:9pt;padding:7pt 8pt 7pt 8pt}
.fac .fc .ic{width:34pt;height:34pt;border-radius:50%;background:#fff;border:.75pt solid #dde5ef;display:flex;align-items:center;justify-content:center;margin-bottom:3pt}
.fac .fc .ic svg{width:20pt;height:20pt}
.fac h4{margin:0;font-weight:800;font-size:11.4pt;color:var(--navy);line-height:1.35}
.fac .fc p{font-size:9.4pt;line-height:14pt;color:var(--text2);margin-top:1pt}
.fac .fc small{flex:1;font-size:8.8pt;line-height:13.4pt;color:var(--muted);margin:2pt 0 4pt 0}
.fac .tg{font-weight:800;font-size:8.4pt;color:#a9670f;background:#fff;border:.75pt solid #eee0b8;border-radius:7pt;padding:0 9pt;line-height:14pt}
.fac .fn{margin-top:7pt;padding:4pt 10pt;border-radius:7pt;background:#fbf6e8;border-right:3pt solid #e29433;font-size:9.2pt;line-height:14.2pt;color:var(--text2);text-wrap:pretty}
.fac .fn b{color:var(--navy2)}
/* جدول الخدمات */
table.svt td{vertical-align:middle}
table.svt td.k{white-space:normal}
.fk{font-size:8.8pt;font-weight:700}
.fk.f1{color:#a9670f} .fk.f2{color:#2e4a78} .fk.f3{color:#6e7f9c}
/* جدول التقنيات والتأثير + صورة الشهادة */
.tx{display:grid;grid-template-columns:1fr 150pt;gap:12pt;align-items:center;margin:0 0 9pt 0}
.tx .tl{border:.75pt solid #dde5ef;border-radius:9pt;overflow:hidden;background:#fff}
.tx .th{display:grid;grid-template-columns:132pt 1fr;background:#eef2f8;font-weight:800;font-size:9.6pt;color:var(--navy);line-height:1.5}
.tx .th span{padding:3pt 10pt}
.tx .tr{display:grid;grid-template-columns:132pt 1fr;border-top:.75pt solid #e3e9f1}
.tx .tn{display:flex;align-items:center;gap:7pt;padding:6pt 9pt;background:#f5f7fb;border-left:.75pt solid #e3e9f1}
.tx .tn .ic{flex:none;width:26pt;height:26pt;border-radius:50%;background:#fff;border:.75pt solid #dde5ef;display:flex;align-items:center;justify-content:center}
.tx .tn .ic svg{width:15pt;height:15pt}
.tx .tn b{display:block;font-weight:800;font-size:10pt;color:var(--navy);line-height:1.35}
.tx .tn small{display:block;font-size:7.8pt;line-height:11pt;color:var(--muted);font-weight:600}
.tx .te{display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:3pt;padding:6pt 10pt}
.tx .te p{font-size:9.4pt;line-height:14.2pt;color:var(--text2);text-wrap:pretty}
.tx .te p b{color:var(--navy2)}
.tx .tg{font-weight:700;font-size:8pt;color:#a9670f;background:#fbf6e8;border:.75pt solid #eee0b8;border-radius:6pt;padding:0 7pt;line-height:13pt}
.tx .txs{background:#fbf6e8;border-top:.75pt solid #eee0b8;padding:3pt 10pt;font-size:9pt;line-height:14pt;color:var(--text2)}
.tx .txs .fx{margin:0 0 0 6pt}
.tx .txs em,.tx .px em{font-style:normal;font-weight:800;color:#a9670f}
.tx .te .px{align-self:stretch;margin-top:2pt;padding-top:3pt;border-top:.75pt dashed #dde5ef;font-size:8.9pt;line-height:13.4pt;color:var(--text);text-wrap:pretty}
.exs{position:relative;background:#fbfcfe;border:.75pt dashed #e2c48f;border-radius:9pt;padding:5pt 12pt;margin:5pt 0 7pt 0;font-size:9.6pt;line-height:15pt;color:var(--text);text-wrap:pretty}
.exs .eh{font-weight:800;color:#a9670f;margin-left:5pt}
.exs b{color:var(--navy)}
/* التهديد ← التقنية */
.thr{padding-top:10pt}
.thr .th2{display:flex;align-items:center;justify-content:center;gap:8pt;margin-bottom:6pt;font-weight:800;font-size:10pt;line-height:1.35}
.thr .th2 .a{color:#a9670f} .thr .th2 .b{color:var(--navy)}
.thr .tgr{display:grid;grid-template-columns:1fr 1fr;gap:6pt 16pt}
.thr .trw{display:grid;grid-template-columns:1.15fr 30pt 1fr;align-items:stretch}
.thr .t1,.thr .t2{display:flex;align-items:center;justify-content:center;border-radius:8pt;padding:3pt 8pt;text-align:center;font-size:9.6pt;line-height:13.6pt;text-wrap:pretty}
.thr .t1{background:#fbf6e8;border:.75pt solid #eee0b8;color:var(--text2)}
.thr .t2{background:#f5f7fb;border:.75pt solid #dde5ef;color:var(--navy);font-weight:800}
.thr .ar{display:flex;align-items:center;justify-content:center}
.thr .ar svg{width:24pt;height:9pt}
/* بنك */
.match ol.la{list-style:none;padding:0}
.match ol.la li{display:flex;align-items:center;gap:6pt}
.match ol.la li b{flex:none;display:inline-flex;align-items:center;justify-content:center;width:15pt;height:15pt;border-radius:50%;background:#eef2f8;border:.75pt solid #dde5ef;font-weight:800;font-size:8.2pt;color:var(--navy2);line-height:1;margin-top:0}
.match ol.la li span:not(.ab){flex:1;margin-left:0}
.match ol.la li .ab{margin-top:0}
.qs.rd{background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:7pt;padding:5pt 10pt;text-wrap:pretty}
/* ---------- جديد في 2-2 ---------- */
.banner .bx{display:block;margin-top:2pt;font-style:italic;font-weight:600;opacity:.92}
.cn{flex:none;display:inline-flex;align-items:center;justify-content:center;width:15pt;height:15pt;border-radius:50%;background:#e29433;color:#fff;font-weight:800;font-size:8.4pt;line-height:1}
.lar{font-style:normal;display:flex;align-items:center;justify-content:center}
.lar svg{width:22pt;height:10pt}
.dyh{font-weight:800;font-size:10.6pt;color:var(--navy);margin:0 0 7pt 0;line-height:1.5}
.dyh b{color:#a9670f}
.rcl{display:flex;align-items:center;gap:10pt;background:#22375c;border-radius:10pt;padding:7pt 12pt;margin:0 0 10pt 0}
.rcl .rl{flex:none;background:#e29433;color:#17263f;font-weight:800;font-size:9.6pt;line-height:18pt;padding:0 11pt;border-radius:8pt}
.rcl .rc{flex:1;display:flex;align-items:center;justify-content:center;gap:8pt;flex-wrap:wrap}
.rcl .rc span{background:#2e4a78;border:.75pt solid #4a6fa5;border-radius:8pt;padding:1pt 12pt;color:#fff;font-weight:800;font-size:10.2pt;line-height:17pt}
.rcl .rc i{font-style:normal;color:#f1c88b;font-weight:800}
figure.bimg{margin:0 auto 9pt auto;width:55%;background:#fff;border:.75pt solid #dde5ef;border-radius:9pt;padding:5pt 5pt 0 5pt}
figure.bimg img{display:block;width:100%;height:auto;border-radius:6pt}
figure.bimg .icap{margin:4pt 2pt 5pt 2pt;text-align:center}
/* جدار الحماية: قواعد المثال + الصورة */
.fwx{display:grid;grid-template-columns:1fr 215pt;gap:12pt;align-items:center;margin:0 0 9pt 0}
.fwx .fig{margin:0}
.fwr{padding-top:10pt}
.fwh{font-weight:800;font-size:10.4pt;color:var(--navy);margin-bottom:6pt}
.fr{display:grid;grid-template-columns:1fr 30pt 1fr 62pt;align-items:center;gap:6pt;margin-bottom:6pt}
.fr .a{display:flex;align-items:center;gap:6pt;background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:8pt;padding:5pt 8pt}
.fr .a svg{flex:none;width:17pt;height:17pt}
.fr .a b{font-weight:800;font-size:9.4pt;color:var(--navy);line-height:1.35}
.fr .w{display:flex;justify-content:center}
.fr .w svg{width:24pt;height:24pt}
.fr .st{display:flex;align-items:center;justify-content:center;gap:4pt;border-radius:8pt;font-weight:800;font-size:9.4pt;color:#fff;line-height:22pt}
.fr .st svg{width:12pt;height:12pt}
.fr.ok .st{background:#2e7d5b} .fr.no .st{background:#a33a30}
.fr.no .a:last-of-type{border-color:#efc6c1;background:#fbeceb}
.fwp{display:flex;align-items:center;flex-wrap:wrap;gap:5pt;margin-top:3pt;padding-top:6pt;border-top:.75pt dashed #dde5ef}
.fwp span{background:#fff;border:.75pt solid #dde5ef;border-radius:8pt;padding:0 9pt;font-weight:700;font-size:9pt;color:var(--navy);line-height:17pt}
.fwp .pl{background:#fbf6e8;border-color:#eee0b8;color:#a9670f}
/* VPN */
.vpu{padding-top:10pt}
.vu2{display:grid;grid-template-columns:1fr 1fr;gap:10pt}
.vc{background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:9pt;padding:6pt 9pt 8pt 9pt}
.vc h5{display:flex;align-items:center;gap:6pt;margin:0 0 6pt 0;font-weight:800;font-size:10.4pt;color:var(--navy)}
.tn{display:grid;grid-template-columns:62pt 1fr 62pt;align-items:center;gap:4pt}
.tn .e{display:flex;flex-direction:column;align-items:center;gap:2pt;text-align:center}
.tn .e svg{width:24pt;height:24pt}
.tn .e b{font-weight:700;font-size:8.6pt;line-height:1.3;color:var(--navy)}
.tn .tb{position:relative;display:flex;align-items:center}
.tn .tb i{flex:1;height:0;border-top:1.6pt dashed #e29433}
.tn .tb em{flex:none;display:flex;align-items:center;gap:3pt;font-style:normal;background:#fbf6e8;border:1.2pt solid #e29433;border-radius:11pt;padding:1pt 8pt;font-weight:800;font-size:8.4pt;color:#a9670f;line-height:15pt}
.tn .tb em svg{width:11pt;height:11pt}
.vw{display:grid;grid-template-columns:1fr 1fr;gap:10pt;margin-top:8pt}
.vb{border-radius:9pt;padding:5pt 10pt;background:#fbeceb;border:.75pt solid #efc6c1}
.vb.g{background:#eaf5ef;border-color:#b9dcc9}
.vb .vl{display:flex;align-items:center;gap:5pt;font-weight:800;font-size:9.4pt;color:#a33a30;line-height:1.5}
.vb.g .vl{color:#2e7d5b}
.vb .vl svg{width:15pt;height:15pt}
.vb p{font-size:9.4pt;line-height:14pt;color:var(--text2)}
/* شكل الكتاب: تكوين DMZ */
.dmz{padding-top:9pt}
.dzh{text-align:center;font-weight:800;font-size:11pt;color:var(--navy);margin-bottom:8pt}
.dz{display:grid;grid-template-columns:1fr 34pt 1.25fr 34pt 1fr;align-items:stretch;gap:5pt}
.zc{border-radius:10pt;padding:6pt 7pt 8pt 7pt;display:flex;flex-direction:column;align-items:center;gap:6pt}
.zc h5{margin:0;text-align:center;font-weight:800;font-size:10.2pt;color:var(--navy);line-height:1.3}
.zc h5 small{display:block;font-weight:600;font-size:8.2pt;color:var(--muted)}
.zc.ext{background:#fbf6e8;border:.75pt solid #eee0b8}
.zc.dmzz{background:#fff;border:1.4pt dashed #a9670f}
.zc.int{background:#eef4fb;border:.75pt solid #c9d6e6}
.dr{display:flex;gap:6pt;justify-content:center;flex-wrap:wrap}
.dn{display:flex;flex-direction:column;align-items:center;gap:2pt;background:#fff;border:.75pt solid #dde5ef;border-radius:8pt;padding:5pt 6pt;min-width:54pt;text-align:center}
.dn svg{width:20pt;height:20pt}
.dn span{font-weight:700;font-size:8.2pt;line-height:1.3;color:var(--navy)}
.zx{text-align:center;background:#f5f7fb;border-radius:7pt;padding:3pt 8pt;line-height:1.35}
.zx b{display:block;font-weight:800;font-size:9pt;color:var(--navy)}
.zx small{display:block;font-size:8pt;color:var(--muted)}
.zx.s{background:#22375c} .zx.s b{color:#fff}
.fw{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4pt;background:#22375c;border-radius:6pt;padding:6pt 0}
.fw i svg{width:18pt;height:18pt}
.fw>span:not(.lbn){writing-mode:vertical-rl;transform:rotate(180deg);color:#fff;font-weight:800;font-size:8.4pt;letter-spacing:.3pt}
.dzf{margin-top:8pt;text-align:center;font-weight:800;font-size:9.4pt;color:var(--navy2);background:#eef2f8;border-radius:7pt;padding:3pt 10pt}
.bnk{padding-top:10pt}
.bnk .zc,.bnk .fw{position:relative}
.lbn{position:absolute;top:-7pt;right:-6pt;width:16pt;height:16pt;border-radius:50%;background:#e29433;color:#fff;font-weight:800;font-size:8.6pt;display:flex;align-items:center;justify-content:center;line-height:1;z-index:2;border:1.2pt solid #fff}
.bnk .fw .lbn{right:auto;left:50%;margin-left:-8pt;top:-9pt;writing-mode:horizontal-tb;transform:none;letter-spacing:0}
.bnk .dz{grid-template-columns:1.35fr 34pt 1fr 34pt 1fr}
.bnk .dn{min-width:48pt;padding:4pt 5pt}
.dn.ep{position:relative}
.dn small{font-size:7.8pt;color:#2e7d5b;font-weight:700;line-height:1.3}
.vtn{position:relative;display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:6pt;margin-top:9pt;background:#fbf6e8;border:.75pt solid #eee0b8;border-radius:9pt;padding:6pt 12pt}
.vtn .e{display:flex;align-items:center;gap:4pt;font-weight:700;font-size:8.8pt;color:var(--navy)}
.vtn .e svg{width:16pt;height:16pt}
.vtn .tb{display:flex;align-items:center}
.vtn .tb i{flex:1;height:0;border-top:1.6pt dashed #e29433}
.vtn .tb em{flex:none;display:flex;align-items:center;gap:3pt;font-style:normal;background:#fff;border:1.2pt solid #e29433;border-radius:11pt;padding:1pt 8pt;font-weight:800;font-size:8.6pt;color:#a9670f;line-height:15pt}
.vtn .tb em svg{width:11pt;height:11pt}
.vtn>.lbn{top:-8pt;right:-6pt}
.per{padding-top:10pt}
.pr2{display:grid;grid-template-columns:1fr 30pt 1fr;align-items:stretch}
.per .pc{display:flex;flex-direction:column;gap:6pt;background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:9pt;padding:6pt 9pt 7pt 9pt}
.per .pc.now{background:#fbf6e8;border-color:#eee0b8}
.per h5{margin:0;font-weight:800;font-size:10.2pt;color:var(--navy);text-align:center}
.per .pc.now h5{color:#a9670f}
.pw{position:relative;display:flex;justify-content:center;gap:6pt;border:2.2pt solid #22375c;border-radius:10pt;padding:14pt 6pt 6pt 6pt;background:#fff}
.pw.dash{border-style:dashed;border-color:#6e7f9c}
.pw .pt{position:absolute;top:-8pt;right:10pt;background:#22375c;color:#fff;font-weight:800;font-size:8.2pt;border-radius:6pt;padding:0 7pt;line-height:14pt}
.pw.dash .pt{background:#6e7f9c}
.po{display:flex;justify-content:center;gap:6pt}
.pm{display:flex;flex-direction:column;align-items:center;gap:2pt;text-align:center;min-width:58pt;padding:3pt 5pt;border-radius:7pt}
.pm svg{width:20pt;height:20pt}
.pm span{font-weight:700;font-size:8.4pt;line-height:1.3;color:var(--navy)}
.pm.out{background:#fff;border:1.2pt dashed #e29433}
.pm.out span{color:#a9670f}
.per .pc p{font-size:9.2pt;line-height:14pt;color:var(--text2);text-align:center;text-wrap:pretty}
.per .pc p b{color:var(--navy2)}
/* جدول الطبقات + لو حاجة فشلت */
table.lyt td.k{white-space:nowrap}
.flx{padding-top:10pt}
.flc,.flr{display:grid;grid-template-columns:1fr 30pt 1fr;align-items:stretch;gap:0}
.flc span{font-weight:800;font-size:8.8pt;color:var(--muted);text-align:center;padding-bottom:3pt}
.flr+.flr{margin-top:6pt}
.flr .f1,.flr .f2{display:flex;align-items:center;gap:7pt;border-radius:8pt;padding:5pt 9pt}
.flr .f1{background:#fbeceb;border:.75pt solid #efc6c1}
.flr .f2{background:#eaf5ef;border:.75pt solid #b9dcc9}
.flr svg{flex:none;width:18pt;height:18pt}
.flr p{font-size:9.4pt;line-height:14pt;color:var(--text);text-wrap:pretty}
/* شكل الكتاب: الأمان التقليدي × انعدام الثقة */
.ztf{padding-top:9pt}
.zt2{display:grid;grid-template-columns:1fr 1fr;gap:12pt;align-items:stretch}
.zs{display:flex;flex-direction:column;gap:5pt}
.zs h5{margin:0;text-align:center;font-weight:800;font-size:10pt;color:#fff;border-radius:6pt;line-height:19pt}
.zs.zero h5{background:#22375c} .zs.trad h5{background:#6e7f9c}
.zb{flex:1;border-radius:9pt;padding:6pt 7pt;display:flex;flex-direction:column;align-items:center;gap:5pt}
.zs.zero .zb{background:#f5f7fb;border:1.3pt dashed #22375c}
.zb.o{background:#fff;border:.75pt solid #c9d3e0} .zb.i{background:#f5f7fb;border:.75pt solid #c9d3e0}
.zl{text-align:center;font-weight:800;font-size:9.4pt;color:var(--navy);line-height:1.35}
.zl small{display:block;font-weight:600;font-size:8.2pt;color:var(--muted)}
.zr{display:flex;gap:6pt;justify-content:center;flex-wrap:wrap}
.zp{position:relative;display:flex;flex-direction:column;align-items:center;gap:2pt;background:#fff;border:.75pt solid #dde5ef;border-radius:8pt;padding:5pt 6pt;min-width:52pt;text-align:center}
.zp svg{width:19pt;height:19pt}
.zp span{font-weight:700;font-size:8.2pt;line-height:1.3;color:var(--navy)}
.zp i{position:absolute;top:-6pt;left:-6pt;width:15pt;height:15pt;border-radius:50%;background:#e29433;display:flex;align-items:center;justify-content:center}
.zp i svg{width:10pt;height:10pt}
.zv{font-weight:800;font-size:9.2pt;color:#a9670f}
.zfw{text-align:center;background:#22375c;color:#fff;font-weight:800;font-size:8.8pt;border-radius:5pt;line-height:16pt}
/* انعدام الثقة: 3 فحوصات */
.ztc{padding-top:10pt}
.zc3{display:grid;grid-template-columns:repeat(3,1fr);gap:9pt}
.zc3>div{display:flex;flex-direction:column;align-items:center;text-align:center;background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:9pt;padding:7pt 8pt}
.zc3 .zi{width:32pt;height:32pt;border-radius:50%;background:#fff;border:.75pt solid #dde5ef;display:flex;align-items:center;justify-content:center;margin-bottom:3pt}
.zc3 .zi svg{width:18pt;height:18pt}
.zc3 h5{margin:0;font-weight:800;font-size:10.8pt;color:var(--navy)}
.zc3 small{font-size:9pt;color:#a9670f;font-weight:700;line-height:1.5}
.zc3 p{margin-top:4pt;padding-top:4pt;border-top:.75pt dashed #dde5ef;font-size:9pt;line-height:13.6pt;color:var(--text);text-wrap:pretty}
.zc3 p em{font-style:normal;font-weight:800;color:#a9670f}
.zcf{margin-top:8pt;background:#eef2f8;border-radius:7pt;padding:4pt 10pt;text-align:center;font-size:9.2pt;line-height:14pt;color:var(--text2)}
.zcf b{color:var(--navy2)}
"""

body = (f'<body data-lesson="الدرس 2-2 — {TITLE}" data-start="{START}" data-total="{TOTAL}">\n<main class="flow">\n'
        + group_html("\n".join(E)) + "\n\n<!-- ===================== بنك الأسئلة ===================== -->\n" + "\n".join(B)
        + "\n</main>\n</body>\n</html>\n")
out = head.replace("</style>", EXTRA_CSS + FLAG_CSS + "</style>", 1) + body
out = out.replace("(el.firstElementChild && el.firstElementChild.tagName === 'H4')", "(el.firstElementChild && /^H[34]$/.test(el.firstElementChild.tagName))")
open(BASE + "lesson_2_2.html", "w", encoding="utf-8").write(out)
print("written", len(out), "| book", BOOK_N, "| mcq", len(MCQ), "| fill", len(FILL), "| tf", len(TF), "| why", len(WHY), "| ess", N_ESS, "| tq", N_TQ)
