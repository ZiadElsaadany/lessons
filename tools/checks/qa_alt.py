import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
HERE=Path(__file__).resolve().parent
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg=await b.new_page(viewport={"width":900,"height":1200})
        for f in sys.argv[1:]:
            await pg.goto((HERE/f).as_uri()); await pg.wait_for_function("document.body.dataset.ready==='1'",timeout=30000)
            r=await pg.evaluate("""()=>[...document.querySelectorAll('.sheet')].map(s=>{const c=s.querySelector('.content');const cr=c.getBoundingClientRect();let mb=0;c.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.height>0&&r.bottom>mb)mb=r.bottom});return [s.dataset.page,((mb-cr.bottom)*0.75).toFixed(1)]})""")
            bad=[x for x in r if float(x[1])>0]
            print(f, 'sheets',len(r),'overflow',bad)
        await b.close()
asyncio.run(main())
