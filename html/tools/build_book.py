# -*- coding: utf-8 -*-
"""يجمّع دروس الترم الأول (14 درس) في HTML واحد مرقّم: غلاف + فهرس + فاصل لكل فصل + الدروس.

    python3 tools/build_book.py            ← يكتب html/term1_book.html

إزاي بيشتغل:
- كل درس بيتفتح في Chromium لحد ما الـJS بتاعه يقسّمه لصفحات (paginate + frame)، وبعدين
  الصفحات الجاهزة (section.page) بتتنسخ زي ما هي — يعني نفس التقسيم اللي بنراجعه في qa/ بالظبط.
- الستايل بتاع كل درس بيتحصر جوه غلاف خاص بيه (.Lxy …) عشان تصميمات الدروس ماتتخانقش مع بعض
  (نفس اسم الكلاس ممكن يكون ليه شكل مختلف في درسين). والـid في كل درس بياخد بادئة باسم الدرس.
- الترقيم: كل صفحة بتاخد رقمها في الكتاب كله «ن / الإجمالي» (الغلاف محسوب ومش مكتوب عليه رقم).
- لو المتصفح مفعّل «أقل حجم للخط» نفس حيلة immunize بتاعة الدروس بتشتغل على الكتاب كله.
"""
import asyncio, os, re, sys, html as H
from playwright.async_api import async_playwright

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)
OUT = os.path.join(BASE, "term1_book.html")

UNITS = [
    (1, "تكنولوجيا المعلومات والمجتمع", ["1-1", "1-2", "1-3", "1-4"]),
    (2, "الأمن السيبراني", ["2-1", "2-2", "2-3"]),
    (3, "تطبيقات الويب", ["3-1", "3-2", "3-3"]),
    (4, "تصميم الويب والوسائط", ["4-1", "4-2", "4-3", "4-4"]),
]
UNIT_ORD = {1: "الأول", 2: "الثاني", 3: "الثالث", 4: "الرابع"}
YEAR = "2026/2027"

JS_FREEZE = r"""() => {
  const pages = [...document.querySelectorAll('section.page')];
  const isBank = p => { const c = p.querySelector('.content'); return !!c && c.innerText.slice(0, 160).includes('بنك الأسئلة'); };
  return {
    lesson: document.body.dataset.lesson, k: document.body.dataset.k,
    css: [...document.querySelectorAll('style')].map(s => s.textContent),
    pages: pages.map(p => p.outerHTML),
    bank: pages.findIndex(isBank),
    extra: [...document.body.children].filter(e => !['SECTION', 'MAIN', 'SCRIPT', 'STYLE'].includes(e.tagName)).map(e => e.outerHTML),
  };
}"""


# ---------------------------------------------------------------- CSS
def blocks(css):
    """يقسّم CSS لبلوكات المستوى الأول: [(prelude, body|None)] — body=None لجملة زي @import;"""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i, n = [], 0, len(css)
    while i < n:
        j, q = i, None
        while j < n:                                    # لحد أول { أو ; بره أي string
            c = css[j]
            if q:
                if c == q: q = None
            elif c in "\"'": q = c
            elif c in "{;": break
            j += 1
        if j >= n:
            if css[i:].strip(): out.append((css[i:].strip(), None))
            break
        pre = css[i:j].strip()
        if css[j] == ";":
            if pre: out.append((pre, None))
            i = j + 1; continue
        d, k, q = 1, j + 1, None                        # القوس المقفول المقابل
        while k < n and d:
            c = css[k]
            if q:
                if c == q: q = None
            elif c in "\"'": q = c
            elif c == "{": d += 1
            elif c == "}": d -= 1
            k += 1
        out.append((pre, css[j + 1:k - 1]))
        i = k
    return out


def split_sel(s):
    parts, d, cur = [], 0, ""
    for c in s:
        if c in "([": d += 1
        elif c in ")]": d -= 1
        if c == "," and d == 0: parts.append(cur); cur = ""
        else: cur += c
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


ROOT = re.compile(r"^(html|body|:root)(?=$|[\s.:\[>#~+])")


