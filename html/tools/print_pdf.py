# -*- coding: utf-8 -*-
"""PDF للمطبعة من term1_book.html (المذكرة 292 صفحة A4) و term1_cover.html (الغلاف وش + ضهر، 216×303 مم بهامش القص).

    python3 tools/print_pdf.py [فولدر الإخراج]      (الافتراضي: html/print/)

- خط Baloo Bhaijaan 2 متغيّر (wght 400–800)، وChromium بيحط الخطوط المتغيّرة في الـPDF كـType 3 — المطابع كتير
  بتعترض عليه في الـpreflight. عشان كده بنعمل نسخ ثابتة لكل وزن (400/500/600/700/800) بـfontTools، ونطبع نسخة مؤقتة
  من الـHTML بتستخدمهم؛ المقاسات نفس المقاسات (نفس الخط) فالتقسيم والشكل مابيتغيّروش.
- الطباعة: حجم الصفحة من CSS + الخلفيات، ومن غير هوامش.
"""
import asyncio, os, re, sys, tempfile
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from playwright.async_api import async_playwright

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "print")
JOBS = [("term1_book.html", "مذكرة_البرمجة_والذكاء_الاصطناعي_الترم_الأول_2026-2027.pdf"),
        ("term1_cover.html", "غلاف_خارجي_وش_وضهر_216x303mm_بهامش_قص.pdf")]
FACE = re.compile(r"@font-face\{font-family:'Baloo Bhaijaan 2';font-weight:400 800;src:url\(fonts/BalooBhaijaan2\.ttf\) format\('truetype'\)\}")


def static_fonts(tmp):
    faces = []
    for w in (400, 500, 600, 700, 800):
        f = instancer.instantiateVariableFont(TTFont(os.path.join(BASE, "fonts", "BalooBhaijaan2.ttf")), {"wght": w})
        p = os.path.join(tmp, f"Baloo-{w}.ttf"); f.save(p)
        faces.append(f"@font-face{{font-family:'Baloo Bhaijaan 2';font-weight:{w};src:url('file://{p}') format('truetype')}}")
    return "".join(faces)


async def main():
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        faces = static_fonts(tmp)
        async with async_playwright() as pw:
            b = await pw.chromium.launch()
            p = await b.new_page()
            for src, name in JOBS:
                h = open(os.path.join(BASE, src), encoding="utf-8").read()
                h, n = FACE.subn(faces, h)
                if not n: sys.exit(f"{src}: مالقيتش @font-face بتاع Baloo")
                tmp_html = os.path.join(BASE, f".print_{src}")        # جنب الأصل عشان assets/ و fonts/ تشتغل
                open(tmp_html, "w", encoding="utf-8").write(h)
                try:
                    await p.goto("file://" + tmp_html)
                    await p.wait_for_function("document.body.dataset.ready==='1'", timeout=180000)
                    await p.evaluate("document.fonts.ready")
                    await p.pdf(path=os.path.join(OUT, name), prefer_css_page_size=True, print_background=True)
                finally:
                    os.remove(tmp_html)
                print("written", os.path.join(OUT, name))
            await b.close()


if __name__ == "__main__":
    asyncio.run(main())
