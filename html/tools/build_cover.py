# -*- coding: utf-8 -*-
"""الغلاف الخارجي لمذكرة الترم الأول (وش + ضهر) — أبيض منقّط (ورق كشكول) + برتقالي وأسود، كلام قليل وكبير، اللوجو بين قوسين كود ‹ ›.

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


def dots():
    """ورقة كشكول منقّطة (نقط رمادي خفيف كل 6 مم) — SVG pattern عشان تفضل vector في الطباعة."""
    return (f'<svg class="dots" viewBox="0 0 {W} {H}" preserveAspectRatio="none"><defs><pattern id="dp" width="6" height="6" patternUnits="userSpaceOnUse">'
            f'<circle cx="3" cy="3" r=".42" fill="#c9c4bc"/></pattern></defs><rect width="{W}" height="{H}" fill="url(#dp)"/></svg>')


def brackets(cy, half=27, gap=46, sw=8.5):
    """قوسين كود كبار ‹ › حوالين اللوجو: كل قوس خطين بنهايات مدوّرة."""
    cx = W / 2; w = half * .78
    l, r = cx - gap, cx + gap
    return (f'<svg class="brk" viewBox="0 0 {W} {H}" preserveAspectRatio="none"><g fill="none" stroke="{AMBER}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M{l - 4:.1f} {cy - half:.1f} L{l - 4 - w:.1f} {cy:.1f} L{l - 4:.1f} {cy + half:.1f}"/>'
            f'<path d="M{r + 4:.1f} {cy - half:.1f} L{r + 4 + w:.1f} {cy:.1f} L{r + 4:.1f} {cy + half:.1f}"/></g></svg>')


def n(t): return f'<span class="n">{t}</span>'


def front():
    return f'''<section class="cv front">
  {dots()}
  <div class="corner"></div>
  {brackets(74)}
  <div class="logo"><img src="assets/logo_warm.jpg" alt=""></div>
  <div class="ttl"><h1>البرمجة</h1><h2><span>والذكاء الاصطناعي</span></h2></div>
  <div class="sub">الصف الثاني الثانوي <i></i> الترم الأول</div>
  <div class="who"><b>أ/ زياد السعدني</b><span>{n(YEAR)}</span></div>
</section>'''


def back():
    return f'''<section class="cv back">
  {dots()}
  <div class="corner"></div>
  <div class="quote"><span class="qmk">{{ }}</span><p>الكود مجرد أداة…<br><b><span>القوة الحقيقية في طريقة تفكيرك.</span></b></p></div>
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
body{background:#c9c9c9;padding:14pt 0;font-family:'Baloo Bhaijaan 2';direction:rtl}
@media print{body{background:#fff;padding:0}}
.cv{position:relative;width:216mm;height:303mm;margin:0 auto 14pt auto;overflow:hidden;color:INK;background:#fff;break-after:page;page-break-after:always}
.cv:last-child{break-after:auto;page-break-after:auto}
@media print{.cv{margin:0}}
.n{direction:ltr;unicode-bidi:isolate}
.dots,.brk{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
/* شريطين (برتقالي + أسود رفيع) قاطعين الركن بزاوية 45° — زي شريط لاصق */
.corner{position:absolute;top:16mm;left:-34mm;width:120mm;height:13mm;background:AMBER;transform:rotate(-45deg)}
.corner::after{content:"";position:absolute;left:0;right:0;top:17mm;height:3.2mm;background:INK}
.back .corner{top:auto;left:auto;bottom:16mm;right:-34mm}
.back .corner::after{top:auto;bottom:17mm}
/* هايلايتر: شريط برتقالي ورا الكلام، مايل سنة */
.hl,.ttl h2 span,.quote b span{position:relative;z-index:0;display:inline-block}
.ttl h2 span::before,.quote b span::before{content:"";position:absolute;z-index:-1;left:-3mm;right:-3mm;top:38%;bottom:4%;background:AMBER;border-radius:1.5mm;transform:rotate(-1.4deg)}
/* ---- الوش ---- */
.logo{position:absolute;top:36mm;left:50%;transform:translateX(-50%);width:76mm;height:76mm;border-radius:50%;overflow:hidden;background:BG;
  box-shadow:0 0 0 1.8mm #fff,0 0 0 2.6mm INK}
.logo img{width:100%;height:100%;display:block}
.ttl{position:absolute;top:128mm;left:0;right:0;text-align:center;line-height:1}
.ttl h1{margin:0;font-size:104pt;font-weight:800;line-height:1;color:INK;letter-spacing:-1pt}
.ttl h2{margin:10pt 0 0 0;font-size:48pt;font-weight:800;line-height:1.2;color:INK}
.sub{position:absolute;top:210mm;left:50%;transform:translateX(-50%);white-space:nowrap;background:INK;color:#fff;border-radius:40pt;
  padding:9pt 26pt 11pt 26pt;font-size:24pt;font-weight:800;line-height:1}
.sub i{display:inline-block;width:8pt;height:8pt;border-radius:50%;background:AMBER;margin:0 12pt;vertical-align:middle}
.who{position:absolute;bottom:22mm;left:0;right:0;text-align:center;line-height:1.2}
.who b{display:block;font-size:36pt;font-weight:800;color:INK}
.who span{font-size:17pt;font-weight:800;color:DEEP;letter-spacing:.5pt}
/* ---- الضهر ---- */
.quote{position:absolute;top:58mm;left:16mm;right:16mm;text-align:center}
.quote .qmk{display:block;font-size:70pt;line-height:1;color:AMBER;font-weight:800;direction:ltr;margin-bottom:6pt}
.quote p{margin:0;font-size:38pt;line-height:1.6;font-weight:800;color:INK}
.qrs{position:absolute;top:165mm;left:0;right:0;display:flex;justify-content:center;gap:24mm}
.qb{display:flex;flex-direction:column;align-items:center;gap:7pt}
.qb .qr{width:42mm;height:42mm;background:#fff;border-radius:10pt;padding:3mm;border:1.6pt solid INK}
.qb .qr img{width:100%;height:100%;display:block}
.qb b{font-size:19pt;font-weight:800;color:INK;line-height:1}
.foot{position:absolute;bottom:22mm;left:0;right:0;text-align:center;line-height:1.3}
.foot b{display:block;font-size:30pt;font-weight:800;color:INK}
.foot span{font-size:20pt;font-weight:800;color:DEEP}
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