def scope_sel(s, P):
    m = ROOT.match(s)
    if m:                                               # html/body/:root ← الغلاف نفسه (.Lxy)
        rest = s[m.end():]
        m2 = ROOT.match(rest.lstrip())
        if rest[:1] == " " and m2: rest = rest.lstrip()[m2.end():]
        return P + rest
    return P + " " + s


def scope_book(css):
    """ستايل صفحات الكتاب: كل قاعدة تحت .bkp — و«.bk-cover …» تبقى «.bkp.bk-cover …» (نفس العنصر)."""
    out = []
    for pre, body in blocks(css):
        if pre.startswith("@media"):
            out.append(pre + "{" + scope_book(body) + "}"); continue
        sels = [(".bkp" + x) if x.startswith(".bk-") else (".bkp " + x) for x in split_sel(pre)]
        out.append(",".join(sels) + "{" + body.strip() + "}")
    return "\n".join(out)


def scope_css(css, P, glob):
    """glob: dict بيتجمع فيه @font-face و@page و@keyframes مرة واحدة للكتاب كله."""
    out = []
    for pre, body in blocks(css):
        if body is None:
            continue                                    # @import/@charset مش مستخدمين
        low = pre.lower()
        if low.startswith("@font-face") or low.startswith("@page") or low.startswith("@keyframes") or low.startswith("@-webkit-keyframes"):
            glob.setdefault(pre + "{" + " ".join(body.split()) + "}", None); continue
        if low.startswith("@media") or low.startswith("@supports"):
            out.append(pre + "{" + scope_css(body, P, glob) + "}"); continue
        if pre.startswith("@"):
            out.append(pre + "{" + body + "}"); continue
        out.append(",".join(scope_sel(s, P) for s in split_sel(pre)) + "{" + body.strip() + "}")
    return "\n".join(out)


# ---------------------------------------------------------------- HTML
def prefix_ids(htm, css, P):
    ids = set(re.findall(r'\sid="([^"]+)"', htm))
    if not ids: return htm, css
    rx = "|".join(re.escape(x) for x in sorted(ids, key=len, reverse=True))
    htm = re.sub(r'(\sid=")(' + rx + r')"', lambda m: f'{m.group(1)}{P}-{m.group(2)}"', htm)
    htm = re.sub(r'((?:xlink:)?href=")#(' + rx + r')"', lambda m: f'{m.group(1)}#{P}-{m.group(2)}"', htm)
    htm = re.sub(r"url\((['\"]?)#(" + rx + r")\1\)", lambda m: f"url({m.group(1)}#{P}-{m.group(2)}{m.group(1)})", htm)
    css = re.sub(r"#(" + rx + r")(?![\w-])", lambda m: f"#{P}-{m.group(1)}", css)
    return htm, css


def renumber(page, n, total):
    page = re.sub(r'data-page="\d+"', f'data-page="{n}"', page, count=1)
    i = page.rfind('<div class="ftr">')                 # رقم الصفحة في الفوتر (فيه كروت جوه الدروس بكلاس pn برضه)
    if i < 0: sys.exit("صفحة من غير فوتر")
    return page[:i] + re.sub(r'<span class="pn">[^<]*</span>', f'<span class="pn">{n} / {total}</span>', page[i:], count=1)


def num(t): return f'<span class="bnum">{t}</span>'


FTR = ('<div class="bftr"><img src="assets/badge.png" alt=""><span class="r"><b>أكواد مع زياد</b><span class="sep">|</span>أ/ زياد السعدني'
       '<span class="sep">|</span><span class="bnum">fb.com/61592749346697</span><span class="sep">|</span>واتساب <span class="bnum">01124840835</span></span>'
       '<span class="pn">{n} / {total}</span></div>')


