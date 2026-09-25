# -*- coding: utf-8 -*-
"""الغلاف الخارجي لمذكرة الترم الأول (وش + ضهر) — نفس روح غلاف «الجزء العملي» (خلفية كحلي بخطوط دواير، لوجو في مربع).

    python3 tools/build_cover.py        ← يكتب html/term1_cover.html

- كل صفحة 216×303 مم = A4 + هامش قص (bleed) 3 مم من كل ناحية؛ الكلام كله جوه منطقة آمنة (≥ 12 مم من حرف الورقة).
- الطباعة: Chromium ← «حجم الصفحة من CSS» + «Background graphics» (أو page.pdf(prefer_css_page_size=True, print_background=True)).
- الـQR: assets/qr_fb.svg و assets/qr_yt.svg (اتعملوا بـsegno واتقروا بقارئ QR).
"""
import os, random

TOOLS = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(TOOLS), "term1_cover.html")
W, H = 216, 303                       # مم
YEAR = "2026 / 2027"
UNITS = [
    (1, "تكنولوجيا المعلومات والمجتمع", ["تطور تكنولوجيا المعلومات والتحول الاجتماعي", "كيف يعمل الذكاء الاصطناعي",
                                          "الذكاء الاصطناعي في الحياة اليومية والصناعة", "القضايا الأخلاقية المتعلقة بالذكاء الاصطناعي"]),
    (2, "الأمن السيبراني", ["تقنيات التشفير والمصادقة", "تصميم أمان الشبكات", "الاستجابة للحوادث وإدارة المخاطر"]),
    (3, "تطبيقات الويب", ["البنية العامة لتطبيقات الويب", "طرق اتصال تطبيقات الويب", "أساسيات تقنية الواجهة الأمامية"]),
    (4, "تصميم الويب والوسائط", ["أنواع الوسائط وخصائصها", "تصميم المعلومات وتجربة المستخدم للمواقع الإلكترونية",
                                  "طرق تقييم المواقع الإلكترونية", "عملية التحسين التكراري للمواقع الإلكترونية"]),
]


