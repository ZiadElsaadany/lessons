# -*- coding: utf-8 -*-
"""الأقسام الجديدة للدرس 3-1 (تصميمات زياد 24 سبتمبر) — كل الأسهم RTL."""

NAVY = "#17263f"; BLUE = "#1f6fb8"; BLUE2 = "#2f7fd0"; ORANGE = "#e8801c"; PURPLE = "#6f5bc9"; GREEN = "#2e9a62"
GREEN2 = "#1f7a4d"; RED = "#c0392b"; GRAY = "#5b6b82"

# ---------------- أيقونات ----------------
def user(c=BLUE2):
    return f'<svg viewBox="0 0 24 24"><circle cx="12" cy="7.2" r="4.6" fill="{c}"/><path d="M3.2 21.5c0-5 3.9-8.4 8.8-8.4s8.8 3.4 8.8 8.4z" fill="{c}"/></svg>'

def browser(c=BLUE2, inner="text"):
    ins = {
        "text": f'<line x1="6" y1="12" x2="20" y2="12" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/><line x1="6" y1="16" x2="16" y2="16" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>',
        "search": f'<circle cx="14" cy="13.2" r="3.4" fill="none" stroke="{c}" stroke-width="1.8"/><line x1="16.5" y1="15.7" x2="19.2" y2="18.4" stroke="{c}" stroke-width="1.9" stroke-linecap="round"/>',
        "send": f'<path d="M21 13.5H10.5" stroke="{ORANGE}" stroke-width="2.4" stroke-linecap="round"/><path d="M13.6 10.2 10 13.5l3.6 3.3" fill="none" stroke="{ORANGE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
        "list": f'<line x1="6" y1="11" x2="22" y2="11" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/><line x1="6" y1="14.2" x2="22" y2="14.2" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/><line x1="6" y1="17.4" x2="17" y2="17.4" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>',
        "none": "",
    }[inner]
    return (f'<svg viewBox="0 0 28 22"><rect x="1.2" y="1.2" width="25.6" height="19.6" rx="2.6" fill="#fff" stroke="{c}" stroke-width="1.9"/>'
            f'<path d="M1.2 3.8a2.6 2.6 0 0 1 2.6-2.6h20.4a2.6 2.6 0 0 1 2.6 2.6V7H1.2z" fill="{c}"/>'
            f'<circle cx="4.8" cy="4.2" r=".9" fill="#fff"/><circle cx="7.4" cy="4.2" r=".9" fill="#fff"/><circle cx="10" cy="4.2" r=".9" fill="#fff"/>{ins}</svg>')

def server(c=ORANGE, gear=False):
    g = ""
    if gear:
        g = ('<g transform="translate(19 17)">' + "".join(f'<rect x="-1.25" y="-6.2" width="2.5" height="3" rx=".6" fill="{BLUE}" transform="rotate({a})"/>' for a in range(0, 360, 45))
             + f'<circle r="4.6" fill="{BLUE}"/><circle r="1.9" fill="#fff"/></g>')
    return (f'<svg viewBox="0 0 26 24"><rect x="1" y="2" width="20" height="9" rx="2" fill="{c}"/><rect x="1" y="12.8" width="20" height="9" rx="2" fill="{c}"/>'
            f'<circle cx="5" cy="6.5" r="1.1" fill="#fff"/><circle cx="5" cy="17.3" r="1.1" fill="#fff"/><circle cx="8.2" cy="6.5" r="1.1" fill="#fff"/><circle cx="8.2" cy="17.3" r="1.1" fill="#fff"/>'
            f'<line x1="11.5" y1="6.5" x2="17.5" y2="6.5" stroke="#fff" stroke-width="1.3" stroke-linecap="round"/><line x1="11.5" y1="17.3" x2="17.5" y2="17.3" stroke="#fff" stroke-width="1.3" stroke-linecap="round"/>{g}</svg>')

def server_line(c=ORANGE):
    return (f'<svg viewBox="0 0 24 24"><rect x="2.5" y="2.5" width="19" height="8.5" rx="2.4" fill="none" stroke="{c}" stroke-width="1.8"/><rect x="2.5" y="13" width="19" height="8.5" rx="2.4" fill="none" stroke="{c}" stroke-width="1.8"/>'
            f'<line x1="14" y1="6.75" x2="18" y2="6.75" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/><line x1="14" y1="17.25" x2="18" y2="17.25" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/></svg>')