def cover_page(lessons):
    units = "".join(f'<div class="cu"><span class="cn">{u}</span><div><small>الفصل {UNIT_ORD[u]}</small><b>{t}</b>'
                    f'<em>{" · ".join(num(x) for x in ls)}</em></div></div>' for u, t, ls in UNITS)
    return f'''<section class="page bkp bk-cover"><div class="bsheet">
  <div class="cv-top"><span class="cv-tag">مذكرة شرح + بنك أسئلة</span><span class="cv-year">العام الدراسي {num(YEAR)}</span></div>
  <div class="cv-logo"><img src="assets/logo.jpg" alt=""></div>
  <div class="cv-title"><h1>البرمجة والذكاء الاصطناعي</h1><div class="cv-line"></div>
    <p class="cv-grade">الصف الثاني الثانوي — <b>الترم الأول</b></p></div>
  <div class="cv-units">{units}</div>
  <div class="cv-quote"><span class="q">”</span><p>الكود مجرد أداة… <b>القوة الحقيقية في طريقة تفكيرك.</b></p></div>
  <div class="cv-foot"><div class="cv-t"><b>أ/ زياد السعدني</b><span>أكواد مع زياد</span></div>
    <div class="cv-c"><div class="cv-qr"><img src="assets/qr_fb.svg" alt=""></div><div class="cv-qt"><b>صفحتنا على فيسبوك</b><span>امسح الكود بكاميرا الموبايل</span><span class="wa">واتساب {num("01124840835")}</span></div></div></div>
</div></section>'''


def toc_page(lessons, n, total):
    rows = []
    for u, t, ls in UNITS:
        rows.append(f'<div class="tu"><span class="tn">{u}</span><b>الفصل {UNIT_ORD[u]} — {t}</b><span class="tp">{num(lessons["unit" + str(u)])}</span></div>')
        for lid in ls:
            L = lessons[lid]
            rows.append(f'<div class="tl"><span class="tid">{num(lid)}</span><span class="tt">{H.escape(L["title"])}</span><span class="dots"></span>'
                        f'<span class="tpg"><small>الشرح</small>{num(L["start"])}</span><span class="tpg bk"><small>البنك</small>{num(L["bank"])}</span></div>')
    return f'''<section class="page bkp bk-toc"><div class="bsheet">
  <div class="bhdr"><span class="r">البرمجة والذكاء الاصطناعي — الترم الأول</span><span class="l">أكواد مع زياد</span></div>
  <div class="toc">
    <div class="toch"><h2>الفهرس</h2><p>كل درس فيه <b>الشرح</b> وبعده <b>بنك الأسئلة</b> — والرقم هو رقم الصفحة.</p></div>
    {"".join(rows)}
    <div class="tnote"><span class="fxk">للفهم</span> أي جزء عليه العلامة دي شرح أو رسم إضافي للتوضيح — واللي من غير علامة نص الكتاب.</div>
  </div>
  {FTR.format(n=n, total=total)}
</div></section>'''


def unit_page(u, t, ls, lessons, n, total):
    items = "".join(f'<div class="ul"><span class="uid">{num(lid)}</span><span class="ut">{H.escape(lessons[lid]["title"])}</span>'
                    f'<span class="up"><small>الشرح</small>ص {num(lessons[lid]["start"])}</span><span class="up bk"><small>البنك</small>ص {num(lessons[lid]["bank"])}</span></div>' for lid in ls)
    return f'''<section class="page bkp bk-unit"><div class="bsheet">
  <div class="un-top"><div class="un-no"><small>الفصل</small><b>{num(u)}</b></div>
    <div class="un-t"><small>الفصل {UNIT_ORD[u]}</small><h2>{t}</h2><p>{num(len(ls))} دروس — شرح + بنك أسئلة لكل درس</p></div></div>
  <div class="un-list">{items}</div>
  <img class="un-logo" src="assets/logo.jpg" alt="">
  {FTR.format(n=n, total=total)}
</div></section>'''


BOOK_CSS = r"""
@font-face{font-family:'Baloo Bhaijaan 2';font-weight:400 800;src:url(fonts/BalooBhaijaan2.ttf) format('truetype')}
html,body{margin:0;padding:0}
body{background:#e6eaf0;padding:18pt 0;direction:rtl;font-family:'Baloo Bhaijaan 2'}
.bk-lesson{padding:0!important;background:transparent!important}
section.page{break-after:page!important;page-break-after:always!important}
body>section.page:last-child,.bk-lesson:last-child section.page:last-of-type{break-after:auto!important;page-break-after:auto!important}
@media print{ body{background:#fff;padding:0} }
"""

