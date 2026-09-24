#!/usr/bin/env python3
"""فحص شامل لملفات الدروس (كل الفحوصات اللي اتعملت في الوحدة التالتة في أمر واحد).

python3 tools/check.py lesson_1_1.html [lesson_1_2.html ...] [--shots] [--no-min] [--no-alt]

بيطبع لكل ملف:
  pages        عدد الصفحات
  overflow     صفحات فيها محتوى طالع برّه (لازم تبقى فاضية)
  alt          نفس الفحص بـchromium-1194 (لو موجود) — لازم نفس عدد الصفحات ومن غير overflow
  min16        عدد الصفحات لو المتصفح مظبوط على أقل حجم خط 16px — لازم = pages
  stems        سؤال آخره في آخر الصفحة من غير مكان إجابته / عنوان لوحده في آخر الصفحة
  splits       كارت سؤال اتقسم في نص سؤال (لازم يتقسم بس قبل سؤال جديد)
  cats         عنوان قسم في البنك في آخر الصفحة ومعاه سؤال واحد أو مفيش
  bidi         إنجليزي جنب إنجليزي بفاصل من غير عزل (<E-mail> بس معروف إنه false positive)
  counts       العدادات (شريط الإحصائيات + عدد جنب كل قسم) مقابل عدد الأسئلة الفعلي
--shots بيحفظ صورة لكل صفحة في qa/<اسم الملف>/pN.png جنب ملف الـHTML.
"""
import asyncio, json, os, sys, tempfile, shutil
from pathlib import Path
from playwright.async_api import async_playwright

ALT = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
READY = "document.body.dataset.ready==='1'"

JS_OVER = """()=>[...document.querySelectorAll('.sheet')].map(s=>{const c=s.querySelector('.content');const cr=c.getBoundingClientRect();
  let mb=0;c.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.height>0&&r.bottom>mb)mb=r.bottom});
  return [+s.dataset.page, +((mb-cr.bottom)*0.75).toFixed(1), +((cr.bottom-mb)*0.75).toFixed(1)]})"""

JS_STEM = """()=>{const out=[];document.querySelectorAll('.sheet').forEach(s=>{const pg=+s.dataset.page;const c=s.querySelector('.content');const l=c.lastElementChild;if(!l)return;
  const last=l.lastElementChild; if(last&&last.matches('.qq,.qi,.qs,h4')) out.push([pg,l.className,(last.className||last.tagName),last.textContent.trim().slice(0,50)]);
  if(l.matches('.qq,.qi,.qs,h2,h3,.chip,.part,hr')) out.push([pg,'TOP-LEVEL',(l.className||l.tagName),l.textContent.trim().slice(0,50)]);});return out}"""

JS_SPLIT = """()=>{const out=[];let n=0;document.querySelectorAll('.sheet').forEach(s=>{const pg=+s.dataset.page;
  s.querySelectorAll('.content > .cont').forEach(c=>{ if(!c.matches('.why, .qcard')) return; if(c.dataset.src==='cont') return; n++;
    const f=c.firstElementChild; if(c.matches('.why') || !f || !f.matches('.qq,.qi,.qs')) out.push([pg,c.className,(f&&(f.className||f.tagName))||'-',c.textContent.trim().slice(0,40)]);});});
  return [n,out]}"""

JS_CAT = """()=>{const out=[];document.querySelectorAll('.sheet').forEach(s=>{const pg=+s.dataset.page;const kids=[...s.querySelector('.content').children];
  kids.forEach((k,j)=>{ if(k.matches('h2.cat') && kids.length-j<=2) out.push([pg,k.textContent.trim().slice(0,24),kids.length-j-1]); });});return out}"""

JS_BIDI = r"""()=>{const out=[];const sheets=[...document.querySelectorAll('.sheet')];
const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;const blocks=new Set();
while(n=w.nextNode()){if(!n.textContent.trim())continue;let b=n.parentElement;while(b&&getComputedStyle(b).display==='inline')b=b.parentElement;blocks.add(b)}
const re=/[A-Za-z0-9][A-Za-z0-9.]*\s*(—|·|،|=|:|-)\s*[A-Za-z]/g;
blocks.forEach(b=>{let t='';const walk=el=>{for(const c of el.childNodes){if(c.nodeType===3)t+=c.textContent;else if(c.nodeType===1){const cs=getComputedStyle(c);if(cs.display!=='inline'){t+='\n';continue}if(cs.unicodeBidi==='isolate'||c.tagName==='BDI'){t+='⁨X⁩';continue}walk(c)}}};walk(b);
let m;re.lastIndex=0;while(m=re.exec(t)){const s=sheets.find(p=>p.contains(b));out.push([s?+s.dataset.page:-1,t.slice(Math.max(0,m.index-25),m.index+m[0].length+25).replace(/\n/g,' ')])}});return out}"""

