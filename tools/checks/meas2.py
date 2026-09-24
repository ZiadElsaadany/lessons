import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
HERE=Path(__file__).resolve().parent
f=sys.argv[1]; pages=[int(x) for x in sys.argv[2:]]
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        pg=await b.new_page(viewport={"width":900,"height":1200},device_scale_factor=2)
        await pg.goto((HERE/f).as_uri()); await pg.wait_for_function("document.body.dataset.ready==='1'",timeout=30000)
        start=int(await pg.evaluate("document.body.dataset.start"))
        for p in pages:
            r=await pg.evaluate("""(i)=>{const c=document.querySelectorAll('.content')[i];const cr=c.getBoundingClientRect();const k=0.75;
              return [...c.children].map(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return [e.tagName+'.'+e.className.replace(/ /g,'.'),((r.top-cr.top)*k).toFixed(1),((r.bottom-cr.top)*k).toFixed(1),(r.height*k).toFixed(1),cs.marginTop,cs.marginBottom,(e.textContent||'').trim().slice(0,30)]})}""",p-start)
            print('== page',p)
            for x in r: print(' ',*x)
        await b.close()
asyncio.run(main())
