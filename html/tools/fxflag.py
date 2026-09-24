# -*- coding: utf-8 -*-
"""fxflag — بادج «للفهم» على شكل علم مموّج طالع من جنب الحاجة (قرار زياد، الوحدة الأولى والتالتة).

- FLAG_CSS: يتحط في EXTRA_CSS بتاع المولّد.
- group_html(flow): ياخد HTML الشرح (العناصر اللي في المستوى الأول جوه main.flow)، ولو فيه حاجتين أو أكتر
  «للفهم» ورا بعض (note-line عليه للفهم · bridge أوله للفهم · صندوق أول حاجة فيه FXA) بيلمّهم في
  <div class="fxg keep"> عليه علم واحد + قوس + سهم لكل حاجة، وبيشيل علاماتهم الفردية.
- python3 tools/fxflag.py lesson_3_1.html  ← للدروس اللي مالهاش مولّد (3-1): بيحط الـCSS في <style id="fxflag">
  قبل </head> وبيعمل التجميع جوه الشرح. كل المولّدات (حتى gen_l21) بتشيل البلوك ده من الـhead بـstrip_style()،
  عشان الوحدة التانية ماتاخدوش من غير قصد.
"""
import re, sys
from html.parser import HTMLParser

FX = '<span class="fx">للفهم</span>'
FXA = '<span class="fx abs">للفهم</span>'
NL_TAG = '<span class="tag">للفهم</span>'
FLAG_CSS = '/* ==== fxflag: بادج «للفهم» علم مموّج طالع من الجنب + علم واحد بقوس وأسهم لكذا حاجة ورا بعض (tools/fxflag.py) ==== */\n.fx.abs,.fx.fl,.note-line .tag{position:absolute;left:-17pt;right:auto;top:50%;bottom:auto;float:none;transform:translateY(-50%) rotate(180deg);writing-mode:vertical-rl;width:26pt;height:auto;min-height:46pt;box-sizing:border-box;padding:9pt 0;margin:0;display:flex;align-items:center;justify-content:center;border:0;border-radius:0;background:#e29433;color:#17263f;font-size:11pt;line-height:26pt;font-weight:800;z-index:3;-webkit-mask:url("data:image/svg+xml;utf8,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 26 100\' preserveAspectRatio=\'none\'%3E%3Cpath d=\'M3,0 Q7,5 3,10 T3,20 T3,30 T3,40 T3,50 T3,60 T3,70 T3,80 T3,90 T3,100 L23,100 Q19,95 23,90 T23,80 T23,70 T23,60 T23,50 T23,40 T23,30 T23,20 T23,10 T23,0 Z\'/%3E%3C/svg%3E") 0 0/100% 100% no-repeat;mask:url("data:image/svg+xml;utf8,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 26 100\' preserveAspectRatio=\'none\'%3E%3Cpath d=\'M3,0 Q7,5 3,10 T3,20 T3,30 T3,40 T3,50 T3,60 T3,70 T3,80 T3,90 T3,100 L23,100 Q19,95 23,90 T23,80 T23,70 T23,60 T23,50 T23,40 T23,30 T23,20 T23,10 T23,0 Z\'/%3E%3C/svg%3E") 0 0/100% 100% no-repeat}\n.note-line{padding-left:14pt}\n.note-line .tag{left:-12pt;top:-1pt;transform:rotate(180deg);min-height:31pt;padding:2pt 0}\n.instr:has(>.fx.fl){position:relative;padding-left:24pt}\n*:has(>.fx.abs:not(.gflag)){position:relative;padding-left:max(24pt,var(--fpl,0pt))}\n.note-box .tag{background:#e29433;border-color:#e29433;color:#17263f}\n.fxr{position:relative;margin-left:20pt!important}\n.note-line.fxr,.bridge.fxr{padding-left:0}\n.fxr>.gline{position:absolute;left:-26pt;top:-15pt;bottom:-1pt;width:0;border-left:1.6pt solid #e29433;z-index:2}\n.fxr1>.gline{top:4pt;width:7pt;border-top:1.6pt solid #e29433;border-top-left-radius:6pt}\n.fxrN>.gline{bottom:4pt;width:7pt;border-bottom:1.6pt solid #e29433;border-bottom-left-radius:6pt}\n.fxr>.gflag{left:-39pt;min-height:44pt}\n.garr{position:absolute;left:-26pt;top:50%;width:23pt;height:0;border-top:1.6pt solid #e29433;margin-top:-.8pt;z-index:2;font-style:normal}\n.garr::after{content:"";position:absolute;right:-1pt;top:-4.6pt;border-left:6pt solid #e29433;border-top:3.8pt solid transparent;border-bottom:3.8pt solid transparent}\n'

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def split_blocks(s):
    """يقسم HTML لعناصر المستوى الأول: [(نص, هو عنصر؟)] بالترتيب."""
    lines = s.split("\n"); offs = [0]
    for l in lines: offs.append(offs[-1] + len(l) + 1)
    idx = lambda p: offs[p[0] - 1] + p[1]
    spans = []

    class P(HTMLParser):
        depth = 0; cur = None
        def handle_starttag(self, tag, attrs):
            if tag in VOID:
                if self.depth == 0:
                    st = idx(self.getpos()); spans.append((st, st + len(self.get_starttag_text())))
                return
            if self.depth == 0: self.cur = idx(self.getpos())
            self.depth += 1
        def handle_startendtag(self, tag, attrs):
            if self.depth == 0:
                st = idx(self.getpos()); spans.append((st, st + len(self.get_starttag_text())))
        def handle_endtag(self, tag):
            if tag in VOID: return
            self.depth -= 1
            if self.depth == 0:
                st = idx(self.getpos()); spans.append((self.cur, s.index(">", st) + 1))
    p = P(convert_charrefs=False); p.feed(s); p.close()
    out, pos = [], 0
    for a, b in spans:
        if a > pos: out.append((s[pos:a], False))
        out.append((s[a:b], True)); pos = b
    if pos < len(s): out.append((s[pos:], False))
    return out