def db_fill(c=PURPLE, top=None):
    top = top or c
    return (f'<svg viewBox="0 0 24 26"><path d="M3 5v15.5c0 1.9 4 3.5 9 3.5s9-1.6 9-3.5V5z" fill="{c}"/><ellipse cx="12" cy="5" rx="9" ry="3.4" fill="{top}" opacity=".75"/>'
            f'<path d="M3 11c0 1.9 4 3.5 9 3.5s9-1.6 9-3.5M3 16.2c0 1.9 4 3.5 9 3.5s9-1.6 9-3.5" fill="none" stroke="#fff" stroke-width="1.3"/></svg>')

def db_line(c=NAVY):
    return (f'<svg viewBox="0 0 24 26"><ellipse cx="12" cy="5" rx="8.6" ry="3.2" fill="none" stroke="{c}" stroke-width="1.7"/>'
            f'<path d="M3.4 5v15.6c0 1.8 3.9 3.3 8.6 3.3s8.6-1.5 8.6-3.3V5M3.4 10.3c0 1.8 3.9 3.3 8.6 3.3s8.6-1.5 8.6-3.3M3.4 15.5c0 1.8 3.9 3.3 8.6 3.3s8.6-1.5 8.6-3.3" fill="none" stroke="{c}" stroke-width="1.7"/></svg>')

def doc_check():
    return (f'<svg viewBox="0 0 24 24"><path d="M5 2.5h9.5l4.5 4.5v14.5H5z" fill="#fff" stroke="{BLUE}" stroke-width="1.7" stroke-linejoin="round"/>'
            f'<line x1="8" y1="9" x2="14" y2="9" stroke="{BLUE}" stroke-width="1.6" stroke-linecap="round"/><line x1="8" y1="12.5" x2="15" y2="12.5" stroke="{BLUE}" stroke-width="1.6" stroke-linecap="round"/><line x1="8" y1="16" x2="12" y2="16" stroke="{BLUE}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<circle cx="17.5" cy="17.5" r="5" fill="{GREEN}"/><path d="M15.2 17.6l1.6 1.6 3-3.2" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def gear(c=ORANGE):
    teeth = "".join(f'<rect x="-1.7" y="-10.5" width="3.4" height="4.5" rx=".8" fill="{c}" transform="rotate({a})"/>' for a in range(0, 360, 45))
    return f'<svg viewBox="-12 -12 24 24">{teeth}<circle r="7.6" fill="{c}"/><circle r="3.2" fill="#fff"/></svg>'

def play_screen(c=NAVY):
    return f'<svg viewBox="0 0 26 22"><rect x="1.5" y="1.5" width="23" height="16" rx="2.4" fill="none" stroke="{c}" stroke-width="1.9"/><path d="M11 6.2v6.6l5.4-3.3z" fill="{BLUE2}"/><line x1="8" y1="20.5" x2="18" y2="20.5" stroke="{c}" stroke-width="1.9" stroke-linecap="round"/></svg>'

def people(c=NAVY):
    return (f'<svg viewBox="0 0 28 22" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round"><circle cx="14" cy="6" r="3.6"/><path d="M7.5 20c0-4 2.9-6.6 6.5-6.6s6.5 2.6 6.5 6.6"/>'
            f'<circle cx="6" cy="8" r="2.7"/><path d="M1.5 18.5c0-3 1.9-5 4.5-5"/><circle cx="22" cy="8" r="2.7"/><path d="M26.5 18.5c0-3-1.9-5-4.5-5"/></svg>')

def cart(c=NAVY):
    return f'<svg viewBox="0 0 26 24" fill="none" stroke="{c}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h3.2l2.6 12.4h12.6L23 7H7"/><circle cx="10" cy="20" r="1.8"/><circle cx="18.5" cy="20" r="1.8"/></svg>'

def bank(c=GREEN2):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"><path d="M2.5 8.5 12 3l9.5 5.5z" fill="{c}"/><line x1="5.5" y1="10.5" x2="5.5" y2="18"/><line x1="10" y1="10.5" x2="10" y2="18"/><line x1="14" y1="10.5" x2="14" y2="18"/><line x1="18.5" y1="10.5" x2="18.5" y2="18"/><line x1="2.5" y1="20.5" x2="21.5" y2="20.5" stroke-width="2.2"/></svg>'

def bulb(c=ORANGE):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round"><path d="M8.2 14.5a5.6 5.6 0 1 1 7.6 0c-.9.8-1.3 1.6-1.3 2.6h-5c0-1-.4-1.8-1.3-2.6z" fill="#fde2b8"/>'
            f'<line x1="9.6" y1="19.6" x2="14.4" y2="19.6"/><line x1="10.4" y1="22" x2="13.6" y2="22"/><line x1="12" y1="1" x2="12" y2="2.6"/><line x1="3.2" y1="4.6" x2="4.4" y2="5.8"/><line x1="20.8" y1="4.6" x2="19.6" y2="5.8"/><line x1="1" y1="11" x2="2.6" y2="11"/><line x1="21.4" y1="11" x2="23" y2="11"/></svg>')

