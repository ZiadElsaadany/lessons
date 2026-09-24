# عنوان قسم في البنك (h2.cat) مايفضلش في آخر الصفحة ومعاه سؤال واحد بس
import asyncio,os,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":900,"height":1200},device_scale_factor=2)
        for f in sys.argv[1:]:
            await pg.goto('file://'+os.path.abspath(f)); await pg.wait_for_selector('body[data-ready="1"]')
            r=await pg.evaluate('''()=>{const st=+document.body.dataset.start;const out=[];
              document.querySelectorAll('.page').forEach((p,i)=>{const kids=[...p.querySelector('.content').children];
                kids.forEach((k,j)=>{ if(k.matches('h2.cat') && kids.length-j<=2) out.push([st+i,k.textContent.trim().slice(0,20),kids.length-j-1]); });});
              return out}''')
            print(f, r if r else 'OK')
        await b.close()
asyncio.run(main())
