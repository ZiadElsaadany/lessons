# -*- coding: utf-8 -*-
"""الغلاف الخارجي لمذكرة الترم الأول (وش + ضهر) — الوش شباك محرر أكواد (البرمجة.py) والعنوان سطور كود؛ الضهر terminal بيطبع الجملة. فاتح، كلام كبير، من غير أزرق.

    python3 tools/build_cover.py        ← يكتب html/term1_cover.html

- كل صفحة 216×303 مم = A4 + هامش قص (bleed) 3 مم من كل ناحية؛ الكلام كله جوه منطقة آمنة (≥ 12 مم من حرف الورقة).
- الطباعة: Chromium ← «حجم الصفحة من CSS» + «Background graphics» (أو page.pdf(prefer_css_page_size=True, print_background=True)).
- الـQR: assets/qr_fb.svg و assets/qr_yt.svg (اتعملوا بـsegno واتقروا بقارئ QR)؛ الغلاف بيستخدم نسخ _warm منهم (لون أسود دافي).
- اللوجو: assets/logo_warm.jpg بيتعمل تلقائي من logo.jpg (الأزرق ← برتقالي).
"""
import os, random

TOOLS = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(TOOLS), "assets")
OUT = os.path.join(os.path.dirname(TOOLS), "term1_cover.html")
W, H = 216, 303                       # مم
YEAR = "2026 / 2027"
BG = "#2e271e"                         # خلفية اللوجو بعد التلوين — اللوجو بيتحط في دايرة غامقة على الغلاف الفاتح
AMBER = "#f98e03"
INK = "#1d1a17"                        # كلام الغلاف (أسود دافي)
GREEN = "#2f8f46"                       # لون النصوص (strings) في المحرر
PAPER = "#f2f1ee"                       # الصفحة رمادي فاتح جدًا والشباك أبيض
DEEP = "#c86a00"                       # برتقالي أغمق للكلام على الخلفية الفاتحة (أوضح من AMBER)