def warn_tri(c=RED):
    return f'<svg viewBox="0 0 24 22"><path d="M12 1.8 23 20.5H1z" fill="#fff" stroke="{c}" stroke-width="2" stroke-linejoin="round"/><line x1="12" y1="8" x2="12" y2="14" stroke="{c}" stroke-width="2.3" stroke-linecap="round"/><circle cx="12" cy="17.2" r="1.3" fill="{c}"/></svg>'

def spinner(c=BLUE):
    out = []
    for k, a in enumerate(range(0, 360, 45)):
        op = 0.25 + 0.75 * (k / 7)
        out.append(f'<line x1="0" y1="-5" x2="0" y2="-10" stroke="{c}" stroke-width="2.4" stroke-linecap="round" opacity="{op:.2f}" transform="rotate({a})"/>')
    return f'<svg viewBox="-12 -12 24 24">{"".join(out)}</svg>'

def doc_x():
    return (f'<svg viewBox="0 0 26 26"><path d="M4 2h11l5 5v15H4z" fill="#fff" stroke="{GRAY}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<line x1="7" y1="9" x2="13" y2="9" stroke="{GRAY}" stroke-width="1.5" stroke-linecap="round"/><line x1="7" y1="12.5" x2="16" y2="12.5" stroke="{GRAY}" stroke-width="1.5" stroke-linecap="round"/><line x1="7" y1="16" x2="12" y2="16" stroke="{GRAY}" stroke-width="1.5" stroke-linecap="round"/>'
            f'<circle cx="19" cy="19" r="5.6" fill="{RED}"/><path d="M16.8 16.8l4.4 4.4M21.2 16.8l-4.4 4.4" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/></svg>')

def store(c=GREEN2):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.7" stroke-linejoin="round"><path d="M3 9.5 4.6 4h14.8L21 9.5z"/><path d="M3 9.5c0 1.5 1.2 2.5 2.5 2.5S8 11 8 9.5c0 1.5 1.2 2.5 2.5 2.5S13 11 13 9.5c0 1.5 1.2 2.5 2.5 2.5S18 11 18 9.5c0 1.5 1.2 2.5 2.5 2.5"/><path d="M4.5 12v8.5h15V12"/><rect x="9.5" y="15" width="5" height="5.5"/></svg>'

def cloche(c=GREEN2):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round"><path d="M3.5 17.5a8.5 8.5 0 0 1 17 0z"/><line x1="2" y1="19.8" x2="22" y2="19.8"/><circle cx="12" cy="7.2" r="1.3"/></svg>'

def clock(c=GREEN2):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5.3l3.4 2"/></svg>'

def doc_lines(c=GREEN2):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 2.5h9.5L19 7v14.5H5z"/><line x1="8" y1="10" x2="16" y2="10"/><line x1="8" y1="13.5" x2="16" y2="13.5"/><line x1="8" y1="17" x2="13" y2="17"/></svg>'

def monitor(c=BLUE):
    return f'<svg viewBox="0 0 24 22" fill="none" stroke="{c}" stroke-width="1.9" stroke-linecap="round"><rect x="1.5" y="1.5" width="21" height="14" rx="2" fill="#e3eefa"/><line x1="12" y1="15.5" x2="12" y2="19.5"/><line x1="7.5" y1="20" x2="16.5" y2="20"/></svg>'

