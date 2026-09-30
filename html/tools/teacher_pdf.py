# -*- coding: utf-8 -*-
"""بنوك الفصل الأول للتصوير: PDF للطالب (صفحات البنك زي ما هي في المذكرة) + نسخة المدرس (نفس الصفحات والإجابات بالأحمر فوقها).

    python3 tools/teacher_pdf.py [فولدر الإخراج]      (الافتراضي: html/print/banks/)

- المصدر: term1_book.html (نفس ترقيم المذكرة)، بالخطوط الثابتة بتاعة print_pdf.
- الإجابات من tools/teacher_keys_u1.py و tools/mcq_keys.json؛ كل خانة (فراغ/مربع/اختيارات/جدول/سطور/رسم) بتتعد
  في ترتيب ظهورها، ولو العدد مختلف عن المفتاح السكربت بيقف — عشان ولا إجابة تتكتب قدام سؤال غلط.
- الإجابات طبقة فوق الصفحة (position:absolute جوه .sheet)؛ مفيش ولا عنصر من الصفحة بيتغيّر مكانه أو مقاسه.
"""
import asyncio, json, os, sys, tempfile
from playwright.async_api import async_playwright

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
from print_pdf import FACE, static_fonts          # noqa: E402
from teacher_keys_u1 import KEYS                  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "print", "banks")
MCQ = json.load(open(os.path.join(TOOLS, "mcq_keys.json"), encoding="utf-8"))