# العدادات: بنمشي على عناصر المحتوى بالترتيب ونعدّ جوه كل قسم (h2.cat). الأجزاء المكمّلة (.cont) مش بتتعد.
JS_COUNT = """()=>{const T=x=>x.textContent.replace(/\\s+/g,' ').trim();
  const stats={}; document.querySelectorAll('.qstats > div').forEach(d=>{const b=d.querySelector('b');if(!b)return;const lab=T(d).replace(T(b),'').trim();stats[lab]=+T(b)});
  const secs=[]; let cur=null;
  document.querySelectorAll('.sheet .content > *').forEach(e=>{
    if(e.matches('h2.cat')){const cnt=e.querySelector('.cnt');cur={title:T(e).replace(cnt?T(cnt):'','').trim(),cnt:cnt?+T(cnt):null,items:[]};secs.push(cur);return}
    if(!cur||e.matches('.cont'))return; cur.items.push(e)});
  const res=[];
  secs.forEach(s=>{let n=0,why=0,ess=0,seenCard=false;
    s.items.forEach(e=>{
      if(s.title.startsWith('اختر')) n+=e.querySelectorAll('.mq').length;
      else if(s.title.startsWith('أكمل')) n+=e.querySelectorAll('.k').length;
      else if(s.title.startsWith('صح')) n+=e.querySelectorAll(':scope > li').length;
      else if(s.title.startsWith('تصنيف')) { if(e.matches('.qcard')&&e.querySelector(':scope > h4')) n++; else if(e.matches('table.cmp,.cmpw')) n++; }
      else if(s.title.startsWith('أسئلة الكتاب')) { if(e.matches('.qcard:not(.sol)')&&e.querySelector(':scope > h4')) n++; }
      else if(s.title.startsWith('علّل')) { if(e.matches('.qcard')&&e.querySelector(':scope > h4')){seenCard=true;ess++} else if(e.matches('.why')){ if(seenCard) ess++; else why++; } }
    });
    if(s.title.startsWith('علّل')) res.push([s.title,s.cnt,why,ess]); else res.push([s.title,s.cnt,n,null]);});
  const tq=[...document.querySelectorAll('.tq')].filter(x=>!x.closest('.qstats')).length;
  return {stats,res,tq}}"""


async def load(pg, f):
    await pg.goto(Path(f).resolve().as_uri())
    await pg.wait_for_function(READY, timeout=60000)
    await pg.wait_for_timeout(300)


async def check(f, shots, do_min, do_alt, pw):
    out = {}
    br = await pw.chromium.launch()
    pg = await br.new_page(viewport={"width": 900, "height": 1200}, device_scale_factor=2)
    await load(pg, f)
    ov = await pg.evaluate(JS_OVER)
    out["pages"] = len(ov)
    out["range"] = f"{ov[0][0]}–{ov[-1][0]}" if ov else "-"
    out["overflow"] = [(p, o) for p, o, _ in ov if o > 0]
    out["slack_min"] = min((s, p) for p, _, s in ov) if ov else None
    out["stems"] = await pg.evaluate(JS_STEM)
    sp = await pg.evaluate(JS_SPLIT); out["splits"] = sp[1]
    out["cats"] = await pg.evaluate(JS_CAT)
    out["bidi"] = [b for b in await pg.evaluate(JS_BIDI) if "E-mail" not in b[1]]
    out["counts"] = await pg.evaluate(JS_COUNT)
    if shots:
        d = Path(f).resolve().parent / "qa" / Path(f).stem
        d.mkdir(parents=True, exist_ok=True)
        for s in await pg.query_selector_all(".sheet"):
            await s.screenshot(path=str(d / f"p{await s.get_attribute('data-page')}.png"))
        out["shots"] = str(d)
    await br.close()
    if do_alt and os.path.exists(ALT):
        b2 = await pw.chromium.launch(executable_path=ALT)
        p2 = await b2.new_page(viewport={"width": 900, "height": 1200})
        await load(p2, f)
        ov2 = await p2.evaluate(JS_OVER)
        out["alt"] = (len(ov2), [(p, o) for p, o, _ in ov2 if o > 0])
        await b2.close()
    if do_min:
        ud = tempfile.mkdtemp(prefix="minfont_")
        try:
            (Path(ud) / "Default").mkdir(parents=True)
            (Path(ud) / "Default" / "Preferences").write_text(json.dumps({"webkit": {"webprefs": {"minimum_font_size": 16, "minimum_logical_font_size": 16}}}))
            kw = dict(headless=True, args=["--headless=new"], viewport={"width": 900, "height": 1200}, device_scale_factor=1.5)
            if os.path.exists(ALT): kw["executable_path"] = ALT
            ctx = await pw.chromium.launch_persistent_context(ud, **kw)
            p3 = await ctx.new_page(); await load(p3, f)
            out["min16"] = await p3.evaluate("document.querySelectorAll('.sheet').length")
            await ctx.close()
        finally:
            shutil.rmtree(ud, ignore_errors=True)
    return out