def burger():
    return ('<svg viewBox="0 0 26 24"><path d="M3 10.5a10 7.5 0 0 1 20 0z" fill="#f2a33a"/><circle cx="9" cy="6.8" r=".8" fill="#fff"/><circle cx="13" cy="5.2" r=".8" fill="#fff"/><circle cx="17" cy="7" r=".8" fill="#fff"/>'
            '<rect x="2.2" y="11.3" width="21.6" height="2.4" rx="1.2" fill="#4caf50"/><rect x="2.8" y="14" width="20.4" height="3.2" rx="1.4" fill="#8d4a1d"/><path d="M3 18h20v1.2a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3z" fill="#f2a33a"/></svg>')

def pin(c="#44506a"):
    return f'<svg viewBox="0 0 24 24"><path d="M12 22s7-7.2 7-12.5A7 7 0 0 0 5 9.5C5 14.8 12 22 12 22z" fill="{c}"/><circle cx="12" cy="9.5" r="2.6" fill="#fff"/></svg>'

def magnifier(c="#fff"):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6"/><line x1="15" y1="15" x2="20.5" y2="20.5"/></svg>'

def pizza():
    return ('<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#e8a24a"/><circle cx="12" cy="12" r="8.6" fill="#f6c453"/>'
            '<circle cx="8.5" cy="9" r="1.7" fill="#c0392b"/><circle cx="15" cy="8.2" r="1.7" fill="#c0392b"/><circle cx="14.6" cy="14.8" r="1.7" fill="#c0392b"/><circle cx="8.8" cy="15" r="1.7" fill="#c0392b"/><circle cx="12" cy="11.8" r="1" fill="#3f7d3a"/></svg>')

def check_sq(c=ORANGE):
    return f'<svg viewBox="0 0 16 16"><rect x="1" y="1" width="14" height="14" rx="3" fill="{c}"/><path d="M4.4 8.3 7 10.8 11.8 5.6" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def arrow_left(c, dashed=False, w=26, h=8):
    da = ' stroke-dasharray="3 2.4"' if dashed else ""
    return f'<svg viewBox="0 0 {w} {h}"><line x1="{w-1}" y1="{h/2}" x2="6" y2="{h/2}" stroke="{c}" stroke-width="1.8"{da}/><path d="M7 {h/2-3.4} 1 {h/2} 7 {h/2+3.4}z" fill="{c}"/></svg>'

def arrow_right(c, dashed=False, w=26, h=8):
    da = ' stroke-dasharray="3 2.4"' if dashed else ""
    return f'<svg viewBox="0 0 {w} {h}"><line x1="1" y1="{h/2}" x2="{w-6}" y2="{h/2}" stroke="{c}" stroke-width="1.8"{da}/><path d="M{w-7} {h/2-3.4} {w-1} {h/2} {w-7} {h/2+3.4}z" fill="{c}"/></svg>'

LARR = '<span class="ar">←</span>'

# ================= القسم 3 — رحلة الطلب والنتيجة (الصورة 1) =================
def path_card(cls, icon, title, sub):
    return f'<div class="pc {cls}">{icon}<b>{title}</b><small>{sub}</small></div>'

path_cards = [
    path_card("b", user(), "المستخدم", "يبحث عن منتج"),
    path_card("b", browser(BLUE2, "none"), "الواجهة الأمامية", "تستقبل الطلب"),
    path_card("o", server(ORANGE), "الواجهة الخلفية", "تعالج الطلب"),
    path_card("p", db_fill(PURPLE, "#8f7fe0"), "طبقة البيانات", "تبحث في البيانات"),
    path_card("o", server(ORANGE), "الواجهة الخلفية", "تجهز الاستجابة"),
    path_card("b", browser(BLUE2, "none"), "الواجهة الأمامية", "تعرض النتيجة"),
    path_card("g", doc_check(), "النتيجة", "تظهر للمستخدم"),
]
PATH = LARR.join(path_cards)

def step(n, cls, title, text, icon):
    return f'<div class="stp {cls}"><span class="n">{n}</span><div class="tx"><h4>{title}</h4><p>{text}</p></div><span class="ic">{icon}</span></div>'