BOOK_PAGES_CSS = r"""
/* ---- صفحات الكتاب نفسه (غلاف · فهرس · فاصل الفصل) — بتتحصر تحت .bkp عشان ماتلمسش الدروس ---- */
.bk-cover,.bk-toc,.bk-unit{position:relative;width:210mm;height:297mm;margin:0 auto 18pt auto;background:#fff;overflow:hidden;box-shadow:0 2pt 14pt rgba(23,38,63,.18)}
@media print{.bk-cover,.bk-toc,.bk-unit{margin:0;box-shadow:none}}
.bsheet{position:absolute;inset:0;font-family:'Baloo Bhaijaan 2';color:#33445f;direction:rtl;text-align:right;line-height:1.5}
.bnum{direction:ltr;unicode-bidi:isolate}
.bhdr{position:absolute;top:0;left:0;right:0;height:31.5pt;font-weight:700;font-size:7.2pt;line-height:1}
.bhdr .r{position:absolute;right:25.4pt;top:17.6pt;color:#17263f}
.bhdr .l{position:absolute;left:39.7pt;top:17.6pt;color:#a9670f}
.bhdr::after{content:'';position:absolute;left:0;right:0;top:27.8pt;height:.7pt;background:#e29433}
.bftr{position:absolute;bottom:0;left:0;right:0;height:36.4pt;font-weight:700;font-size:7.39pt;line-height:1;color:#4e5f7c}
.bftr img{position:absolute;right:28.2pt;top:10.7pt;width:10.5pt;height:10.5pt;border-radius:50%}
.bftr .r{position:absolute;right:43.2pt;top:11.9pt;white-space:nowrap}
.bftr .r b{color:#17263f}
.bftr .sep{margin:0 5pt;color:#9aa8bd}
.bftr .pn{position:absolute;left:45pt;top:11.5pt;font-weight:600;color:#17263f;direction:ltr}
/* الغلاف */
.bk-cover .bsheet{background:radial-gradient(120% 70% at 50% 30%,#0b1f5c 0%,#041140 45%,#020c2e 100%);color:#fff}
.bk-cover .bsheet::before{content:'';position:absolute;inset:14pt;border:1pt solid rgba(226,148,51,.55);border-radius:14pt;pointer-events:none}
.cv-top{position:absolute;top:34pt;left:40pt;right:40pt;display:flex;justify-content:space-between;align-items:center}
.cv-tag{background:#e29433;color:#17263f;font-weight:800;font-size:11pt;border-radius:20pt;padding:3pt 16pt}
.cv-year{color:#c9d6f2;font-weight:700;font-size:10.5pt}
.cv-logo{position:absolute;top:72pt;left:50%;transform:translateX(-50%);width:250pt;height:250pt;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3pt rgba(47,111,237,.35),0 0 40pt rgba(47,111,237,.35)}
.cv-logo img{width:100%;height:100%;display:block}
.cv-title{position:absolute;top:338pt;left:30pt;right:30pt;text-align:center}
.cv-title h1{margin:0;font-weight:800;font-size:34pt;line-height:1.25;color:#fff;letter-spacing:.3pt}
.cv-line{width:120pt;height:3pt;border-radius:3pt;background:#e29433;margin:8pt auto 8pt auto}
.cv-grade{margin:0;font-size:16pt;font-weight:700;color:#c9d6f2}
.cv-grade b{color:#f1c88b}
.cv-units{position:absolute;top:466pt;left:44pt;right:44pt;display:grid;grid-template-columns:1fr 1fr;gap:9pt}
.cu{display:flex;align-items:center;gap:10pt;background:rgba(255,255,255,.06);border:.9pt solid rgba(255,255,255,.16);border-radius:10pt;padding:8pt 11pt}
.cu .cn{flex:none;width:30pt;height:30pt;border-radius:8pt;background:#e29433;color:#17263f;font-weight:800;font-size:16pt;display:flex;align-items:center;justify-content:center}
.cu small{display:block;font-size:8.6pt;color:#9fb3da;font-weight:600;line-height:1.2}
.cu b{display:block;font-size:12pt;color:#fff;font-weight:800;line-height:1.35}
.cu em{display:block;font-style:normal;font-size:8.8pt;color:#f1c88b;font-weight:700;line-height:1.3}
.cv-quote{position:absolute;top:614pt;left:70pt;right:70pt;text-align:center;padding:14pt 24pt 12pt 24pt;border-top:.8pt solid rgba(226,148,51,.45);border-bottom:.8pt solid rgba(226,148,51,.45)}
.cv-quote .q{position:absolute;top:-17pt;left:50%;transform:translateX(-50%);background:#041140;padding:0 10pt;font-size:34pt;line-height:1;color:#e29433;font-weight:800}
.cv-quote p{margin:0;font-size:17pt;line-height:1.5;font-weight:700;color:#dbe4f7}
.cv-quote p b{color:#f1c88b;font-weight:800}
.cv-foot{position:absolute;bottom:34pt;left:44pt;right:44pt;display:flex;justify-content:space-between;align-items:center;border-top:.8pt solid rgba(255,255,255,.18);padding-top:12pt}
.cv-t b{display:block;font-size:17pt;font-weight:800;color:#fff;line-height:1.2}
.cv-t span{font-size:10.5pt;color:#f1c88b;font-weight:700}
.cv-c{display:flex;align-items:center;gap:10pt}
.cv-qr{flex:none;width:72pt;height:72pt;background:#fff;border-radius:9pt;padding:6pt;box-shadow:0 0 0 2pt rgba(226,148,51,.8)}
.cv-qr img{display:block;width:100%;height:100%}
.cv-qt{display:flex;flex-direction:column;align-items:flex-start;gap:1pt;line-height:1.3}
.cv-qt b{font-size:11pt;font-weight:800;color:#fff}
.cv-qt span{font-size:9pt;font-weight:600;color:#9fb3da}
.cv-qt .wa{margin-top:3pt;font-size:10pt;font-weight:700;color:#c9d6f2}
/* الفهرس */
.toc{position:absolute;top:44pt;left:40pt;right:40pt;bottom:50pt}
.toch{display:flex;align-items:baseline;gap:14pt;border-bottom:2pt solid #17263f;padding-bottom:6pt;margin-bottom:10pt}
.toch h2{margin:0;font-size:26pt;font-weight:800;color:#17263f;line-height:1.2}
.toch p{margin:0;font-size:9.6pt;color:#4e5f7c}
.toch p b{color:#a9670f}
.tu{display:flex;align-items:center;gap:9pt;background:#17263f;color:#fff;border-radius:8pt;padding:7pt 10pt;margin:17pt 0 6pt 0}
.tu:first-of-type{margin-top:4pt}
.tu .tn{flex:none;width:22pt;height:22pt;border-radius:6pt;background:#e29433;color:#17263f;font-weight:800;font-size:12pt;display:flex;align-items:center;justify-content:center}
.tu b{flex:1;font-size:12.4pt;font-weight:800}
.tu .tp{font-size:10pt;color:#f1c88b;font-weight:700}
.tl{display:flex;align-items:center;gap:8pt;padding:6.8pt 6pt;border-bottom:.75pt dashed #dce5f1;font-size:11pt}
.tl .tid{flex:none;width:30pt;text-align:center;background:#f1f6fc;border:.75pt solid #d7e4f5;border-radius:6pt;font-weight:800;color:#22375c;font-size:10pt}
.tl .tt{font-weight:700;color:#1c2a44}
.tl .dots{flex:1;border-bottom:1.2pt dotted #b9c6da;transform:translateY(3pt);min-width:14pt}
.tl .tpg{flex:none;width:52pt;display:flex;align-items:baseline;justify-content:space-between;gap:4pt;font-weight:800;color:#17263f;font-size:11pt}
.tl .tpg small{font-size:7.6pt;font-weight:700;color:#6e7f9c}
.tl .tpg.bk{color:#a9670f}
.tnote{margin-top:16pt;font-size:9.2pt;color:#4e5f7c;display:flex;align-items:center;gap:8pt}
.fxk{flex:none;background:#e29433;color:#17263f;font-weight:800;font-size:9pt;border-radius:5pt;padding:0 8pt}
/* فاصل الفصل */
.un-top{position:absolute;top:0;left:0;right:0;height:360pt;background:radial-gradient(110% 90% at 50% 20%,#0b1f5c 0%,#041140 55%,#020c2e 100%);color:#fff;display:flex;align-items:center;gap:26pt;padding:0 48pt}
.un-top::after{content:'';position:absolute;left:0;right:0;bottom:0;height:5pt;background:#e29433}
.un-no{flex:none;width:130pt;height:130pt;border-radius:22pt;background:#e29433;color:#17263f;display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1}
.un-no small{font-size:15pt;font-weight:800}
.un-no b{font-size:72pt;font-weight:800;line-height:1}
.un-t small{display:block;font-size:13pt;color:#f1c88b;font-weight:700}
.un-t h2{margin:2pt 0 4pt 0;font-size:31pt;font-weight:800;line-height:1.25;color:#fff}
.un-t p{margin:0;font-size:11pt;color:#c9d6f2;font-weight:600}
.un-list{position:absolute;top:396pt;left:52pt;right:52pt}
.ul{display:flex;align-items:center;gap:12pt;padding:11pt 4pt;border-bottom:.9pt dashed #dce5f1}
.ul .uid{flex:none;width:44pt;height:30pt;border-radius:8pt;background:#17263f;color:#fff;font-weight:800;font-size:13pt;display:flex;align-items:center;justify-content:center}
.ul .ut{flex:1;font-size:14pt;font-weight:800;color:#1c2a44;line-height:1.35}
.ul .up{flex:none;font-size:10.5pt;font-weight:800;color:#17263f;width:74pt;white-space:nowrap}
.ul .up.bk{color:#a9670f}
.ul .up small{font-size:8pt;color:#6e7f9c;font-weight:700;margin-left:3pt}
.un-logo{position:absolute;bottom:58pt;left:50%;transform:translateX(-50%);width:74pt;height:74pt;border-radius:50%;opacity:.95}
"""