JS = r"""
([L, key, mcq]) => {
  const RED = '#d0021b', FONT = "'Baloo Bhaijaan 2'";
  const pages = [...document.querySelectorAll('section.page')];
  const mine = pages.map((p, i) => [p, i]).filter(([p]) => p.closest('.' + L));
  const b0 = mine.findIndex(([p]) => p.querySelector('.content').innerText.slice(0, 160).includes('بنك الأسئلة'));
  if (b0 < 0) throw new Error(L + ': مفيش بنك');
  const bank = mine.slice(b0);
  const txt = e => e.innerText.replace(/\s+/g, ' ').trim();
  const letter = li => (li.querySelector('b') ? li.querySelector('b').textContent : '').replace(/[‌‍\s]/g, '');

  // 1) الخانات بالترتيب، لكل قسم
  const slots = {}; let sec = null;
  const secName = t => Object.keys(key).concat(['اختر الإجابة الصحيحة']).find(n => t.startsWith(n));
  for (const [pg] of bank) for (const e of pg.querySelector('.content').children) {
    if (e.matches('h2.cat')) { sec = secName(txt(e)); if (!sec) throw new Error(L + ': قسم مش معروف ' + txt(e)); slots[sec] = slots[sec] || {}; continue; }
    if (!sec || e.matches('.band,.qstats,.qcard.sol')) continue;
    const S = slots[sec]; const push = (t, v) => (S[t] = S[t] || []).push(v);
    let prevWL = false;
    for (const s of e.querySelectorAll('.bl, ul.op, .ab, td, .wl, li, .drawbox')) {
      let t = null;
      if (s.matches('.bl')) t = 'BL';
      else if (s.matches('ul.op')) t = 'OP';
      else if (s.matches('.ab')) t = 'AB';
      else if (s.matches('td')) t = txt(s) ? null : 'TD';
      else if (s.matches('.wl')) t = 'WL';
      else if (s.matches('li') && s.parentElement.matches('ul.tfb')) t = 'TF';
      else if (s.matches('.drawbox')) t = 'DB';
      if (!t) continue;
      if (t === 'WL' && prevWL) S.WL[S.WL.length - 1].push(s);
      else push(t, t === 'WL' ? [s] : s);
      prevWL = t === 'WL';
    }
  }

  // 2) مطابقة الأعداد
  const want = JSON.parse(JSON.stringify(key)); want['اختر الإجابة الصحيحة'] = { OP: mcq };
  const errs = [];
  for (const n of new Set([...Object.keys(want), ...Object.keys(slots)])) {
    const A = want[n] || {}, B = slots[n] || {};
    for (const t of new Set([...Object.keys(A), ...Object.keys(B)]))
      if ((A[t] || []).length !== (B[t] || []).length) errs.push(`${n}/${t}: مفتاح ${(A[t] || []).length} × صفحات ${(B[t] || []).length}`);
  }
  if (errs.length) throw new Error(L + ': ' + errs.join(' · '));

  // 3) الرسم
  const warn = [];
  const box = (s, r, css) => {
    const sh = s.closest('.sheet'), R = sh.getBoundingClientRect();
    const d = document.createElement('div'); d.className = 'tans';
    Object.assign(d.style, { position: 'absolute', left: (r.left - R.left) + 'px', top: (r.top - R.top) + 'px',
      width: r.width + 'px', height: r.height + 'px', color: RED, fontFamily: FONT, fontWeight: 700,
      direction: 'rtl', zIndex: 50, boxSizing: 'border-box', pointerEvents: 'none' }, css || {});
    sh.appendChild(d); return d;
  };
  const rect = (l, t, w, h) => ({ left: l, top: t, width: w, height: h });
  // يصغّر الخط لحد ما النص يدخل (min بالبوينت)
  const fit = (d, max, min, lh) => {
    for (let f = max; f >= min - 1e-6; f -= 0.25) {
      d.style.fontSize = f + 'pt'; if (lh) d.style.lineHeight = lh(f);
      if (d.scrollHeight <= d.clientHeight + 0.5 && d.scrollWidth <= d.clientWidth + 0.5) return f;
    }
    warn.push(txt(d).slice(0, 40)); return min;
  };
  const put = (d, v) => { const t = document.createElement('span'); t.textContent = v; d.appendChild(t); return t; };
  const fits = (d, t) => t.getBoundingClientRect().width <= d.clientWidth + 0.5;
  const one = (s, v, max = 10, min = 5.5) => {           // كلمة/جملة قصيرة في سطر واحد متوسّطة على الخانة
    if (!v) return;
    const r = s.getBoundingClientRect();
    const d = box(s, rect(r.left - 4, r.top, r.width + 8, r.height),
      { display: 'flex', alignItems: 'center', justifyContent: 'center', whiteSpace: 'nowrap', lineHeight: '1' });
    const t = put(d, v);
    for (let f = max; f >= min; f -= 0.25) { d.style.fontSize = f + 'pt'; if (fits(d, t)) return; }
    d.style.overflow = 'visible';                          // أقصر ما يمكن: يسيب الخانة تمتد بالعرض من الناحيتين
  };
  const blank = (s, v) => {                               // فوق خط الفراغ
    const r = s.getBoundingClientRect(), h = Math.max(r.height, 13);
    const d = box(s, rect(r.left - 3, r.bottom - h - 2, r.width + 6, h),
      { display: 'flex', alignItems: 'flex-end', justifyContent: 'center', whiteSpace: 'nowrap', lineHeight: '1.15' });
    const t = put(d, v);
    for (let f = 9.5; f >= 8.5; f -= 0.25) { d.style.fontSize = f + 'pt'; if (fits(d, t)) return; }
    // لو شمال الفراغ فاضي في نفس السطر (آخر الجملة/السطر): الإجابة تكمل ناحية الشمال بنفس الخط
    const par = s.parentElement, rg = document.createRange();
    rg.setStartAfter(s); rg.setEnd(par, par.childNodes.length);
    const same = [...rg.getClientRects()].filter(q => q.width > 0.5 && q.bottom > r.top + 2 && q.top < r.bottom - 2);
    const P = par.getBoundingClientRect(), limit = same.length ? Math.max(...same.map(q => q.right)) + 6 : P.left;
    for (let f = 9; f >= 7.5; f -= 0.25) {
      d.style.fontSize = f + 'pt';
      const need = t.getBoundingClientRect().width + 4;
      if (need <= r.right - 2 - limit) {
        const R = s.closest('.sheet').getBoundingClientRect();
        d.style.width = need + 'px'; d.style.left = (r.right - 2 - need - R.left) + 'px'; return;
      }
    }
    // أطول من الفراغ: سطرين فوق بعض في عرض الفراغ نفسه (جوه ارتفاع سطر الجملة) عشان مايغطيش الكلام اللي جنبه
    const lh = parseFloat(getComputedStyle(s.parentElement).lineHeight) || 24, H = Math.max(h, lh - 2);
    Object.assign(d.style, { top: (r.bottom - H - 1 - s.closest('.sheet').getBoundingClientRect().top) + 'px', height: H + 'px',
      whiteSpace: 'normal', textAlign: 'center', lineHeight: '1.05' });
    t.style.display = 'block';
    for (let f = 8.5; f >= 6.5; f -= 0.25) {
      d.style.fontSize = f + 'pt'; const b = t.getBoundingClientRect();
      if (b.height <= d.clientHeight + 0.5 && t.scrollWidth <= d.clientWidth + 0.5) return;
    }
    Object.assign(d.style, { whiteSpace: 'nowrap', lineHeight: '1.15', fontSize: '8.5pt', top: (r.bottom - h - 2 - s.closest('.sheet').getBoundingClientRect().top) + 'px', height: h + 'px' });
    t.style.display = '';
    // لسه مادخلش: سطر واحد يبدأ من أول الفراغ (يمين) ويكمل ناحية الشمال
    const w = t.getBoundingClientRect().width + 4, R = s.closest('.sheet').getBoundingClientRect();
    warn.push('فراغ ممدود: ' + v);
    d.style.width = w + 'px'; d.style.left = (r.right - 2 - w - R.left) + 'px'; d.style.justifyContent = 'flex-end';
  };
  const para = (s, r, v, max, pad) => {                  // نص طويل جوه مساحة (خانة جدول/مربع رسم)
    const d = box(s, r, { padding: pad || '2px 4px', display: 'flex', alignItems: 'center', justifyContent: 'center',
      textAlign: 'center', overflow: 'hidden' });
    const i = document.createElement('div'); i.textContent = v; d.appendChild(i);
    fit(d, max, 5.5, f => (f * 1.3) + 'pt');
  };
  const lines = (g, v) => {                               // على سطور الإجابة
    const rs = g.map(w => w.getBoundingClientRect());
    const top = rs[0].top, bot = rs[rs.length - 1].bottom, pitch = rs.length > 1 ? rs[1].top - rs[0].top : rs[0].height;
    const l = Math.min(...rs.map(r => r.left)), rr = Math.max(...rs.map(r => r.right));
    const d = box(g[0], rect(l + 6, top, rr - l - 12, bot - top), { textAlign: 'right', overflow: 'hidden' });
    d.textContent = v;
    // الأول: كل سطر نص على سطر من السطور؛ لو مادخلش، سطور أقرب لبعض بخط أصغر
    const w0 = warn.length; if (fit(d, 9.5, 7.5, () => pitch + 'px') !== 7.5 || d.scrollHeight <= d.clientHeight + 0.5) return;
    warn.length = w0; fit(d, 9, 5.5, f => (f * 1.32 * 96 / 72) + 'px');
  };
  const nest = (s, labels) => {                          // رسم مربعات متداخلة (الأوسع برّه)
    const r = s.getBoundingClientRect(), n = labels.length;
    const m = 10, top = 27, side = Math.min(60, (r.width - 2 * m - 200) / (2 * (n - 1))), bot = 7;
    labels.forEach((t, k) => {
      const d = box(s, rect(r.left + m + k * side, r.top + m + k * top, r.width - 2 * (m + k * side), r.height - 2 * m - k * (top + bot)),
        { border: '1.4pt solid ' + RED, borderRadius: '8px', fontSize: '9pt', lineHeight: '1.2', padding: '4px 10px',
          textAlign: 'right', background: `rgba(208,2,27,${0.03 + k * 0.025})` });
      d.textContent = t;
    });
  };
  const tf = (li, [m, fix]) => {
    const pr = li.querySelector('.pr'), t = li.querySelector('.t');
    one(pr, m, 12, 8);
    if (!fix) return;
    const rg = document.createRange(); rg.selectNodeContents(t);
    const lr = [...rg.getClientRects()].pop(), P = pr.getBoundingClientRect();
    const gap = lr.left - P.right - 12;
    if (gap > 40) {                                       // في المسافة بين آخر الجملة والقوس
      const d = box(li, rect(P.right + 8, lr.top - 1, gap, lr.height + 2),
        { display: 'flex', alignItems: 'center', justifyContent: 'center', whiteSpace: 'nowrap', lineHeight: '1' });
      const t = put(d, '← ' + fix);
      for (let f = 8.5; f >= 5.5; f -= 0.25) { d.style.fontSize = f + 'pt'; if (fits(d, t)) return; }
      d.remove();
    }
    const L0 = li.getBoundingClientRect();                // مفيش مكان: تحت السطر بخط صغير جوه حدود البند
    const d = box(li, rect(L0.left, L0.bottom - 9, L0.width - 30, 10),
      { whiteSpace: 'nowrap', fontSize: '6.5pt', lineHeight: '10px', textAlign: 'right' });
    d.textContent = '← ' + fix;
    warn.push('TF تحت السطر: ' + fix);
  };
  const op = (ul, v) => {
    if (v === null) return;
    const want = [].concat(v);
    const lis = [...ul.children].filter(li => want.includes(letter(li)));
    if (lis.length !== want.length) throw new Error(L + ': حرف مش موجود ' + want + ' في ' + txt(ul).slice(0, 40));
    for (const li of lis) {
      const r = li.getBoundingClientRect();
      box(li, rect(r.left - 2, r.top - 1, r.width + 4, r.height + 2),
        { border: '1.3pt solid ' + RED, borderRadius: '5px', background: 'rgba(208,2,27,.07)' });
    }
  };

  for (const n of Object.keys(want)) {
    const S = slots[n] || {}, A = want[n];
    (S.BL || []).forEach((s, i) => blank(s, A.BL[i]));
    (S.AB || []).forEach((s, i) => one(s, A.AB[i], 10, 5.5));
    (S.OP || []).forEach((s, i) => op(s, A.OP[i]));
    (S.TF || []).forEach((s, i) => tf(s, A.TF[i]));
    (S.TD || []).forEach((s, i) => para(s, s.getBoundingClientRect(), A.TD[i], 9));
    (S.WL || []).forEach((g, i) => lines(g, A.WL[i]));
    (S.DB || []).forEach((s, i) => Array.isArray(A.DB[i]) ? nest(s, A.DB[i]) : para(s, s.getBoundingClientRect(), A.DB[i], 11, '10px 18px'));
  }
  // علامة صغيرة إن دي نسخة المدرس
  for (const [pg] of bank) {
    const sh = pg.querySelector('.sheet'), H = sh.querySelector('.hdr').getBoundingClientRect(), R = sh.getBoundingClientRect();
    const d = document.createElement('div'); d.className = 'tans'; d.textContent = 'نسخة المدرس — الإجابات';
    Object.assign(d.style, { position: 'absolute', left: '50%', transform: 'translateX(-50%)', top: (H.top - R.top + H.height / 2 - 8) + 'px',
      color: RED, border: '1pt solid ' + RED, borderRadius: '8px', padding: '0 8px', fontFamily: FONT, fontWeight: 700,
      fontSize: '8pt', lineHeight: '14px', background: '#fff', zIndex: 50 });
    sh.appendChild(d);
  }
  return { first: bank[0][1] + 1, last: bank[bank.length - 1][1] + 1, warn };
}
"""