STEPS = "\n".join([
    step(1, "cool", "الأمامية تستقبل", "تستقبل <b>الواجهة الأمامية</b> كلمات البحث التي أدخلها المستخدم.", browser(BLUE2, "search")),
    step(2, "warm", "الأمامية ترسل", "ترسل <b>الواجهة الأمامية</b> كلمات البحث إلى <b>الواجهة الخلفية</b>.", browser(BLUE2, "send")),
    step(3, "cool", "الخلفية تطلب البيانات", "تطلب <b>الواجهة الخلفية</b> من <b>طبقة البيانات</b> المنتجات التي تطابق عبارة البحث.", server(ORANGE, gear=True)),
    step(4, "warm", "البيانات ترجع النتائج", "تعيد <b>طبقة البيانات</b> النتائج المطلوبة إلى <b>الواجهة الخلفية</b>.",
         '<span class="dbret">' + arrow_right(PURPLE, w=18, h=10) + db_fill(PURPLE, "#8f7fe0") + '</span>'),
    step(5, "cool", "الخلفية تجهّز الاستجابة", "تجهّز <b>الواجهة الخلفية</b> النتائج لإرسالها إلى <b>الواجهة الأمامية</b>.", server(ORANGE, gear=True)),
    step(6, "warm", "الأمامية تعرض", "تعرض <b>الواجهة الأمامية</b> نتائج البحث على شاشة المستخدم.", browser(BLUE2, "list")),
])

SEC3 = f'''<div class="part p2"><span>الجزء الثاني</span></div>
<div class="ctitle kwn"><h2><span class="num">3</span> · رحلة الطلب والنتيجة</h2><div class="st">تدفق تعاون الطبقات الثلاث</div></div>
<div class="quote q2"><span class="qmark">”</span>في كثير من تطبيقات الويب، تعمل الأجزاء معًا لاستقبال <b>طلب المستخدم ومعالجته ثم عرض النتيجة</b>.<br><span class="exl">مثال:</span> <b>البحث عن منتج في متجر إلكتروني.</b></div>
<div class="panel kwn"><div class="ph">المسار العام للطلب</div><div class="pbody path">{PATH}</div></div>
<div class="panel"><div class="ph">خطوات الرحلة بالتفصيل</div><div class="pbody steps2">
{STEPS}
</div></div>
<div class="info green"><span class="lab">{bulb()}معلومة مهمة</span><p>تعمل الطبقات الثلاث معًا بشكل متكامل، وكل طبقة لديها دور محدد، وعند تعاونها نحصل على تجربة استخدام سلسة وفعّالة.</p></div>'''

# ================= كيفية تعاون الطبقات الثلاث (الصورة 3، الرسم + فهم) =================
X = {"db": 70, "back": 200, "front": 330, "user": 462}
Y = [62, 98, 134, 170, 206, 242]
NAVY_A = "#1d4b7f"; OR_A = "#e8761c"

def msg(k, x1, x2, ret, label, lbl_dx=0):
    y = Y[k]
    c = OR_A if ret else NAVY_A
    da = ' stroke-dasharray="4 3"' if ret else ""
    if x2 < x1:   # سهم لليسار
        head = f'<path d="M{x2+7} {y-3.6} {x2} {y} {x2+7} {y+3.6}z" fill="{c}"/>'
        line = f'<line x1="{x1}" y1="{y}" x2="{x2+5}" y2="{y}" stroke="{c}" stroke-width="1.6"{da}/>'
        cx = x1 - 12
    else:
        head = f'<path d="M{x2-7} {y-3.6} {x2} {y} {x2-7} {y+3.6}z" fill="{c}"/>'
        line = f'<line x1="{x1}" y1="{y}" x2="{x2-5}" y2="{y}" stroke="{c}" stroke-width="1.6"{da}/>'
        cx = x1 + 12
    mid = (min(x1, x2) + max(x1, x2)) / 2 + lbl_dx
    lines = label.count("<br>") + 1
    top = y - 4 - 11 * lines
    svg = line + head
    html = (f'<span class="nb {"o" if ret else "r"}" style="left:{cx}pt;top:{y}pt">{k+1}</span>'
            f'<span class="lb" style="left:{mid}pt;top:{top}pt">{label}</span>')
    return svg, html

