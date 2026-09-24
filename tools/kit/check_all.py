#!/usr/bin/env python3
"""Run every QA check on one or more lesson files.
   python3 kit/check_all.py html/lesson_1_1.html [--no-shots]
Pass criteria: same sheet count in all 3 renders, no OVERFLOW, stem/split OK, catcheck only allows the «صح وخطأ» header case,
bidiscan empty (except known false positive <E-mail>), and the stats bar matching the counted sections."""
import asyncio, sys, os, json, shutil, subprocess, tempfile
from pathlib import Path
from playwright.async_api import async_playwright
KIT = Path(__file__).resolve().parent
sys.path.insert(0, str(KIT)); from kit import HTML as _H
HTML = Path(_H)
ALT = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
OVER_JS = """()=>[...document.querySelectorAll('.sheet')].map(s=>{const c=s.querySelector('.content');const cr=c.getBoundingClientRect();
 let mb=0,w='';c.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.height>0&&r.bottom>mb){mb=r.bottom;w=e.className||e.tagName}});
 return [s.dataset.page,((mb-cr.top)*0.75).toFixed(1),(cr.height*0.75).toFixed(1),((mb-cr.bottom)*0.75).toFixed(1),String(w).slice(0,30)]})"""
async def render(pw, f, exe=None, dpr=2, shots=None, minfont=None):
    if minfont:
        ud = tempfile.mkdtemp(prefix="chmin_"); (Path(ud) / "Default").mkdir(parents=True)
        (Path(ud) / "Default" / "Preferences").write_text(json.dumps({"webkit": {"webprefs": {"minimum_font_size": minfont, "minimum_logical_font_size": minfont}}}))
        ctx = await pw.chromium.launch_persistent_context(ud, headless=True, executable_path=ALT, args=["--headless=new"], viewport={"width": 900, "height": 1200}, device_scale_factor=1.5)
        pg = await ctx.new_page(); closer = ctx
    else:
        br = await pw.chromium.launch(executable_path=exe) if exe else await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 900, "height": 1200}, device_scale_factor=dpr); closer = br
    await pg.goto(Path(f).resolve().as_uri()); await pg.wait_for_function("document.body.dataset.ready==='1'", timeout=40000)
    await pg.wait_for_timeout(300)
    info = await pg.evaluate(OVER_JS)
    if shots:
        shots.mkdir(exist_ok=True)
        for s in await pg.query_selector_all('.sheet'):
            await s.screenshot(path=str(shots / f"p{await s.get_attribute('data-page')}.png"))
    await closer.close()
    if minfont: shutil.rmtree(ud, ignore_errors=True)
    return info
async def main():
    files = [str(Path(a).resolve()) for a in sys.argv[1:] if not a.startswith("--")]
    shots = "--no-shots" not in sys.argv
    ok_all = True
    async with async_playwright() as pw:
        for f in files:
            f = str(Path(f).resolve()); stem = Path(f).stem
            a = await render(pw, f, shots=(HTML / f"qa_{stem}") if shots else None)
            b = await render(pw, f, exe=ALT, dpr=1)
            c = await render(pw, f, minfont=16)
            print(f"== {stem}: sheets default={len(a)} alt={len(b)} minfont16={len(c)}", "OK" if len(a) == len(b) == len(c) else "⚠️ SHEET COUNT MISMATCH")
            ok = len(a) == len(b) == len(c)
            for tag, info in (("default", a), ("alt", b)):
                for p, used, avail, over, last in info:
                    if float(over) > 0: print(f"   ⚠️ OVERFLOW [{tag}] page {p}: +{over}pt last={last}"); ok = False
            print("   page usage (default):", " ".join(f"{p}:{used}" for p, used, *_ in a))
            if shots: print(f"   screenshots: {HTML / ('qa_' + stem)}/pN.png")
            ok_all &= ok
    for script in ("stemcheck.py", "splitcheck.py", "catcheck.py"):
        r = subprocess.run([sys.executable, str(HTML / script)] + files, capture_output=True, text=True, cwd=HTML)
        print(f"-- {script}:", r.stdout.strip() or r.stderr.strip()[-400:])
    for f in files:
        r = subprocess.run([sys.executable, str(HTML / "bidiscan.py"), f], capture_output=True, text=True, cwd=HTML)
        print(f"-- bidiscan {Path(f).name}:", r.stdout.strip() or ("OK" if r.returncode == 0 else "ERROR " + r.stderr.strip()[-300:]))
        r = subprocess.run([sys.executable, str(HTML / "counts.py"), f], capture_output=True, text=True, cwd=HTML)
        print(f"-- counts {Path(f).name}:\n" + r.stdout.strip())
    print("RESULT:", "PASS (renders)" if ok_all else "FAIL")
asyncio.run(main())
