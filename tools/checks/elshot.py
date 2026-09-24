#!/usr/bin/env python3
"""لقطة لعنصر معيّن: python3 elshot.py file.html 'selector' out.png [index]"""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).resolve().parent
async def main():
    html = HERE / sys.argv[1]; sel = sys.argv[2]; out = sys.argv[3]; idx = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 900, "height": 1200}, device_scale_factor=2)
        await pg.goto(html.as_uri()); await pg.wait_for_function("document.body.dataset.ready===\"1\"", timeout=20000)
        await pg.wait_for_timeout(300)
        els = await pg.query_selector_all(sel)
        await els[idx].screenshot(path=out)
        await br.close()
asyncio.run(main())