def _kind(x):
    if x.startswith('<div class="note-line">') and NL_TAG in x: return "nl"
    if x.startswith('<div class="bridge">' + FX): return "br"
    m = re.match(r'<div class="[^"]*">', x)
    if m and x[m.end():].lstrip().startswith(FXA): return "abs"
    return None


def _mark(x, k, pos):
    """pos: 'first' / 'mid' / 'last' — كل عنصر بيفضل عنصر لوحده (عشان التقسيم على الصفحات)،
    وبيتضافله: جزء من القوس + سهم، والأول عليه العلم."""
    x = x.replace({"nl": NL_TAG, "br": FX, "abs": FXA}[k], "", 1)
    cls = " fxr" + {"first": " fxr1", "mid": "", "last": " fxrN"}[pos]
    x = re.sub(r'^<div class="([^"]*)"', lambda m: f'<div class="{m.group(1)}{cls}"', x, count=1)
    add = ('<span class="fx abs gflag">للفهم</span>' if pos == "first" else "") + '<i class="gline"></i><i class="garr"></i>'
    return re.sub(r'^(<div[^>]*>)', lambda m: m.group(1) + add, x, count=1)


def _pre(t):
    """قرارات زياد: «نموذج إجابة مقترح…» من غير «للفهم» خالص · «مثال من حياتنا» علامته تبقى علم على الجنب."""
    i = t.find("نموذج إجابة مقترح")
    if i != -1:
        j = t.find(FX, i)
        if j != -1 and j - i < 400: t = t[:j] + t[j + len(FX):]
    i = t.find("مثال من حياتنا")
    if i != -1:
        j = t.find(FX, i)
        if j != -1 and j - i < 80:
            t = t[:j] + t[j + len(FX):]
            t = re.sub(r'^(<div[^>]*>)', lambda m: m.group(1) + FXA, t, count=1)
    return t


def group_html(flow):
    parts = split_blocks(flow)
    out, run = [], []   # run: [(text, kind)] — kind=None للمسافات بين العناصر

    def flush():
        els = [i for i, (t, k) in enumerate(run) if k]
        if len(els) >= 2:
            for n, i in enumerate(els):
                t, k = run[i]
                run[i] = (_mark(t, k, "first" if n == 0 else "last" if n == len(els) - 1 else "mid"), k)
        out.extend(t for t, _ in run)
        run.clear()

    for t, is_el in parts:
        if is_el: t = _pre(t)
        if not is_el:
            if run and not t.strip(): run.append((t, None)); continue
            flush(); out.append(t); continue
        k = _kind(t)
        if k: run.append((t, k))
        else: flush(); out.append(t)
    flush()
    return "".join(out)


def strip_style(head):
    """المولّدات بتاخد الـhead من lesson_3_1.html — شيل بلوك fxflag بتاعه (المولّد بيضيف FLAG_CSS بنفسه لو عايزه)."""
    return re.sub(r'<style id="fxflag">.*?</style>\n?', "", head, flags=re.S)


def apply_file(path):
    h = open(path, encoding="utf-8").read()
    h = re.sub(r'\n?<style id="fxflag">.*?</style>', "", h, flags=re.S)
    i = h.index("</head>")
    h = h[:i] + '<style id="fxflag">\n' + FLAG_CSS + '</style>\n' + h[i:]
    a = h.index('<main class="flow">') + len('<main class="flow">')
    b = h.index('<!-- =====', a)
    h = h[:a] + group_html(h[a:b]) + h[b:]
    open(path, "w", encoding="utf-8").write(h)


if __name__ == "__main__":
    for f in sys.argv[1:]: apply_file(f); print("fxflag:", f)
