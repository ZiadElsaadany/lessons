import asyncio,os,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        for f in sys.argv[1:]:
            await pg.goto('file://'+os.path.abspath(f)); await pg.wait_for_selector('body[data-ready="1"]')
            r=await pg.evaluate('''()=>{const st=+document.body.dataset.start;const out=[];
              document.querySelectorAll('.page').forEach((p,i)=>{const c=p.querySelector('.content');const l=c.lastElementChild;if(!l)return;
                const last=l.lastElementChild; if(last&&last.matches('.qq,.qi,.qs,h4')) out.push([st+i,l.className,last.className||last.tagName,last.textContent.trim().slice(0,50)]);
                if(l.matches('.qq,.qi,.qs,h2,h3,.chip,.part,hr')) out.push([st+i,'TOP-LEVEL',l.className||l.tagName,l.textContent.trim().slice(0,50)]);});
              return out}''')
            print(f, r if r else 'OK')
        await b.close()
asyncio.run(main())