async def main():
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        h = open(os.path.join(BASE, "term1_book.html"), encoding="utf-8").read()
        h, n = FACE.subn(static_fonts(tmp), h)
        if not n: sys.exit("مالقيتش @font-face بتاع Baloo")
        tmp_html = os.path.join(BASE, ".teacher_book.html")
        open(tmp_html, "w", encoding="utf-8").write(h)
        try:
            async with async_playwright() as pw:
                b = await pw.chromium.launch()
                p = await b.new_page()

                async def load():
                    await p.goto("file://" + tmp_html)
                    await p.wait_for_function("document.body.dataset.ready==='1'", timeout=180000)
                    await p.evaluate("document.fonts.ready")

                await load()
                ranges = {}
                for lid in KEYS:
                    ranges[lid] = await p.evaluate("""L=>{const ps=[...document.querySelectorAll('section.page')];
                        const m=ps.map((p,i)=>[p,i]).filter(([p])=>p.closest('.'+L));
                        const b=m.find(([p])=>p.querySelector('.content').innerText.slice(0,160).includes('بنك الأسئلة'));
                        return [b[1]+1, m[m.length-1][1]+1]}""", "L" + lid.replace("-", ""))
                    f, l = ranges[lid]
                    out = os.path.join(OUT, f"بنك_{lid}_للطالب.pdf")
                    await p.pdf(path=out, prefer_css_page_size=True, print_background=True, page_ranges=f"{f}-{l}")
                    print("written", out, f"({f}-{l})")
                for lid, key in KEYS.items():
                    await load()                                     # نسخة نضيفة لكل درس
                    r = await p.evaluate(JS, ["L" + lid.replace("-", ""), key, MCQ[lid]])
                    assert [r["first"], r["last"]] == ranges[lid], r
                    for w in r["warn"]: print("  !", lid, w)
                    out = os.path.join(OUT, f"بنك_{lid}_نسخة_المدرس.pdf")
                    await p.pdf(path=out, prefer_css_page_size=True, print_background=True, page_ranges=f"{r['first']}-{r['last']}")
                    print("written", out)
                await b.close()
        finally:
            os.remove(tmp_html)


if __name__ == "__main__":
    asyncio.run(main())