def warm_logo():
    """assets/logo_warm.jpg: نفس اللوجو، الأزرق اتحوّل برتقالي والكحلي بقى أسود دافي (الوش والقميص زي ما هما)."""
    import numpy as np
    from PIL import Image
    src, dst = os.path.join(ASSETS, "logo.jpg"), os.path.join(ASSETS, "logo_warm.jpg")
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src): return
    im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    mx, mn = im.max(-1), im.min(-1); v = mx; d = np.maximum(mx - mn, 1e-6)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    blue = (h > 180) & (h < 265) & (s > .12)
    H = np.where(blue, 34.0, h); S = np.where(blue, np.where(v < .35, s * .35, s), s)
    c = v * S; x = c * (1 - np.abs((H / 60) % 2 - 1)); m = v - c; k = (H // 60).astype(int) % 6; z = 0 * c
    out = np.zeros_like(im)
    for i, (a, bb, cc) in enumerate([(c, x, z), (x, c, z), (z, c, x), (z, x, c), (x, z, c), (c, z, x)]):
        sel = k == i
        for ch, val in enumerate((a, bb, cc)): out[..., ch][sel] = val[sel]
    Image.fromarray((np.clip(out + m[..., None], 0, 1) * 255).astype(np.uint8)).save(dst, quality=93)


def warm_qr():
    """نسخة من أكواد الـQR بلون أسود دافي للغلاف (الأصلية كحلي ومستخدمة جوه المذكرة)."""
    for k in ("fb", "yt"):
        q = open(os.path.join(ASSETS, f"qr_{k}.svg"), encoding="utf-8").read()
        open(os.path.join(ASSETS, f"qr_{k}_warm.svg"), "w", encoding="utf-8").write(q.replace("#0b1230", "#1e1912"))


def n(t): return f'<span class="n">{t}</span>'


def win(tab, body, cls=""):
    """شباك محرر أكواد: شريط العنوان (3 نقط + تاب الملف) وتحته السطور مترقّمة."""
    rows = "".join(f'<div class="ln">{k}</div><div class="cd {c}">{t}</div>' for k, (c, t) in enumerate(body, 1))
    return (f'<div class="win {cls}"><div class="tb"><span class="tab"><i></i>{tab}</span><span class="dt"><b></b><b></b><b></b></span></div>'
            f'<div class="ed">{rows}</div></div>')


def front():
    body = [
        ("cm", "# مذكرة شرح + بنك أسئلة"),
        ("", ""),
        ("big", "البرمجة"),
        ("big2", "والذكاء الاصطناعي"),
        ("", ""),
        ("kv", 'الصف <o>=</o> <s>"الثاني الثانوي"</s>'),
        ("kv", 'الترم <o>=</o> <s>"الأول"</s>'),
        ("kv", 'المدرس <o>=</o> <s>"أ/ زياد السعدني"</s><u></u>'),
    ]
    return f'''<section class="cv front">
  <div class="logo"><img src="assets/logo_warm.jpg" alt=""></div>
  {win('<bdi>البرمجة.py</bdi>', body)}
  <div class="yr">{n(YEAR)}</div>
</section>'''


def back():
    body = [
        ("sh", '<span class="pr">$</span> python3 think.py'),
        ("out", "الكود مجرد أداة…"),
        ("out o", "القوة الحقيقية في طريقة تفكيرك."),
        ("", ""),
        ("cm", "# تابعنا — امسح الكود بكاميرا الموبايل"),
        ("qrrow", '<div class="qb"><div class="qr"><img src="assets/qr_fb_warm.svg" alt=""></div><b>فيسبوك</b></div>'
                  '<div class="qb"><div class="qr"><img src="assets/qr_yt_warm.svg" alt=""></div><b>يوتيوب</b></div>'),
        ("", ""),
        ("kv", 'واتساب <o>=</o> <s>"<span class="n">01124840835</span>"</s><u></u>'),
    ]
    return f'''<section class="cv back">
  {win("terminal", body, "term")}
  <div class="brand"><img src="assets/logo_warm.jpg" alt=""><b>أكواد مع زياد</b></div>
</section>'''


CSS = r"""
@font-face{font-family:'Baloo Bhaijaan 2';font-weight:400 800;src:url(fonts/BalooBhaijaan2.ttf) format('truetype')}
@font-face{font-family:'CodeMono';src:url(fonts/DejaVuSansMono-Bold.ttf) format('truetype');unicode-range:U+0000-024F}
@page{size:216mm 303mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#bdbdbd;padding:14pt 0;font-family:'Baloo Bhaijaan 2';direction:rtl}
@media print{body{background:#fff;padding:0}}
.cv{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:space-evenly;padding:12mm 15mm;width:216mm;height:303mm;margin:0 auto 14pt auto;overflow:hidden;color:INK;break-after:page;page-break-after:always;
  background:PAPER}
.cv:last-child{break-after:auto;page-break-after:auto}
@media print{.cv{margin:0}}
.n{direction:ltr;unicode-bidi:isolate}
/* ---- شباك المحرر ---- */
.win{position:relative;flex:none;width:100%;background:#fff;border:2.2pt solid INK;border-radius:5mm;overflow:hidden}
.tb{height:13mm;display:flex;align-items:stretch;justify-content:space-between;background:#ecebe8;border-bottom:2.2pt solid INK}
.tab{display:flex;align-items:center;gap:7pt;padding:0 16pt;background:#fff;border-left:2.2pt solid INK;font-family:'CodeMono','Baloo Bhaijaan 2';font-size:15pt;font-weight:800;margin-bottom:-2.2pt}
.tab i{width:9pt;height:9pt;border-radius:2pt;background:AMBER}
.dt{display:flex;align-items:center;gap:6pt;padding:0 14pt;direction:ltr}
.dt b{width:11pt;height:11pt;border-radius:50%;border:1.2pt solid rgba(0,0,0,.25)}
.dt b:nth-child(1){background:#ff5f57}.dt b:nth-child(2){background:#febc2e}.dt b:nth-child(3){background:#28c840}
.ed{display:grid;grid-template-columns:15mm minmax(0,1fr);align-items:baseline;padding:9mm 0 11mm 0}
.ln{font-family:'CodeMono';font-size:12pt;color:#b5b0a8;text-align:center;direction:ltr;line-height:1}
.cd{padding-left:8mm;min-height:8mm;line-height:1.25;font-weight:800;white-space:nowrap}
.cm{font-size:21pt;color:#9a948b;font-weight:700}
.big{font-size:112pt;line-height:1.1;color:INK;letter-spacing:-1pt}
.big2{font-size:55pt;line-height:1.2;color:AMBER}
.kv{font-size:28pt;color:INK;line-height:1.6}
.kv o{color:AMBER;margin:0 3pt}
.kv s{text-decoration:none;color:GREEN}
u{display:inline-block;width:3.2mm;height:9mm;background:AMBER;vertical-align:-1.5mm;margin-right:2pt;text-decoration:none}
/* ---- الوش ---- */
.front .logo{flex:none;width:62mm;height:62mm;border-radius:50%;overflow:hidden;background:BG;
  border:2.2pt solid INK}
.front .logo img{width:100%;height:100%;display:block}
.yr{text-align:center;font-family:'CodeMono';font-size:17pt;color:INK;letter-spacing:1pt}
/* ---- الضهر ---- */
.sh{font-family:'CodeMono','Baloo Bhaijaan 2';font-size:17pt;color:#77716a;direction:ltr;text-align:left;padding-right:8mm}
.sh .pr{color:GREEN;margin-right:6pt}
.out{font-size:33pt;line-height:1.45;color:INK}
.out.o{color:AMBER}
.qrrow{display:flex;gap:16mm;padding:3mm 0 0 0}
.qb{display:flex;flex-direction:column;align-items:center;gap:6pt}
.qb .qr{width:44mm;height:44mm;background:#fff;border-radius:3mm;padding:2.6mm;border:2pt solid INK}
.qb .qr img{width:100%;height:100%;display:block}
.qb b{font-size:20pt;font-weight:800;color:INK;line-height:1}
.brand{display:flex;align-items:center;justify-content:center;gap:10pt}
.brand img{width:30mm;height:30mm;border-radius:50%;border:2pt solid INK}
.brand b{font-size:34pt;font-weight:800;color:INK}
""".replace("BG", BG).replace("AMBER", AMBER).replace("INK", INK).replace("DEEP", DEEP).replace("GREEN", GREEN).replace("PAPER", PAPER)


def main():
    warm_logo(); warm_qr()
    doc = ('<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
           '<title>الغلاف الخارجي — البرمجة والذكاء الاصطناعي — الترم الأول | أكواد مع زياد</title>\n'
           f'<style>{CSS}</style>\n</head>\n<body>\n{front()}\n{back()}\n'
           '<script>document.fonts.ready.then(() => document.body.dataset.ready = "1")</script>\n</body>\n</html>\n')
    open(OUT, "w", encoding="utf-8").write(doc)
    print("written", OUT, len(doc) // 1024, "KB")


if __name__ == "__main__":
    main()
