# -*- coding: utf-8 -*-
"""Shared kit for building one lesson HTML from the unit-3 template (html/lesson_3_1.html).

Usage inside a generator (e.g. gen_l11.py):
    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "kit"))
    from kit import *
    E, B = [], []          # E = explanation blocks, B = bank blocks
    ...
    write_lesson("1-1", "تطور تكنولوجيا المعلومات والتحول الاجتماعي", E, B, extra_css=EXTRA_CSS, start=2, total=99)

Rules: never edit html/lesson_3_1.html (the template) or this file from a lesson generator.
Lesson-specific CSS goes in extra_css and must be prefixed/scoped so it cannot leak into other lessons.
"""
import os, re

KIT = os.path.dirname(os.path.abspath(__file__))
def _find_html():
    """html/ folder with the template: $LESSON_HTML, or ../html, or ../../html (when kit lives in tools/kit)."""
    cands = [os.environ.get("LESSON_HTML", ""), os.path.join(os.path.dirname(KIT), "html"),
             os.path.join(os.path.dirname(os.path.dirname(KIT)), "html")]
    for c in cands:
        if c and os.path.exists(os.path.join(c, "lesson_3_1.html")): return c
    raise SystemExit("html/ folder with lesson_3_1.html not found; set LESSON_HTML")
HTML = _find_html()                              # lesson files + fonts/ + assets/
ROOT = os.path.dirname(HTML)
TEMPLATE = os.path.join(HTML, "lesson_3_1.html")

# ---------- inline markers ----------
FX = '<span class="fx">للفهم</span>'            # «للفهم» pill: only on explanation content that is NOT from the book
FXA = '<span class="fx abs">للفهم</span>'       # same, absolutely positioned (inside boxes that use it in unit 3)
TQ = '<span class="tq">تقييمات</span>'          # «تقييمات» badge: bank question that appears in تقييمات الترم الاول.pdf
MARK6 = '<span class="mk">[<span class="num">6</span> درجات]</span>'
L = ["أ", "ب", "ج", "د", "هـ", "و"]
AB = '<span class="ab"></span>'                  # small answer box

def num(t): return f'<span class="num">{t}</span>'                       # digits in Baloo numerals
def tg(t): return f'<bdi class="tg">&lt;{t}&gt;</bdi>'                  # HTML tag inside Arabic text
def en(t): return f'<bdi>{t}</bdi>'                                     # English term next to another English term
def nw(t): return f'<bdi class="nw">{t}</bdi>'                          # English chunk that must stay on one line
def lines(n): return '<div class="wl"><i></i></div>' * n                # n writing lines
def blank(w=70): return f'<span class="bl" style="width:{w}pt"></span>'  # inline blank
def opts(items, cols=1):
    return f'<ul class="op c{cols}">' + "".join(f'<li><b>{L[k]}‌</b>{t}</li>' for k, t in enumerate(items)) + '</ul>'
def classify(items, letters=None, w=False):
    """numbered items each with an answer box; w=True -> wide box (answer is a word)."""
    ks = letters or [str(k + 1) for k in range(len(items))]
    ab = AB.replace('class="ab"', 'class="ab w"') if w else AB
    return '<ul class="cl">' + "".join(f'<li><span class="k">{ks[k]}</span><span class="t">{t}</span>{ab}</li>' for k, t in enumerate(items)) + '</ul>'
def card(n, title, body, tag=""):
    """bank question card. n="" -> continuation card (no header)."""
    t = f'<h4><span class="n">{n}</span> · {title}{tag}</h4>' if n else ""
    return f'<div class="qcard split {"cont" if not n else ""}">{t}{body}</div>'