IMMUNIZE = r"""<script>
// لو المتصفح مفعّل «أقل حجم للخط»: نفس حيلة الدروس (tools/… lesson_3_1.html → immunize) على الكتاب كله.
let K = 1;
(function immunize(){
  const t = document.createElement('span'); t.style.fontSize = '1px'; t.textContent = 'x';
  document.body.appendChild(t); const mc = parseFloat(getComputedStyle(t).fontSize); t.remove();
  const wid = px => { const s = document.createElement('span');
    s.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;font-family:sans-serif;font-size:' + px + 'px';
    s.textContent = 'abcdefghij'; document.body.appendChild(s); const w = s.getBoundingClientRect().width; s.remove(); return w; };
  const mr = 4 * wid(4) / (wid(40) / 10);
  const m = Math.max(mc, mr > 6 ? mr : 0);
  if (!(m > 1.5)) { document.body.dataset.ready = '1'; return; }
  K = Math.max(2, Math.ceil(m / 7));
  const sc = v => v.replace(/(-?\d*\.?\d+)(pt|px|mm)\b/g, (_, n, u) => (parseFloat(n) * K).toFixed(3) + u);
  const skip = s => s.includes('.bkp') || s.split(',').every(x => /^(html|body|\.L\d+|\.L\d+ \.page|\.page|section\.page|body>.*|\.bk-lesson.*)$/.test(x.trim()));
  const walk = rules => { for (const r of rules) {
    if (r instanceof CSSMediaRule) { walk(r.cssRules); continue; }
    if (!(r instanceof CSSStyleRule) || skip(r.selectorText)) continue;
    for (let i = 0; i < r.style.length; i++) { const p = r.style[i], v = r.style.getPropertyValue(p);
      if (/\d(pt|px|mm)/.test(v)) r.style.setProperty(p, sc(v), r.style.getPropertyPriority(p)); }
  } };
  for (const s of document.styleSheets) { try { walk(s.cssRules); } catch (e) {} }
  document.querySelectorAll('.sheet [style]').forEach(el => { el.style.cssText = sc(el.style.cssText); });
  const probe = css => { const w = document.createElement('div'); w.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;' + css;
    const s = document.createElement('span'); s.style.fontSize = (6 * K) + 'px'; s.textContent = 'abcdefghij';
    w.appendChild(s); document.body.appendChild(w); const r = s.getBoundingClientRect().width; w.remove(); return r; };
  const big = probe(''), zoomed = probe('zoom:' + (1 / K)), zoomOK = Math.abs(zoomed - big / K) < 1.5;
  const st = document.createElement('style');
  st.textContent = zoomOK ? `.sheet{zoom:${1 / K}}` : `.sheet{transform:scale(${1 / K})}`;
  document.head.appendChild(st);
  document.querySelectorAll('.bk-lesson').forEach(w => w.dataset.mode = zoomOK ? 'zoom' : 'transform');
  document.body.dataset.ready = '1'; document.body.dataset.k = K;
})();
</script>"""