parts = [
    msg(0, X["user"], X["front"] + 4, False, "إدخال كلمة البحث", 6),
    msg(1, X["front"] - 4, X["back"] + 4, False, "إرسال الكلمة المفتاحية<br>إلى الواجهة الخلفية", 6),
    msg(2, X["back"] - 4, X["db"] + 4, False, "البحث عن المنتجات<br>المطابقة", 6),
    msg(3, X["db"] + 4, X["back"] - 4, True, "إعادة بيانات المنتج", -6),
    msg(4, X["back"] + 4, X["front"] - 4, True, "إرسال النتائج<br>إلى الواجهة الأمامية", -6),
    msg(5, X["front"] + 4, X["user"], True, "عرض النتائج", -6),
]
lifelines = "".join(f'<line x1="{x}" y1="28" x2="{x}" y2="258" stroke="#a9c1dc" stroke-width="1.1" stroke-dasharray="4 3"/>' for x in X.values())
bars = (f'<rect x="{X["front"]-4}" y="{Y[0]-8}" width="8" height="{Y[5]-Y[0]+16}" fill="#eef5fc" stroke="{NAVY_A}" stroke-width="1"/>'
        f'<rect x="{X["back"]-4}" y="{Y[1]-8}" width="8" height="{Y[4]-Y[1]+16}" fill="#eef5fc" stroke="{NAVY_A}" stroke-width="1"/>'
        f'<rect x="{X["db"]-4}" y="{Y[2]-8}" width="8" height="{Y[3]-Y[2]+16}" fill="#eef5fc" stroke="{NAVY_A}" stroke-width="1"/>')
heads = "".join(f'<div class="hd{" u" if k == "user" else ""}" style="left:{x-55}pt">{n}</div>' for k, x, n in [
    ("db", X["db"], "قاعدة البيانات"), ("back", X["back"], "الواجهة الخلفية"), ("front", X["front"], "الواجهة الأمامية"), ("user", X["user"], "المستخدم")])
SEQ_SVG = f'<svg class="lines" viewBox="0 0 532 264">{lifelines}{bars}{"".join(p[0] for p in parts)}</svg>'
SEQ = f'''<div class="sqh kwn"><div><h3>كيفية تعاون الطبقات الثلاث</h3><div class="st">مثال: البحث عن منتج في موقع تسوق</div></div>
  <div class="legend"><span>{arrow_left(NAVY_A)}طلب</span><span>{arrow_right(OR_A, dashed=True)}بيانات عائدة</span></div></div>
<div class="sq">{heads}{SEQ_SVG}{"".join(p[1] for p in parts)}</div>
<div class="info gray"><span class="lab">فهم</span><p>يوضح هذا النموذج بشكل مبسّط كيفية تعاون أجزاء تطبيق الويب فيما بينها، وهو نموذج تعليمي يساعد على فهم تدفق البيانات بين الطبقات الثلاث.</p></div>'''

# ================= القسم 4 — إعدادات تطبيقات الويب المألوفة (الصورة 2) =================
def col(cls, icon, title, sub, items):
    lis = "".join(f"<li>{t}</li>" for t in items)
    return f'<div class="col {cls}"><div class="ch">{icon}<div><b>{title}</b><small>{sub}</small></div></div><ul>{lis}</ul></div>'

def svc(icon, name, f, b, d):
    return (f'<div class="svc"><div class="nm"><span class="ci">{icon}</span><h4>{name}</h4></div>'
            + col("f", browser(NAVY, "none"), "الواجهة الأمامية", "العرض والتفاعل", f)
            + col("b", server_line(ORANGE), "الواجهة الخلفية", "المعالجة والتحكم", b)
            + col("d", db_line(NAVY), "قاعدة البيانات", "التخزين والإدارة", d) + "</div>")