def circuits(seed):
    """خطوط دواير (زي اللوحة الإلكترونية) على الأطراف — بتسيب النص فاضي للكلام."""
    rnd = random.Random(seed)
    out = []
    for k in range(34):
        side = rnd.choice("LRTB")
        if side in "LR":
            y = rnd.uniform(8, H - 8)
            x0 = 0 if side == "L" else W
            d = 1 if side == "L" else -1
            l1, l2 = rnd.uniform(10, 45), rnd.uniform(6, 22)
            dy = rnd.choice([-1, 1]) * rnd.uniform(4, 14)
            pts = [(x0, y), (x0 + d * l1, y), (x0 + d * (l1 + abs(dy)), y + dy), (x0 + d * (l1 + abs(dy) + l2), y + dy)]
        else:
            x = rnd.uniform(8, W - 8)
            y0 = 0 if side == "T" else H
            d = 1 if side == "T" else -1
            l1, l2 = rnd.uniform(10, 40), rnd.uniform(6, 20)
            dx = rnd.choice([-1, 1]) * rnd.uniform(4, 14)
            pts = [(x, y0), (x, y0 + d * l1), (x + dx, y0 + d * (l1 + abs(dx))), (x + dx, y0 + d * (l1 + abs(dx) + l2))]
        path = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        op = rnd.uniform(.18, .42)
        out.append(f'<path d="{path}" stroke="#3d7bff" stroke-opacity="{op:.2f}" stroke-width=".35" fill="none"/>'
                   f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r=".9" fill="#5b93ff" fill-opacity="{op + .25:.2f}"/>')
    # نقط منوّرة متفرقة
    for k in range(40):
        out.append(f'<circle cx="{rnd.uniform(0, W):.1f}" cy="{rnd.uniform(0, H):.1f}" r="{rnd.uniform(.3, .8):.2f}" fill="#7fb0ff" fill-opacity="{rnd.uniform(.15, .5):.2f}"/>')
    return f'<svg class="circ" viewBox="0 0 {W} {H}" preserveAspectRatio="none">{"".join(out)}</svg>'


def streaks(y0, seed):
    rnd = random.Random(seed)
    s = []
    for k in range(9):
        y = y0 + k * 2.2 + rnd.uniform(-.5, .5)
        a = rnd.uniform(0, 60); b = rnd.uniform(W - 60, W)
        s.append(f'<line x1="{a:.1f}" y1="{y:.1f}" x2="{b:.1f}" y2="{y:.1f}" stroke="url(#stk)" stroke-width="{rnd.uniform(.15, .45):.2f}"/>')
    return (f'<svg class="stk" viewBox="0 0 {W} {H}" preserveAspectRatio="none"><defs><linearGradient id="stk" x1="0" x2="1">'
            '<stop offset="0" stop-color="#6fa3ff" stop-opacity="0"/><stop offset=".5" stop-color="#9cc2ff" stop-opacity=".55"/>'
            f'<stop offset="1" stop-color="#6fa3ff" stop-opacity="0"/></linearGradient></defs>{"".join(s)}</svg>')


# ---- رسومات صغيرة للفصول الأربعة (SVG)
ILL = {
    1: '''<svg viewBox="0 0 120 80"><g stroke="#8fb6ff" stroke-width="1.6" opacity=".9">
        <path d="M22 18 L60 12 M22 18 L60 40 M22 40 L60 12 M22 40 L60 40 M22 40 L60 68 M22 62 L60 40 M22 62 L60 68 M60 12 L98 28 M60 40 L98 28 M60 40 L98 54 M60 68 L98 54 M60 12 L98 54 M60 68 L98 28"/></g>
        <g fill="#3fa0ff"><circle cx="22" cy="18" r="6"/><circle cx="22" cy="40" r="6"/><circle cx="22" cy="62" r="6"/><circle cx="60" cy="12" r="6"/><circle cx="60" cy="40" r="6"/><circle cx="60" cy="68" r="6"/></g>
        <g fill="#f0b43c"><circle cx="98" cy="28" r="7"/><circle cx="98" cy="54" r="7"/></g></svg>''',
    2: '''<svg viewBox="0 0 120 80"><path d="M60 6 L90 17 V38 C90 56 77 68 60 75 C43 68 30 56 30 38 V17 Z" fill="#12306e" stroke="#5b93ff" stroke-width="2.4"/>
        <rect x="47" y="36" width="26" height="20" rx="3" fill="#f0b43c"/><path d="M52 36 V30 A8 8 0 0 1 68 30 V36" fill="none" stroke="#f0b43c" stroke-width="3.2"/>
        <circle cx="60" cy="45" r="2.6" fill="#12306e"/><path d="M60 46 V51" stroke="#12306e" stroke-width="2.4"/>
        <g stroke="#8fb6ff" stroke-width="1.4" opacity=".75"><path d="M8 30 H24 M8 42 H24 M96 30 H112 M96 42 H112"/></g></svg>''',
    3: '''<svg viewBox="0 0 120 80"><rect x="14" y="8" width="92" height="64" rx="6" fill="#12306e" stroke="#5b93ff" stroke-width="2"/>
        <path d="M14 22 H106" stroke="#5b93ff" stroke-width="1.6"/><circle cx="23" cy="15" r="2.4" fill="#ff6b6b"/><circle cx="31" cy="15" r="2.4" fill="#f0b43c"/><circle cx="39" cy="15" r="2.4" fill="#5fd38d"/>
        <path d="M24 60 L40 40 L54 50 L70 30 L84 44 L96 34" fill="none" stroke="#f0b43c" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
        <path d="M24 64 H96" stroke="#8fb6ff" stroke-width="1.2" opacity=".7"/></svg>''',
    4: '''<svg viewBox="0 0 120 80"><rect x="20" y="6" width="80" height="68" rx="6" fill="#12306e" stroke="#5b93ff" stroke-width="2"/>
        <rect x="28" y="14" width="64" height="12" rx="2" fill="#f0b43c"/><rect x="28" y="31" width="30" height="24" rx="2" fill="#2a5bbf"/>
        <path d="M62 33 H92 M62 39 H92 M62 45 H84 M62 51 H88" stroke="#8fb6ff" stroke-width="2.4" stroke-linecap="round"/>
        <rect x="28" y="60" width="26" height="8" rx="4" fill="#3fa0ff"/><rect x="58" y="60" width="16" height="8" rx="4" fill="#8fb6ff" opacity=".6"/></svg>''',
}
ICON_BOOK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H2z"/><path d="M22 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z"/></svg>'
ICON_DOC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/></svg>'
ICON_Q = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14"/><circle cx="12" cy="17.3" r=".6" fill="currentColor"/></svg>'


def n(t): return f'<span class="n">{t}</span>'


def qr_bar():
    return f'''<div class="qbar">
    <div class="qb"><div class="qr"><img src="assets/qr_fb.svg" alt=""></div><b>فيسبوك</b></div>
    <div class="qm"><b>تابعنا وامسح الكود بكاميرا الموبايل</b>
      <span>واتساب: {n("01124840835")}</span>
      <span>{n("fb.com/61592749346697")}</span><span>{n("youtube.com/@ZiadElsa3dany")}</span></div>
    <div class="qb"><div class="qr"><img src="assets/qr_yt.svg" alt=""></div><b>يوتيوب</b></div>
  </div>'''


def front():
    tiles = "".join(f'<div class="il"><div class="ic">{ILL[u]}</div><small>الفصل {n(u)}</small><b>{t}</b></div>' for u, t, _ in UNITS)
    return f'''<section class="cv front">
  {circuits(7)}{streaks(128, 3)}
  <div class="glow"></div>
  <div class="logo"><img src="assets/logo.jpg" alt=""></div>
  <div class="ttl"><small>مذكرة</small><h1>البرمجة</h1><h2>والذكاء الاصطناعي</h2></div>
  <div class="pills"><span class="gold">شرح + بنك أسئلة</span><span class="pl">الصف الثاني الثانوي <i>•</i> الترم الأول</span><span class="pl yr">{n(YEAR)}</span></div>
  <div class="stats"><div><i>{ICON_BOOK}</i><b>{n(4)} فصول</b></div><div><i>{ICON_DOC}</i><b>{n(14)} درس</b></div><div><i>{ICON_Q}</i><b>بنك أسئلة لكل درس</b></div></div>
  <div class="ills">{tiles}</div>
  <div class="who"><b>أ/ زياد السعدني</b><span>أكواد مع زياد</span></div>
  {qr_bar()}
</section>'''


def back():
    units = "".join(f'<div class="bu"><div class="bh"><span class="bn">{n(u)}</span><b>{t}</b></div><ul>'
                    + "".join(f'<li><span class="lid">{n(f"{u}-{k + 1}")}</span>{x}</li>' for k, x in enumerate(ls)) + '</ul></div>' for u, t, ls in UNITS)
    return f'''<section class="cv back">
  {circuits(11)}
  <div class="glow g2"></div>
  <div class="blogo"><img src="assets/logo.jpg" alt=""></div>
  <div class="quote"><span class="qmk">”</span><p>الكود مجرد أداة…<br><b>القوة الحقيقية في طريقة تفكيرك.</b></p></div>
  <div class="inside"><h3>في المذكرة دي</h3><div class="bus">{units}</div></div>
  <div class="who bwho"><b>أ/ زياد السعدني</b><span>أكواد مع زياد</span></div>
  {qr_bar()}
</section>'''


CSS = r"""
@font-face{font-family:'Baloo Bhaijaan 2';font-weight:400 800;src:url(fonts/BalooBhaijaan2.ttf) format('truetype')}
@page{size:216mm 303mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#d9dee6;padding:14pt 0;font-family:'Baloo Bhaijaan 2';direction:rtl}
@media print{body{background:#fff;padding:0}}
.cv{position:relative;width:216mm;height:303mm;margin:0 auto 14pt auto;overflow:hidden;color:#fff;
  background:radial-gradient(90% 55% at 50% 30%,#0f2f7a 0%,#082063 35%,#041448 70%,#020c2e 100%);break-after:page;page-break-after:always}
.cv:last-child{break-after:auto;page-break-after:auto}
@media print{.cv{margin:0}}
.n{direction:ltr;unicode-bidi:isolate}
.circ,.stk{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.glow{position:absolute;left:50%;top:40mm;width:150mm;height:150mm;transform:translateX(-50%);border-radius:50%;background:radial-gradient(closest-side,rgba(63,140,255,.28),rgba(63,140,255,0));pointer-events:none}
/* ---- الوش ---- */
.logo{position:absolute;top:15mm;left:50%;transform:translateX(-50%);width:43mm;height:43mm;border-radius:10mm;overflow:hidden;
  box-shadow:0 0 0 1.3mm rgba(91,147,255,.45),0 0 9mm rgba(63,140,255,.55)}
.logo img{width:100%;height:100%;display:block}
.ttl{position:absolute;top:65mm;left:0;right:0;text-align:center;line-height:1}
.ttl small{display:block;font-size:20pt;font-weight:700;color:#e6eeff}
.ttl h1{margin:4pt 0 0 0;font-size:62pt;font-weight:800;line-height:1.05;color:#fff;text-shadow:0 0 18pt rgba(120,170,255,.55)}
.ttl h2{margin:2pt 0 0 0;font-size:31pt;font-weight:800;line-height:1.2;background:linear-gradient(90deg,#9fc4ff,#5b93ff 55%,#bcd6ff);-webkit-background-clip:text;background-clip:text;color:transparent}
.pills{position:absolute;top:119mm;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:8pt}
.pills span{border-radius:30pt;font-weight:800;line-height:1}
.pills .gold{background:linear-gradient(180deg,#ffc24d,#e29433);color:#1a1300;font-size:15pt;padding:8pt 26pt;box-shadow:0 3pt 10pt rgba(226,148,51,.4)}
.pills .pl{background:rgba(10,28,80,.75);border:1pt solid rgba(120,165,255,.55);color:#fff;font-size:14pt;padding:8pt 22pt}
.pills .pl i{font-style:normal;color:#f0b43c;margin:0 4pt}
.pills .yr{font-size:12.5pt;padding:7pt 20pt}
.stats{position:absolute;top:163mm;left:17mm;right:17mm;display:grid;grid-template-columns:repeat(3,1fr);gap:9pt}
.stats div{background:rgba(12,34,92,.7);border:1pt solid rgba(120,165,255,.45);border-radius:10pt;padding:9pt 6pt;text-align:center}
.stats i{display:block;width:17pt;height:17pt;margin:0 auto 4pt auto;color:#8fb6ff}
.stats i svg{width:100%;height:100%;display:block}
.stats b{font-size:13pt;font-weight:800;color:#fff;line-height:1.2}
.ills{position:absolute;top:189mm;left:17mm;right:17mm;display:grid;grid-template-columns:repeat(4,1fr);gap:9pt}
.il{text-align:center}
.il .ic{background:rgba(8,26,78,.75);border:1pt solid rgba(120,165,255,.4);border-radius:9pt;padding:6pt 4pt;height:25mm;display:flex;align-items:center;justify-content:center}
.il .ic svg{width:100%;height:100%}
.il small{display:block;margin-top:5pt;font-size:8.5pt;color:#f0b43c;font-weight:700;line-height:1}
.il b{display:block;font-size:9.8pt;font-weight:800;color:#e6eeff;line-height:1.3;margin-top:2pt}
.who{position:absolute;top:230mm;left:0;right:0;text-align:center;line-height:1.2}
.who b{display:block;font-size:26pt;font-weight:800;color:#fff}
.who span{font-size:13pt;font-weight:700;color:#8fb6ff}
.bwho{top:229mm}
.bwho b{font-size:20pt}
.bwho span{font-size:11pt}
.qbar{position:absolute;left:14mm;right:14mm;bottom:13mm;height:31mm;display:flex;align-items:center;justify-content:space-between;
  background:rgba(4,16,56,.78);border:1pt solid rgba(120,165,255,.45);border-radius:12pt;padding:0 10pt}
.qb{display:flex;flex-direction:column;align-items:center;gap:3pt}
.qb .qr{width:22mm;height:22mm;background:#fff;border-radius:7pt;padding:2mm}
.qb .qr img{width:100%;height:100%;display:block}
.qb b{font-size:9.5pt;font-weight:800;color:#f0b43c;line-height:1}
.qm{flex:1;display:flex;flex-direction:column;align-items:center;gap:1pt;line-height:1.35}
.qm b{font-size:11pt;font-weight:800;color:#fff;margin-bottom:2pt}
.qm span{font-size:10pt;font-weight:700;color:#c9d6f2}
/* ---- الضهر ---- */
.blogo{position:absolute;top:18mm;left:50%;transform:translateX(-50%);width:30mm;height:30mm;border-radius:8mm;overflow:hidden;box-shadow:0 0 0 1mm rgba(91,147,255,.45),0 0 7mm rgba(63,140,255,.5)}
.blogo img{width:100%;height:100%;display:block}
.glow.g2{top:20mm}
.quote{position:absolute;top:60mm;left:22mm;right:22mm;text-align:center;padding:4pt 10pt 12pt 10pt;border-bottom:1pt solid rgba(240,180,60,.55)}
.quote .qmk{display:block;font-size:44pt;line-height:.8;height:22pt;color:#f0b43c;font-weight:800}
.quote p{margin:0;font-size:21pt;line-height:1.45;font-weight:700;color:#e6eeff}
.quote b{color:#f0c46a}
.inside{position:absolute;top:106mm;left:17mm;right:17mm}
.inside h3{margin:0 0 8pt 0;text-align:center;font-size:15pt;font-weight:800;color:#f0b43c}
.bus{display:grid;grid-template-columns:1fr 1fr;gap:11pt}
.bu{background:rgba(8,26,78,.72);border:1pt solid rgba(120,165,255,.4);border-radius:10pt;padding:10pt 11pt 9pt 11pt}
.bh{display:flex;align-items:center;gap:7pt;margin-bottom:4pt}
.bn{flex:none;width:21pt;height:21pt;border-radius:6pt;background:#e29433;color:#17263f;font-weight:800;font-size:12pt;display:flex;align-items:center;justify-content:center}
.bh b{font-size:12.6pt;font-weight:800;color:#fff;line-height:1.25}
.bu ul{list-style:none;margin:0;padding:0}
.bu li{display:flex;align-items:flex-start;gap:5pt;font-size:10.2pt;line-height:1.45;color:#d4e0f7;font-weight:600;padding:3.5pt 0;border-top:.7pt dashed rgba(143,182,255,.25)}
.bu li .lid{flex:none;font-weight:800;color:#8fb6ff;min-width:20pt}
"""


def main():
    doc = ('<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
           '<title>الغلاف الخارجي — البرمجة والذكاء الاصطناعي — الترم الأول | أكواد مع زياد</title>\n'
           f'<style>{CSS}</style>\n</head>\n<body>\n{front()}\n{back()}\n'
           '<script>document.fonts.ready.then(() => document.body.dataset.ready = "1")</script>\n</body>\n</html>\n')
    open(OUT, "w", encoding="utf-8").write(doc)
    print("written", OUT, len(doc) // 1024, "KB")


if __name__ == "__main__":
    main()