def report(f, r):
    bad = []
    print(f"\n=== {f}")
    print(f"  pages      {r['pages']}  (ص{r['range']})   أقل مساحة فاضية في صفحة: {r['slack_min']}")
    print(f"  overflow   {r['overflow'] or 'OK'}");   bad += ["overflow"] if r["overflow"] else []
    if "alt" in r:
        a = r["alt"]; ok = a[0] == r["pages"] and not a[1]
        print(f"  alt        pages={a[0]} overflow={a[1] or 'OK'}" + ("" if ok else "   ⚠️")); bad += [] if ok else ["alt"]
    if "min16" in r:
        ok = r["min16"] == r["pages"]; print(f"  min16      pages={r['min16']}" + ("  OK" if ok else "   ⚠️")); bad += [] if ok else ["min16"]
    print(f"  stems      {r['stems'] or 'OK'}");   bad += ["stems"] if r["stems"] else []
    print(f"  splits     {r['splits'] or 'OK'}");  bad += ["splits"] if r["splits"] else []
    print(f"  cats       {r['cats'] or 'OK'}   (صح وخطأ ككتلة واحدة مقبول)")
    print(f"  bidi       {r['bidi'] or 'OK'}");    bad += ["bidi"] if r["bidi"] else []
    c = r["counts"]; st = c["stats"]
    print(f"  stats      {st}")
    for title, cnt, n, ess in c["res"]:
        if ess is None:
            key = next((k for k in st if title.startswith(k) or k.startswith(title.split()[0])), None)
            s = st.get(key) if key else None
            ok = (cnt == n or title.startswith("أسئلة الكتاب")) and (s is None or s == cnt)
            note = "  (أسئلة الكتاب: n = عدد الكروت؛ العدد الحقيقي بقاعدة الـplaybook)" if title.startswith("أسئلة الكتاب") else ""
            print(f"  count      {title}: header={cnt} stats={s} actual={n}" + ("" if ok else "   ⚠️") + note)
            bad += [] if ok else [f"count:{title}"]
        else:
            s1, s2 = st.get("علّل"), st.get("مقالي وأنشطة")
            ok = cnt == n and (s1 is None or s1 == n) and (s2 is None or s2 == ess)
            print(f"  count      علّل: header={cnt} stats={s1} actual={n} · مقالي وأنشطة: stats={s2} actual={ess}" + ("" if ok else "   ⚠️"))
            bad += [] if ok else ["count:علّل/مقالي"]
    s = st.get("تقييمات")
    ok = s is None or s == c["tq"]
    print(f"  tq         stats={s} badges={c['tq']}" + ("" if ok else "   ⚠️")); bad += [] if ok else ["tq"]
    if "shots" in r: print(f"  shots      {r['shots']}")
    print("  RESULT     " + ("ALL OK" if not bad else "FIX: " + ", ".join(bad)))
    return not bad


async def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    shots = "--shots" in sys.argv; do_min = "--no-min" not in sys.argv; do_alt = "--no-alt" not in sys.argv
    ok = True
    async with async_playwright() as pw:
        for f in args:
            ok &= report(f, await check(f, shots, do_min, do_alt, pw))
    sys.exit(0 if ok else 1)

asyncio.run(main())