SEC4 = f'''<div class="part p3"><span>الجزء الثالث</span></div>
<div class="tbar kwn"><h2><span class="num">4</span> · إعدادات تطبيقات الويب المألوفة</h2></div>
<div class="warn kwn"><span class="ex">!</span><p>يمكن تطبيق هذا <b>النموذج المبسط</b> على كثير من تطبيقات الويب لفهم توزيع <b>المهام</b>، مع أن البنية الفعلية قد تختلف.</p></div>
{svc(play_screen(), "موقع مشاركة الفيديو",
     ["عرض شاشات تشغيل الفيديو والبحث.", "استقبال إجراءات المستخدم."],
     ["اختيار الفيديوهات الموصى بها.", "تجميع عدد المشاهدات."],
     ["تخزين بيانات الفيديو.", "معلومات المستخدمين.", "سجل المشاهدة."])}
{svc(people(), "شبكة التواصل الاجتماعي",
     ["عرض الخط الزمني وشاشات النشر.", "استقبال وإرسال المحتوى المُدخل."],
     ["تحديد الجمهور المستهدف للمنشورات.", "التحكم في الإشعارات الفورية."],
     ["تخزين بيانات المنشورات.", "علاقات المتابعة.", "الرسائل."])}
{svc(cart(), "موقع تجارة إلكترونية",
     ["عرض قوائم المنتجات وشاشات سلة التسوق.", "استقبال عمليات الطلب."],
     ["التحقق من المخزون.", "إرسال طلبات الدفع.", "التعامل مع نتائجها."],
     ["تخزين معلومات المنتجات.", "سجل الطلبات.", "معلومات العملاء."])}
<div class="simply"><span class="lab">{bulb("#fff")}ببساطة</span><p>الذي يختلف من خدمة إلى أخرى هو <b>نوع البيانات والعمليات</b> التي تقوم بها كل طبقة، بينما يبقى هذا العرض <b>نموذجًا مبسطًا</b> للتعلم وفهم الفكرة العامة.</p></div>'''

# ================= القسم 5 — نفس النموذج في خدمات مختلفة (الصورة 4) =================
def rest(name, rate):
    return f'<div class="ri"><span class="th">{pizza()}</span><span class="rn"><b>{name}</b><i>{rate} <em>★</em></i></span></div>'

PHONE = f'''<div class="phonecol">
  <div class="ucard"><span class="n1">1</span><div><b>المستخدم</b><small>يكتب اسم مطعم ويضغط «بحث»</small></div></div>
  <div class="phone"><div class="scr">
    <div class="loc">{pin()}القاهرة<span class="dd">⌄</span></div>
    <div class="ms"><span class="q">بيتزا</span><span class="go">{magnifier()}</span></div>
    <div class="chips"><span class="on">الكل</span><span>بيتزا</span><span>برجر</span><span>مشويات</span></div>
    {rest("بيتزا الركن", "4.5")}{rest("بيتزا الميدان", "4.2")}{rest("بيتزا البيت", "4.1")}
  </div></div>
</div>'''

ARRS = f'<div class="arrs">{arrow_left(BLUE, w=18, h=10)}{arrow_right(BLUE, w=18, h=10)}</div>'

FRONT = f'''<div class="ecard f"><div class="eh2">{monitor()}الواجهة الأمامية</div><div class="eb">
  <div class="mock"><div class="msearch"><span class="q">بيتزا</span><span class="go">{magnifier()}</span></div><div class="ghost"></div></div>
  <ul class="dots b"><li>تعرض مربع البحث.</li><li>تستقبل كلمة البحث من المستخدم.</li><li>تعرض النتائج التي تصل من الواجهة الخلفية.</li></ul>
</div></div>'''

BACK = f'''<div class="ecard b"><div class="eh2">{server(ORANGE)}الواجهة الخلفية</div><div class="eb">
  <div class="chk"><ul>{"".join(f"<li>{check_sq()}{t}</li>" for t in ["استقبال الطلب", "تطبيق قواعد التطبيق", "معالجة البيانات", "تجهيز النتائج"])}</ul><span class="gr">{gear("#f2a33a")}</span></div>
  <div class="rules"><b>أمثلة على قواعد التطبيق:</b><ul><li>هل المطعم مفتوح الآن؟</li><li>هل يطابق اسم المطعم البحث؟</li><li>هل يوصل لمنطقة المستخدم؟</li><li>ترتيب النتائج حسب التقييم.</li></ul></div>
</div></div>'''

def dbrow(icon, t, s):
    return f'<div class="dr">{icon}<div><b>{t}</b><small>{s}</small></div></div>'

DB = f'''<div class="ecard d"><div class="eh2">{db_fill(GREEN2, "#3aa574")}قاعدة البيانات</div><div class="eb">
  {dbrow(store(), "معلومات المطاعم", "(الاسم – الموقع – التقييم)")}{dbrow(cloche(), "قائمة المنيو", "(الأصناف – الأسعار)")}{dbrow(clock(), "حالة المطعم", "(مفتوح / مقفول)")}{dbrow(doc_lines(), "الطلبات السابقة", "(تقييمات وآراء المستخدمين)")}
</div></div>'''

