#!/usr/bin/env python3
"""فحص الصفحات: لقطة لكل .sheet + قياس أي محتوى خارج حدود الصفحة.
python3 qa.py lesson_3_1.html [--pdf]"""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).resolve().parent
html = HERE / sys.argv[1]
out = HERE / "qa"; out.mkdir(exist_ok=True)
async def main():
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 900, "height": 1200}, device_scale_factor=2)
        await pg.goto(html.as_uri()); await pg.wait_for_function("document.body.dataset.ready===\"1\"", timeout=20000)
        await pg.wait_for_timeout(300)
        info = await pg.evaluate("""() => [...document.querySelectorAll('.sheet')].map(s => {
            const c = s.querySelector('.content'); const cr = c.getBoundingClientRect();
            let maxBottom = 0, worst = '';
            c.querySelectorAll('*').forEach(el => { const r = el.getBoundingClientRect(); if (r.height>0 && r.bottom > maxBottom) { maxBottom = r.bottom; worst = el.className || el.tagName; } });
            return {page: s.dataset.page, avail: (cr.height*0.75).toFixed(1), used: ((maxBottom - cr.top)*0.75).toFixed(1), over: ((maxBottom - cr.bottom)*0.75).toFixed(1), last: worst};
        })""")
        for r in info:
            flag = "  ⚠️ OVERFLOW" if float(r["over"]) > 0 else ""
            print(f"page {r['page']}: used {r['used']} / {r['avail']} pt (slack {float(r['avail'])-float(r['used']):.1f}){flag}  last={r['last']}")
        sheets = await pg.query_selector_all('.sheet')
        for s in sheets:
            p = await s.get_attribute('data-page')
            await s.screenshot(path=str(out / f"p{p}.png"))
        if "--pdf" in sys.argv:
            await pg.emulate_media(media="print")
            await pg.pdf(path=str(out / (html.stem + ".pdf")), format="A4", print_background=True, margin={"top":"0","bottom":"0","left":"0","right":"0"}, prefer_css_page_size=True)
            print("pdf:", out / (html.stem + ".pdf"))
        await br.close()
asyncio.run(main())
