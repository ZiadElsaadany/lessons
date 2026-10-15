# -*- coding: utf-8 -*-
"""الغلاف الخارجي لمذكرة الترم الأول (وش + ضهر) — على ستايل أغلفة مذكرات المدرسين: صورة المدرس (assets/teacher_cut.png) قدام دايرة برتقالي، بيشاور على كارت كود، وحواليه روبوت/أقواس/شريحة AI؛ عنوان ضخم فوق واسم ضخم تحت. خلفية برتقالي فاتح، من غير أزرق.
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
WMC = "#fbd29f"                         # لون العلامة المائية (أغمق سنة من الخلفية)
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


ROBOT = f'''<svg viewBox="0 0 120 120"><line x1="60" y1="8" x2="60" y2="24" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
  <circle cx="60" cy="8" r="7" fill="{AMBER}" stroke="{INK}" stroke-width="4"/>
  <rect x="10" y="50" width="12" height="28" rx="6" fill="{INK}"/><rect x="98" y="50" width="12" height="28" rx="6" fill="{INK}"/>
  <rect x="18" y="24" width="84" height="80" rx="22" fill="#fff" stroke="{INK}" stroke-width="5"/>
  <rect x="30" y="40" width="60" height="38" rx="14" fill="{INK}"/>
  <circle cx="47" cy="59" r="8" fill="{AMBER}"/><circle cx="73" cy="59" r="8" fill="{AMBER}"/>
  <path d="M46 90 Q60 98 74 90" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></svg>'''
BRK = f'''<svg viewBox="0 0 120 80"><g fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round">
  <path d="M38 14 L12 40 L38 66"/><path d="M82 14 L108 40 L82 66"/></g><path d="M68 10 L52 70" stroke="{AMBER}" stroke-width="11" stroke-linecap="round"/></svg>'''
CHIP = f'''<svg viewBox="0 0 100 100"><g stroke="{INK}" stroke-width="5" stroke-linecap="round">
  <path d="M32 8v14M50 8v14M68 8v14M32 78v14M50 78v14M68 78v14M8 32h14M8 50h14M8 68h14M78 32h14M78 50h14M78 68h14"/></g>
  <rect x="20" y="20" width="60" height="60" rx="10" fill="{AMBER}" stroke="{INK}" stroke-width="5"/>
  <text x="50" y="62" text-anchor="middle" font-family="CodeMono" font-size="28" font-weight="700" fill="{INK}">AI</text></svg>'''


def front():
    return f'''<section class="cv front">
  <div class="wm">{{ }}</div>
  <div class="top"><span class="yr">{n(YEAR)}</span><img class="mini" src="assets/logo_warm.jpg" alt=""></div>
  <div class="ttl"><h1>البرمجة</h1><h2>والذكاء الاصطناعي</h2><div class="grade">الصف الثاني الثانوي <i></i> الترم الأول</div></div>
  <div class="disc"></div>
  <div class="robot">{ROBOT}</div>
  <div class="brk">{BRK}</div>
  <div class="chip">{CHIP}</div>
  <img class="me" src="assets/teacher_cut.png" alt="">
  <div class="card"><div class="cbar"><b></b><b></b><b></b></div><pre><k>if</k> study:
    success = <v>True</v></pre></div>
  <div class="name"><b>زياد السعدني</b><span>أستاذ البرمجة والذكاء الاصطناعي</span></div>
</section>'''


def back():
    return f'''<section class="cv back">
  <div class="wm">&lt;/&gt;</div>
  <div class="quote"><p>الكود مجرد أداة…</p><p class="q2">القوة الحقيقية<br>في طريقة تفكيرك.</p></div>
  <div class="disc d2"></div>
  <img class="me m2" src="assets/teacher_cut.png" alt="">
  <div class="qrs">
    <div class="qc"><div class="qr"><img src="assets/qr_fb_warm.svg" alt=""></div><b>فيسبوك</b></div>
    <div class="qc"><div class="qr"><img src="assets/qr_yt_warm.svg" alt=""></div><b>يوتيوب</b></div>
    <div class="wa"><small>واتساب</small><b>{n("01124840835")}</b></div>
  </div>
  <div class="bname"><img src="assets/logo_warm.jpg" alt=""><b>أكواد مع زياد</b></div>
</section>'''


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
.cv{position:relative;width:216mm;height:303mm;margin:0 auto 14pt auto;overflow:hidden;color:INK;background:PAPER;break-after:page;page-break-after:always}
.cv:last-child{break-after:auto;page-break-after:auto}
@media print{.cv{margin:0}}
.n{direction:ltr;unicode-bidi:isolate}
/* علامة مائية: أقواس كود ضخمة باهتة ورا كل حاجة */
.wm{position:absolute;left:-12mm;top:96mm;font-family:'CodeMono';font-size:360pt;line-height:1;color:WM;direction:ltr;letter-spacing:-20pt;white-space:nowrap}
.back .wm{left:auto;right:-20mm;top:150mm;font-size:300pt}
/* ---- الوش ---- */
.top{position:absolute;top:13mm;left:14mm;right:14mm;display:flex;align-items:center;justify-content:space-between;direction:ltr}
.mini{width:22mm;height:22mm;border-radius:50%;border:2pt solid INK}
.yr{font-family:'CodeMono';font-size:15pt;color:#fff;background:INK;border-radius:20pt;padding:5pt 14pt}
.ttl{position:absolute;top:33mm;left:0;right:0;text-align:center}
.ttl h1{margin:0;font-weight:900;font-size:108pt;line-height:1.05;color:INK}
.ttl h2{margin:6pt 0 0 0;font-weight:900;font-size:48pt;line-height:1.15;color:DEEP}
.grade{display:inline-block;margin-top:9pt;background:INK;color:#fff;border-radius:30pt;padding:5pt 20pt 7pt 20pt;font-weight:700;font-size:19pt;line-height:1.3}
.grade i{display:inline-block;width:7pt;height:7pt;border-radius:50%;background:AMBER;margin:0 9pt;vertical-align:middle}
.disc{position:absolute;left:58mm;top:130mm;width:136mm;height:136mm;border-radius:50%;background:AMBER}
.disc::after{content:"";position:absolute;inset:7mm;border-radius:50%;border:1.6pt dashed rgba(29,26,23,.45)}
.me{position:absolute;left:68mm;bottom:40mm;height:148mm}
.robot{position:absolute;left:162mm;top:124mm;width:36mm;transform:rotate(10deg)}
.brk{position:absolute;left:16mm;top:138mm;width:36mm;transform:rotate(-8deg)}
.chip{position:absolute;left:176mm;top:206mm;width:24mm;transform:rotate(-10deg)}
.robot svg,.brk svg,.chip svg{width:100%;display:block}
.card{position:absolute;left:12mm;top:180mm;width:58mm;background:#fff;border:2.2pt solid INK;border-radius:4mm;overflow:hidden;transform:rotate(-4deg);direction:ltr}
.cbar{height:6.5mm;background:INK;display:flex;align-items:center;gap:4pt;padding:0 7pt}
.cbar b{width:7pt;height:7pt;border-radius:50%;background:#fff}.cbar b:first-child{background:AMBER}
.card pre{margin:0;padding:4mm 4mm 4.5mm 4mm;font-family:'CodeMono';font-size:13pt;line-height:1.5;color:INK}
.card k{color:DEEP}.card v{color:GREEN}
.name{position:absolute;left:0;right:0;bottom:12mm;text-align:center;line-height:1}
.name b{display:block;font-weight:900;font-size:66pt;line-height:1.1;color:INK;text-shadow:2.60pt 0.00pt 0 PAPER,2.40pt 0.99pt 0 PAPER,1.84pt 1.84pt 0 PAPER,0.99pt 2.40pt 0 PAPER,0.00pt 2.60pt 0 PAPER,-0.99pt 2.40pt 0 PAPER,-1.84pt 1.84pt 0 PAPER,-2.40pt 0.99pt 0 PAPER,-2.60pt 0.00pt 0 PAPER,-2.40pt -0.99pt 0 PAPER,-1.84pt -1.84pt 0 PAPER,-0.99pt -2.40pt 0 PAPER,-0.00pt -2.60pt 0 PAPER,0.99pt -2.40pt 0 PAPER,1.84pt -1.84pt 0 PAPER,2.40pt -0.99pt 0 PAPER}
.name span{display:inline-block;margin-top:2pt;font-weight:700;font-size:17pt;color:#fff;background:DEEP;border-radius:20pt;padding:4pt 16pt 6pt 16pt;line-height:1.3}
/* ---- الضهر ---- */
.quote{position:absolute;top:24mm;left:14mm;right:14mm;text-align:center;line-height:1.15}
.quote p{margin:0;font-weight:900;font-size:44pt;color:INK}
.quote .q2{margin-top:8pt;font-size:50pt;color:DEEP}
.disc.d2{left:auto;right:-30mm;top:150mm;width:150mm;height:150mm}
.me.m2{left:auto;right:-6mm;bottom:0;height:150mm}
.qrs{position:absolute;left:14mm;top:128mm;width:70mm;display:flex;flex-direction:column;align-items:center;gap:7mm}
.qc{display:flex;flex-direction:column;align-items:center;gap:4pt;background:#fff;border:2.2pt solid INK;border-radius:5mm;padding:3mm 3mm 3.5mm 3mm}
.qc .qr{width:40mm;height:40mm}
.qc .qr img{width:100%;height:100%;display:block}
.qc b{font-weight:900;font-size:18pt;color:INK;line-height:1.2}
.wa{background:INK;color:#fff;border-radius:5mm;padding:3mm 6mm;text-align:center;line-height:1.2}
.wa small{display:block;font-weight:700;font-size:13pt;color:AMBER}
.wa b{font-family:'CodeMono';font-size:17pt}
.bname{position:absolute;left:14mm;bottom:12mm;display:flex;align-items:center;gap:8pt}
.bname img{width:18mm;height:18mm;border-radius:50%;border:2pt solid INK}
.bname b{font-weight:900;font-size:24pt;color:INK}
""".replace("BG", BG).replace("AMBER", AMBER).replace("INK", INK).replace("DEEP", DEEP).replace("GREEN", GREEN).replace("PAPER", PAPER).replace("WM", WMC)


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
