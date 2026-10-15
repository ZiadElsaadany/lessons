# -*- coding: utf-8 -*-
"""الغلاف الخارجي لمذكرة الترم الأول (وش + ضهر) — بسيط: خلفية فاتحة، كلام قليل وكبير، برتقالي (من غير أزرق).

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
INK = "#2b2117"                        # كلام الغلاف (بني غامق قريب من الأسود)
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


def circuits(seed, count=22):
    """خطوط دواير خفيفة على الأطراف بس — النص فاضي."""
    rnd = random.Random(seed)
    out = []
    for k in range(count):
        side = rnd.choice("LRTB")
        if side in "LR":
            y = rnd.uniform(8, H - 8)
            x0 = 0 if side == "L" else W
            d = 1 if side == "L" else -1
            l1, l2 = rnd.uniform(8, 30), rnd.uniform(5, 16)
            dy = rnd.choice([-1, 1]) * rnd.uniform(4, 12)
            pts = [(x0, y), (x0 + d * l1, y), (x0 + d * (l1 + abs(dy)), y + dy), (x0 + d * (l1 + abs(dy) + l2), y + dy)]
        else:
            x = rnd.uniform(8, W - 8)
            y0 = 0 if side == "T" else H
            d = 1 if side == "T" else -1
            l1, l2 = rnd.uniform(8, 26), rnd.uniform(5, 14)
            dx = rnd.choice([-1, 1]) * rnd.uniform(4, 12)
            pts = [(x, y0), (x, y0 + d * l1), (x + dx, y0 + d * (l1 + abs(dx))), (x + dx, y0 + d * (l1 + abs(dx) + l2))]
        path = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        op = rnd.uniform(.10, .24)
        out.append(f'<path d="{path}" stroke="{AMBER}" stroke-opacity="{op:.2f}" stroke-width=".35" fill="none"/>'
                   f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r=".9" fill="{AMBER}" fill-opacity="{op + .15:.2f}"/>')
    return f'<svg class="circ" viewBox="0 0 {W} {H}" preserveAspectRatio="none">{"".join(out)}</svg>'


def n(t): return f'<span class="n">{t}</span>'


def front():
    return f'''<section class="cv front">
  {circuits(7)}
  <div class="logo"><img src="assets/logo_warm.jpg" alt=""></div>
  <div class="ttl"><h1>البرمجة</h1><h2>والذكاء الاصطناعي</h2></div>
  <div class="bar"></div>
  <div class="sub">الصف الثاني الثانوي <i></i> الترم الأول</div>
  <div class="who"><b>أ/ زياد السعدني</b><span>{n(YEAR)}</span></div>
</section>'''


def back():
    return f'''<section class="cv back">
  {circuits(11)}
  <div class="quote"><span class="qmk">”</span><p>الكود مجرد أداة…<br><b>القوة الحقيقية في طريقة تفكيرك.</b></p></div>
  <div class="qrs">
    <div class="qb"><div class="qr"><img src="assets/qr_fb_warm.svg" alt=""></div><b>فيسبوك</b></div>
    <div class="qb"><div class="qr"><img src="assets/qr_yt_warm.svg" alt=""></div><b>يوتيوب</b></div>
  </div>
  <div class="foot"><b>أكواد مع زياد</b><span>واتساب {n("01124840835")}</span></div>
</section>'''


CSS = r"""
@font-face{font-family:'Baloo Bhaijaan 2';font-weight:400 800;src:url(fonts/BalooBhaijaan2.ttf) format('truetype')}
@page{size:216mm 303mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#cfc8bc;padding:14pt 0;font-family:'Baloo Bhaijaan 2';direction:rtl}
@media print{body{background:#fff;padding:0}}
.cv{position:relative;width:216mm;height:303mm;margin:0 auto 14pt auto;overflow:hidden;color:INK;
  background:radial-gradient(90% 60% at 50% 30%,#fffdf8 0%,#fbf5ea 55%,#f3e8d6 100%);break-after:page;page-break-after:always}
.cv:last-child{break-after:auto;page-break-after:auto}
@media print{.cv{margin:0}}
.n{direction:ltr;unicode-bidi:isolate}
.circ{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
/* ---- الوش ---- */
.logo{position:absolute;top:22mm;left:50%;transform:translateX(-50%);width:98mm;height:98mm;border-radius:50%;overflow:hidden;
  background:BG;box-shadow:0 0 0 2.2mm #fff,0 0 0 3mm rgba(249,142,3,.55),0 4mm 10mm rgba(80,50,10,.25)}
.logo img{width:100%;height:100%;display:block}
.ttl{position:absolute;top:132mm;left:0;right:0;text-align:center;line-height:1}
.ttl h1{margin:0;font-size:84pt;font-weight:800;line-height:1.05;color:INK}
.ttl h2{margin:6pt 0 0 0;font-size:46pt;font-weight:800;line-height:1.2;color:DEEP}
.bar{position:absolute;top:198mm;left:50%;width:40mm;height:1.6mm;margin-left:-20mm;border-radius:1mm;background:AMBER}
.sub{position:absolute;top:208mm;left:0;right:0;text-align:center;font-size:26pt;font-weight:800;color:INK;line-height:1.1}
.sub i{display:inline-block;width:8pt;height:8pt;border-radius:50%;background:AMBER;margin:0 12pt;vertical-align:middle}
.who{position:absolute;bottom:20mm;left:0;right:0;text-align:center;line-height:1.25}
.who b{display:block;font-size:34pt;font-weight:800;color:INK}
.who span{font-size:17pt;font-weight:800;color:DEEP;letter-spacing:.5pt}
/* ---- الضهر ---- */
.quote{position:absolute;top:70mm;left:20mm;right:20mm;text-align:center}
.quote .qmk{display:block;font-size:80pt;line-height:.8;height:38pt;color:AMBER;font-weight:800}
.quote p{margin:0;font-size:34pt;line-height:1.5;font-weight:800;color:INK}
.quote b{color:DEEP}
.qrs{position:absolute;top:160mm;left:0;right:0;display:flex;justify-content:center;gap:24mm}
.qb{display:flex;flex-direction:column;align-items:center;gap:7pt}
.qb .qr{width:42mm;height:42mm;background:#fff;border-radius:10pt;padding:3mm;border:1.2pt solid rgba(249,142,3,.6);box-shadow:0 2mm 6mm rgba(80,50,10,.12)}
.qb .qr img{width:100%;height:100%;display:block}
.qb b{font-size:18pt;font-weight:800;color:DEEP;line-height:1}
.foot{position:absolute;bottom:20mm;left:0;right:0;text-align:center;line-height:1.3}
.foot b{display:block;font-size:28pt;font-weight:800;color:INK}
.foot span{font-size:19pt;font-weight:800;color:DEEP}
""".replace("BG", BG).replace("AMBER", AMBER).replace("INK", INK).replace("DEEP", DEEP)


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