def instr(t): return f'<p class="qi">{t}</p>'
def hint(t, label="عناصر الإجابة"): return f'<div class="hint"><b>{label}</b> {t}</div>'
def cat(title, count): return f'<h2 class="cat kwn">{title}<span class="cnt">{count}</span></h2>'
def cmp_table(heads, rows, tall=False):
    th = "".join(f"<th>{x}</th>" for x in heads)
    tr = "".join(f'<tr><td class="k">{r}</td>' + "<td></td>" * (len(heads) - 1) + "</tr>" for r in rows)
    return f'<table class="cmp{" tall" if tall else ""}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
def why(k, text, n_lines=2, tq=False, ess=False):
    """one «علّل» / essay item: number + text + writing lines (never splits across pages)."""
    return f'<div class="why{" ess" if ess else ""} split"><div class="qq"><span class="k">{k}</span>{TQ if tq else ""}<p>{text}</p></div>{lines(n_lines)}</div>'

def mcq_rows(mcq, tq_set=()):
    """mcq = [(stem, [4 options]), ...] -> list of '.mrow' blocks (2 questions per row)."""
    out = []
    def mq(j): return f'<div class="mq"><div class="qq"><span class="k">{j+1}</span>{TQ if j+1 in tq_set else ""}<p>{mcq[j][0]}</p></div>{opts(mcq[j][1], 2)}</div>'
    for i in range(0, len(mcq), 2):
        out.append('<div class="mrow">' + "".join(mq(j) for j in range(i, min(i + 2, len(mcq)))) + '</div>')
    return out
def fill_rows(fill):
    out = []
    for i in range(0, len(fill), 2):
        out.append('<div class="frow">' + "".join(f'<div><span class="k">{j+1}</span><p>{fill[j]}</p></div>' for j in range(i, min(i + 2, len(fill)))) + '</div>')
    return out
def tf_rows(tf):
    out = []
    for i in range(0, len(tf), 3):
        out.append('<ul class="tfb">' + "".join(f'<li><span class="k">{j+1}</span><span class="t">{tf[j]}</span><span class="pr">(&nbsp;&nbsp;&nbsp;&nbsp;)</span></li>' for j in range(i, min(i + 3, len(tf)))) + '</ul>')
    return out
def stats_bar(stats, n_tq):
    """stats = [(count, label), ...]; n_tq = number of «تقييمات» badges on questions."""
    return ('<div class="qstats">' + "".join(f'<div><b class="num">{n}</b><span>{t}</span></div>' for n, t in stats)
            + f'<div><b class="num">{n_tq}</b>{TQ}</div></div>')

def template_head(code, title, kind="الشرح + بنك الأسئلة"):
    tpl = open(TEMPLATE, encoding="utf-8").read()
    head = tpl[:tpl.index('<body data-lesson=')]
    head = head.replace("<title>الدرس 3-1 — البنية العامة لتطبيقات الويب</title>", f"<title>الدرس {code} — {title}</title>")
    head = head.replace("الدرس 3-1 (الشرح)", f"الدرس {code} ({kind})")
    return head

def write_lesson(code, title, E, B, extra_css="", start=1, total=1, out_name=None):
    """assemble and write html/lesson_X_Y.html. Returns output path."""
    head = template_head(code, title)
    body = (f'<body data-lesson="الدرس {code} — {title}" data-start="{start}" data-total="{total}">\n<main class="flow">\n'
            + "\n".join(E) + "\n\n<!-- ===================== بنك الأسئلة ===================== -->\n" + "\n".join(B)
            + "\n</main>\n</body>\n</html>\n")
    css = f"\n/* ---------- إضافات الدرس {code} ---------- */\n" + extra_css if extra_css else ""
    out = head.replace("</style>", css + "</style>", 1) + body
    # زي 3-3: الكارت اللي أوله h3 أو h4 يتعامل كعنوان
    out = out.replace("(el.firstElementChild && el.firstElementChild.tagName === 'H4')",
                      "(el.firstElementChild && /^H[34]$/.test(el.firstElementChild.tagName))")
    name = out_name or f"lesson_{code.replace('-', '_')}.html"
    path = os.path.join(HTML, name)
    open(path, "w", encoding="utf-8").write(out)
    return path
