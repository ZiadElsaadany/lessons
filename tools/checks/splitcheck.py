# كل سؤال (نصه + مكان إجابته) لازم يفضل في صفحة واحدة:
# أي جزء مكمّل (.cont) لكارت سؤال لازم يبدأ بسؤال جديد، و.why ما يتقسمش خالص.
import asyncio,os,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        for f in sys.argv[1:]:
            await pg.goto('file://'+os.path.abspath(f)); await pg.wait_for_selector('body[data-ready="1"]')
            r=await pg.evaluate('''()=>{const st=+document.body.dataset.start;const out=[];let n=0;
              document.querySelectorAll('.page').forEach((p,i)=>{p.querySelectorAll('.content > .cont').forEach(c=>{
                if(!c.matches('.why, .qcard')) return; n++;
                const f=c.firstElementChild;
                if(c.matches('.why') || !f || !f.matches('.qq,.qi,.qs')) out.push([st+i,c.className,(f&&(f.className||f.tagName))||'-',c.textContent.trim().slice(0,40)]);});});
              return [n,out]}''')
            print(f, 'splits:',r[0], r[1] if r[1] else 'OK')
        await b.close()
asyncio.run(main())
