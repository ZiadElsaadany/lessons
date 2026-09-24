import sys,asyncio,os
from playwright.async_api import async_playwright
JS=r'''()=>{const out=[];const pages=[...document.querySelectorAll('.page')];
const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
// build block text excluding isolated spans
const blocks=new Set();while(n=w.nextNode()){if(!n.textContent.trim())continue;let b=n.parentElement;while(b&&getComputedStyle(b).display==='inline')b=b.parentElement;blocks.add(b)}
const re=/[A-Za-z0-9][A-Za-z0-9.]*\s*(—|·|،|=|:|-)\s*[A-Za-z]/g;
blocks.forEach(b=>{let t='';const walk=el=>{for(const c of el.childNodes){if(c.nodeType===3)t+=c.textContent;else if(c.nodeType===1){const cs=getComputedStyle(c);if(cs.display!=='inline'){t+='\n';continue}if(cs.unicodeBidi==='isolate'||c.tagName==='BDI'){t+='⁨X⁩';continue}walk(c)}}};walk(b);
let m;re.lastIndex=0;while(m=re.exec(t)){const pg=pages.findIndex(p=>p.contains(b));out.push([pg,t.slice(Math.max(0,m.index-25),m.index+m[0].length+25).replace(/\n/g,' ')])}});return out}'''
async def main(f):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        await pg.goto('file://'+os.path.abspath(f)); await pg.wait_for_selector('body[data-ready="1"]')
        for r in await pg.evaluate(JS): print(r)
        await b.close()
asyncio.run(main(sys.argv[1]))
