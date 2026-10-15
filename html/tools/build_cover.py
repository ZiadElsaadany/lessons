# -*- coding: utf-8 -*-
"""الغلاف الخارجي لمذكرة الترم الأول (وش + ضهر) — على ستايل أغلفة مذكرات المدرسين: صورة المدرس (assets/teacher_cut.png) قدام دايرة برتقالي، بيشاور على كارت كود، وحواليه روبوت/أقواس/شريحة AI؛ عنوان ضخم فوق واسم ضخم تحت. خلفية برتقالي فاتح، من غير أزرق.
- صورة المدرس وضلّها: tools/teacher_photo.py (حواف نضيفة + طبعة <AI/> على التيشيرت + fade تحت).
- خط Cairo: نسخ ثابتة fonts/Cairo-Black.ttf و Cairo-Bold.ttf (من Cairo.ttf المتغيّر) عشان يتطبع TrueType.

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
PAPER = "#ffe3bf"                       # خلفية برتقالي فاتح
WMC = "#fdd8a9"                         # لون العلامة المائية (أغمق سنة صغيرة من الخلفية)
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


LW = 0.9                               # سُمك الخط الموحّد لكل الرسومات (مم) — كل الـSVG هنا وحدتها مم


def robot():
    w = LW
    return (f'<svg viewBox="0 0 34 36"><g stroke="{INK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">'
            f'<line x1="17" y1="3.6" x2="17" y2="8.5"/><circle cx="17" cy="2.6" r="1.9" fill="{AMBER}"/>'
            f'<rect x="1.2" y="16" width="3.4" height="9" rx="1.7" fill="{INK}"/><rect x="29.4" y="16" width="3.4" height="9" rx="1.7" fill="{INK}"/>'
            f'<rect x="4.6" y="8.5" width="24.8" height="24" rx="6.5" fill="#fff"/>'
            f'<rect x="8.2" y="13" width="17.6" height="11" rx="3.8" fill="{INK}"/>'
            f'<path d="M13 28.2 Q17 30.6 21 28.2" fill="none"/></g>'
            f'<circle cx="13.2" cy="18.5" r="2.2" fill="{AMBER}"/><circle cx="20.8" cy="18.5" r="2.2" fill="{AMBER}"/></svg>')


def brackets():
    w = 2.6
    return (f'<svg viewBox="0 0 34 26"><g fill="none" stroke="{INK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M10 5 L2.5 13 L10 21"/><path d="M24 5 L31.5 13 L24 21"/></g>'
            f'<path d="M19.6 3.6 L14.4 22.4" stroke="{AMBER}" stroke-width="{w}" stroke-linecap="round"/></svg>')


def sparks(rot=0):
    """3 شرطات «لمعة» صغيرة جنب الرسمة."""
    return (f'<svg viewBox="0 0 12 12" style="transform:rotate({rot}deg)"><g stroke="{AMBER}" stroke-width="1.1" stroke-linecap="round">'
            f'<path d="M2 7.5 L4.6 6.4"/><path d="M5.2 3.4 L6.6 1"/><path d="M8.2 5.2 L10.8 3.8"/></g></svg>')


def dots(cols, rows, gap=3.4):
    pts = "".join(f'<circle cx="{1 + c * gap:.1f}" cy="{1 + r * gap:.1f}" r=".55"/>' for r in range(rows) for c in range(cols))
    return f'<svg viewBox="0 0 {2 + (cols - 1) * gap:.1f} {2 + (rows - 1) * gap:.1f}" fill="rgba(200,106,0,.30)">{pts}</svg>'


def deco(side):
    """أشكال الخلفية زي المرجع: بلوكات بأركان مدوّرة متداخلة على الشمال، ومستطيل مفرّغ + بارات على اليمين،
    دواير مفرّغة، ومجموعات نقط — كلها برتقالي شفاف ومن الأطراف بس."""
    if side == "front":
        shapes = "c1 b1 b2 b3 b4 o1 o2 p1 p2 r1 r2 r3"
        dts = f'<div class="dt t1">{dots(6, 5)}</div><div class="dt t2">{dots(5, 4)}</div><div class="dt t3">{dots(6, 5)}</div>'
    else:
        shapes = "c1 b1 b2 o1 p1 r1 r3"
        dts = f'<div class="dt t1">{dots(6, 5)}</div><div class="dt t2">{dots(5, 4)}</div>'
    return "".join(f'<div class="dc {k}"></div>' for k in shapes.split()) + dts


def chip():
    w = LW
    pins = "".join(f'M{x} 1.2v3M{x} 20.8v3M1.2 {x}h3M20.8 {x}h3' for x in (8, 12.5, 17))
    return (f'<svg viewBox="0 0 25 25"><path d="{pins}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<rect x="4.4" y="4.4" width="16.2" height="16.2" rx="3" fill="{AMBER}" stroke="{INK}" stroke-width="{w}"/>'
            f'<text x="12.5" y="15.4" text-anchor="middle" font-family="CodeMono" font-size="7.2" fill="{INK}">AI</text></svg>')


def ring():
    """الخط المتقطّع حوالين الدايرة: SVG بشَرط منتظمة ونهايات مدوّرة (الـborder dashed بيطلع مش منتظم)."""
    return ('<svg class="ring" viewBox="0 0 136 136"><circle cx="68" cy="68" r="61" fill="none" stroke="rgba(29,26,23,.38)" '
            'stroke-width=".55" stroke-linecap="round" stroke-dasharray="2.2 2.6"/></svg>')


# صورة المدرس + ضلّها (teacher_photo.py): الضل متعمل بربع الدقة وحواليه pad=160px من مقاس الصورة الكاملة
PH_W, PH_H, SH_W, SH_H, SH_PAD = 1612, 2334, 1932, 2652, 160


def photo(cls):
    return (f'<div class="ph {cls}"><img class="sh" src="assets/teacher_shadow.png" alt="">'
            f'<img class="me" src="assets/teacher_cut.png" alt=""></div>')


def front():
    return f'''<section class="cv front">
  {deco("front")}
  <div class="top"><span class="yr">{n(YEAR)}</span><img class="mini" src="assets/logo_warm.jpg" alt=""></div>
  <div class="ttl"><h1>البرمجة</h1><h2>والذكاء الاصطناعي</h2><div class="grade">الصف الثاني الثانوي <i></i> الترم الأول</div></div>
  <div class="halo"></div>
  <div class="disc"><div class="amb"></div>{ring()}</div>
  <div class="ill robot">{robot()}</div><div class="spk s1">{sparks(0)}</div>
  <div class="ill brk">{brackets()}</div>
  <div class="ill chip">{chip()}</div><div class="spk s3">{sparks(10)}</div>
  <div class="spk s2">{sparks(-60)}</div>
  {photo("pf")}
  <div class="card"><div class="cbar"><b></b><b></b><b></b></div><pre><k>if</k> study:
    success = <v>True</v></pre></div>
  <div class="name"><b>زياد السعدني</b><div class="sub"><i></i><span>أستاذ البرمجة والذكاء الاصطناعي</span><i></i></div></div>
</section>'''


def back():
    return f'''<section class="cv back">
  {deco("back")}
  <div class="quote"><p>الكود مجرد أداة…</p><p class="q2">القوة الحقيقية<br>في طريقة تفكيرك.</p></div>
  <div class="halo h2"></div>
  <div class="disc d2"><div class="amb"></div>{ring()}</div>
  {photo("pb")}
  <div class="qrs">
    <div class="qc"><div class="qr"><img src="assets/qr_fb_warm.svg" alt=""></div><b>فيسبوك</b></div>
    <div class="qc"><div class="qr"><img src="assets/qr_yt_warm.svg" alt=""></div><b>يوتيوب</b></div>
    <div class="wa"><small>واتساب</small><b>{n("01124840835")}</b></div>
  </div>
  <div class="bname"><img src="assets/logo_warm.jpg" alt=""><b>أكواد مع زياد</b></div>
</section>'''


def photo_css(cls, left, bottom, height, right=None):
    w = height * PH_W / PH_H
    k = height / PH_H                                   # مم لكل بكسل
    pos = f"right:{right}mm" if right is not None else f"left:{left}mm"
    return (f".{cls}{{position:absolute;{pos};bottom:{bottom}mm;width:{w:.2f}mm;height:{height}mm}}"
            f".{cls} .sh{{left:{-SH_PAD * k + 2.6:.2f}mm;top:{-SH_PAD * k + 2.2:.2f}mm;width:{SH_W * k:.2f}mm;height:{SH_H * k:.2f}mm}}")


CSS = r"""
@font-face{font-family:'Baloo Bhaijaan 2';font-weight:400 800;src:url(fonts/BalooBhaijaan2.ttf) format('truetype')}
@font-face{font-family:'CairoX';font-weight:900;src:url(fonts/Cairo-Black.ttf) format('truetype')}
@font-face{font-family:'CairoX';font-weight:700;src:url(fonts/Cairo-Bold.ttf) format('truetype')}
@font-face{font-family:'CodeMono';src:url(fonts/DejaVuSansMono-Bold.ttf) format('truetype');unicode-range:U+0000-024F}
@page{size:216mm 303mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#bdbdbd;padding:14pt 0;font-family:'CairoX','Baloo Bhaijaan 2';direction:rtl}
@media print{body{background:#fff;padding:0}}
.cv{position:relative;width:216mm;height:303mm;margin:0 auto 14pt auto;overflow:hidden;color:INK;break-after:page;page-break-after:always;
  background:radial-gradient(65% 42% at 50% 60%,#fff2df 0%,rgba(255,242,223,0) 100%),linear-gradient(180deg,#ffe8cb 0%,PAPER 60%,#ffdcb2 100%)}
.cv:last-child{break-after:auto;page-break-after:auto}
@media print{.cv{margin:0}}
.n{direction:ltr;unicode-bidi:isolate}
/* أشكال الخلفية (زي المرجع): بلوكات مدوّرة بتدرّج خفيف + خطوط مفرّغة — من الأطراف بس */
.dc{position:absolute;pointer-events:none}
.dc.b1,.dc.b2,.dc.b3,.dc.b4,.dc.r1,.dc.r2,.dc.r3,.dc.p1,.dc.p2{background:linear-gradient(135deg,rgba(249,142,3,.16),rgba(249,142,3,.07))}
.front .c1{left:-38mm;top:32mm;width:72mm;height:72mm;border-radius:50%;background:radial-gradient(circle at 65% 40%,rgba(249,142,3,.13),rgba(249,142,3,.05))}
.front .b1{left:-14mm;top:110mm;width:66mm;height:40mm;border-radius:13mm}
.front .b2{left:-26mm;top:140mm;width:52mm;height:58mm;border-radius:15mm;opacity:.85}
.front .b3{left:-8mm;top:204mm;width:44mm;height:30mm;border-radius:11mm;opacity:.8}
.front .b4{left:-30mm;bottom:-22mm;width:76mm;height:62mm;border-radius:16mm}
.front .o1{left:-34mm;top:228mm;width:70mm;height:70mm;border-radius:50%;border:.45mm solid rgba(200,106,0,.22)}
.front .o2{right:-26mm;top:86mm;width:62mm;height:128mm;border-radius:30mm;border:.45mm solid rgba(200,106,0,.22)}
.front .p1{left:30mm;top:246mm;width:24mm;height:6.5mm;border-radius:3.25mm}
.front .p2{right:16mm;top:200mm;width:22mm;height:6mm;border-radius:3mm;opacity:.8}
.front .r1{right:-22mm;top:108mm;width:58mm;height:24mm;border-radius:12mm}
.front .r2{right:-14mm;top:150mm;width:40mm;height:52mm;border-radius:13mm;opacity:.8}
.front .r3{right:-20mm;bottom:-16mm;width:68mm;height:52mm;border-radius:15mm}
.back .c1{right:-40mm;top:-30mm;width:90mm;height:90mm;border-radius:50%;background:radial-gradient(circle at 40% 60%,rgba(249,142,3,.13),rgba(249,142,3,.05))}
.back .b1{left:-16mm;top:92mm;width:54mm;height:34mm;border-radius:12mm}
.back .b2{left:-24mm;top:118mm;width:40mm;height:60mm;border-radius:13mm;opacity:.8}
.back .o1{left:-30mm;top:200mm;width:64mm;height:64mm;border-radius:50%;border:.45mm solid rgba(200,106,0,.22)}
.back .p1{left:22mm;top:268mm;width:22mm;height:6mm;border-radius:3mm}
.back .r1{right:-18mm;top:70mm;width:56mm;height:22mm;border-radius:11mm}
.back .r3{left:-14mm;bottom:-24mm;width:70mm;height:56mm;border-radius:15mm}
.dt{position:absolute}.dt svg{width:100%;height:100%;display:block}
.front .t1{right:9mm;top:58mm;width:19mm;height:15.6mm}
.front .t2{left:7mm;top:104mm;width:15.6mm;height:12.2mm}
.front .t3{right:9mm;top:246mm;width:19mm;height:15.6mm}
.back .t1{right:12mm;top:110mm;width:19mm;height:15.6mm}
.back .t2{left:9mm;top:20mm;width:15.6mm;height:12.2mm}
/* ---- الوش ---- */
.top{position:absolute;top:14mm;left:15mm;right:15mm;height:21mm;display:flex;align-items:center;justify-content:space-between;direction:ltr}
.mini{width:21mm;height:21mm;border-radius:50%;border:1.1mm solid #fff;outline:LWmm solid INK;display:block}
.yr{font-weight:700;font-size:15pt;color:#fff;background:INK;border-radius:5mm;height:9.5mm;padding:0 5.5mm 1mm 5.5mm;display:flex;align-items:center;word-spacing:2pt}
.ttl{position:absolute;top:34mm;left:0;right:0;text-align:center}
.ttl h1{margin:0;font-weight:900;font-size:108pt;line-height:1;color:INK;text-shadow:0 .9mm 0 rgba(249,142,3,.22),0 1.8mm 0 rgba(249,142,3,.12)}
.ttl h2{margin:12pt 0 0 0;font-weight:900;font-size:46pt;line-height:1.1;color:DEEP;text-shadow:0 .7mm 0 rgba(130,60,0,.22),0 1.4mm 0 rgba(249,142,3,.15)}
.grade{display:inline-flex;align-items:center;height:11mm;margin-top:15pt;background:INK;color:#fff;border-radius:5.5mm;padding:0 7mm 1.2mm 7mm;font-weight:700;font-size:18pt}
.grade i{display:inline-block;width:2.2mm;height:2.2mm;border-radius:50%;background:AMBER;margin:1.2mm 3.5mm 0 3.5mm}
/* الدايرة: تدرّج برتقالي خفيف + نور هادي ورا الراس + خط متقطّع منتظم */
.halo{position:absolute;left:49mm;top:120mm;width:160mm;height:160mm;border-radius:50%;background:radial-gradient(closest-side,rgba(255,170,60,.42) 0%,rgba(255,170,60,.42) 80%,rgba(255,170,60,0) 100%)}
.halo.h2{left:auto;right:-42mm;top:138mm;width:174mm;height:174mm}
.disc{position:absolute;left:61mm;top:132mm;width:136mm;height:136mm;border-radius:50%;
  background:radial-gradient(circle at 38% 30%,#ffa83d 0%,AMBER 52%,#ea7d00 100%)}
.disc .amb{position:absolute;left:22%;top:4%;width:60%;height:50%;border-radius:50%;background:radial-gradient(closest-side,rgba(255,236,200,.45),rgba(255,236,200,0))}
.disc .ring{position:absolute;inset:0;width:100%;height:100%}
.ph .me,.ph .sh{position:absolute;display:block}
.ph .me{left:0;top:0;width:100%;height:100%}
PHOTO_CSS
/* الرسومات: نفس سُمك الخط ونفس الأركان، ومسافة حوالين كل واحدة */
.ill svg{width:100%;height:100%;display:block}
.robot{position:absolute;left:167mm;top:127mm;width:31mm;height:33mm;transform:rotate(8deg)}
.brk{position:absolute;left:16mm;top:140mm;width:32mm;height:24.5mm;transform:rotate(-6deg)}
.spk{position:absolute;width:10mm;height:10mm}.spk svg{width:100%;height:100%;display:block}
.s1{left:196mm;top:122mm}.s2{left:44mm;top:169mm}.s3{left:194mm;top:208mm}
.chip{position:absolute;left:177mm;top:217mm;width:22mm;height:22mm;transform:rotate(-8deg)}
.card{position:absolute;left:13mm;top:181mm;width:57mm;background:#fff;border:LWmm solid INK;border-radius:3mm;overflow:hidden;transform:rotate(-4deg);direction:ltr;box-shadow:1.3mm 1.5mm 0 rgba(29,26,23,.16)}
.cbar{height:6mm;background:INK;display:flex;align-items:center;gap:1.6mm;padding:0 2.6mm}
.cbar b{width:2.2mm;height:2.2mm;border-radius:50%;background:#fff}.cbar b:first-child{background:AMBER}
.card pre{margin:0;padding:3.6mm 4mm 4mm 4mm;font-family:'CodeMono';font-size:12.5pt;line-height:1.5;color:INK}
.card k{color:DEEP}.card v{color:GREEN}
.name{position:absolute;left:0;right:0;bottom:14mm;text-align:center;line-height:1}
.name b{display:block;font-weight:900;font-size:54pt;line-height:1.15;color:INK;text-shadow:0 .8mm 0 rgba(249,142,3,.25)}
.name .sub{display:flex;align-items:center;justify-content:center;gap:4mm;margin-top:3.5mm}
.name .sub i{width:26mm;height:.7mm;border-radius:.35mm;background:AMBER}
.name span{display:inline-flex;align-items:center;height:10mm;padding:0 6mm 1mm 6mm;font-weight:700;font-size:16pt;color:#fff;background:DEEP;border-radius:5mm}
/* ---- الضهر ---- */
.quote{position:absolute;top:26mm;left:15mm;right:15mm;text-align:center;line-height:1.15}
.quote p{margin:0;font-weight:900;font-size:42pt;color:INK;text-shadow:0 .8mm 0 rgba(249,142,3,.22)}
.quote .q2{margin-top:10pt;font-size:50pt;color:DEEP;text-shadow:0 .7mm 0 rgba(130,60,0,.22),0 1.4mm 0 rgba(249,142,3,.15)}
.disc.d2{left:auto;right:-30mm;top:150mm;width:150mm;height:150mm}
.qrs{position:absolute;left:15mm;top:128mm;width:70mm;display:flex;flex-direction:column;align-items:center;gap:7mm}
.qc{display:flex;flex-direction:column;align-items:center;gap:1.5mm;background:#fff;border:LWmm solid INK;border-radius:4mm;padding:3mm 3mm 3.5mm 3mm;box-shadow:1.3mm 1.5mm 0 rgba(29,26,23,.14)}
.qc .qr{width:40mm;height:40mm}
.qc .qr img{width:100%;height:100%;display:block}
.qc b{font-weight:900;font-size:17pt;color:INK;line-height:1.2}
.wa{background:INK;color:#fff;border-radius:4mm;padding:3mm 6mm;text-align:center;line-height:1.2}
.wa small{display:block;font-weight:700;font-size:13pt;color:AMBER}
.wa b{font-family:'CodeMono';font-size:16pt}
.bname{position:absolute;left:15mm;bottom:14mm;display:flex;align-items:center;gap:3mm}
.bname img{width:17mm;height:17mm;border-radius:50%;border:.9mm solid #fff;outline:LWmm solid INK}
.bname b{font-weight:900;font-size:23pt;color:INK}
""".replace("PHOTO_CSS", photo_css("pf", 74, 47, 140) + photo_css("pb", None, 0, 158, right=-14)) \
   .replace("BG", BG).replace("AMBER", AMBER).replace("INK", INK).replace("DEEP", DEEP).replace("GREEN", GREEN) \
   .replace("PAPER", PAPER).replace("WM", WMC).replace("LWmm", f"{LW}mm")


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