async def freeze_all():
    order = [lid for _, _, ls in UNITS for lid in ls]
    res = {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        p = await b.new_page(viewport={"width": 900, "height": 1200})
        for lid in order:
            f = os.path.join(BASE, f"lesson_{lid.replace('-', '_')}.html")
            await p.goto("file://" + f)
            await p.wait_for_function("document.body.dataset.ready==='1'", timeout=120000)
            res[lid] = await p.evaluate(JS_FREEZE)
            print(f"  {lid}: {len(res[lid]['pages'])} صفحة · البنك من صفحة {res[lid]['bank'] + 1} · K={res[lid]['k']} · extra={len(res[lid]['extra'])}")
        await b.close()
    return order, res


def main():
    order, R = asyncio.run(freeze_all())
    for lid in order:
        if R[lid]["bank"] < 0: sys.exit(f"{lid}: مالقيتش صفحة بداية البنك")
    # ---- الترقيم: غلاف (1) · فهرس (2) · [فاصل الفصل · دروسه] × 4
    lessons, n = {}, 3
    for u, t, ls in UNITS:
        lessons["unit" + str(u)] = n; n += 1
        for lid in ls:
            title = R[lid]["lesson"].split("—", 1)[1].strip()
            lessons[lid] = {"title": title, "start": n, "bank": n + R[lid]["bank"], "n": len(R[lid]["pages"])}
            n += len(R[lid]["pages"])
    total = n - 1
    glob, css_parts, body = {}, [], [cover_page(lessons), toc_page(lessons, 2, total)]
    for u, t, ls in UNITS:
        body.append(unit_page(u, t, ls, lessons, lessons["unit" + str(u)], total))
        for lid in ls:
            P = "L" + lid.replace("-", "")
            css = scope_css("\n".join(R[lid]["css"]), "." + P, glob)
            htm = "\n".join(R[lid]["extra"] + [renumber(pg, lessons[lid]["start"] + k, total) for k, pg in enumerate(R[lid]["pages"])])
            htm, css = prefix_ids(htm, css, P)
            css_parts.append(f"/* ===== الدرس {lid} ===== */\n{css}")
            body.append(f'<div class="bk-lesson {P}" data-lesson="{H.escape(R[lid]["lesson"])}">\n{htm}\n</div>')
    head = ('<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
            '<title>البرمجة والذكاء الاصطناعي — الترم الأول | أكواد مع زياد</title>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n<style>\n'
            + "\n".join(glob) + "\n" + BOOK_CSS + "\n" + scope_book(BOOK_PAGES_CSS) + "\n" + "\n".join(css_parts) + "\n</style>\n</head>\n")
    doc = head + '<body>\n' + "\n".join(body) + "\n" + IMMUNIZE + "\n</body>\n</html>\n"
    open(OUT, "w", encoding="utf-8").write(doc)
    print(f"written {OUT} · {total} صفحة · {len(doc) // 1024} KB")
    for u, t, ls in UNITS:
        print(f"  الفصل {u}: فاصل ص{lessons['unit' + str(u)]} · " + " · ".join(f"{lid} ص{lessons[lid]['start']}–{lessons[lid]['start'] + lessons[lid]['n'] - 1} (البنك ص{lessons[lid]['bank']})" for lid in ls))


if __name__ == "__main__":
    main()