# مسار الرجوع: من الواجهة الخلفية للواجهة الأمامية (تحت الكروت)
RET = '''<div class="ret"><svg viewBox="0 0 512.7 30"><path d="M210.7 0 V12 H349.7 V6" fill="none" stroke="#1f5f99" stroke-width="1.6"/><path d="M345.9 7.5 349.7 0 353.5 7.5z" fill="#1f5f99"/></svg>
  <span class="rl">إرسال النتائج إلى الواجهة الأمامية لعرضها للمستخدم</span></div>'''

OTHER_BANK = '<div class="mk bankm"><div class="ph3"><small>الرصيد الحالي</small><b>12,450 جنيه</b><i></i><i></i></div></div>'
OTHER_VID = '<div class="mk vidm"><div class="pl"><svg viewBox="0 0 40 26"><path d="M0 26 13 11l8 8 6-5 13 12z" fill="#7d8ea8"/><circle cx="31" cy="7" r="3" fill="#c9d4e3"/><path d="M16.5 8.5v9l7.5-4.5z" fill="#fff"/></svg></div><i></i><i></i></div>'
OTHER_SHOP = '<div class="mk shopm"><div class="pr">' + cart("#7d8ea8") + '</div><span class="btn">إضافة إلى السلة</span></div>'

def ocard(icon, title, items, mock):
    lis = "".join(f"<li>{t}</li>" for t in items)
    return f'<div class="ocard"><div class="ot"><h5>{icon}{title}</h5><ul>{lis}</ul></div>{mock}</div>'

SEC5 = f'''<div class="ntitle kwn"><h2><span class="n5 num">5</span>نفس النموذج في خدمات مختلفة</h2><div class="st">نفس فكرة التعاون بين الطبقات الثلاث تظهر في جميع تطبيقات الويب تقريبًا، مهما اختلف النوع أو المجال.</div></div>
<div class="exw"><div class="eh"><span class="tag">{burger()}مثال من حياتنا</span><span class="sub">البحث عن مطعم في تطبيق توصيل طعام</span></div>
  <div class="exg">{PHONE}<div class="sp1"></div>{FRONT}{ARRS}{BACK}{ARRS}{DB}</div>
  {RET}
</div>
<div class="probs"><div class="ph2">{warn_tri()}لو حصلت مشكلة؟</div><div class="pg">
  <div class="pcard"><div><h5>ظهر مطعم غير مناسب أو بيانات غلط؟</h5><ul><li>السبب قد يكون في قاعدة البيانات (بيانات غير صحيحة).</li><li>أو في قواعد التطبيق (شروط غير سليمة).</li><li>أو في طريقة عرض النتائج في الواجهة الأمامية.</li></ul></div>{doc_x()}</div>
  <div class="pcard"><div><h5>الشاشة فضلت بتتحمل؟</h5><ul><li>غالبًا الواجهة الأمامية شغالة لكن ما زالت تنتظر الرد من الواجهة الخلفية.</li></ul></div>{spinner()}</div>
</div></div>
<div class="others"><div class="ph2">أمثلة أخرى بنفس النموذج</div><div class="og">
  {ocard(bank(), "خدمات بنكية", ["الاستعلام عن الرصيد", "عرض كشف الحساب", "تحويل الأموال", "عرض آخر العمليات"], OTHER_BANK)}
  {ocard(play_screen(BLUE), "موقع فيديو", ["البحث عن فيديو", "عرض قائمة النتائج", "جلب معلومات الفيديو", "عرض التعليقات والمشاهدات"], OTHER_VID)}
  {ocard(cart(ORANGE), "متجر إلكتروني", ["البحث عن منتج", "عرض تفاصيل المنتج", "التحقق من المخزون", "إتمام الشراء"], OTHER_SHOP)}
</div></div>
<div class="info blue"><span class="lab">{bulb()}معلومة مهمة</span><p>جميع تطبيقات الويب – سواء لتوصيل الطعام أو التسوق أو مشاهدة الفيديو أو الخدمات البنكية – تستخدم نفس فكرة التعاون بين الطبقات الثلاث مع اختلاف البيانات وقواعد التطبيق وطريقة العرض فقط.</p></div>'''
