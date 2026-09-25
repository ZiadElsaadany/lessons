# -*- coding: utf-8 -*-
"""يبني html/lesson_1_1.html من قالب lesson_3_1.html (نفس الستايل والسكريبتات) + محتوى الدرس 1-1.
المصدر: المذكرة القديمة (الوحدة الأولى ص2–24) + كتاب الوزارة (ص5–12 من الـPDF) + «تقييمات الترم الأول» (ص3–9)."""
import re, sys
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fxflag import FLAG_CSS, group_html, strip_style

import os
TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import newsec as N

BASE = os.path.join(os.path.dirname(TOOLS), "")   # فولدر html (أبو فولدر tools)
tpl = open(BASE + "lesson_3_1.html", encoding="utf-8").read()
head = tpl[:tpl.index('<body data-lesson=')]
head = strip_style(head)
TITLE = "تطور تكنولوجيا المعلومات والتحول الاجتماعي"
head = head.replace("<title>الدرس 3-1 — البنية العامة لتطبيقات الويب</title>", f"<title>الدرس 1-1 — {TITLE}</title>")
head = head.replace("الدرس 3-1 (الشرح)", "الدرس 1-1 (الشرح + بنك الأسئلة)")

START, TOTAL = 2, 93      # ترقيم الوحدة الأولى: 1-1 ص2–26 · 1-2 ص27–47 · 1-3 ص48–71 · 1-4 ص72–93

FX = '<span class="fx">للفهم</span>'
FXA = '<span class="fx abs">للفهم</span>'
TQ = '<span class="tq">تقييمات</span>'
L = ["أ", "ب", "ج", "د", "هـ", "و"]
AB = '<span class="ab"></span>'
ARR = '<span class="arr">←</span>'
def num(t): return f'<span class="num">{t}</span>'
def en(t): return f'<bdi>{t}</bdi>'                             # كلمة إنجليزي جنب كلمة إنجليزي
def nw(t): return f'<bdi class="nw">{t}</bdi>'                  # لازم تفضل في سطر واحد
def lines(n): return '<div class="wl"><i></i></div>' * n
def blank(w=70): return f'<span class="bl" style="width:{w}pt"></span>'
def opts(items, cols=1):
    return f'<ul class="op c{cols}">' + "".join(f'<li><b>{L[k]}‌</b><span>{t}</span></li>' for k, t in enumerate(items)) + '</ul>'
def classify(items, letters=None, w=False):
    ks = letters or [str(k + 1) for k in range(len(items))]
    ab = AB.replace('class="ab"', 'class="ab w"') if w else AB
    return '<ul class="cl">' + "".join(f'<li><span class="k">{ks[k]}</span><span class="t">{t}</span>{ab}</li>' for k, t in enumerate(items)) + '</ul>'
def card(n, title, body, tag=""):
    t = f'<h4><span class="n">{n}</span> · {title}{tag}</h4>' if n else ""
    return f'<div class="qcard split {"cont" if not n else ""}">{t}{body}</div>'
def instr(t): return f'<p class="qi">{t}</p>'
def hint(t, label="عناصر الإجابة"): return f'<div class="hint"><b>{label}</b> {t}</div>'
def cat(title, count): return f'<h2 class="cat kwn">{title}<span class="cnt">{count}</span></h2>'
def cmp_table(heads, rows, badge=False, tall=False):
    th = "".join(f"<th>{x}</th>" for x in heads)
    tr = "".join(f'<tr><td class="k">{r}</td>' + "<td></td>" * (len(heads) - 1) + "</tr>" for r in rows)
    t = f'<table class="cmp{" tall" if tall else ""}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
    return f'<div class="cmpw">{TQ}{t}</div>' if badge else t
MARK6 = '<span class="mk">[<span class="num">6</span> درجات]</span>'

def lk(cls, d, c, cx, cy):
    return f'<svg class="lk {cls}" viewBox="0 0 20 16"><path d="{d}" fill="none" stroke="{c}" stroke-width="1.55" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="2" fill="{c}"/></svg>'

# ---------------- أيقونات خطية 24×24 ----------------
IC = {
    "gear": '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="6.8"/><path d="M12 2.6v2.6M12 18.8v2.6M2.6 12h2.6M18.8 12h2.6M5.4 5.4l1.8 1.8M16.8 16.8l1.8 1.8M5.4 18.6l1.8-1.8M16.8 7.2l1.8-1.8"/>',
    "bars": '<path d="M5 20v-6M10 20V9M15 20v-8M20 20V4"/>',
    "bulb": '<path d="M8.2 14.5a5.6 5.6 0 1 1 7.6 0c-.9.8-1.3 1.6-1.3 2.6h-5c0-1-.4-1.8-1.3-2.6z"/><path d="M9.6 19.6h4.8M10.4 22h3.2"/>',
 "expand": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 12h10M7 12l2.5-2.5M7 12l2.5 2.5M17 12l-2.5-2.5M17 12l-2.5 2.5"/>',
 "bolt": '<path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12z"/>',
 "wrench": '<path d="M14.5 3.5a5 5 0 0 0-5.9 6.6L3.5 15.2a2 2 0 0 0 2.8 2.8l5.1-5.1a5 5 0 0 0 6.6-5.9l-3 3-2.4-.6-.6-2.4z"/>',
 "coins": '<ellipse cx="12" cy="6" rx="7" ry="2.8"/><path d="M5 6v6c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8V6M5 12v6c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8v-6"/>',
 "chip": '<rect x="6" y="6" width="12" height="12" rx="1.5"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2.5V6M15 2.5V6M9 18v3.5M15 18v3.5M2.5 9H6M2.5 15H6M18 9h3.5M18 15h3.5"/>',
 "monitor": '<rect x="2.5" y="3.5" width="19" height="13" rx="1.8"/><path d="M8 20.5h8M12 16.5v4"/>',
 "down": '<path d="M12 3v12M7 10l5 5 5-5M5 20.5h14"/>',
 "home": '<path d="M3.5 11 12 4l8.5 7M6 9.5V20h12V9.5M10 20v-5h4v5"/>',
 "file": '<path d="M6 2.5h8l4 4v15H6z"/><path d="M14 2.5v4h4M9 12h6M9 15.5h6"/>',
 "usb": '<rect x="7" y="9" width="10" height="12.5" rx="1.5"/><path d="M9 9V3h6v6M10.5 5.5v1M13.5 5.5v1"/>',
 "net": '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="18" r="2.2"/><circle cx="19" cy="18" r="2.2"/><path d="M11 7 6 16M13 7l5 9M7.2 18h9.6"/>',
 "building": '<path d="M4 21V5l8-2.5V21M12 8.5l8 2.5v10M2.5 21h19M7 8h2M7 12h2M7 16h2M15 13h2M15 17h2"/>',
 "link": '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/>',
 "web": '<rect x="2.5" y="4" width="19" height="16" rx="2"/><path d="M2.5 8.5h19M5.5 6.3h.01M8 6.3h.01M6 12.5h8M6 16h12"/>',
 "phone": '<rect x="6.5" y="2" width="11" height="20" rx="2.2"/><path d="M10.5 18.5h3"/>',
 "food": '<path d="M3.5 12h17a8.5 8.5 0 0 1-17 0zM9 8.5c0-1.5 1.5-1.5 1.5-3M13 8.5c0-1.5 1.5-1.5 1.5-3"/>',
 "card": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M2.5 9.5h19M6 15h4"/>',
 "bus": '<rect x="4" y="3" width="16" height="15" rx="2.5"/><path d="M4 11h16M8 21v-3M16 21v-3M7.5 14.5h.01M16.5 14.5h.01"/>',
 "server": '<rect x="3.5" y="3" width="17" height="7.5" rx="1.5"/><rect x="3.5" y="13.5" width="17" height="7.5" rx="1.5"/><path d="M7 6.8h.01M7 17.3h.01M11 6.8h6M11 17.3h6"/>',
 "cloud": '<path d="M7 19h10.5a4.5 4.5 0 0 0 .6-9 6 6 0 0 0-11.6 1.5A3.8 3.8 0 0 0 7 19z"/>',
 "gauge": '<path d="M4 17a8 8 0 1 1 16 0"/><path d="M12 17l4-5"/><circle cx="12" cy="17" r="1.3"/>',
 "db": '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/><path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/>',
 "grid": '<rect x="3.5" y="3.5" width="7.5" height="7.5" rx="1.2"/><rect x="13" y="3.5" width="7.5" height="7.5" rx="1.2"/><rect x="3.5" y="13" width="7.5" height="7.5" rx="1.2"/><rect x="13" y="13" width="7.5" height="7.5" rx="1.2"/>',
 "lanes": '<path d="M20 6H7M20 12H7M20 18H7M9.5 3.5 7 6l2.5 2.5M9.5 9.5 7 12l2.5 2.5M9.5 15.5 7 18l2.5 2.5"/>',
 "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
 "leak": '<path d="M11 2.5 4.5 12h5l-1 7 6.5-9.5h-5z"/><path d="M18.5 14.5c1 1.4 1.6 2.3 1.6 3.1a1.6 1.6 0 0 1-3.2 0c0-.8.6-1.7 1.6-3.1z"/>',
 "tunnel": '<path d="M11 3v18M13.5 3v18"/><path d="M2.5 13.5c1.6 0 2.6-3 4.6-3M17.3 13.5c1.6 0 2.6-3 4.2-3"/><path d="M7.5 10.5h9" stroke-dasharray="1.4 1.8"/>',
 "chat": '<path d="M3.5 5.5h13v9H9l-4 3.5v-3.5H3.5z"/><path d="M16.5 9h4v8.5H19v3l-3.2-3H11v-3"/>',
 "cart": '<path d="M2.5 4h2.8l2.2 11h11l2-8H6.3"/><circle cx="9" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/>',
 "remote": '<rect x="4" y="4.5" width="16" height="11" rx="1.5"/><path d="M2 19.5h20M12 7.5a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM8.8 15.5c.5-1.8 1.7-2.6 3.2-2.6s2.7.8 3.2 2.6"/>',
 "grad": '<path d="M2 9.5 12 5l10 4.5-10 4.5z"/><path d="M6.5 11.5V16c1.5 1.5 3.4 2.2 5.5 2.2s4-.7 5.5-2.2v-4.5M21 10v5"/>',
 "pay": '<rect x="4" y="2.5" width="10" height="19" rx="2"/><path d="M7 7h4v4H7zM17 8.5c1 1 1.5 2.2 1.5 3.5s-.5 2.5-1.5 3.5M19.8 6.5c1.4 1.5 2.1 3.4 2.1 5.5s-.7 4-2.1 5.5"/>',
 "wheel": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.2"/><path d="M3.3 10.5h6.5M14.2 10.5h6.5M12 14.2V21"/>',
 "ar": '<rect x="5" y="2.5" width="14" height="19" rx="2"/><path d="M8 15h8M8 18h5"/><rect x="9" y="6" width="6" height="5" rx="1"/>',
 "vr": '<path d="M2.5 8h19v8.5h-6L12 13.5l-3.5 3H2.5z"/><path d="M6.5 11.3h2.5M15 11.3h2.5"/>',
 "atom": '<circle cx="12" cy="12" r="1.8"/><ellipse cx="12" cy="12" rx="9.5" ry="3.8"/><ellipse cx="12" cy="12" rx="9.5" ry="3.8" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="9.5" ry="3.8" transform="rotate(-60 12 12)"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "camera": '<rect x="2.5" y="6.5" width="19" height="13" rx="2"/><path d="M8 6.5 9.5 4h5L16 6.5"/><circle cx="12" cy="13" r="3.5"/>',
 "sensor": '<circle cx="12" cy="12" r="2"/><path d="M7.8 7.8a6 6 0 0 0 0 8.4M16.2 7.8a6 6 0 0 1 0 8.4M4.9 4.9a10 10 0 0 0 0 14.2M19.1 4.9a10 10 0 0 1 0 14.2"/>',
 "car": '<path d="M3 16.5v-4l2-5h14l2 5v4z"/><path d="M3 12.5h18"/><circle cx="7.5" cy="16.5" r="1.8"/><circle cx="16.5" cy="16.5" r="1.8"/>',
 "wifi": '<path d="M2.5 9a14 14 0 0 1 19 0M5.5 12.3a9.5 9.5 0 0 1 13 0M8.6 15.6a5 5 0 0 1 6.8 0"/><circle cx="12" cy="19" r="1.2"/>',
 "up": '<path d="M12 21V4M6.5 9.5 12 4l5.5 5.5"/>',
 "turn": '<path d="M17 21v-6a5 5 0 0 0-5-5H4M8 6 4 10l4 4"/>',
 "stop": '<path d="M8 2.5h8l5.5 5.5v8L16 21.5H8L2.5 16V8z"/><path d="M8 12h8"/>',
 "flag": '<path d="M5.5 21V3.5M5.5 4h11l-2.5 4 2.5 4h-11"/>',
 "people": '<circle cx="9" cy="8" r="3"/><path d="M3.5 19c.5-3.2 2.7-5 5.5-5s5 1.8 5.5 5"/><circle cx="17" cy="9" r="2.3"/><path d="M15.8 14.2c2.6-.3 4.4 1.2 4.9 4"/>',
 "camera2": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3.2"/>',
 "check": '<path d="M5 12.5 10 17 19 7"/>',
}
def ic(name, c="#22375c", w=1.8):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{IC[name]}</svg>')
def ic_ai(c="#22375c"):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="3"/>'
            f'<path d="M8 1.5V4M12 1.5V4M16 1.5V4M8 20v2.5M12 20v2.5M16 20v2.5M1.5 8H4M1.5 16H4M20 8h2.5M20 16h2.5"/>'
            f'<text x="12" y="15.2" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="8" fill="{c}" stroke="none">AI</text></svg>')
BULB = N.bulb("#e29433")

# ---------------- رسومات ----------------
TRANSISTOR = ('<svg class="tr" viewBox="0 0 90 96"><path d="M30 8h30a14 14 0 0 1 14 14v28H16V22A14 14 0 0 1 30 8z" fill="#22375c"/>'
              '<rect x="16" y="46" width="58" height="6" fill="#17263f"/><circle cx="45" cy="30" r="5" fill="#e29433"/>'
              '<path d="M29 52v38M45 52v38M61 52v38" stroke="#8a9ab3" stroke-width="3.2" stroke-linecap="round"/>'
              '<path d="M8 8v44" stroke="#e29433" stroke-width="1.4"/><path d="M4.5 12 8 7.5l3.5 4.5M4.5 48 8 52.5l3.5-4.5" fill="none" stroke="#e29433" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
_pins = "".join(f'<rect x="{18 + k * 9}" y="10" width="4" height="8" rx="1" fill="#8a9ab3"/><rect x="{18 + k * 9}" y="62" width="4" height="8" rx="1" fill="#8a9ab3"/>' for k in range(6))
_dots = "".join(f'<circle cx="{104 + (k % 4) * 8}" cy="{28 + (k // 4) * 8}" r="2.6" fill="#e29433"/>' for k in range(16))
IC_DRAW = (f'<svg class="icd" viewBox="0 0 150 80">{_pins}<rect x="12" y="17" width="62" height="46" rx="5" fill="#22375c"/><circle cx="21" cy="26" r="2.6" fill="#e29433"/>'
           f'<circle cx="116" cy="40" r="27" fill="#fff" stroke="#22375c" stroke-width="1.6" stroke-dasharray="3 2.5"/>{_dots}'
           '<path d="M74 30 90 22M74 50l16 8" stroke="#8a9ab3" stroke-width="1" stroke-dasharray="2 2"/></svg>')

def win(active=False, w=112):
    c = "#22375c"
    bar = '<rect x="30" y="7" width="70" height="7" rx="3.5" fill="#fff" stroke="#b9c7da" stroke-width="1"/>' if active else ""
    lk_ = '<rect x="14" y="52" width="46" height="8" rx="3" fill="#fdf3e2" stroke="#e29433" stroke-width="1" stroke-dasharray="2.5 1.8"/>' if active else '<rect x="14" y="52" width="40" height="7" rx="3" fill="#fff" stroke="#e29433" stroke-width="1.1"/>'
    return (f'<svg class="win" viewBox="0 0 {w} 76"><rect x="1.5" y="1.5" width="{w - 3}" height="73" rx="6" fill="#fff" stroke="{c}" stroke-width="2"/>'
            f'<path d="M1.5 19h{w - 3}" stroke="{c}" stroke-width="1.6"/><circle cx="10" cy="10.5" r="2.2" fill="#e29433"/><circle cx="17" cy="10.5" r="2.2" fill="#b9c7da"/>{bar}'
            f'<rect x="14" y="27" width="44" height="5" rx="2.5" fill="#22375c"/><rect x="14" y="37" width="{w - 36}" height="4" rx="2" fill="#b9c7da"/><rect x="14" y="44" width="{w - 50}" height="4" rx="2" fill="#b9c7da"/>{lk_}'
            f'<rect x="14" y="65" width="{w - 44}" height="4" rx="2" fill="#b9c7da"/></svg>')

PHONE = ('<svg class="ph" viewBox="0 0 120 110"><path d="M27 38a26 26 0 0 0 0 34M20 32a36 36 0 0 0 0 46M93 38a26 26 0 0 1 0 34M100 32a36 36 0 0 1 0 46" fill="none" stroke="#e29433" stroke-width="2" stroke-linecap="round"/>'
         '<rect x="38" y="6" width="44" height="98" rx="7" fill="#22375c"/><rect x="42" y="16" width="36" height="74" rx="2.5" fill="#fff"/><rect x="54" y="9.5" width="12" height="2.5" rx="1.2" fill="#8a9ab3"/><circle cx="60" cy="97" r="3" fill="none" stroke="#8a9ab3" stroke-width="1.2"/>'
         + "".join(f'<rect x="{45 + (k % 3) * 11}" y="{20 + (k // 3) * 11}" width="8" height="8" rx="2" fill="{"#e29433" if k < 6 else "#22375c"}"/>' for k in range(9))
         + '<rect x="45" y="56" width="30" height="16" rx="3" fill="#f5f7fb" stroke="#dde5ef"/><path d="M50 67c4-5 9-5 13-2s7 2 8 0" fill="none" stroke="#e29433" stroke-width="1.5" stroke-linecap="round"/></svg>')

CLOUD_DEV = ('<svg class="cd" viewBox="0 0 200 132"><path d="M72 50h58a16 16 0 0 0 2-31.8A22 22 0 0 0 90 22a14 14 0 0 0-18 28z" fill="#fdf3e2" stroke="#e29433" stroke-width="2.2" stroke-linejoin="round"/>'
             '<circle cx="62" cy="14" r="2.4" fill="#e29433"/><circle cx="146" cy="12" r="2.4" fill="#e29433"/><circle cx="156" cy="36" r="2" fill="#e29433"/>'
             '<path d="M100 52 44 82M100 52v30M100 52l56 30" stroke="#8a9ab3" stroke-width="1.3" stroke-dasharray="3 2.6"/>'
             '<rect x="28" y="82" width="32" height="22" rx="2.5" fill="#fff" stroke="#22375c" stroke-width="2"/><path d="M38 110h12M44 104v6" stroke="#22375c" stroke-width="2" stroke-linecap="round"/>'
             '<rect x="91" y="80" width="18" height="32" rx="3" fill="#fff" stroke="#22375c" stroke-width="2"/>'
             '<rect x="140" y="82" width="32" height="26" rx="3" fill="#fff" stroke="#22375c" stroke-width="2"/>'
             + "".join(f'<text x="{x}" y="128" direction="rtl" text-anchor="middle" font-size="10" fill="#4e5f7c" font-family="Baloo Bhaijaan 2" font-weight="700">{t}</text>' for x, t in [(44, "حاسب"), (100, "موبايل"), (156, "تابلت")])
             + '</svg>')

# قانون مور (رسم الكتاب) — مقياس لوغاريتمي من 10^3 لـ 10^11
def moore_svg():
    import math
    X0, X1, Y0, Yb = 58, 500, 40, 196            # حدود منطقة الرسم (Yb = المحور الأفقي)
    LO, HI = 2.2, 11                               # المحور الرأسي لوغاريتمي من 10^2.2 لـ 10^11 (الخطوط من 10^3)
    xa = lambda yr: X0 + (yr - 1967) * (X1 - X0) / 59
    ya = lambda lg: Yb - (lg - LO) * (Yb - Y0) / (HI - LO)
    F = 'font-family="Baloo Bhaijaan 2"'
    s = [f'<svg class="moore" viewBox="0 0 520 {Yb + 46}">']
    for e in range(3, 12):
        y = ya(e)
        s.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" stroke="#e6edf6" stroke-width="1"/>')
        s.append(f'<text x="{X0 - 8}" y="{y + 3.5:.1f}" direction="ltr" text-anchor="end" font-size="10" fill="#6e7f9c" {F} font-weight="600">10<tspan dy="-4" font-size="7">{e}</tspan></text>')
    for yr in range(1970, 2030, 10):
        x = xa(yr)
        s.append(f'<line x1="{x:.1f}" y1="{Yb}" x2="{x:.1f}" y2="{Yb + 4}" stroke="#8a9ab3" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{Yb + 15}" direction="ltr" text-anchor="middle" font-size="10" fill="#4e5f7c" {F} font-weight="600">{yr}</text>')
    s.append(f'<path d="M{X0} {Y0 - 8}V{Yb}H{X1 + 6}" fill="none" stroke="#22375c" stroke-width="1.4"/>')
    lg0 = math.log10(2300)
    x1, y1 = xa(1971), ya(lg0)
    x2, y2 = xa(2022), ya(lg0 + (2022 - 1971) * math.log10(2) / 2)
    s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#e29433" stroke-width="1.6" stroke-dasharray="5 4"/>')
    pts = [(1971, 2300, "Intel 4004 (1971)", "2,300", "r"), (1978, 29000, "Intel 8086 (1978)", "29,000", "r"),
           (1989, 1.2e6, "Intel 80486 (1989)", "1,200,000", "r"), (2000, 4.2e7, "Pentium 4 (2000)", "42,000,000", "r"),
           (2010, 1.17e9, "Core i7 (2010)", "1.17 مليار", "l"), (2022, 1.14e11, "Apple M1 Ultra (2022)", "114 مليار", "l")]
    for yr, v, name, val, side in pts:
        x, y = xa(yr), ya(math.log10(v))
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="#22375c" stroke="#fff" stroke-width="1.4"/>')
        if side == "r":   # تحت الخط ويمين النقطة: الاسم والقيمة في سطر واحد (ltr)
            s.append(f'<text x="{x + 7:.1f}" y="{y + 14:.1f}" direction="ltr" font-size="9.6" fill="#17263f" {F} font-weight="700">{name}<tspan fill="#a9670f" font-weight="600" font-size="8.8" dx="5">{val}</tspan></text>')
        else:             # فوق الخط وشمال النقطة: الاسم ltr بنهايته عند x−8، والقيمة (عربي rtl) فوقه بتبدأ عند x−8
            s.append(f'<text x="{x - 8:.1f}" y="{y - 5:.1f}" direction="ltr" text-anchor="end" font-size="9.6" fill="#17263f" {F} font-weight="700">{name}</text>')
            s.append(f'<text x="{x - 8:.1f}" y="{y - 17:.1f}" direction="rtl" font-size="8.8" fill="#a9670f" {F} font-weight="600">{val}</text>')
    s.append(f'<rect x="72" y="{Y0 - 4}" width="170" height="44" rx="5" fill="#fff" stroke="#dde5ef"/>')
    s.append(f'<line x1="212" y1="{Y0 + 10}" x2="234" y2="{Y0 + 10}" stroke="#e29433" stroke-width="1.6" stroke-dasharray="5 4"/>')
    s.append(f'<text x="206" y="{Y0 + 13.5}" direction="rtl" font-size="10" fill="#33445f" {F} font-weight="600">تضاعف تقريبا كل عامين</text>')
    s.append(f'<circle cx="223" cy="{Y0 + 28}" r="4" fill="#22375c"/>')
    s.append(f'<text x="206" y="{Y0 + 31.5}" direction="rtl" font-size="10" fill="#33445f" {F} font-weight="600">معالجات فعلية</text>')
    s.append(f'<text x="{(X0 + X1) / 2:.0f}" y="{Yb + 36}" direction="rtl" text-anchor="middle" font-size="11" fill="#22375c" {F} font-weight="800">السنة</text>')
    s.append(f'<text transform="translate(14 {(Y0 + Yb) / 2:.0f}) rotate(-90)" direction="rtl" text-anchor="middle" font-size="10.5" fill="#22375c" {F} font-weight="800">عدد الترانزستورات في الشريحة</text>')
    s.append('</svg>')
    return "".join(s)

AR_SVG = ('<svg viewBox="0 0 200 118"><rect width="200" height="118" rx="6" fill="#eef2f8"/>'
          '<rect x="14" y="22" width="44" height="80" fill="#d5dfec"/><rect x="146" y="30" width="42" height="72" fill="#d5dfec"/>'
          '<path d="M0 102h200" stroke="#c3cfdf" stroke-width="2"/>'
          '<rect x="66" y="14" width="68" height="94" rx="7" fill="#17263f"/><rect x="71" y="20" width="58" height="82" rx="3" fill="#f8fafd"/>'
          '<rect x="71" y="20" width="16" height="82" fill="#d5dfec"/><rect x="113" y="20" width="16" height="82" fill="#d5dfec"/>'
          '<rect x="93" y="32" width="26" height="15" rx="3" fill="none" stroke="#e29433" stroke-width="2.4"/>'
          '<circle cx="84" cy="42" r="6" fill="#2e4a78"/><path d="M84 38.5v7M80.5 42h7" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>'
          '<path d="M100 62l7-11 7 11z" fill="#2e4a78"/><rect x="85" y="72" width="32" height="6" rx="3" fill="#2e4a78"/>'
          '<path d="M104 108c8-8 18-9 30-6 6 1.5 8 5 6 8" fill="#f1c9a5"/></svg>')
VR_SVG = ('<svg viewBox="0 0 200 118"><rect width="200" height="118" rx="6" fill="#1d4163"/>'
          '<path d="M30 118 60 70M170 118 140 70M0 96h200M0 82h200" stroke="#2e5a82" stroke-width="1"/>'
          '<rect x="36" y="24" width="20" height="20" rx="3" fill="#3e9ccb" transform="rotate(-15 46 34)"/>'
          '<path d="M96 16l13 22H83z" fill="#dde5ef"/><circle cx="154" cy="32" r="10" fill="#e29433"/>'
          '<path d="M72 118c0-20 12-32 28-32s28 12 28 32z" fill="#2e4a78"/>'
          '<circle cx="100" cy="70" r="17" fill="#f1c9a5"/><path d="M83 66a17 17 0 0 1 34 0z" fill="#17263f"/>'
          '<rect x="80" y="64" width="40" height="13" rx="6" fill="#3e9ccb" stroke="#17263f" stroke-width="2"/></svg>')
BIT_SVG = ('<svg viewBox="0 0 160 70"><rect x="20" y="15" width="120" height="40" rx="20" fill="#eef2f8" stroke="#dde5ef" stroke-width="1.5"/>'
           '<text x="52" y="41" text-anchor="middle" font-size="16" fill="#9aa8bd" font-family="Baloo Bhaijaan 2" font-weight="800">0</text>'
           '<circle cx="108" cy="35" r="16" fill="#22375c"/><text x="108" y="41" text-anchor="middle" font-size="16" fill="#fff" font-family="Baloo Bhaijaan 2" font-weight="800">1</text></svg>')
QUBIT_SVG = ('<svg viewBox="0 0 160 96"><circle cx="80" cy="50" r="34" fill="#dbe8f5" stroke="#22375c" stroke-width="1.8"/>'
             '<ellipse cx="80" cy="50" rx="34" ry="10" fill="none" stroke="#22375c" stroke-width="1.2" stroke-dasharray="3 2.5"/>'
             '<path d="M80 16v68" stroke="#8a9ab3" stroke-width="1" stroke-dasharray="2 2"/>'
             '<path d="M80 50 102 25" stroke="#e29433" stroke-width="2.6" stroke-linecap="round"/><circle cx="102" cy="25" r="4" fill="#e29433"/><circle cx="80" cy="50" r="2.6" fill="#22375c"/>'
             '<text x="80" y="11" text-anchor="middle" font-size="11" fill="#22375c" font-family="Baloo Bhaijaan 2" font-weight="800">0</text>'
             '<text x="80" y="96" text-anchor="middle" font-size="11" fill="#22375c" font-family="Baloo Bhaijaan 2" font-weight="800">1</text></svg>')


# رسم الكتاب: سيارة ذاتية القيادة تقرر على متنها (إعادة رسم SVG للصورة اللي في الكتاب)
def selfdrive_svg():
    F = 'font-family="Baloo Bhaijaan 2"'
    return ('<svg class="sdv" viewBox="0 0 520 176">'
      '<rect x="0" y="0" width="520" height="176" rx="8" fill="#f5f7fb"/>'
      '<rect x="0" y="146" width="520" height="22" fill="#e6edf6"/><path d="M8 157H512" stroke="#fff" stroke-width="2.4" stroke-dasharray="14 10"/>'
      # أشعة الاستشعار
      '<path d="M150 118 92 76V148z" fill="#3e9ccb" opacity=".16"/><path d="M332 118 402 72V150z" fill="#3e9ccb" opacity=".16"/>'
      # المشاة
      '<rect x="40" y="70" width="54" height="80" rx="3" fill="none" stroke="#22375c" stroke-width="1.2" stroke-dasharray="4 3"/>'
      '<circle cx="67" cy="86" r="6" fill="#2e4a78"/><path d="M67 93v24M67 100l-8 9M67 100l7 8M67 117l-7 20M67 117l6 20" stroke="#2e4a78" stroke-width="3.6" stroke-linecap="round" fill="none"/>'
      # السيارة التانية
      '<rect x="402" y="72" width="104" height="78" rx="3" fill="none" stroke="#22375c" stroke-width="1.2" stroke-dasharray="4 3"/>'
      '<path d="M412 136v-18l12-22h52l18 20v20z" fill="#b9c6d8"/><path d="M430 100h22v16h-32zM458 100h16l14 16h-30z" fill="#eef2f8"/>'
      '<circle cx="432" cy="138" r="9" fill="#44506a"/><circle cx="484" cy="138" r="9" fill="#44506a"/>'
      # السيارة ذاتية القيادة
      '<path d="M148 136v-16c0-6 4-10 10-11l26-4 22-18h70l30 20 22 4c5 1 8 5 8 10v15z" fill="#2e6fd1"/>'
      '<path d="M212 91h30v18h-50zM250 91h24l22 18h-46z" fill="#dbe8f5"/>'
      '<rect x="244" y="78" width="14" height="8" rx="2" fill="#22375c"/>'
      '<circle cx="182" cy="138" r="11" fill="#22375c"/><circle cx="182" cy="138" r="4.5" fill="#b9c6d8"/><circle cx="302" cy="138" r="11" fill="#22375c"/><circle cx="302" cy="138" r="4.5" fill="#b9c6d8"/>'
      '<circle cx="246" cy="122" r="13" fill="#e29433" opacity=".25"/><rect x="238" y="114" width="16" height="16" rx="2.5" fill="#e29433"/><rect x="242.5" y="118.5" width="7" height="7" fill="#fff"/>'
      # السحابة (مش بتتبعت لها)
      '<path d="M258 78 402 32" stroke="#8a9ab3" stroke-width="1.3" stroke-dasharray="4 3.5"/>'
      '<path d="M404 44h52a13 13 0 0 0 1-26 18 18 0 0 0-34-4 12 12 0 0 0-19 30z" fill="#fff" stroke="#8a9ab3" stroke-width="1.6"/>'
      '<path d="M398 8 466 52" stroke="#c0453a" stroke-width="3" stroke-linecap="round"/>'
      f'<text x="512" y="68" direction="rtl" font-size="10" fill="#4e5f7c" {F} font-weight="700">لا تُرسل إلى السحابة</text>'
      # لافتة الحوسبة الطرفية
      '<rect x="176" y="18" width="150" height="38" rx="5" fill="#22375c"/><path d="M246 56l5 7 5-7z" fill="#22375c"/><path d="M251 63V112" stroke="#22375c" stroke-width="1.2"/>'
      f'<text x="304" y="33" direction="rtl" font-size="11" fill="#f1c88b" {F} font-weight="800">حوسبة طرفية</text>'
      f'<text x="317" y="49" direction="rtl" font-size="9.4" fill="#fff" {F} font-weight="600">معالجة فورية على متن المركبة</text>'
      f'<text x="160" y="24" direction="rtl" font-size="10.4" fill="#22375c" {F} font-weight="800">سيارة ذاتية القيادة — قرار في الحال</text>'
      '</svg>')

def recall(items):
    return ('<div class="rcl keep"><span class="rl">ثبّت الصفحة في 10 ثواني</span><div class="rc">'
            + '<i>·</i>'.join(f'<span>{t}</span>' for t in items) + '</div></div>')

# ============================ الشرح ============================
E = []
A = E.append
A(f'''<div class="band">
  <div class="badge"><span class="l">الدرس</span><span class="n">1-1</span></div>
  <h1>{TITLE}</h1>
  <div class="who">
    <div class="t"><span class="u">الفصل الأول</span><span class="k">الشرح والمراجعة</span></div>
    <img src="assets/avatar.png" alt="">
  </div>
</div>''')
A(f'''<div class="two">
  <div class="intro">
    <h3>أهلًا بيك — أول درس معانا</h3>
    <div class="body">
      <img class="robot" src="assets/robot.svg" alt="">
      <p>تخيل نفسك رجعت <b>تلاتين سنة لورا</b>…</p>
      <p>الإنترنت مش بالشكل اللي تعرفه دلوقتي، والموبايل مش في إيد كل واحد، وخدمات زي <b>التعلم أونلاين</b>، و<b>التسوق الإلكتروني</b>، و<b>الدفع من غير كاش</b> ما كانتش منتشرة أو متاحة بالصورة اللي نعرفها النهارده.</p>
      <p>طب إزاي وصلنا من <b>الحواسيب الضخمة اللي كانت بتملأ غرفة</b>، لحد <b>موبايل في إيدك يوصلك بالعالم كله</b>؟</p>
      <p>في الدرس ده هنمشي في رحلة تطور تكنولوجيا المعلومات:</p>
      <p class="trip">من الحواسيب الإلكترونية الأولى والصمامات المفرغة <span class="arw">←</span> للحاسب الشخصي <span class="arw">←</span> للإنترنت والويب <span class="arw">←</span> للهواتف الذكية <span class="arw">←</span> للحوسبة السحابية والتقنيات الحديثة.</p>
      <p>وفي كل مرحلة هنشوف حاجة مهمة:</p>
      <p>التكنولوجيا ما غيرتش الأجهزة بس… دي غيرت <b>طريقة تواصل الناس، وشغلهم، وتعلمهم، وتسوقهم، ودفعهم</b>.</p>
    </div>
    <div class="foot"><span class="pill-dark">جاهز؟ يلا نبدأ الرحلة</span></div>
  </div>
  <div class="goals">
    <h3>أهداف التعلم</h3>
    <div class="g"><span class="tag">اشرح</span><span class="x">المراحل الرئيسية في تطور تكنولوجيا المعلومات وأثرها في المجتمع.</span></div>
    <div class="g"><span class="tag">اذكر</span><span class="x">أمثلة على التغيرات الاجتماعية والتقنيات الناشئة التي أحدثتها تكنولوجيا المعلومات، واشرح خصائصها.</span></div>
    <div class="g"><span class="tag">حلّل</span><span class="x">أثر إحدى تقنيات المعلومات في فئات مختلفة من المجتمع، وبرّر قرارًا مستندًا إلى الأدلة.</span></div>
  </div>
</div>''')
A('<div class="note-box"><span class="tag">للفهم</span>أي جزء عليه علامة «للفهم» هو شرح أو رسم إضافي للتوضيح، ومش مطلوب حفظه كنص من الكتاب.</div>')
A(f'''<div class="map m2">
  <div class="cell c1"><h4><span class="mn">1</span>مراحل التطوّر الخمس</h4><ul>
    <li><b>الأربعينيات–الستينيات:</b> حواسيب إلكترونية</li>
    <li><b>السبعينيات–الثمانينيات:</b> حواسب شخصية</li>
    <li><b>التسعينيات:</b> الإنترنت التجاري والويب</li>
    <li><b>العقد الأول من الألفية:</b> الهواتف الذكية</li>
    <li><b>من العقد الثاني فصاعدًا:</b> الحوسبة السحابية</li></ul>
    <div class="imp"><b>أثر كل مرحلة:</b> أجهزة أصغر وأكثر ترابطًا.</div></div>
  <div class="cell c3"><h4><span class="mn">2</span>قانون مور</h4><ul>
    <li>عدد الترانزستورات في الدوائر المتكاملة يتضاعف تقريبًا كل عامين.</li>
    <li>اتجاه تاريخي، لا قانون فيزيائي ثابت.</li>
    <li><b>تحديات:</b> تيارات التسرّب والنفق الكمومي.</li>
    <li><b>بدائل:</b> تعدّد الأنوية والمعالجة المتوازية.</li></ul></div>
  <div class="hub">تطوّر تكنولوجيا<br>المعلومات والتحوّل<br>الاجتماعي
    {lk("r1", "M0 14 C7 14 10 3 17 3", "#22375c", 17.5, 3)}
    {lk("r2", "M0 2 C7 2 10 13 17 13", "#e29433", 17.5, 13)}
    {lk("l1", "M20 14 C13 14 10 3 3 3", "#2e4a78", 2.5, 3)}
    {lk("l2", "M20 2 C13 2 10 13 3 13", "#a9670f", 2.5, 13)}
  </div>
  <div class="cell c2"><h4><span class="mn">3</span>خمسة تغيّرات اجتماعية</h4><ul>
    <li>شبكات التواصل الاجتماعي</li>
    <li>التجارة الإلكترونية</li>
    <li>العمل عن بُعد</li>
    <li>التعلّم عبر الإنترنت</li>
    <li>الدفع غير النقدي</li></ul>
    <div class="imp"><b>ومعاها تحديات:</b> الأمان والإنصاف وإتاحة الوصول.</div></div>
  <div class="cell c4"><h4><span class="mn">4</span>تقنيات ناشئة بارزة</h4><ul>
    <li>القيادة الذاتية (+ الحوسبة الطرفية)</li>
    <li>الواقع المعزّز: يضيف عناصر رقمية للواقع</li>
    <li>الواقع الافتراضي: بيئة افتراضية كاملة</li>
    <li>الحوسبة الكمومية والكيوبت</li></ul></div>
</div>''')
A('''<div class="iq">
  <div class="q">
    <div class="lab">السؤال الرئيسي — الدرس كله بيجاوب عليه</div>
    <div class="qq">كيف تطورت تكنولوجيا المعلومات عبر مراحلها الرئيسية، وكيف غيّرت كل مرحلة المجتمع؟</div>
  </div>
  <div class="idea"><span class="qmark">”</span><b>الفكرة الأساسية:</b> في كل مرحلة أضافت تكنولوجيا المعلومات <b>جهازًا جديدًا</b>، وغيّرت معه <b>طريقة تواصل المجتمع وعمله وتجارته</b>.</div>
</div>''')

# ---- الجزء الأول
A('<div class="part p1"><span>الجزء الأول</span></div>\n<hr class="rule">')
A(f'<h2 class="sec"><span class="num"></span>قبل أي حاجة: «تكنولوجيا المعلومات» دي إيه أصلًا؟{FX}</h2>')
A('<p class="lead kwn">الكتاب هيبدأ يحكيلك تاريخها على طول — فخلّينا نتفق الأول هي إيه، عشان التاريخ يبقى ليه معنى. أي حاجة بتعملها بمعلومة، بتعملها بواحد من <b>خمسة أفعال</b> بس: <b>تجمعها · تخزّنها · تعالجها · تنقلها · تعرضها</b>. و<b>تكنولوجيا المعلومات <bdi>(IT)</bdi></b> هي كل <b>الأجهزة والبرامج والشبكات</b> اللي بتأدّي الأفعال دي إلكترونيًا.</p>')
VERBS = [("camera", "جمع", "بتصوّر صورة بموبايلك"), ("db", "تخزين", "بتتحفظ في الذاكرة"), ("chip", "معالجة", "بتحط عليها فلتر"),
         ("net", "نقل", "بتبعتها على واتساب"), ("monitor", "عرض", "بتظهر على شاشة صاحبك")]
A('<div class="verbs keep"><div class="vh"><span class="lb">' + BULB + 'خُد مثال من يومك إنت</span></div><div class="vr">'
  + f'<i class="va">{ARR}</i>'.join(f'<div class="vc"><span class="vi">{ic(i, "#22375c")}</span><b>{v}</b><small>{t}</small></div>' for i, v, t in VERBS)
  + '</div><div class="vf">الخمسة دول حصلوا في <b>تلات ثواني</b> وإنت مش واخد بالك — وده كله اسمه <b>تكنولوجيا معلومات</b>.</div></div>')
A(f'<div class="note-line"><span class="tag">للفهم</span><span class="lead">طب ليه؟</span><b>وليه الدرس ده موجود أصلًا؟</b> لأن الأفعال الخمسة دي ما اتغيّرتش ولا مرة من ساعة أول حاسب لحد النهارده. اللي اتغيّر هو <b>العدّة</b> اللي بتعملهم بيها: بقت أصغر وأسرع وأرخص، وأهم حاجة — <b>بقت متوصّلة ببعض</b>. والدرس بيرتّب مراحل التطوّر وبيوضّح أثر كل مرحلة على حياة الناس.</div>')

A(f'<h2 class="sec"><span class="num">1</span><span class="dot">·</span> المفتاح الصغير اللي كل حاجة مبنية عليه{FX}</h2>')
A(f'<p class="lead kwn"><b>الدوائر الرقمية</b> بتمثّل البيانات باستخدام <b>حالتين</b> بنرمز لهما بـ{num("0")} و{num("1")}. وللتبسيط، نقدر نتخيّل <b>الترانزستور</b> كأنه <b>مفتاح إلكتروني</b> بيتحكّم في مرور التيار. عشان الجهاز يحسب أي حاجة، لازم يكون عنده مفاتيح زي دي تقدر تفتح وتقفل ملايين المرات في الثانية. وتصغير المفتاح ده <b>ساعد</b> على تطوّر الحواسيب — <b>جنب</b> تطوّر البرمجيات والشبكات ووسائل التخزين، مش لوحده.</p>')
A(f'''<div class="comp3 keep">
  <div class="cc"><div class="cv"><img src="assets/u1/vacuum_tube.jpg" alt=""></div><h4><span class="cn">1</span>الصمام المفرَّغ</h4><p>لمبة زجاج مفرَّغة من الهوا، حجمها زي صباعك تقريبًا، بتشتغل كمفتاح. الحاسب الواحد كان محتاج <b>آلاف</b> منها.</p></div>
  <i class="ca">{ARR}</i>
  <div class="cc"><div class="cv">{TRANSISTOR}<span class="sm">أصغر بكتير</span></div><h4><span class="cn">2</span>الترانزستور</h4><p>مفتاح إلكتروني بيعمل <b>نفس شغل الصمام</b> بس من مادة صلبة: أصغر بمراحل، بيسخن أقل، بيستهلك كهربا أقل، وعمره أطول.</p></div>
  <i class="ca">{ARR}</i>
  <div class="cc"><div class="cv">{IC_DRAW}</div><h4><span class="cn">3</span>الدائرة المتكاملة <bdi>(IC)</bdi></h4><p>بدل ما نلحّم ترانزستورات منفصلة بأسلاك، بنطبع <b>ملايين منها على قطعة سيليكون واحدة</b> — دي اللي بنسمّيها <b>الشريحة</b>.</p></div>
</div>''')
A('<div class="credit">صورة الصمام: ويكيميديا كومنز — صمام حديث بنفس مبدأ صمامات الحواسيب الأولى.</div>')
A(f'''<div class="stats3 keep"><div class="sh">وشكل حاسب مبني بالصمامات فعلًا كان كده:</div><div class="sg">
  <div><b>{num("~18,000")}</b><span>صمام مفرَّغ</span></div><div><b>{num("30")}</b><span>طن وزنه</span></div><div><b>{num("~167")}</b><span>متر مربع مساحته</span></div></div></div>''')

A('<h2 class="sec"><span class="num">2</span><span class="dot">·</span> تاريخ تكنولوجيا المعلومات <bdi>(IT)</bdi></h2>')
HIST = [("الأربعينيات–الستينيات", "ظهور الحواسيب الإلكترونية (ومنها <bdi>ENIAC</bdi>) واستخدام الصمامات المفرغة", "استُخدم أساسًا للأغراض العسكرية والحسابات العلمية"),
        ("السبعينيات–الثمانينيات", "انتشار الحواسب الشخصية <bdi>(PCs)</bdi>", "بداية استخدام الأفراد للحاسب"),
        ("التسعينيات", "إتاحة الإنترنت للاستخدام التجاري؛ ظهور الويب", "انتشار الوصول العالمي إلى المعلومات والبريد الإلكتروني"),
        ("العقد الأول من الألفية", "ظهور الهواتف الذكية (آيفون وغيره)", "انتشار سريع وواسع للإنترنت عبر الهواتف المحمولة"),
        ("من العقد الثاني من الألفية فصاعدًا", "انتشار الحوسبة السحابية", "تحليل البيانات الضخمة والذكاء الاصطناعي؛ انتشار تقديم موارد تكنولوجيا المعلومات في صورة خدمات عبر الإنترنت")]
A('<div class="tlrow kwn"><div class="tlh"><span class="qm">”</span><span class="tico">' + ic("bars", "#e29433", 2.6) + '</span><b>المراحل الرئيسية في تطور تكنولوجيا المعلومات</b></div>'
  + '<figure class="tlimg"><img src="assets/u1/it_history.jpg" alt=""><figcaption class="icap">تطورت تقنيات المعلومات عبر مراحل متتابعة، وأصبحت الأجهزة أصغر حجمًا وأكثر ترابطًا.</figcaption></figure></div>')
A('<div class="tl keep"><div class="cols">' + "".join(
    f'<div class="tc"><span class="n">{k + 1}</span><h5>{p}</h5><img src="assets/u1/tl{k + 1}.jpg" alt="">'
    f'<div class="lb">{ic("gear", "#e29433")}التقنيات والأحداث الرئيسية</div><p>{t}</p>'
    f'<div class="lb">{ic("people", "#e29433")}التأثير على المجتمع</div><p>{i}</p></div>' for k, (p, t, i) in enumerate(HIST)) + '</div></div>')
A('<div class="tipbar">' + ic("bulb", "#e29433") + '<b>للفهم:</b> كلما اقتربنا من الحاضر أصبحت الأجهزة أصغر وأسرع وأكثر انتشارًا.</div>')

def stage(n, title, period, body, cls=""):
    return (f'<div class="stg keep {cls}"><h3 class="sh"><span class="sn">{n}</span><span class="st">{title}</span><span class="pd">{period}</span></h3>{body}</div>')
def chips(items):
    return '<div class="ich">' + "".join(f'<div><span>{ic(i, "#22375c")}</span>{t}</div>' for i, t in items) + '</div>'
def chain(items, cls=""):
    return f'<div class="chain {cls}">' + f'<i>{ARR}</i>'.join(f'<div><span>{ic(i, "#22375c")}</span><b>{t}</b></div>' for i, t in items) + '</div>'

# المرحلة 1
A(stage("1", "المرحلة الأولى: الحواسيب الإلكترونية الأولى", "الأربعينيات – الستينيات",
  '<p class="sp">ظهر في هذه المرحلة الحاسب الإلكتروني مثل <bdi>ENIAC</bdi>، واعتمدت الحواسيب على الصمامات المفرغة، وكان استخدامها أساسًا للأغراض العسكرية والحسابات العلمية.</p>'
  + '<div class="pnl"><h5 class="fh">' + ic("bulb", "#e29433") + '<span>للفهم</span> — لماذا لم تكن في البيوت؟</h5>'
  + chips([("expand", "مساحة كبيرة"), ("bolt", "استهلاك طاقة"), ("wrench", "تشغيل وصيانة"), ("coins", "تكلفة عالية")]) + '</div>'
  + '<div class="ph2 eq"><figure><img src="assets/u1/eniac.jpg" alt=""><figcaption><b>ENIAC</b> اختصار لـ <bdi>Electronic Numerical Integrator and Computer</bdi></figcaption></figure>'
  + '<figure><img src="assets/u1/early_computer.jpg" alt=""><figcaption class="icap">كانت الحواسب الأولى تملأ غرفة بأكملها.</figcaption></figure></div>'))
# المرحلة 2 (صفحة جديدة)
A(stage("2", "المرحلة الثانية: الحواسيب الشخصية", "السبعينيات – الثمانينيات",
  '<p class="sp">انتشرت في هذه المرحلة الحواسب الشخصية <bdi>(PCs)</bdi>، وبدأ الأفراد يستخدمون الحاسب بعد أن كان مقصورًا على المؤسسات الكبيرة.</p>' +
  f'<div class="pnl">{FXA}<h5>طب إيه اللي ساعد على ده؟</h5>'
  + chain([("chip", f"المعالج الدقيق {num('1971')}"), ("monitor", "مكوّنات المعالجة على شريحة واحدة"), ("down", "حواسيب أصغر وأرخص"), ("home", "الحاسب الشخصي في البيت")])
  + '<p class="pf">من <b>أهم التطورات</b> اللي مهّدت لانتشار <b>الحواسب الشخصية</b> — الكمبيوتر نزل من المؤسسات ودخل البيوت.</p>'
  + '</div>'
  + f'<div class="ph2 eq big"><figure class="stp"><img src="assets/u1/tl2.jpg" alt=""></figure><figure class="chipf"><img src="assets/u1/intel4004.jpg" alt=""><figcaption>معالج <bdi class="nw">Intel 4004</bdi> — {num("2,300")} ترانزستور جوّه القطعة دي.</figcaption></figure></div>'))
# المرحلة 3
BA = (f'<div class="ba"><div class="br"><span class="bl0">قبل الإنترنت</span>'
      + f'<div class="bi"><span>{ic("file")}</span>ملف على جهاز</div><i>{ARR}</i><div class="bi"><span>{ic("usb")}</span>تنقل وسيط التخزين بنفسك</div><i>{ARR}</i><div class="bi"><span>{ic("monitor")}</span>جهاز تاني</div></div>'
      + f'<div class="br af"><span class="bl0">بعد الإنترنت</span><div class="bi"><span>{ic("monitor")}</span>جهازك</div><i>{ARR}</i><div class="bi"><span>{ic("net")}</span>الشبكة بتنقل البيانات</div><i>{ARR}</i><div class="bi"><span>{ic("monitor")}</span>جهاز بعيد</div></div></div>')
A(stage("3", "المرحلة الثالثة: الإنترنت والويب", "التسعينيات",
  '<p class="sp">أُتيح الإنترنت في هذه المرحلة للاستخدام التجاري وظهر الويب، فانتشر الوصول العالمي إلى المعلومات والبريد الإلكتروني.</p>' +
  f'<div class="pnl">{FXA}<h5>إيه اللي اتغيّر فعليًا؟</h5>{BA}'
  + '<p class="pf">بدل ما إنت تتحرك بالملف، <b>البيانات نفسها</b> بقت تقدر تتحرك عبر الشبكة.</p></div>'))
A(f'<div class="simply">{FXA}<span class="lab">{BULB}ببساطة</span><p><b>متلخبطش: الإنترنت ≠ الويب.</b> <b>الإنترنت</b> هو <b>البنية التحتية</b> اللي بتربط الأجهزة والشبكات ببعضها — الكابلات اللي تحت الأرض وتحت البحر، والأجهزة، والقواعد اللي بتخلّي أي جهازين في الدنيا يبعتوا لبعض بيانات. أما <b>الويب</b> فهو <b>خدمة واحدة</b> من كذا خدمة شغّالة فوقه، بتتكوّن من صفحات ومواقع مترابطة. يعني الإنترنت هو <b>الطريق</b>، والويب <b>عربية ماشية عليه</b> — والإيميل عربية تانية على نفس الطريق. عشان كده الكتاب ذكر الاتنين مع بعض في سطر واحد: دول مش اسمين لحاجة واحدة.</p></div>')
A(f'''<div class="pnl new90 keep">{FXA}<h4>طب إيه الجديد في التسعينيات؟</h4><p class="ps">الشبكات ونقل الملفات كانوا موجودين قبلها — الجديد <b>حاجتين</b>:</p>
  <div class="two9"><div class="t9"><h6><span class="cn">1</span>الإنترنت بقى متاح للاستخدام التجاري</h6>{chain([("net", "الإنترنت"), ("building", "شركات ومؤسسات"), ("people", "استخدام أوسع")], "sm")}</div>
  <div class="t9"><h6><span class="cn">2</span>ظهور الويب</h6>{chain([("net", "الإنترنت"), ("web", "الويب"), ("link", "صفحات وروابط")], "sm")}</div></div>
  <p class="pf">الويب خلّى الوصول للمعلومات <b>أسهل وأكتر انتشارًا</b> بين الناس — بدل ما تحفظ أوامر، بقيت تدوس على كلمة توصّلك للصفحة.</p>
  <div class="lk3"><div class="lk2"><div class="links"><div class="lw"><b>صفحة</b>{win(True)}</div><div class="la"><span>{ic("link", "#e29433")}</span><i>{ARR}</i><small>رابط</small></div><div class="lw"><b>صفحة</b>{win(False, 96)}</div><div class="la"><span>{ic("link", "#e29433")}</span><i>{ARR}</i><small>رابط</small></div><div class="lw"><b>صفحة</b>{win(False, 84)}</div></div>
  <div class="lcap">الويب = صفحات مرتبطة ببعض باستخدام الروابط.</div></div><figure class="stp"><img src="assets/u1/tl3.jpg" alt=""></figure></div></div>''')
def phone_big():
    tiles = [("food", "#e29433"), ("card", "#2e4a78"), ("bus", "#4a6fa5"), ("wifi", "#1f7a8c")]
    pos = [(30, 50), (66, 50), (30, 88), (66, 88)]
    g = "".join(f'<rect x="{x}" y="{y}" width="26" height="26" rx="7" fill="{c}"/>'
                f'<g transform="translate({x + 4} {y + 4}) scale(.75)" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{IC[n]}</g>'
                for (n, c), (x, y) in zip(tiles, pos))
    return ('<svg class="pbig" viewBox="0 0 122 222">'
            '<rect x="16" y="6" width="90" height="210" rx="17" fill="#22375c"/>'
            '<rect x="22" y="22" width="78" height="176" rx="9" fill="#eef4fb"/>'
            '<rect x="47" y="11" width="28" height="5" rx="2.5" fill="#3b5683"/>'
            '<rect x="47" y="205" width="28" height="4" rx="2" fill="#6f86a8"/>'
            '<rect x="30" y="30" width="36" height="5" rx="2.5" fill="#b9c7da"/><circle cx="90" cy="32.5" r="3.5" fill="#e29433"/>'
            + g +
            '<rect x="30" y="126" width="62" height="58" rx="7" fill="#fff" stroke="#dde5ef"/>'
            '<path d="M36 176c10-6 12-20 24-20s14 10 26-4" fill="none" stroke="#4a6fa5" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="4 3"/>'
            '<path d="M84 136a6 6 0 0 1 6 6c0 5-6 11-6 11s-6-6-6-11a6 6 0 0 1 6-6z" fill="#e29433"/><circle cx="84" cy="142" r="2.2" fill="#fff"/>'
            '<circle cx="37" cy="176" r="3" fill="#2e4a78"/>'
            '</svg>')
SVC4 = [("food", "طلب أكل", "تطلب أكل وإنت في الشارع", "r1"),
        ("card", "دفع إلكتروني", "تدفع من موبايلك", "r2"),
        ("bus", "مواصلات وخرائط", "تعرف العربية جاية إمتى", "l1"),
        ("wifi", "اتصال بالإنترنت في أي مكان", "في الأتوبيس وفي الطابور", "l2")]
POCKET = ('<div class="pk">' + FXA + '<div class="pkh"><b>الإنترنت بقى معاك في جيبك</b></div><div class="pkg">'
  + "".join(f'<div class="pkc {c}"><span class="ci">{ic(i, "#22375c")}</span><span class="ct"><b>{t}</b><small>{d}</small></span></div>' for i, t, d, c in SVC4)
  + '<div class="pkp">' + phone_big() + '</div></div></div>')
POCKET2 = ('<div class="pk">' + FXA + '<div class="cmp4"><div class="cb"><span class="cl">قبل الهاتف الذكي</span><p>لازم تكون <b>قدام جهاز ثابت</b>.</p></div>'
  + '<div class="ca">←</div>'
  + '<div class="cb af"><span class="cl">بعد الهاتف الذكي</span><p>الاتصال والخدمات <b>بقوا معاك أثناء الحركة</b>.</p></div></div>'
  + '<div class="save4"><span class="sl">احفظها</span><div class="sc"><span><bdi>Smartphone</bdi></span><i>←</i><span>إنترنت محمول واسع الانتشار</span><i>←</i><span>خدمات رقمية أسهل وأكثر عملية</span></div></div>'
  + '</div>')
# المرحلة 4 (صفحة جديدة)
A(stage("4", "المرحلة الرابعة: الهواتف الذكية", "العقد الأول من الألفية",
  '<p class="sp">ظهرت في هذه المرحلة الهواتف الذكية (آيفون وغيره)، فانتشر الإنترنت بسرعة وعلى نطاق واسع عبر الهواتف المحمولة.</p>' +
  f'<div class="pnl">{FXA}<h5>طب إيه اللي اتغيّر لما الاتصال بقى معاك طول الوقت؟</h5>'
  + f'<div class="dp"><div class="bi"><span>{ic("monitor")}</span>جهاز على المكتب — تستنّى ترجع البيت</div><i>{ARR}</i><div class="bi on"><span>{ic("phone")}</span>جهاز في جيبك — معاك في الأتوبيس وفي الطابور</div></div>'
  + '<div class="pr4"><p class="pf"><b>انتشرت خدمات جديدة بقوة</b>، و<b>بقت خدمات موجودة أصلًا أسهل وأكتر عملية</b>.</p>'
  + '</div></div>'))
A('<div class="stg keep cont">' + POCKET + '</div>')
A('<div class="stg keep cont">' + POCKET2 + '</div>')
A(f'<div class="bridge">{FX}وصلنا لسنة {num("2010")} تقريبًا — والمرحلة اللي جاية عن <b>السحابة</b>، وبعدها هنتكلم عن <b>الحدود اللي بدأت تقف قدّام التصغير</b>.</div>')
# المرحلة 5 (صفحة جديدة)
A(stage("5", "المرحلة الخامسة: الحوسبة السحابية", "من العقد الثاني من الألفية فصاعدًا",
  '<p class="sp">انتشرت في هذه المرحلة الحوسبة السحابية، وأصبحت موارد تكنولوجيا المعلومات تُقدَّم في صورة خدمات عبر الإنترنت، مع انتشار تحليل البيانات الضخمة والذكاء الاصطناعي.</p>' +
  f'<div class="pnl">{FXA}<h5>تمتلك وتشغّل… ولا تستخدم كخدمة؟</h5>'
  + f'<div class="own"><div><span class="bl0">قبل</span><span class="oi">{ic("server")}</span><p>المؤسسة <b>تمتلك وتشغّل</b> كل موارد الحوسبة والتخزين بنفسها.</p></div>'
  + f'<div class="af"><span class="bl0">بعد</span><span class="oi">{ic("gauge")}</span><p>تستخدم موارد <b>مقدَّمة لها كخدمة عبر الإنترنت</b>، وتزوّدها أو تقلّلها حسب احتياجها — زي عدّاد الكهربا.</p></div></div>'
  + chain([("db", "كميات بيانات ضخمة"), ("cloud", "قدرة حوسبة كخدمة"), ("chip", "انتشار تطبيقات الذكاء الاصطناعي")])
  + '<p class="pf"><b>توافر كميات ضخمة من البيانات مع قدرة حوسبة كبيرة</b> كان من العوامل المهمة اللي ساعدت على انتشار تطبيقات الذكاء الاصطناعي — علمًا إن <b>بعض</b> التطبيقات هي اللي بتحتاج الموارد دي، مش كلها.</p></div>'
  + f'<div class="ph2 c5 big"><figure class="cdw">{CLOUD_DEV}<figcaption>{FX}أجهزتك بتتوصّل بقدرة مركز بيانات.</figcaption></figure>'
  + '<figure><img src="assets/u1/cloud_datacenter.jpg" alt=""><figcaption class="icap">هذه هي "السحابة" – أجهزة حقيقية في مكان حقيقي.</figcaption></figure>'
  + '<figure class="stp"><img src="assets/u1/tl5.jpg" alt=""></figure></div>'))
STRIP = [("server", "أوضة"), ("monitor", "مكتب"), ("phone", "جيبك"), ("cloud", "السحابة")]
A(f'<div class="strip keep">{FXA}<div class="sr">' + f'<i>{ARR}</i>'.join(f'<div class="{"g" if k == 3 else ""}"><span>{ic(i, "#e29433" if k == 3 else "#22375c", 1.6)}</span><b>{t}</b></div>' for k, (i, t) in enumerate(STRIP))
  + '</div><div class="sc">في كل مرحلة الجهاز بيصغر ويقرّب منك أكتر.</div></div>')

# ---- قانون مور (صفحة جديدة دايمًا)
A('<h2 class="sec"><span class="num">3</span><span class="dot">·</span> قانون مور</h2>')
A(f'<span class="chip">قانون مور {nw("(Moore’s Law)")}</span>')
A('<div class="banner kwn">يصف <b>اتجاهًا تاريخيًا</b> لازدياد عدد الترانزستورات في الدوائر المتكاملة بمعدل يقارب <b>الضعف كل عامين</b>، وهو <b>ليس قانونًا فيزيائيًا ثابتًا</b>.</div>')
A(f'<div class="mw keep">{FXA}<h5><span class="cn">؟</span>لماذا كان مهمًا؟</h5>'
  + chain([("chip", "زيادة عدد الترانزستورات"), ("gauge", "زيادة قدرات الحوسبة"), ("up", "تحسين أداء المعالجات")]) + '</div>')
A('<div class="quote"><span class="qmark">”</span>استمر هذا الاتجاه <b>عقودًا</b>، وأسهم في <b>زيادة قدرات الحوسبة وتحسين أداء المعالجات</b>.<br>لكن استمرار تصغير مكوّنات الدوائر يواجه <b>تحديات هندسية وفيزيائية</b>، منها <b>ازدياد تيارات التسرب</b> وتأثيرات كمومية مثل <b>النفق الكمومي</b>. لذلك يعتمد تحسين الأداء أيضًا على <b>تعدد الأنوية والمعالجة المتوازية وتصميمات متخصصة</b>.</div>')
A(f'''<div class="chal keep">{FXA}
  <div class="ch2"><h5>لكن ظهرت تحديات</h5>
    <div class="cc2"><span class="ci">{ic("leak", "#a9670f")}</span><div><b>تيارات التسرّب</b><p>عند تصغير المكوّنات جدًا قد يتسرّب جزء من التيار حتى عند عدم الرغبة في مروره.</p></div></div>
    <div class="cc2"><span class="ci">{ic("tunnel", "#a9670f")}</span><div><b>النفق الكمومي</b><p>عندما تصبح المكوّنات شديدة الصغر قد تظهر تأثيرات كمّية تسمح باحتمال عبور الإلكترون للحاجز.</p></div></div></div>
  <div class="ch2 now"><h5>إذن كيف يتحسّن الأداء اليوم؟</h5>
    <div class="cc3"><div><span>{ic("grid")}</span>تعدّد الأنوية</div><div><span>{ic("lanes")}</span>المعالجة المتوازية</div><div><span>{ic("target")}</span>تصميمات متخصّصة</div></div>
    <p>لذلك لا يعتمد تحسين الأداء اليوم على التصغير وحده، بل أيضًا على هذه الأساليب.</p></div>
</div>''')
A('<div class="warn kwn"><span class="ex">!</span><div><b>مهم:</b> أما <b>الحوسبة الكمومية</b> فهي نهج مختلف قد يفيد في <b>فئات محددة</b> من المسائل، <b>وليست بديلًا عامًا</b> لكل الحواسيب التقليدية.</div></div>')
A(f'<div class="fig mfig keep">{moore_svg()}<div class="cap">قانون مور: عدد الترانزستورات عبر الزمن<span class="mnote">المحور الرأسي لوغاريتمي — كل خطوة = عشرة أضعاف اللي قبلها.</span></div></div>')
A(f'<div class="bridge">{FX}لحد هنا اتكلمنا عن <b>الأجهزة</b>. الجزء اللي جاي عن <b>الناس</b>: التغيّرات دي عملت إيه في حياتنا فعلًا؟</div>')

# ---- الجزء الثاني
A('<div class="part p2"><span>الجزء الثاني</span></div>\n<hr class="rule">')
A('<h2 class="sec"><span class="num">4</span><span class="dot">·</span> التغيرات الاجتماعية الناتجة عن تكنولوجيا المعلومات</h2>')
SOC_LBL = ["مواقع التواصل الاجتماعي · المشاركة الاجتماعية", "التسوق عبر الإنترنت", "العمل من المنزل", "الدراسة في أي مكان", "الدفع بدون نقد · الدفع بلمسة واحدة"]   # عناوين صورة الكتاب
SOC = [("chat", "شبكات التواصل الاجتماعي", "SNS", "منصات تتيح للمستخدمين التواصل ونشر المحتوى ومشاركته <b>بسرعة</b>.", ""),
       ("cart", "التجارة الإلكترونية", "E-commerce", "بيع <b>السلع والخدمات</b> وشراؤها عبر الإنترنت.", "مثال: متاجر إلكترونية مثل أمازون وإيباي."),
       ("remote", "العمل عن بُعد", "Remote Work", "نمط عمل يؤدي فيه الشخص مهامه <b>من المنزل أو من موقع آخر بعيد</b> باستخدام الإنترنت.", ""),
       ("grad", "التعلّم عبر الإنترنت", "Online Learning", "نمط تعليمي تُقدَّم فيه <b>الدروس والمواد التعليمية</b> عبر الإنترنت.", ""),
       ("pay", "الدفع غير النقدي", "Cashless Payment", "دفع قيمة السلع أو الخدمات <b>بوسائل غير نقدية</b>، مثل البطاقات المصرفية أو تطبيقات الهاتف أو رموز <bdi>QR</bdi>.", "")]
def soc_row(k, i, t, e, d, x):
    return (f'<div class="sc"><span class="si">{ic(i, "#22375c", 1.7)}</span><div class="st"><h4><span class="cn">{k + 1}</span>{t}<small>{nw(e)}</small><em class="fl">{SOC_LBL[k]}</em></h4><p>{d}</p>{f"<p class=ex>{x}</p>" if x else ""}</div></div>')
A('<div class="fig soc split">' + "".join(soc_row(k, *SOC[k]) for k in range(4))
  + '<div class="sl">' + soc_row(4, *SOC[4]) + '<div class="cap">خمسة تحولات مجتمعية أحدثتها تكنولوجيا المعلومات.</div></div></div>')
A(recall(["تواصل", "تجارة", "عمل عن بُعد", "تعلّم", "دفع"]))

# ---- الجزء الثالث
A('<div class="part p3"><span>الجزء الثالث</span></div>\n<hr class="rule">')
A('<h2 class="sec"><span class="num">5</span><span class="dot">·</span> تقنيات ناشئة بارزة</h2>')
EMG = [("wheel", "القيادة الذاتية", "", "تقنية تستخدم <b>الذكاء الاصطناعي للمساعدة</b> على قيادة المركبة."),
       ("ar", "الواقع المعزز", "AR – Augmented Reality", "تقنية <b>تضيف</b> عناصر أو معلومات رقمية <b>إلى مشهد من العالم الحقيقي</b>."),
       ("vr", "الواقع الافتراضي", "VR – Virtual Reality", "تقنية <b>تضع المستخدم داخل</b> بيئة افتراضية مولَّدة حاسوبيًا."),
       ("atom", "الحوسبة الكمومية", "Quantum Computing", "نهج حوسبي يستخدم خصائص ميكانيكا الكم لمعالجة المعلومات، وقد يوفر تفوقًا في <b>فئات محددة</b> من المسائل، لكنه <b>لا يسرّع جميع أنواع الحسابات</b>.")]
A('<div class="emgw keep"><div class="eh"><span>أبرز التقنيات الناشئة</span></div><div class="ebr"><i class="s"></i><i class="h"></i>'
  + "".join(f'<i class="d d{k}"></i><i class="a a{k}"></i>' for k in range(4)) + '</div>'
  + '<div class="emg">' + "".join(
    f'<div class="ec e{k}"><span class="ei">{ic(i, "#22375c", 1.7)}</span><h4>{t}</h4>{f"<small>{nw(e)}</small>" if e else ""}<p>{d}</p></div>'
    for k, (i, t, e, d) in enumerate(EMG)) + '</div></div>')

A('<h3 class="sub">القيادة الذاتية — والحوسبة الطرفية</h3>')
A(f'<div class="fig sdf keep">{selfdrive_svg()}<div class="cap">تتخذ السيارة ذاتية القيادة قرارها على متنها (الحوسبة الطرفية)، دون انتظار السحابة.</div></div>')
A(f'<p class="lead kwn">{FX}الكتاب بيرتّب الفكرة هنا في خطوات مترابطة، فامشي عليها بالترتيب وهتلاقي الحتة أوضح.</p>')
def stp(n, t, body, link=""):
    lk_ = f'<div class="lnk">{link}</div>' if link else ""
    return f'<div class="s"><span class="n">{n}</span><h4>{t}</h4>{body}{lk_}</div>'
def simp(t): return f'<p class="sp">{FX}<b class="sl">ببساطة</b> {t}</p>'
A('<div class="steps sd split">'
  + stp("1", "إيه هي القيادة الذاتية؟", '<p>تقنية تستخدم <b>الذكاء الاصطناعي للمساعدة على</b> قيادة المركبة، ويتفاوت مقدار التدخل البشري <b>بحسب مستوى الأتمتة</b>.</p>'
        + simp('خلّي بالك من كلمتين: الكتاب قال <b>«للمساعدة على»</b> مش «تقود بدل السائق»، وقال إن التدخّل البشري <b>بيتفاوت</b> مش ثابت. الاتنين دول بيتحوّلوا لأسئلة صح وخطأ.'),
        "طيب وبتقود إزاي؟ إيه اللي بيخلّيها «تشوف» الطريق؟")
  + stp("2", "بتشتغل إزاي؟", '<p>تستخدم المركبة <b>كاميرات ومستشعرات</b> لإدراك محيطها، ثم <b>يعالج النظام البيانات</b> لاتخاذ <b>قرارات القيادة والتحكم فيها</b>.</p>'
        + simp('المستشعر جهاز صغيّر بيقيس حاجة في الواقع — مسافة، سرعة، حرارة — ويحوّلها لـ<b>أرقام</b>. فالعربية مش «شايفة» بمعنى إنها بتتفرّج؛ هي بتستقبل أرقام كل جزء من الثانية والنظام بيقرأها وياخد قرار: تفرمل · تلفّ · تكمّل.'),
        "تمام. طب المعالجة دي بتحصل فين بالظبط؟ وليه ده يفرق أصلًا؟")
  + stp("3", "فين المشكلة؟", '<p>ولأن <b>التأخير في معالجة بيانات القيادة قد يؤثر في السلامة</b>، <b>تُعالج بعض البيانات محليًا بالحوسبة الطرفية</b> لتقليل زمن الاستجابة.</p>',
        "طب يعني إيه «حوسبة طرفية»؟")
  + stp("4", "يعني إيه الحوسبة الطرفية؟", '<p><b>الحوسبة الطرفية</b> – معالجة البيانات <b>على الجهاز نفسه، فورًا</b>، بدلًا من إرسالها إلى السحابة.</p>'
        + simp('كلمة <b>«الطرف»</b> هنا معناها <b>طرف الشبكة</b> — يعني عندك إنت، في العربية نفسها، مش في مركز بيانات بعيد.'),
        "طب خلّينا نحس بالأرقام: ليه التأخير ممكن يفرق فعلًا؟")
  + stp("5", "ليه لازم حوسبة طرفية في القيادة الذاتية بالذات؟", f'<p class="sp">{FX}<b>مثال افتراضي للتوضيح:</b> لو افترضنا إن الرد من السحابة اتأخّر <b>نص ثانية</b> والعربية ماشية {num("100")} كم/ساعة، تبقى مشيت حوالي <b>{num("14")} متر</b> قبل ما القرار يوصلها — وده ممكن يكون الفرق بين إنها تقف وإنها تخبط. الرسمة اللي تحت بتلخّص خطوات الاستشعار والمعالجة واتخاذ القرار.</p>')
  + '</div>')

EDGE = f'''<div class="fig edge keep">{FXA}
  <div class="e3">
    <div class="es"><h6><span class="cn">1</span>استشعار البيئة</h6><div class="eic">{ic("camera")}{ic("sensor")}{ic("car")}</div><p>كاميرات ومستشعرات تجمع بيانات عن الطريق والمحيط.</p></div>
    <i class="ea">{ARR}</i>
    <div class="es"><h6><span class="cn">2</span>معالجة محلية</h6><div class="eic">{ic_ai()}</div><p>تُعالَج البيانات على متن المركبة.</p></div>
    <i class="ea">{ARR}</i>
    <div class="es"><h6><span class="cn">3</span>اتخاذ القرار</h6><div class="eic dec"><span>{ic("up")}<small>استمرار</small></span><span>{ic("turn")}<small>انعطاف</small></span><span>{ic("stop")}<small>فرملة</small></span></div><p>القرار بيتنفّذ فورًا.</p></div>
  </div>
  <div class="evs">
    <div class="ep ok"><div class="eh"><span class="et">الحوسبة الطرفية</span><span class="em">{ic("check", "#fff", 2.4)}</span></div>
      <div class="ech"><span>{ic("car")}<small>السيارة</small></span><i>{ARR}</i><span>{ic_ai()}<small>معالجة محلية</small></span><i>{ARR}</i><span>{ic("bolt")}<small>قرار فوري</small></span><i>{ARR}</i><span>{ic("up")}<small>تنفيذ</small></span></div>
      <p>معالجة البيانات قريبًا من مصدرها وعلى المركبة نفسها، مما يقلل زمن الاستجابة.</p></div>
    <div class="ep bad"><div class="eh"><span class="et">الاعتماد على السحابة وحدها</span><span class="em">!</span></div>
      <div class="ech"><span>{ic("car")}<small>السيارة</small></span><i>{ARR}</i><span>{ic("wifi")}<small>الإنترنت</small></span><i>{ARR}</i><span>{ic("cloud")}<small>خادم بعيد</small></span><i>{ARR}</i><span>{ic("clock", "#a9670f")}<small>القرار</small></span></div>
      <p>إرسال البيانات إلى السحابة واستقبال الرد قد يضيف تأخيرًا، لذلك لا تعتمد المركبة على السحابة وحدها في القرارات الحرجة.</p></div>
    <div class="ex14"><b>مثال افتراضي</b><div><bdi class="nw">{num("100")}</bdi> كم/س ≈ {num("28")} مترًا في الثانية</div><div>× زمن رد {num("0.5")} ث</div><div class="r">≈ <b>{num("14")} مترًا</b> تقطعها السيارة قبل عودة الرد</div></div>
  </div>
  <div class="mnote">الأرقام على الشمال مثال افتراضي للتوضيح فقط: افترضنا زمن استجابة {num("0.5")} ثانية، وده مش زمن ثابت للسحابة.</div>
  <div class="cap">من الاستشعار للقرار — وليه القرار بيتاخد على متن العربية.</div>
</div>'''
A(EDGE)

A('<h3 class="sub">الواقع المعزز والواقع الافتراضي</h3>')
A(f'''<div class="fig arvr keep"><div class="av2">
  <div class="avp"><div class="avh"><b>AR</b>الواقع المعزز</div>{AR_SVG}<p class="avd">تقنية <b>تضيف</b> عناصر أو معلومات رقمية <b>إلى مشهد من العالم الحقيقي</b>.</p></div>
  <div class="avp v"><div class="avh"><b>VR</b>الواقع الافتراضي</div>{VR_SVG}<p class="avd">تقنية <b>تضع المستخدم داخل</b> بيئة افتراضية مولَّدة حاسوبيًا.</p></div></div>
  <div class="cap">يضيف الواقع المعزز عناصر رقمية إلى العالم الحقيقي، بينما يضع الواقع الافتراضي المستخدم داخل بيئة رقمية كاملة.</div></div>''')
A(f'<div class="avq keep">{FXA}<div class="aq">السؤال اللي بيفرّق بينهم: <b>العالم الحقيقي لسه قدّامك؟</b></div><div class="aa">'
  + '<div><b>AR</b>أيوه — والتقنية <b>بتضيف</b> عليه عناصر أو معلومات رقمية.</div>'
  + '<div class="v"><b>VR</b>لأ — إنت <b>جوّه</b> بيئة افتراضية مولَّدة حاسوبيًا.</div></div></div>')
A(recall(["حوسبة طرفية ← على الجهاز", "AR ← يضيف", "VR ← يدخّلك جوّه"]))
ANAL = [("ar", "الواقع المعزّز", "AR", "زي <b>طبقة شفّافة</b> اتحطّت فوق الشارع — الشارع زي ما هو، والتكنولوجيا بترسم عليه."),
        ("vr", "الواقع الافتراضي", "VR", "زي <b>باب بينقلك أوضة تانية</b> — الشارع اتشال من قدّامك، وإنت جوّه عالم مبني بالحاسب."),
        ("atom", "الحوسبة الكمومية", "Quantum Computing", "زي <b>عملة بتلفّ</b> — مش مستقرّة على وش وهي بتحسب.")]

A(f'<h3 class="sub">الحوسبة الكمومية — الفرق بين البت والكيوبت {nw("(Qubit)")}</h3>')
A(f'''<div class="fig qbf keep"><div class="qdef"><b>الحوسبة الكمومية {nw("(Quantum Computing)")}:</b> نهج حوسبي يستخدم خصائص ميكانيكا الكم لمعالجة المعلومات، وقد يوفر تفوقًا في <b>فئات محددة</b> من المسائل، لكنه <b>لا يسرّع جميع أنواع الحسابات</b>.</div><div class="qb2">
  <div class="qp"><div class="qh">البت الكلاسيكي</div>{BIT_SVG}<b>حالة محددة واحدة في كل وقت</b><small>إما {num("0")} أو {num("1")} — وليس كلاهما أبدًا</small>
    <p class="qx">{FX}تخيّل <b>عملة معدنية واقعة على الطاولة</b>: يا صورة ({num("1")}) يا كتابة ({num("0")}) — ومستحيل الاتنين مع بعض.</p></div>
  <div class="qp k"><div class="qh">الكيوبت <bdi>(qubit)</bdi></div><div class="qs">التراكب الكمي</div>{QUBIT_SVG}<b>مزيج من {num("0")} و{num("1")} في نفس الوقت</b>
    <p class="qx">{FX}الكيوبت ممكن يبقى في <b>حالة تراكب</b> مرتبطة بـ{num("0")} و{num("1")} مع بعض. وأول ما <b>نقيسه</b> بتطلع نتيجة <b>واحدة بس</b>: {num("0")} أو {num("1")}، باحتمالات بتحدّدها حالته. ودي <b>حالة كمومية فعلية</b> — مش مجرد إننا مش عارفين النتيجة المخبّأة. ده اللي بيسمّوه <b>التراكب الكمومي</b>.</p></div></div>
  <div class="qn"><span class="ex">!</span><p>بفضل خاصية التراكب الكمي <bdi class="nw">(Superposition)</bdi>، يمكن للكيوبتات أن تمثّل عددًا هائلًا من الحالات في نفس الوقت، وهو ما يسمح بإجراء معالجة متوازية ضخمة لحل مسائل معينة بسرعة أكبر.</p></div>
  <div class="cap">يحمل البت التقليدي حالة واحدة، أما الكيوبت <bdi>(qubit)</bdi> فيستخدم مبدأ التراكب الكمومي.</div></div>''')
A(f'<div class="simply">{FXA}<span class="lab">{BULB}ببساطة</span><p><b>طب التراكب ده بيفيد في إيه؟</b> في <b>خوارزميات كمومية معيّنة</b> بتستغلّ خصائص زي التراكب والتداخل عشان تحلّ <b>فئات محدّدة</b> من المسائل — زي البحث جوّه احتمالات هائلة أو محاكاة الجزيئات. <b>بس خلّي بالك:</b> التراكب <b>مش</b> معناه إننا نقدر نقرا كل الإجابات الممكنة مرة واحدة. في جمع فاتورة أو تشغيل فيديو <b>مش هتفرق معاك في حاجة</b>.<br><b>خلّي بالك في الامتحان:</b> «الحوسبة الكمومية تسرّع <b>جميع</b> أنواع الحسابات» عبارة <b>خاطئة</b>.</p></div>')

A(f'<div class="anl3 keep">{FXA}' + "".join(f'<div><span class="ai">{ic(i, "#22375c", 1.7)}</span><h5>{t} <small>{nw(e)}</small></h5><span class="tg">تشبيه للفهم</span><p>{d}</p></div>' for i, t, e, d in ANAL) + '</div>')
A(recall(["بت ← 0 أو 1", "كيوبت ← تراكب", "فئات محددة بس"]))
A('<div class="kidea keep"><div class="kh">الفكرة الرئيسة</div><p>في كل مرحلة أضافت تكنولوجيا المعلومات <b>جهازًا جديدًا</b>، وغيّرت معه <b>طريقة تواصل المجتمع وعمله وتجارته</b>.</p></div>')
A('<div class="big">سؤال على نمط الامتحان — ونموذج إجابته</div>\n<hr class="rule">')
A(f'''<div class="exam keep">
  <div class="hd"><span class="n">1</span><span class="t">سؤال على نمط الامتحان</span><span class="m">[{num("6")} درجات]</span></div>
  <div class="qt">حلّل كيف غيّر انتشار الحوسبة السحابية (من العقد الثاني من الألفية فصاعدًا) طريقة استخدام تكنولوجيا المعلومات.</div>
  <div class="hint"><b>في إجابتك، أشِر إلى:</b> تحليل البيانات الضخمة، والذكاء الاصطناعي، و"تكنولوجيا المعلومات كخدمة".</div>
</div>''')
A('<h3 class="sub">سؤال على نمط الامتحان — إجابة نموذجية</h3>')
A(f'''<div class="box white split">
  <h3>نموذج إجابة مقترح لسؤال الـ{num("6")} درجات{FX}</h3>
  <ol style="counter-reset:n 0"><li><b>نقطة التحوّل:</b> قبل السحابة كانت المؤسسة لازم <b>تمتلك أجهزتها وتشغّلها بنفسها</b>؛ ومع انتشار الحوسبة السحابية بقت موارد تكنولوجيا المعلومات <b>تُقدَّم في صورة خدمات عبر الإنترنت</b> — وده معنى «تكنولوجيا المعلومات كخدمة».</li></ol>
  <ol style="counter-reset:n 1"><li><b>الأثر على البيانات:</b> إتاحة قدرة تخزين ومعالجة كبيرة خلّت <b>تحليل البيانات الضخمة</b> ممكنًا عمليًا لجهات ما كانتش تقدر عليه قبل كده.</li></ol>
  <ol style="counter-reset:n 2"><li><b>الأثر على الذكاء الاصطناعي:</b> <b>بعض</b> تطبيقاته بتحتاج بيانات كتيرة وحوسبة كبيرة؛ والسحابة سهّلت إتاحة الموارد دي، فانتشرت التطبيقات دي معاها.</li></ol>
  <ol style="counter-reset:n 3"><li><b>النتيجة المجتمعية:</b> خدمات رقمية كتير بقت جزء من الحياة اليومية — و<b>ظهرت في المقابل تحديات جديدة</b> تتعلق بالأمان والإنصاف وإتاحة الوصول.</li></ol>
  <div class="tip"><span class="l">ركّز:</span> السؤال طلب منك الإشارة صراحةً لتلات عناصر — <b>تحليل البيانات الضخمة · الذكاء الاصطناعي · تكنولوجيا المعلومات كخدمة</b>. اتأكد إن التلاتة ظاهرين بوضوح في إجابتك.</div>
</div>''')
A('<h2 class="sec"><span class="num"></span>إجابة السؤال الرئيسي</h2>')
A('''<div class="mq kwn">
  <div class="lab">السؤال</div>
  <div class="qq">كيف تطورت تكنولوجيا المعلومات عبر مراحلها الرئيسية، وكيف غيّرت كل مرحلة المجتمع؟</div>
</div>''')
A('<div class="quote"><span class="qmark">”</span>تناول السؤال الرئيسي تطور تكنولوجيا المعلومات وأثر كل مرحلة في المجتمع. مرت تكنولوجيا المعلومات <b>بسلسلة من المراحل المتتابعة</b>، ولم يقتصر أثرها على أجهزة أسرع أو أصغر؛ بل امتد إلى <b>طرق الوصول إلى المعلومات والتواصل والعمل والتعلّم والدفع</b>. ومع انتشار الإنترنت والهواتف الذكية والحوسبة السحابية، أصبحت خدمات رقمية كثيرة جزءًا من الحياة اليومية، وظهرت <b>تحديات جديدة تتعلق بالأمان والإنصاف وإتاحة الوصول</b>. لذلك يرتبط تطور التقنية دائمًا <b>بتغيرات اجتماعية واقتصادية</b> تحتاج إلى فهم وتقييم.</div>')
A(f'<div class="note-line"><span class="tag">للفهم</span><span class="lead">طب ليه؟</span><b>لو السؤال ده جالك في الامتحان</b> ما تحكيش المراحل وخلاص. الإجابة القوية تعمل {num("3")} حاجات: <b>(1)</b> ترتّب المراحل صح · <b>(2)</b> تقول كل مرحلة غيّرت <b>إيه في سلوك الناس</b> (تواصل · شغل · تعلّم · دفع) مش بس إيه الجهاز اللي ظهر · <b>(3)</b> تقفل بإن التطوّر جاب معاه <b>تحديات</b> في الأمان والإنصاف وإتاحة الوصول.</div>')
A('''<div class="terms keep">
  <div class="th"><h3>مصطلحات أساسية</h3></div>
  <div class="t2">
    <div><b>قانون مور</b> – الملاحظة القائلة إن عدد الترانزستورات في الشريحة يتضاعف تقريبًا كل عامين.</div>
    <div><b>الحوسبة الطرفية</b> – معالجة البيانات على الجهاز نفسه، فورًا، بدلًا من إرسالها إلى السحابة.</div>
    <div><b>الحوسبة السحابية</b> – تكنولوجيا المعلومات المقدَّمة كخدمة عبر الإنترنت.</div>
    <div><b>التجارة الإلكترونية</b> – البيع والشراء عبر الإنترنت.</div>
    <div><b>العمل عن بُعد</b> – العمل من المنزل أو من موقع بعيد آخر عبر الإنترنت.</div>
    <div><b>التعلم عبر الإنترنت</b> – تقديم الدروس والمواد عبر الإنترنت.</div>
    <div><b>شبكات التواصل الاجتماعي</b> – تربط المستخدمين لنشر المعلومات ومشاركتها.</div>
    <div><b>الدفع غير النقدي</b> – الدفع دون استخدام النقد (نقود إلكترونية، رموز <bdi>QR</bdi>).</div>
  </div>
</div>''')
A('''<div class="box cream keep">
  <h3>خلي بالك من العبارات دي</h3>
  <ul>
    <li>قانون مور <b>«اتجاه تاريخي»</b> – <b>«ليس قانونًا فيزيائيًا ثابتًا»</b>.</li>
    <li>الحوسبة الكمومية قد توفر تفوقًا في <b>«فئات محددة»</b> من المسائل – <b>«لا يسرّع جميع أنواع الحسابات»</b>، و<b>«ليست بديلًا عامًا»</b> للحواسيب التقليدية.</li>
    <li>القيادة الذاتية تستخدم الذكاء الاصطناعي <b>«للمساعدة على»</b> قيادة المركبة – والتدخل البشري <b>«يتفاوت بحسب مستوى الأتمتة»</b>.</li>
    <li><b>«تُعالج بعض البيانات محليًا»</b> بالحوسبة الطرفية – «بعض» مش «كل».</li>
    <li><b>الإنترنت ≠ الويب</b> – الكتاب ذكرهم مع بعض، بس الويب خدمة شغّالة فوق الإنترنت.</li>
    <li>الحوسبة السحابية: موارد تكنولوجيا المعلومات <b>«تُقدَّم في صورة خدمات عبر الإنترنت»</b>.</li>
  </ul>
</div>''')
A(f'''<div class="dark keep">
  <h3>الخلاصة في دقيقة</h3>
  <p class="rem"><b>تذكّر:</b> تطورت تكنولوجيا المعلومات عبر مراحل – الحواسب، والإنترنت، والهواتف الذكية، والحوسبة السحابية. وفي كل مرحلة أضافت جهازًا جديدًا، وغيّرت معه طريقة تواصل المجتمع وعمله وتعلمه وسداده لمدفوعاته.</p>
  <div class="g2">
    <ul>
      <li><b>خمس مراحل:</b> حاسب {ARR} حاسب شخصي {ARR} إنترنت وويب {ARR} هاتف ذكي {ARR} سحابة. الأجهزة بتصغر وتترابط أكتر.</li>
      <li><b>خمسة تغيّرات اجتماعية:</b> تواصل · تجارة إلكترونية · عمل عن بُعد · تعلّم أونلاين · دفع غير نقدي.</li>
      <li><b>الخلاصة:</b> تأثير كل مرحلة ما كانش مقتصر على ظهور جهاز جديد؛ امتدّ كمان لطريقة التواصل والعمل والتعلّم والدفع، وجاب معاه تحديات في الأمان والإنصاف وإتاحة الوصول.</li>
    </ul>
    <ul>
      <li><b>قانون مور:</b> عدد الترانزستورات في الدوائر المتكاملة يتضاعف تقريبًا كل عامين — <b>اتجاه تاريخي</b> مش قانون فيزيائي ثابت، وبيواجه تحديات (تسرّب + نفق كمومي).</li>
      <li><b>أربع تقنيات ناشئة:</b> قيادة ذاتية (بالحوسبة الطرفية) · <bdi>AR</bdi> · <bdi>VR</bdi> · حوسبة كمومية (<b>قد</b> تفيد في فئات محددة من المسائل).</li>
    </ul>
  </div>
</div>''')
A('''<div class="check keep kwn">
  <h3>اتأكد إنك قادر على</h3>
  <div class="g2">
    <ul>
      <li><span>أقدر أرتّب <b>المراحل الخمس</b> بالترتيب الزمني الصحيح.</span></li>
      <li><span>أقدر أذكر <b>التحدّيين</b> اللي بيواجهوا استمرار التصغير.</span></li>
      <li><span>أفرّق بين <b>الواقع المعزّز والافتراضي</b> في جملة واحدة.</span></li>
    </ul>
    <ul>
      <li><span>أعرف تعريف <b>قانون مور</b> بنصّه، وليه هو ملاحظة مش قانون فيزيائي.</span></li>
      <li><span>أعرف <b>الخمس تغيّرات الاجتماعية</b> وأصنّف أي مثال تحت واحد منهم.</span></li>
      <li><span>أعرف ليه القيادة الذاتية محتاجة <b>حوسبة طرفية</b>، وأشرحها في جملتين.</span></li>
    </ul>
  </div>
</div>''')
A('<div class="endline">أكواد مع زياد — أ/ زياد السعدني · مذكرة البرمجة والذكاء الاصطناعي — تانية ثانوي <span class="num">2026/2027</span> · الفصل الأول — الدرس <span class="num">1-1</span></div>')
A('<div class="pb"></div>')
A('''<div class="band" style="height:55pt;padding-right:12pt">
  <div class="badge"><span class="n">1-1</span></div>
  <h1 style="text-align:right;margin-right:12pt;font-size:14pt">لخّص الدرس بأسلوبك</h1>
</div>''')
A('<div class="instr"><span class="fx fl">للفهم</span>اقفل المذكرة وحاول تلخّص الدرس من غير ما تبصّ: اكتب أهم <b>المصطلحات</b>، و<b>الفكرة الأساسية</b>، و<b>النقطة اللي لسه محتاجة مراجعة</b>. بعد كده افتح المذكرة وقارن اللي كتبته.</div>')
A('<div class="lines">' + '<div></div>' * 24 + '</div>')


# ============================ بنك الأسئلة ============================
B = []
A = B.append
A('<div class="pb"></div>')
A(f'''<div class="band">
  <div class="badge"><span class="l">الدرس</span><span class="n">1-1</span></div>
  <h1>{TITLE}</h1>
  <div class="who"><div class="t"><span class="u">الفصل الأول</span><span class="k">بنك الأسئلة</span></div><img src="assets/avatar.png" alt=""></div>
</div>''')

# ---- أسئلة الكتاب (بنصها)
BOOK = []
BOOK.append(card("01", "المثال المحلول — الجزء الأول",
       instr("من بين الخيارات التالية (أ - د)، اختر الخيار الذي يُرتِّب مراحل تطور تكنولوجيا المعلومات <bdi>(IT)</bdi> بالترتيب الزمني الصحيح.")
       + opts([f"بداية ظهور الحاسب {ARR} ظهور الهواتف الذكية {ARR} تسويق الإنترنت تجاريًا {ARR} انتشار الحوسبة السحابية",
               f"بداية ظهور الحاسب {ARR} تسويق الإنترنت تجاريًا {ARR} ظهور الهواتف الذكية {ARR} انتشار الحوسبة السحابية",
               f"تسويق الإنترنت تجاريًا {ARR} بداية ظهور الحاسب {ARR} انتشار الحوسبة السحابية {ARR} ظهور الهواتف الذكية",
               f"ظهور الهواتف الذكية {ARR} تسويق الإنترنت تجاريًا {ARR} ظهور الحاسب {ARR} انتشار الحوسبة السحابية"], 1)))
BOOK.append(card("02", "المثال المحلول — الجزء الثاني",
       instr("ضع أمام كل عبارة (أ - د) علامة ○ إذا كانت صحيحة أو × إذا كانت خاطئة.")
       + '<ul class="tf">' + "".join(f'<li><b>{L[k]}</b><span class="t">{t}</span><span class="pr">(&nbsp;&nbsp;&nbsp;&nbsp;)</span></li>' for k, t in enumerate([
           "قانون مور هو الملاحظة التجريبية القائلة إن \"عدد الترانزستورات في الدائرة المتكاملة يتضاعف تقريبًا كل عامين.\"",
           "يواجه استمرار تصغير مكوّنات الدوائر تحديات هندسية وفيزيائية تُبطئ الاتجاه الذي وصفه قانون مور.",
           "شبكات التواصل الاجتماعي فعّالة جدًا في نشر المعلومات بسرعة.",
           "التجارة الإلكترونية تعني شراء السلع من المتاجر الفعلية باستخدام النقد."])) + '</ul>'))
BOOK.append(card("03", "المثال المحلول — الجزء الثالث",
       instr("طابق كل وصف (1 - 3) مع التقنية الأنسب من الخيارات أدناه (أ - ج).")
       + '<div class="match"><div class="mb"><h5>الأوصاف</h5><ol>'
       + "".join(f'<li><span>{t}</span>{AB}</li>' for t in [
           "تقنية تُضيف معلومات رقمية فوق صور من العالم الحقيقي",
           "تقنية تستخدم الذكاء الاصطناعي لقيادة مركبة بأقل تدخل بشري بحسب مستوى الأتمتة",
           "تقنية تتيح للمستخدمين الانغماس في فضاء افتراضي يولّده الحاسب"])
       + '</ol></div><div class="mb"><h5>الخيارات</h5>' + opts(["القيادة الذاتية", "الواقع المعزز", "الواقع الافتراضي"], 1) + '</div></div>'))
SOL2 = [("أ", "تعريف صحيح لقانون مور. وبالتالي، ○."),
        ("ب", "يواجه استمرار تصغير المكوّنات تحديات هندسية وفيزيائية (مثل تيارات التسرب والتأثيرات الكمومية) تُبطئ هذا الاتجاه. وبالتالي، ○."),
        ("ج", "شبكات التواصل الاجتماعي خدمات فعّالة جدًا في نشر المعلومات بسرعة. وبالتالي، ○."),
        ("د", "التجارة الإلكترونية تعني البيع والشراء عبر الإنترنت، وليس الشراء في المتاجر الفعلية باستخدام النقد. وبالتالي، ×.")]
SOL3 = [("1", "إضافة معلومات رقمية فوق صور من العالم الحقيقي هو الواقع المعزز <bdi>(AR)</bdi>.", "ب"),
        ("2", "قيادة مركبة بأقل تدخل بشري بحسب مستوى الأتمتة هي القيادة الذاتية.", "أ"),
        ("3", "الانغماس في فضاء افتراضي هو الواقع الافتراضي <bdi>(VR)</bdi>.", "ج")]
BOOK.append('<div class="qcard sol keep"><h4><span class="ck">✓</span> الحل — المثال المحلول</h4>'
       + f'<div class="sp">(1)</div><div class="sr s1"><span>الترتيب الصحيح هو "بداية ظهور الحاسب (الأربعينيات-الستينيات) {ARR} تسويق الإنترنت تجاريًا (التسعينيات) {ARR} ظهور الهواتف الذكية (العقد الأول من الألفية) {ARR} انتشار الحوسبة السحابية (من العقد الثاني من الألفية فصاعدًا)." وبالتالي، <i>ب</i>.</span></div>'
       + '<div class="sg"><div><div class="sp">(2)</div>' + "".join(f'<div class="sr"><b>{a}</b><span>{t}</span></div>' for a, t in SOL2) + '</div>'
       + '<div><div class="sp">(3)</div>' + "".join(f'<div class="sr"><b>{a}:</b><span>{t} <i>{c}</i></span></div>' for a, t, c in SOL3) + '</div>'
       + '</div></div>')
TADARAB1 = [
    "ما اسم الملاحظة التجريبية القائلة إن \"عدد الترانزستورات في الدائرة المتكاملة يتضاعف تقريبًا كل عامين\"؟",
    "ما المصطلح الذي يشير إلى بيع السلع والخدمات وشرائها عبر الإنترنت؟",
    "ما المصطلح الذي يصف أداء الشخص عمله من المنزل أو من موقع بعيد عبر الإنترنت؟",
    "ما المصطلح الذي يشير إلى نظام إجراء المدفوعات بالنقود الإلكترونية ورموز <bdi>QR</bdi> وغيرها، دون استخدام النقد؟",
    "ما المصطلح الذي يشير إلى التقنية التي تستخدم الذكاء الاصطناعي لقيادة مركبة بأقل تدخل بشري بحسب مستوى الأتمتة؟"]
BOOK.append(card("04", "تدرّب — أجب عن الأسئلة التالية",
       '<div class="sa">' + "".join(f'<div><span class="k">{k+1}</span><p>{t} {blank(80)}</p></div>' for k, t in enumerate(TADARAB1)) + '</div>'))
BOOK.append(card("05", "تدرّب — تصنيف واختيار",
       '<div class="qq"><span class="k">1</span><p>صنّف كل مثال من (1 - 4) ضمن الفئة الأنسب: <b>أ</b> تغيرات في الحياة اليومية، <b>ب</b> تغيرات في الصناعة والاقتصاد، <b>ج</b> تغيرات في الرعاية الصحية والتعليم. ثم فسّر اختيارًا واحدًا.</p></div>'
       + classify(["شراء منتجات عبر التسوق الإلكتروني.", "الدفع مقابل المشتريات بتطبيق دفع على الهاتف الذكي.", "مشاركة الصور مع الأصدقاء على شبكات التواصل الاجتماعي.", "شركة تُطبّق نظام العمل من المنزل."])
       + lines(2)
       + '<div class="qq"><span class="k">2</span><p>من بين الخيارات التالية (أ - د)، اختر الخيار الذي <b>لا يُعد وصفًا مناسبًا</b> لتقنية ناشئة.</p></div>'
       + opts(["القيادة الذاتية تستخدم الذكاء الاصطناعي للمساعدة على قيادة المركبة، ويتفاوت مقدار التدخل البشري بحسب مستوى الأتمتة.",
               "الواقع المعزز تقنية تُضيف معلومات رقمية فوق صور من العالم الحقيقي.",
               "الواقع الافتراضي تقنية تُحسّن بشكل كبير سرعة معالجة الحاسب.",
               "يُتوقع أن تسرّع الحوسبة الكمومية الحسابات الصعبة على الحواسب التقليدية."], 1)))
BOOK.append(card("06", "سؤال على نمط الامتحان",
       '<p class="qs">حلّل كيف غيّر انتشار الحوسبة السحابية (من العقد الثاني من الألفية فصاعدًا) طريقة استخدام تكنولوجيا المعلومات.</p>'
       + hint("<b>في إجابتك، أشِر إلى:</b> تحليل البيانات الضخمة، والذكاء الاصطناعي، و\"تكنولوجيا المعلومات كخدمة\".") + lines(6), tag=MARK6 + TQ))
BOOK.append(card("07", "تمارين — اقرأ الفقرة التالية وأجب عن كل سؤال",
       f'<p class="para">ظهرت الحواسيب الإلكترونية في أربعينيات القرن العشرين، واستُخدمت أولًا في أغراض عسكرية وحسابات علمية. ثم انتشرت (<b>1</b>) {blank(75)} في السبعينيات والثمانينيات، فبدأ استخدامها على نطاق أوسع بين الأفراد. وفي التسعينيات أُتيح (<b>2</b>) {blank(75)} للاستخدام التجاري وانتشر الويب، فتوسع الوصول العالمي إلى المعلومات. وفي العقد الأول من الألفية ظهرت (<b>3</b>) {blank(75)}، فانتشر الإنترنت عبر الهواتف المحمولة بسرعة.</p>'
       + '<div class="qq"><span class="k">1</span><p>املأ الفراغات (1 - 3).</p></div>'
       + f'<div class="qq"><span class="k">2</span><p>ما التقنية التي انتشرت من العقد الثاني من الألفية فصاعدًا، والتي تدعم تحليل البيانات الضخمة واستخدام الذكاء الاصطناعي؟ {blank(90)}</p></div>'
       + f'<div class="qq"><span class="k">3</span><p>ما اسم الملاحظة التجريبية القائلة إن "عدد الترانزستورات في الدائرة المتكاملة يتضاعف تقريبًا كل عامين"؟ {blank(90)}</p></div>'))
BOOK.append(card("08", "تمارين — اختيار",
       '<div class="qq"><span class="k">1</span><p>من بين الخيارات التالية (أ - و)، اختر <b>كل</b> ما يُعد من التقنيات الناشئة.</p></div>'
       + opts(["البريد الإلكتروني", "القيادة الذاتية", "الحواسب الشخصية", "الواقع المعزز", "الواقع الافتراضي", "الحوسبة الكمومية"], 3)
       + '<div class="qq"><span class="k">2</span><p>من بين الخيارات التالية (أ - د)، اختر الخيار الذي يصف بشكل أنسب خصائص شبكات التواصل الاجتماعي.</p></div>'
       + opts(["خدمة تتيح للمستخدمين التواصل فيما بينهم ونشر المعلومات ومشاركتها، وهي فعّالة جدًا في نشر المعلومات بسرعة.",
               "خدمة لبيع السلع والخدمات وشرائها عبر الإنترنت.",
               "أسلوب يعمل فيه الشخص من المنزل أو من مواقع بعيدة أخرى.",
               "نظام لإجراء المدفوعات بالنقود الإلكترونية أو رموز <bdi>QR</bdi> دون استخدام النقد."], 1)))
N_BOOK = 3 + len(TADARAB1) + 2 + 1 + 3 + 2      # 01–03 · 04 (5) · 05 (2) · 06 · 07 (3) · 08 (2)

# ---- اختر (كلها من «تقييمات الترم الأول»، والأسئلة المتكررة اتدمجت)
MCQ = [
 ("أي من الخيارات التالية يمثّل التقنية أو الحدث الرئيسي المرتبط بفترة <b>السبعينيات والثمانينيات</b> من القرن الماضي؟", ["ظهور الهواتف الذكية", "إتاحة الإنترنت للاستخدام التجاري وظهور الويب", "انتشار الحوسبة السحابية", "انتشار الحواسيب الشخصية <bdi>(PCs)</bdi>"]),
 ("أي الملاحظات الآتية تصف بدقة ما يفعله «قانون مور»؟", ["تضاعف عدد الترانزستورات في الدائرة المتكاملة تقريبًا كل عامين", "ثبات عدد الترانزستورات وعدم تغيرها عبر الزمن نهائيًا", "زيادة استهلاك الطاقة في الحواسيب التقليدية بمقدار الضعف سنويًا", "انخفاض قدرات الحوسبة ومعالجة البيانات مع مرور السنوات"]),
 ("ما المصطلح الذي يشير إلى نمط عمل يؤدي فيه الشخص مهامه من المنزل أو من موقع آخر بعيد باستخدام الإنترنت؟", ["التعلم عبر الإنترنت", "التجارة الإلكترونية", "الدفع غير النقدي", "العمل عن بعد <bdi>(Remote Work)</bdi>"]),
 ("ما المقصود بخدمة «شبكات التواصل الاجتماعي <bdi>(SNS)</bdi>»؟", ["دفع قيمة السلع أو الخدمات بوسائل غير نقدية", "بيع السلع والخدمات وشراؤها عبر الإنترنت", "منصات تتيح للمستخدمين التواصل ونشر المحتوى ومشاركته بسرعة", "نمط تعليمي تُقدَّم فيه الدروس عبر الإنترنت"]),
 ("ما التقنية التي تقضي بمعالجة البيانات على الجهاز نفسه فورًا بدلًا من إرسالها إلى السحابة، لتجنّب التأخير في اتخاذ القرار؟", ["الحوسبة السحابية", "الحوسبة الكمومية", "الحوسبة الطرفية", "شبكات التواصل الاجتماعي"]),
 ("أي من الخيارات الآتية يمثّل المفهوم الدقيق لتقنية «الواقع المعزز <bdi>(AR)</bdi>»؟", ["تقنية تضع المستخدم داخل بيئة افتراضية مولدة حاسوبيًا بالكامل", "تقنية تضيف عناصر أو معلومات رقمية إلى مشهد من العالم الحقيقي", "نهج حوسبي يستخدم خصائص ميكانيكا الكم لمعالجة المعلومات", "نظام لإجراء المدفوعات بالنقود الإلكترونية ورموز <bdi>QR</bdi>"]),
 ("ما الذي يميّز «الكيوبت <bdi>(qubit)</bdi>» عن «البت الكلاسيكي» في الحوسبة الكمومية؟", [f"يحمل حالة محددة واحدة إما {num('0')} أو {num('1')} في كل وقت", "يقتصر استخدامه حصريًا على الحسابات البسيطة", "يعتمد فقط على الدوائر المتكاملة التقليدية وثبات التيار الكهربائي", f"يستخدم مبدأ التراكب الكمي ليكون مزيجًا من {num('0')} و{num('1')} في نفس الوقت"]),
 ("ما المقصود بمصطلح «الدفع غير النقدي <bdi>(Cashless Payment)</bdi>»؟", ["دفع قيمة السلع أو الخدمات بوسائل غير نقدية مثل البطاقات أو تطبيقات الهاتف أو رموز <bdi>QR</bdi>", "بيع السلع والخدمات وشراؤها عبر المتاجر الفعلية باستخدام النقد الورقي", "العمل من المنزل باستخدام الإنترنت والبريد الإلكتروني", "تقديم الدروس والمواد التعليمية عبر الإنترنت للمستخدمين"]),
 ("في أي فترة زمنية أُتيح الإنترنت للاستخدام التجاري وظهر الويب، فتوسّع معه الوصول العالمي إلى المعلومات؟", ["الأربعينيات والستينيات", "السبعينيات والثمانينيات", "التسعينيات", "من العقد الثاني من الألفية فصاعدًا"]),
 ("ما التقنية التي تستخدم الذكاء الاصطناعي للمساعدة على قيادة المركبة باستخدام الكاميرات والمستشعرات لإدراك المحيط واتخاذ القرار؟", ["الحوسبة السحابية", "القيادة الذاتية", "الواقع الافتراضي", "الحوسبة الكمومية"]),
 ("ما المصطلح الذي يعبّر عن تكنولوجيا المعلومات المقدَّمة كخدمة عبر الإنترنت لدعم تحليل البيانات الضخمة والذكاء الاصطناعي؟", ["البت الكلاسيكي", "الحوسبة الطرفية", "الحوسبة السحابية", "التراكب الكمي"]),
 ("أي من الآتي يُعد الوصف الصحيح لمفهوم «الواقع الافتراضي <bdi>(VR)</bdi>»؟", ["تقنية تضيف معلومات رقمية فوق صور من العالم الحقيقي", "نظام لإجراء المدفوعات بالنقود الإلكترونية ورموز <bdi>QR</bdi>", "تقنية لمعالجة البيانات على الجهاز نفسه فورًا دون السحابة", "تقنية تضع المستخدم داخل بيئة افتراضية مولدة حاسوبيًا"]),
 ("الفترة الزمنية التي شهدت ظهور الهواتف الذكية وانتشار الإنترنت عبر الهواتف المحمولة بسرعة هي:", ["العقد الأول من الألفية", "السبعينيات والستينيات", "التسعينيات", "الأربعينيات من القرن العشرين"]),
 ("نمط تعليمي وتدريبي تُقدَّم فيه الدروس والمواد التعليمية حصريًا أو جزئيًا عبر شبكة الإنترنت هو:", ["التعلم عبر الإنترنت <bdi>(Online Learning)</bdi>", "العمل عن بعد", "التجارة الإلكترونية", "الدفع غير النقدي"]),
 ("بدأت الحواسيب الإلكترونية في الظهور، واستُخدمت أساسًا للأغراض العسكرية والحسابات العلمية مثل حاسوب <bdi>ENIAC</bdi> باستخدام الصمامات (المفرغة)، في فترة:", ["السبعينيات", "الأربعينيات", "التسعينيات", "العقد الأول من الألفية"]),
 ("مبدأ أو نهج حوسبي يستخدم خصائص ميكانيكا الكم لمعالجة المعلومات، وقد يوفر تفوقًا في فئات محددة من المسائل، هو:", ["الحوسبة الطرفية", "الحوسبة الكمومية", "الدفع غير النقدي", "شبكات التواصل الاجتماعي"]),
]
assert len(MCQ) == 16
TQ_MCQ = set(range(1, len(MCQ) + 1))

# ---- أكمل
FILL = [
 f"أول الحواسيب الإلكترونية التي ظهرت في الأربعينيات، ومن أشهرها {blank()}",
 f"المفاتيح التي اعتمدت عليها الحواسيب الأولى تُسمّى {blank()}",
 f"تقديم الدروس والمواد التعليمية عبر الإنترنت يُسمّى {blank()}",
 f"دفع قيمة السلع أو الخدمات بوسائل غير نقدية مثل البطاقات المصرفية ورموز <bdi>QR</bdi> يُسمّى {blank()}",
 f"المنصات التي تربط المستخدمين لنشر المعلومات ومشاركتها بسرعة هي {blank()}",
 f"تكنولوجيا المعلومات المقدَّمة كخدمة عبر الإنترنت تُسمّى {blank()}",
 f"معالجة البيانات على الجهاز نفسه فورًا بدلًا من إرسالها إلى السحابة تُسمّى {blank()}",
 f"التقنية التي تستخدم الذكاء الاصطناعي للمساعدة على قيادة المركبة هي {blank()}",
 f"التقنية التي تُضيف معلومات رقمية فوق مشهد من العالم الحقيقي هي {blank()}",
 f"التقنية التي تضع المستخدم داخل بيئة افتراضية مولَّدة حاسوبيًا هي {blank()}",
 f"يحمل البت التقليدي حالة واحدة، أما {blank(62)} فيستخدم مبدأ {blank(62)}",
 f"من التحديات الفيزيائية أمام استمرار تصغير المكوّنات: {blank(62)} و{blank(62)}",
]

# ---- صح وخطأ (6 صح / 6 غلط — ومفيش عبارة منقولة من المثال المحلول)
TF = [
 "قانون مور قانون فيزيائي ثابت لا يتغيّر.",
 "استمر اتجاه قانون مور عقودًا، وأسهم في زيادة قدرات الحوسبة وتحسين أداء المعالجات.",
 "العمل عن بُعد نمط تعليمي تُقدَّم فيه الدروس والمواد التعليمية عبر الإنترنت.",
 "من أمثلة التجارة الإلكترونية متاجر إلكترونية مثل أمازون وإيباي.",
 "الحوسبة الكمومية لا تسرّع جميع أنواع الحسابات.",
 "الواقع الافتراضي تقنية تضيف عناصر رقمية فوق العالم الحقيقي.",
 "تُعالَج بعض بيانات القيادة الذاتية محليًا لتقليل زمن الاستجابة.",
 "مقدار التدخّل البشري في القيادة الذاتية ثابت لا يتفاوت.",
 "استُخدمت الحواسيب الإلكترونية الأولى أساسًا في التجارة الإلكترونية.",
 "أُتيح الإنترنت للاستخدام التجاري في التسعينيات.",
 "يعتمد تحسين أداء المعالجات اليوم على التصغير وحده.",
 "البت التقليدي يحمل حالة واحدة في اللحظة.",
]
assert len(TF) == 12

# ---- علّل
WHY = [
 "لا يُعدّ قانون مور قانونًا فيزيائيًا ثابتًا.",
 "كانت الحواسيب الأولى تشغل غرفة بأكملها.",
 "استُخدمت الحواسيب الإلكترونية الأولى أساسًا في الأغراض العسكرية والحسابات العلمية.",
 "يواجه استمرار تصغير مكوّنات الدوائر تحديات هندسية وفيزيائية.",
 "لم يعد تحسين أداء المعالجات معتمدًا على التصغير وحده.",
 "الحوسبة الكمومية ليست بديلًا عامًا للحواسيب التقليدية.",
 "تُعدّ التسعينيات نقطة تحوّل في تاريخ تكنولوجيا المعلومات.",
 "ارتبط انتشار الذكاء الاصطناعي بانتشار الحوسبة السحابية.",
 "يُعدّ ظهور الهواتف الذكية نقلة في طريقة استخدام الإنترنت.",
 "يرتبط تطور التقنية دائمًا بتغيرات اجتماعية واقتصادية تحتاج إلى فهم وتقييم.",
 "يُصنَّف الدفع برمز <bdi>QR</bdi> ضمن الدفع غير النقدي.",
]
TQ_WHY = {1, 4, 7}

# ---- مقالي (كلها من «تقييمات الترم الأول» — المتكرر اتدمج، واللي ليه شبيه في البنك اتشال وخد الشبيه الشارة)
ESS = [
 ("اشرح تطور تكنولوجيا المعلومات في الفترة الممتدة من الأربعينيات إلى الستينيات، موضحًا استخدامها الأساسي في تلك الفترة.", 3),
 ("ما المقصود بمصطلح «التجارة الإلكترونية <bdi>(E-commerce)</bdi>»؟ موضحًا ذلك بمثالين.", 3),
 ("اشرح «قانون مور» موضحًا ما يصفه، والتحديات الهندسية والفيزيائية التي تواجه استمرار تصغير مكونات الدوائر.", 4),
 ("عدّد التحولات المجتمعية الخمسة الناتجة عن تكنولوجيا المعلومات، موضحًا مفهوم كل من «العمل عن بعد» و«التجارة الإلكترونية».", 4),
 ("وضّح خصائص واستخدامات التقنيات الناشئة الثلاث البارزة المذكورة في الدرس (القيادة الذاتية، الواقع المعزز/الافتراضي، والحوسبة الكمومية).", 4),
 ("اشرح كيف أثّر ظهور الحواسيب الشخصية <bdi>(PCs)</bdi> في السبعينيات والثمانينيات، وانتشار الوصول العالمي إلى المعلومات والبريد الإلكتروني في التسعينيات، على المجتمع.", 4),
 ("وضّح باختصار مفهوم كل من «شبكات التواصل الاجتماعي <bdi>(SNS)</bdi>» و«التعلم عبر الإنترنت» و«الدفع غير النقدي» باعتبارها تحولات مجتمعية.", 4),
]
STOPS = [
 ("من بين هذه التغيرات الخمسة، أيها سيكون الأصعب في التخلي عنه، ولماذا؟", False, hint("اختر واحدًا <b>بالاسم</b> · اذكر <b>ماذا ستفقد</b> بالتحديد لو اختفى · وقارنه بواحد آخر أسهل في الاستغناء عنه.")),
 ("في القيادة الذاتية، لماذا يكون من الضروري معالجة البيانات فورًا على المركبة نفسها بالحوسبة الطرفية، بدلًا من إرسالها إلى السحابة لاتخاذ القرار؟ اشرح إجابتك.", True, ""),
 ("ينتشر الدفع غير النقدي في دول كثيرة. فلو تحقّق مجتمع خالٍ تمامًا من النقد، فاختر ميزة واحدة ومصدر قلق واحدًا محتملًا، واشرح باختصار سبب كل منهما.", False, ""),
]

# ---- تصنيف وقارن
CLS = []
IMPACTS = ["انتشار الوصول العالمي إلى المعلومات والبريد الإلكتروني", "استُخدم أساسًا للأغراض العسكرية والحسابات العلمية",
           "تحليل البيانات الضخمة والذكاء الاصطناعي؛ وتقديم موارد تكنولوجيا المعلومات في صورة خدمات عبر الإنترنت",
           "بداية استخدام الأفراد للحاسب", "انتشار سريع وواسع للإنترنت عبر الهواتف المحمولة"]
CLS.append(card("01", "طابق كل أثر على المجتمع بالفترة الزمنية بتاعته",
       '<div class="match"><div class="mb"><h5>التأثير على المجتمع</h5><ol>'
       + "".join(f'<li><span>{t}</span>{AB}</li>' for t in IMPACTS)
       + '</ol></div><div class="mb"><h5>الفترة الزمنية</h5>' + opts(["الأربعينيات–الستينيات", "السبعينيات–الثمانينيات", "التسعينيات", "العقد الأول من الألفية", "من العقد الثاني من الألفية فصاعدًا"], 1) + '</div></div>'))
DEFS = ["الملاحظة القائلة إن عدد الترانزستورات في الشريحة يتضاعف تقريبًا كل عامين", "معالجة البيانات على الجهاز نفسه، فورًا، بدلًا من إرسالها إلى السحابة",
        "تكنولوجيا المعلومات المقدَّمة كخدمة عبر الإنترنت", "تربط المستخدمين لنشر المعلومات ومشاركتها",
        "الدفع دون استخدام النقد (نقود إلكترونية، رموز <bdi>QR</bdi>)"]
CLS.append(card("02", "طابق كل مصطلح بتعريفه",
       '<div class="match"><div class="mb"><h5>التعريف</h5><ol>'
       + "".join(f'<li><span>{t}</span>{AB}</li>' for t in DEFS)
       + '</ol></div><div class="mb"><h5>المصطلح</h5>' + opts(["الدفع غير النقدي", "الحوسبة الطرفية", "شبكات التواصل الاجتماعي", "الحوسبة السحابية", "قانون مور"], 1) + '</div></div>'))
CLS.append(card("03", "قارن بين الواقع المعزز والواقع الافتراضي", cmp_table(["وجه المقارنة", "الواقع المعزز <bdi>(AR)</bdi>", "الواقع الافتراضي <bdi>(VR)</bdi>"], ["التعريف", "طريقة العمل"], tall=True), tag=TQ))
CLS.append(card("04", "قارن بين البت الكلاسيكي والكيوبت", cmp_table(["وجه المقارنة", "البت الكلاسيكي", "الكيوبت <bdi>(qubit)</bdi>"], ["الحالة التي يحملها", "المبدأ الذي يستخدمه"], tall=True), tag=TQ))
CLS.append(card("05", "قارن بين التجارة الإلكترونية والدفع غير النقدي", cmp_table(["وجه المقارنة", "التجارة الإلكترونية", "الدفع غير النقدي"], ["المفهوم", "مثال"], tall=True), tag=TQ))


N_ESS = 2 + len(ESS) + len(STOPS) + 3      # كارتين + المقالي + توقّف وفكّر + (استكشف، فكّر وتحدَّ، اختبر فهمك)
N_CLS = len(CLS)
N_TQ = len(TQ_MCQ) + sum(TQ in c for c in BOOK) + sum(TQ in c for c in CLS) + len(TQ_WHY) + len(ESS) + sum(1 for x in STOPS if x[1])   # الشارات كلها (الكتاب 06 + جداول المقارنة)
stats = [(str(N_BOOK), "أسئلة الكتاب"), (str(len(MCQ)), "اختر"), (str(len(FILL)), "أكمل"), (str(len(TF)), "صح وخطأ"), (str(N_CLS), "تصنيف وقارن"), (str(len(WHY)), "علّل"), (str(N_ESS), "مقالي وأنشطة")]
A('<div class="qstats">' + "".join(f'<div><b class="num">{n}</b><span>{t}</span></div>' for n, t in stats) + f'<div><b class="num">{N_TQ}</b>{TQ}</div></div>')

A(cat("أسئلة الكتاب", stats[0][0]))
for c in BOOK: A(c)

A(cat("اختر الإجابة الصحيحة", str(len(MCQ))))
def plain(t): return re.sub(r"<[^>]+>", "", t)
def mq(j):
    cols = 2 if max(len(plain(o)) for o in MCQ[j][1]) <= 24 else 1
    return f'<div class="mq"><div class="qq"><span class="k">{j+1}</span>{TQ if j+1 in TQ_MCQ else ""}<p>{MCQ[j][0]}</p></div>{opts(MCQ[j][1], cols)}</div>'
for i in range(0, len(MCQ), 2):
    A(f'<div class="mrow{" kwn" if i == 0 else ""}">' + "".join(mq(j) for j in range(i, min(i + 2, len(MCQ)))) + '</div>')   # عنوان «اختر» ينزل مع أول صفين

A(cat("أكمل", str(len(FILL))))
for i in range(0, len(FILL), 2):
    A('<div class="frow">' + "".join(f'<div><span class="k">{j+1}</span><p>{FILL[j]}</p></div>' for j in (i, i + 1)) + '</div>')

A(cat("صح وخطأ", str(len(TF))))
for i in range(0, len(TF), 3):
    A('<ul class="tfb">' + "".join(f'<li><span class="k">{j+1}</span><span class="t">{TF[j]}</span><span class="pr">(&nbsp;&nbsp;&nbsp;&nbsp;)</span></li>' for j in range(i, i + 3)) + '</ul>')

A(cat("تصنيف وقارن", str(N_CLS)))
for c in CLS: A(c)

A(cat("علّل", str(len(WHY))))
for k, t in enumerate(WHY):
    A(f'<div class="why split"><div class="qq"><span class="k">{k+1}</span>{TQ if k+1 in TQ_WHY else ""}<p>{t}</p></div>{lines(2)}</div>')

# ---- مقالي وأنشطة (من غير عنوان)
A(card("01", "طبّق ما تعلمته — قرية اتصلت بالإنترنت",
       '<p class="qs">قرية لم يكن فيها اتصال بالإنترنت من قبل، ثم اتصلت بالإنترنت عالي السرعة وأصبحت خدمات الدفع غير النقدي متاحة فيها. توقّع <b>تغييرين</b> قد يطرآن على الحياة اليومية، وحدد <b>تحديًا جديدًا محتملًا</b>، وفسّر إجابتك.</p>'
       + hint("<b>تغييران محددان</b> (مش كلام عام) · <b>تحدٍّ واحد</b> · <b>تفسير</b> لكل واحد منهم.") + lines(5)))
A(card("02", "فكّر كمهندس — ابحث ثم قرر",
       '<p class="qs">ابدأ من الميزة ومصدر القلق اللذين ذكرتهما في ملاحظة "توقّف وفكّر"، ثم استقصِ أكثر واتخذ قرارك.</p>'
       + '<p class="qs"><b>(1) اجمع البيانات.</b> اسأل عشرة من زملائك في الصف: هل يدفعون عادةً نقدًا أم بطريقة غير نقدية (بطاقة، أو تطبيق على الهاتف المحمول، أو رمز <bdi>QR</bdi>)؟ سجّل النتائج في جدول وحدّد الإجابة الأكثر شيوعًا.</p>' + lines(2)
       + '<p class="qs"><b>(2) حلّل أصحاب المصلحة.</b> استنادًا إلى نتائج الاستطلاع ورأيك، اذكر لكل مجموعة أدناه فائدة واحدة وتحديًا واحدًا لمجتمع يعتمد بدرجة كبيرة على الدفع غير النقدي.</p>'
       + cmp_table(["المجموعة", "الفائدة", "العيب"], ["عميل يدفع", "صاحب متجر صغير", "شخص ليس لديه بطاقة بنكية أو هاتف ذكي"])))
A(card("", "",
       '<p class="qs"><b>(3) اتخذ قرارًا.</b> بالاستناد إلى استطلاعك وجدولك، قرِّر: هل ينبغي أن يتجه مجتمعك نحو الدفع غير النقدي؟ أوصِ بخطوة واحدة واذكر سببين.</p>' + lines(3)
       + hint("ابدأ من احتياجات العميل؛ فسرعة الدفع فائدة محتملة، والحاجة إلى بطاقة أو هاتف تحدٍّ محتمل.", "تلميح الكتاب:")))
for k, (t, n) in enumerate(ESS, start=3):
    A(f'<div class="why ess split"><div class="qq"><span class="k">{k}</span>{TQ}<p>{t}</p></div>{lines(n)}</div>')
T0 = 3 + len(ESS)
for k, (t, tq, h) in enumerate(STOPS, start=T0):
    A(f'<div class="why split"><div class="qq"><span class="k">{k}</span>{TQ if tq else ""}<p><b>توقّف وفكّر:</b> {t}</p></div>{h}{lines(2)}</div>')
T1 = T0 + len(STOPS)
A(f'<div class="why split"><div class="qq"><span class="k">{T1}</span><p><b>استكشف (في ثنائيات):</b> مع زميلك، انظرا إلى الفترات الزمنية الخمس في الجدول أدناه قبل أن تكملا القراءة. ولكل فترة، اذكرا جهازًا أو خدمة واحدة من تلك الحقبة ما زلتما تستخدمانها أو تسمعان عنها اليوم. ثم اتفقا على المرحلة التي تعتقدان أنها غيّرت الحياة اليومية أكثر من غيرها، وسجّلا سببًا واحدًا يدعم اختياركما.</p></div>{lines(3)}</div>')
A(f'<div class="why split"><div class="qq"><span class="k">{T1 + 1}</span><p><b>فكّر وتحدَّ – تأمّل:</b> أي مرحلة من مراحل تكنولوجيا المعلومات تعتقد أنها ستكون الأهم في السنوات العشر القادمة؟ اذكر سببًا واحدًا. هل كان توقعك في بداية الدرس صحيحًا؟ ما الذي غيّر رأيك؟ · <b>وتحدَّ:</b> اختر تقنية ناشئة واحدة من هذا الدرس (القيادة الذاتية، الواقع المعزز/ الواقع الافتراضي، أو الحوسبة الكمومية). اقترح طريقة واحدة يمكن أن تساعد بها في حل مشكلة حقيقية، واذكر خطرًا واحدًا.</p></div>'
  + hint("قارن توقّعك الأول باللي اتعلمته، واربط رأيك بدليل من الدرس · اربط الخطر بالأمان أو الإنصاف أو إتاحة الوصول.") + f'{lines(3)}</div>')
A(f'<div class="why split"><div class="qq"><span class="k">{T1 + 2}</span><p><b>اختبر فهمك:</b> أجب عن أسئلة هذا البنك <b>دون الرجوع</b> إلى الشرح، ثم راجع إجاباتك.</p></div>{lines(1)}</div>')
assert T1 + 2 == N_ESS

EXTRA_CSS = """
/* المرحلة الرابعة: الإنترنت بقى معاك في جيبك */
.pk{position:relative;border:.75pt solid #dde5ef;border-radius:10pt;background:#fbfcfe;padding:9pt 12pt 11pt 12pt;margin:10pt 10pt 0 10pt}
.pk .pkh{text-align:center;margin:0 0 10pt 0}
.pk .pkh b{display:inline-block;background:#22375c;color:#fff;font-weight:800;font-size:11pt;line-height:20pt;padding:0 18pt;border-radius:10pt}
.pkg{display:grid;grid-template-columns:1fr 112pt 1fr;grid-template-rows:auto auto;column-gap:28pt;row-gap:16pt;align-items:center}
.pkp{grid-column:2;grid-row:1 / 3;display:flex;justify-content:center}
.pkp svg.pbig{height:196pt;width:auto;display:block}
.pkc{position:relative;display:flex;align-items:center;gap:8pt;background:#fff;border:.75pt solid #dde5ef;border-radius:9pt;padding:8pt 10pt;min-height:62pt}
.pkc.r1{grid-column:1;grid-row:1} .pkc.r2{grid-column:1;grid-row:2} .pkc.l1{grid-column:3;grid-row:1} .pkc.l2{grid-column:3;grid-row:2}
.pkc .ci{flex:none;width:32pt;height:32pt;border-radius:50%;background:#eef2f8;display:flex;align-items:center;justify-content:center}
.pkc .ci svg{width:18pt;height:18pt}
.pkc .ct b{display:block;font-weight:800;font-size:10.4pt;line-height:15pt;color:var(--navy)}
.pkc .ct small{display:block;font-size:8.8pt;line-height:13pt;color:var(--muted)}
.pkc.r1::after,.pkc.r2::after{content:"";position:absolute;top:50%;left:-28pt;width:26pt;border-top:1.5pt dashed #e29433}
.pkc.l1::after,.pkc.l2::after{content:"";position:absolute;top:50%;right:-28pt;width:26pt;border-top:1.5pt dashed #e29433}
.pkc.r1::before,.pkc.r2::before{content:"";position:absolute;top:calc(50% - 2.25pt);left:-31pt;width:5pt;height:5pt;border-radius:50%;background:#e29433}
.pkc.l1::before,.pkc.l2::before{content:"";position:absolute;top:calc(50% - 2.25pt);right:-31pt;width:5pt;height:5pt;border-radius:50%;background:#e29433}
.cmp4{display:grid;grid-template-columns:1fr 24pt 1fr;align-items:stretch;margin:12pt 0 0 0}
.cmp4 .cb{background:#fff;border:.75pt solid #dde5ef;border-radius:9pt;padding:7pt 11pt 8pt 11pt}
.cmp4 .cb.af{border:1pt solid #e29433}
.cmp4 .cl{display:inline-block;font-weight:800;font-size:8.8pt;line-height:16pt;border-radius:8pt;padding:0 10pt;margin:0 0 3pt 0;background:#eef2f8;color:#2e4a78}
.cmp4 .af .cl{background:#e29433;color:#fff}
.cmp4 p{margin:0;font-size:10pt;line-height:15.4pt;color:var(--text)}
.cmp4 p b{color:var(--navy)}
.cmp4 .ca{display:flex;align-items:center;justify-content:center;color:#e29433;font-family:'DejaVuArr';font-weight:700;font-size:13pt}
.save4{display:flex;align-items:center;gap:10pt;background:#22375c;border-radius:10pt;padding:8pt 12pt;margin:12pt 0 0 0}
.save4 .sl{flex:none;background:#e29433;color:#17263f;font-weight:800;font-size:9.6pt;line-height:18pt;padding:0 11pt;border-radius:8pt}
.save4 .sc{display:flex;align-items:center;gap:5pt;flex-wrap:nowrap}
.save4 .sc span{background:#2e4a78;border:.75pt solid #4a6fa5;border-radius:8pt;padding:2pt 8pt;color:#fff;font-weight:700;font-size:9.3pt;line-height:15pt;white-space:nowrap}
.save4 .sc i{font-style:normal;color:#f1c88b;font-family:'DejaVuArr';font-weight:700;font-size:12pt}

/* صفحات المراحل: صور أكبر ومساحات مريحة */
.ph2.big{margin-top:12pt}
.ph2.eq.big img{height:170pt}
.ph2.c5.big img{height:128pt}
.ph2.c5.big svg.cd{height:126pt}
.pr4 .stp.w4{width:250pt}
.pr4 .stp.w4 img{height:160pt}
.stg.keep{margin-bottom:12pt}

/* التقنيات الناشئة: عنوان وأسهم نازلة لأربع كروت */
.emgw{margin:2pt 0 9pt 0}
.emgw .eh{display:flex;justify-content:center}
.emgw .eh span{background:var(--navy);color:#fff;font-weight:800;font-size:10.5pt;line-height:18pt;padding:0 16pt;border-radius:9pt}
.emgw .ebr{position:relative;height:18pt}
.emgw .ebr i{position:absolute;display:block}
.emgw .ebr .s{top:0;left:calc(50% - .75pt);width:1.5pt;height:6pt;background:#e29433}
.emgw .ebr .h{top:5.25pt;left:calc((100% - 24pt) / 8 - .75pt);right:calc((100% - 24pt) / 8 - .75pt);border-top:1.5pt solid #e29433}
.emgw .ebr .d{top:5.25pt;width:1.5pt;height:7.5pt;background:#e29433}
.emgw .ebr .a{top:12.5pt;width:0;height:0;border-left:4pt solid transparent;border-right:4pt solid transparent;border-top:5.5pt solid #e29433}
.emgw .ebr .d0{left:calc((100% - 24pt) / 8 - .75pt)} .emgw .ebr .a0{left:calc((100% - 24pt) / 8 - 4pt)}
.emgw .ebr .d1{left:calc((100% - 24pt) * 3 / 8 + 8pt - .75pt)} .emgw .ebr .a1{left:calc((100% - 24pt) * 3 / 8 + 8pt - 4pt)}
.emgw .ebr .d2{left:calc((100% - 24pt) * 5 / 8 + 16pt - .75pt)} .emgw .ebr .a2{left:calc((100% - 24pt) * 5 / 8 + 16pt - 4pt)}
.emgw .ebr .d3{left:calc((100% - 24pt) * 7 / 8 + 24pt - .75pt)} .emgw .ebr .a3{left:calc((100% - 24pt) * 7 / 8 + 24pt - 4pt)}
.emgw .emg{grid-template-columns:repeat(4,1fr);margin:0}
.emgw .emg .ec{display:flex;flex-direction:column;align-items:center;text-align:center;padding:8pt 7pt 9pt 7pt}
.emgw .emg .ei{margin:0 0 4pt 0}
.emgw .emg p{font-size:9pt;line-height:13.8pt;text-wrap:pretty}

.qdef{margin:0 0 8pt 0;padding:6pt 12pt;background:#eef2f8;border-right:3pt solid #e29433;border-radius:8pt;font-size:9.8pt;line-height:15.2pt;color:var(--text);text-wrap:pretty}
.qdef b{color:var(--navy)}

.avp .avd{margin:0;padding:6pt 10pt 7pt 10pt;background:#fff;border-top:.75pt solid #dde5ef;font-size:9.6pt;line-height:14.6pt;text-align:center;color:var(--text);text-wrap:pretty}
.avp .avd b{color:var(--navy)}

/* صور المراحل 2–5 */
figure.stp{margin:0}
.stp img{width:100%;height:96pt;object-fit:cover;border-radius:6pt;border:.75pt solid #dde5ef;display:block}
.ph2 .chipf img{object-fit:contain;background:#fff}
.lk3{display:grid;grid-template-columns:1fr 176pt;gap:10pt;align-items:center}
.pr4 .stp.w4{flex:none;width:176pt}

/* الخط الزمني للمراحل (تصميم زياد) */
.tlrow{display:grid;grid-template-columns:1fr 206pt;gap:10pt;align-items:center;margin:0 0 8pt 0}
.tlh{position:relative;display:flex;align-items:center;gap:9pt;background:#fbf6e8;border-radius:10pt;padding:10pt 14pt;margin:0}
.tlimg{margin:0}
.tlimg img{width:100%;height:84pt;object-fit:cover;border-radius:8pt;border:.75pt solid #dde5ef;display:block}
.tlimg .icap{margin:3pt 0 0 0;padding-top:0;border-top:0;font-size:7.8pt;line-height:11.5pt;text-align:center}
.tlh .tico svg{width:20pt;height:20pt;display:block}
.tlh b{font-weight:800;font-size:12pt;line-height:1.4;color:var(--navy)}
.tlh .qm{position:absolute;left:12pt;top:-3pt;font-family:Georgia,serif;font-size:30pt;line-height:1;color:#ecd9ad}
.tl{border:.75pt solid #dde5ef;border-radius:10pt;padding:6pt 7pt 7pt 7pt;margin:0 0 7pt 0;background:#fff}
.tl .cols{position:relative;display:grid;grid-template-columns:repeat(5,1fr);gap:6pt;padding-top:24pt}
.tl .cols::before{content:"";position:absolute;top:11pt;right:16pt;left:7pt;border-top:1.4pt solid #4a6fa5}
.tl .cols::after{content:"";position:absolute;top:7.4pt;left:0;border-style:solid;border-width:4.3pt 8pt 4.3pt 0;border-color:transparent #4a6fa5 transparent transparent}
.tl .tc{position:relative;background:#fbfcfe;border:.75pt solid #e3e9f1;border-radius:8pt;padding:5pt 5pt 6pt 5pt;text-align:center}
.tl .tc .n{position:absolute;top:-24.5pt;left:50%;transform:translateX(-50%);width:19pt;height:19pt;border-radius:50%;background:#e29433;border:2pt solid #fff;color:#fff;font-weight:800;font-size:9.4pt;display:flex;align-items:center;justify-content:center;line-height:1}
.tl .tc:not(:last-child)::after{content:"";position:absolute;top:-15.4pt;left:-5.4pt;width:4.8pt;height:4.8pt;border-radius:50%;background:#4a6fa5}
.tl .tc h5{margin:0 0 4pt 0;font-weight:800;font-size:9.4pt;line-height:13pt;color:var(--navy);min-height:26pt;display:flex;align-items:center;justify-content:center}
.tl .tc img{width:100%;height:56pt;object-fit:cover;border-radius:5pt;display:block;margin:0 0 5pt 0}
.tl .tc .lb{display:flex;align-items:center;justify-content:center;gap:2pt;background:#eef2f8;border-radius:6pt;font-weight:700;font-size:6.9pt;line-height:12.5pt;color:var(--navy2);margin:0 0 3pt 0;white-space:nowrap;padding:0 2pt}
.tl .tc .lb svg{width:9pt;height:9pt;flex:none}
.tl .tc p{margin:0 0 5pt 0;font-size:8.5pt;line-height:12.6pt;color:var(--text);text-wrap:pretty}
.tl .tc p:last-child{margin-bottom:0}
.tipbar{display:flex;align-items:center;justify-content:center;gap:6pt;background:#eef2f8;border-radius:9pt;padding:5pt 12pt;margin:0 0 9pt 0;font-size:9.6pt;line-height:15pt;color:var(--text2)}
.tipbar svg{width:15pt;height:15pt;flex:none}
.tipbar b{color:var(--navy)}
.stg .sp{margin:7pt 12pt 0 12pt;font-size:9.8pt;line-height:15.6pt;color:var(--text2)}
.pnl h5.fh{display:flex;align-items:center;gap:5pt}
.pnl h5.fh svg{width:15pt;height:15pt;flex:none}
.pnl h5.fh span{color:#a9670f}
.ph2.eq{grid-template-columns:1fr 1fr}
.ph2.eq img{height:86pt}

.intro .arw{font-family:'DejaVuArr';font-weight:700;color:#e29433;padding:0 1pt}
.intro .trip{text-wrap:pretty}
/* ---------- إضافات الدرس 1-1 ---------- */
.banner,.quote,.box p,.box li,.note-line,.simply p,.pnl p,.chal p,.soc p,.emg p,.anl3 p,.qbf p,p.lead,.steps .s p,.qcard .qs,.qq p,.why p{text-wrap:pretty}
.intro .body p+p{margin-top:4pt}
.map .cell li{text-wrap:pretty}
.map.m2 .cell h4{display:flex;align-items:flex-start;gap:5pt;line-height:1.4;margin-bottom:2pt}
.map.m2 .cell h4 .mn{flex:none;display:inline-flex;align-items:center;justify-content:center;width:13pt;height:13pt;border-radius:50%;background:var(--navy2);color:#fff;font-size:7.8pt;font-weight:800;margin-top:1.5pt}
.map.m2 .cell .imp{font-size:8.7pt;line-height:13.5pt;color:var(--text);margin-top:3pt;padding-top:3pt;border-top:.75pt dashed #e3e9f1}
.map.m2 .cell .imp b{color:var(--gold2);font-weight:800}
.map.m2 .cell li b{color:var(--navy2);font-weight:700}
.map.m2{grid-template-columns:1fr 104pt 1fr;column-gap:15pt}
.map.m2 .hub{font-size:10pt;padding:6pt 5pt;text-align:center}
.nw{white-space:nowrap}
.fig{position:relative}
.arr{font-family:'DejaVuArr','Baloo Bhaijaan 2';font-weight:700;color:#e29433}
p.lead{font-size:10.2pt;line-height:16.6pt;color:var(--text);margin:0 0 8pt 0}
p.lead b{color:var(--navy2)}
h2.sec .fx{vertical-align:3pt}
.bridge{position:relative;background:#eef2f8;border-radius:9pt;padding:5pt 12pt;margin:0 0 9pt 0;text-align:center;font-size:9.6pt;line-height:15pt;color:var(--text2)}
.bridge .fx{margin:0 0 0 7pt;vertical-align:1pt}
.credit{font-size:7.8pt;color:var(--muted2);line-height:12pt;margin:-3pt 0 8pt 0}
.cn{display:inline-flex;flex:none;align-items:center;justify-content:center;width:14pt;height:14pt;border-radius:50%;background:#e29433;color:#fff;font-size:7.8pt;font-weight:800;line-height:1;margin-left:5pt;vertical-align:1pt}
/* خمسة أفعال */
.verbs{background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:9pt;padding:6pt 10pt 7pt 10pt;margin:0 0 8pt 0}
.verbs .vh{margin-bottom:5pt}
.verbs .lb{display:inline-flex;align-items:center;gap:4pt;font-weight:800;font-size:10pt;color:var(--gold2)}
.verbs .lb svg{width:15pt;height:15pt}
.verbs .vr{display:flex;align-items:stretch;gap:3pt}
.verbs .vc{flex:1;display:flex;flex-direction:column;align-items:center;text-align:center;gap:1pt;background:#fff;border:.75pt solid #dde5ef;border-radius:8pt;padding:5pt 4pt}
.verbs .vi{width:24pt;height:24pt;border-radius:50%;background:#eef2f8;display:flex;align-items:center;justify-content:center}
.verbs .vi svg{width:14pt;height:14pt}
.verbs .vc b{font-weight:800;font-size:10.4pt;color:var(--navy);line-height:1.35}
.verbs .vc small{font-size:8.4pt;line-height:12pt;color:var(--muted)}
.verbs .va{flex:none;align-self:center;font-style:normal;font-size:11pt}
.verbs .vf{margin-top:6pt;text-align:center;font-size:9.6pt;line-height:14.5pt;color:var(--text2)}
/* الصمام · الترانزستور · الدائرة المتكاملة */
.comp3{display:flex;align-items:stretch;gap:4pt;margin:0 0 6pt 0}
.comp3 .cc{flex:1;background:#fff;border:.75pt solid #dde5ef;border-radius:9pt;padding:7pt 9pt 8pt 9pt}
.comp3 .cv{height:72pt;display:flex;align-items:center;justify-content:center;gap:6pt;margin-bottom:5pt;border-bottom:.75pt dashed #dde5ef;padding-bottom:4pt}
.comp3 .cv img{height:66pt;border-radius:6pt}
.comp3 svg.tr{height:62pt;width:auto}
.comp3 svg.icd{height:58pt;width:auto}
.comp3 .sm{font-size:7.8pt;font-weight:700;color:var(--gold2);writing-mode:vertical-rl;transform:rotate(180deg)}
.comp3 h4{margin:0 0 2pt 0;font-weight:800;font-size:10.4pt;color:var(--navy);line-height:1.4}
.comp3 p{font-size:9pt;line-height:14pt;color:var(--text)}
.comp3 .ca{flex:none;align-self:center;font-style:normal;font-size:11pt}
.stats3{background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:9pt;padding:6pt 12pt 7pt 12pt;margin:0 0 8pt 0}
.stats3 .sh{font-weight:800;font-size:9.8pt;color:var(--navy);margin-bottom:4pt}
.stats3 .sg{display:grid;grid-template-columns:repeat(3,1fr);gap:8pt}
.stats3 .sg div{background:#fff;border:.75pt solid #dde5ef;border-radius:7pt;text-align:center;padding:3pt 0 4pt 0}
.stats3 b{display:block;font-weight:800;font-size:15pt;color:var(--gold2);line-height:1.3}
.stats3 span{font-size:8.8pt;font-weight:700;color:var(--muted)}
/* تاريخ IT */
.bphoto{text-align:center;margin:0 0 7pt 0}
.bphoto img{width:46%;border-radius:8pt;border:.75pt solid #dde5ef;display:block;margin:0 auto}
.bphoto .icap{margin:4pt 0 0 0}
table.hist{font-size:9.3pt;line-height:13.8pt}
table.hist td{padding:5pt 9pt 4.5pt 9pt}
table.hist td.k{white-space:normal}
table.hist .sn{display:inline-flex;align-items:center;justify-content:center;width:13pt;height:13pt;border-radius:50%;background:#e29433;color:#fff;font-size:7.6pt;font-weight:800;margin-left:5pt;line-height:1;vertical-align:1pt}
.stg{background:#fff;border:.75pt solid #dde5ef;border-right:3pt solid #e29433;border-radius:9pt;padding:0 0 8pt 0;margin:0 0 8pt 0}
.stg h3.sh{display:flex;align-items:center;gap:7pt;background:#eef2f8;padding:4pt 11pt;border-radius:0 6pt 0 0;margin:0}
.stg .sh .sn{flex:none;width:17pt;height:17pt;border-radius:50%;background:#e29433;color:#fff;font-weight:800;font-size:9pt;display:flex;align-items:center;justify-content:center;line-height:1}
.stg .sh .st{flex:1;font-weight:800;font-size:11.4pt;color:var(--navy);line-height:1.45}
.stg.cont{padding-top:0;border-top-right-radius:0}
.stg.cont>:first-child{margin-top:8pt}
.stg .sh .pd{flex:none;background:#fff;border:.75pt solid #e29433;color:#a9670f;font-weight:700;font-size:8.4pt;line-height:14pt;border-radius:8pt;padding:0 8pt}
.stg>.pnl{margin:8pt 10pt 0 10pt}
.pnl{position:relative;background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:8pt;padding:7pt 10pt 7pt 10pt}
.content>.pnl{margin:0 0 8pt 0}
.pnl.cont{padding-top:8pt}
.pnl.cont>.fx.abs{display:none}
.pnl h5,.pnl h4{margin:0 0 5pt 0;font-weight:800;font-size:10.2pt;color:var(--navy);line-height:1.45}
.pnl .ps{font-size:9.2pt;line-height:14pt;color:var(--muted);margin:-3pt 0 5pt 0}
.pnl .pf{margin-top:6pt;padding-top:5pt;border-top:.75pt dashed #dde5ef;text-align:center;font-size:9.5pt;line-height:14.6pt;color:var(--text2)}
.ich{display:flex;gap:6pt}
.ich>div{flex:1;display:flex;flex-direction:column;align-items:center;gap:2pt;background:#fff;border:.75pt solid #dde5ef;border-radius:7pt;padding:5pt 3pt 4pt 3pt;text-align:center;font-size:8.8pt;font-weight:600;line-height:12.5pt;color:var(--text)}
.ich span svg{width:16pt;height:16pt;display:block}
.chain{display:flex;align-items:stretch;gap:0}
.chain>div{flex:1;display:flex;flex-direction:column;align-items:center;gap:2pt;background:#fff;border:.75pt solid #dde5ef;border-radius:7pt;padding:5pt 4pt 4pt 4pt;text-align:center}
.chain>div span svg{width:16pt;height:16pt;display:block}
.chain>div b{font-weight:700;font-size:8.8pt;line-height:12.5pt;color:var(--navy)}
.chain>i{flex:none;width:15pt;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:10pt}
.chain.sm>div{padding:3pt 3pt}
.chain.sm>div b{font-size:8.4pt}
.ph2{display:grid;grid-template-columns:1.5fr 1fr;gap:8pt;margin:8pt 10pt 0 10pt;align-items:start}
.ph2 figure{margin:0}
.ph2 img{width:100%;height:94pt;object-fit:cover;border-radius:6pt;border:.75pt solid #dde5ef;display:block}
.ph2 figcaption{font-size:8.2pt;line-height:12.2pt;color:var(--muted);text-align:center;margin-top:3pt}
.ph2 figcaption b{color:var(--navy2)}
.ph2 .icap{border-top:0;margin:3pt 0 0 0;padding-top:0}
.p4004{display:flex;align-items:center;justify-content:center;gap:10pt;margin-top:6pt}
.p4004 img{height:46pt;border-radius:5pt}
.p4004 span{font-size:8.8pt;color:var(--muted)}
.ba .br{display:flex;align-items:center;gap:5pt;margin-bottom:5pt}
.bl0{flex:none;width:58pt;text-align:center;background:#eef2f8;border:.75pt solid #dde5ef;border-radius:8pt;font-weight:800;font-size:8.6pt;line-height:15pt;color:var(--navy)}
.af .bl0,.bl0.af{background:#22375c;border-color:#22375c;color:#fff}
.bi{flex:1;display:flex;align-items:center;gap:5pt;background:#fff;border:.75pt solid #dde5ef;border-radius:7pt;padding:4pt 7pt;font-size:8.8pt;line-height:12.5pt;color:var(--text)}
.bi span svg{width:14pt;height:14pt;display:block}
.bi.on{border-color:#e29433}
.ba i,.dp i{flex:none;font-style:normal;font-size:10pt}
.two9{display:grid;grid-template-columns:1fr 1fr;gap:8pt}
.two9 .t9{background:#fff;border:.75pt solid #dde5ef;border-radius:8pt;padding:5pt 8pt 6pt 8pt}
.two9 h6{margin:0 0 4pt 0;font-weight:800;font-size:9.6pt;color:var(--navy);line-height:1.45}
.links{display:flex;align-items:flex-end;justify-content:center;gap:5pt;margin:8pt 0 2pt 0}
.links .lw{display:flex;flex-direction:column;align-items:center;gap:1pt}
.links .lw b{font-size:8pt;color:var(--navy)}
.links svg.win{height:50pt;width:auto;display:block}
.links .la{display:flex;flex-direction:column;align-items:center;margin-bottom:12pt}
.links .la span svg{width:13pt;height:13pt;display:block}
.links .la i{font-style:normal;font-size:12pt;line-height:1}
.links .la small{font-size:7.6pt;font-weight:700;color:var(--gold2)}
.lcap{text-align:center;font-weight:800;font-size:9.6pt;color:var(--navy);margin-top:3pt}
.dp{display:flex;align-items:center;gap:5pt;margin-bottom:6pt}
.pr4{display:flex;align-items:center;gap:10pt}
.pr4 .pf{flex:1;margin-top:0;border-top:0;padding-top:0;text-align:right}
.pr4 .phw{flex:none;display:flex;flex-direction:column;align-items:center}
.pr4 svg.ph{height:50pt;width:auto}
.pr4 small{font-size:7.8pt;color:var(--muted)}
.own{display:grid;grid-template-columns:1fr 1fr;gap:8pt;margin-bottom:6pt}
.own>div{display:flex;align-items:center;gap:7pt;background:#fff;border:.75pt solid #dde5ef;border-radius:7pt;padding:5pt 8pt}
.own>div.af{border-color:#e29433}
.own .oi svg{width:18pt;height:18pt;display:block}
.own p{font-size:8.9pt;line-height:13.5pt;color:var(--text)}
.ph2.c5{grid-template-columns:1fr 1fr 1fr}
.ph2 .cdw{background:#fff;border:.75pt solid #dde5ef;border-radius:6pt;padding:4pt 4pt 3pt 4pt}
.ph2 svg.cd{width:100%;height:92pt;display:block}
.ph2 .cdw figcaption .fx{margin:0 0 0 5pt;vertical-align:0}
.strip{position:relative;background:#fff;border:.75pt solid #dde5ef;border-radius:9pt;padding:10pt 12pt 6pt 12pt;margin:0 0 9pt 0}
.strip .sr{display:flex;align-items:center;justify-content:center;gap:16pt}
.strip .sr>div{display:flex;flex-direction:column;align-items:center;gap:3pt}
.strip .sr span svg{width:30pt;height:30pt;display:block}
.strip .sr b{font-weight:800;font-size:9.8pt;color:var(--navy)}
.strip .sr .g b{color:var(--gold2)}
.strip .sr i{font-style:normal;font-size:14pt}
.strip .sc{margin-top:5pt;padding-top:4pt;border-top:.75pt dashed #dde5ef;text-align:center;font-weight:800;font-size:9.6pt;color:var(--navy)}
.avq{position:relative;border:.75pt solid #dde5ef;border-radius:9pt;background:#fbfcfe;padding:11pt 12pt 10pt 12pt;margin:0 0 10pt 0}
.avq .aq{text-align:center;color:var(--navy);font-size:10.4pt;line-height:16pt;margin-bottom:7pt}
.avq .aq b{font-weight:800}
.avq .aa{display:grid;grid-template-columns:1fr 1fr;gap:12pt}
.avq .aa>div{background:#fff;border:.75pt solid #dde5ef;border-radius:8pt;padding:6pt 10pt;font-size:9.8pt;line-height:15.6pt;color:var(--text)}
.avq .aa>div>b:first-child{display:inline-block;background:#e29433;color:#17263f;border-radius:5pt;padding:0 6pt;margin-left:7pt;font-size:8.8pt;line-height:14pt}
.avq .aa .v{background:#1d4163;border-color:#1d4163;color:#fff}
.avq .aa .v b{color:#f1c88b}
.rcl{display:flex;align-items:center;gap:10pt;background:#22375c;border-radius:10pt;padding:7pt 12pt;margin:0 0 10pt 0}
.rcl .rl{flex:none;background:#e29433;color:#17263f;font-weight:800;font-size:9.6pt;line-height:18pt;padding:0 11pt;border-radius:8pt}
.rcl .rc{flex:1;display:flex;align-items:center;justify-content:center;gap:8pt;flex-wrap:wrap}
.rcl .rc span{background:#2e4a78;border:.75pt solid #4a6fa5;border-radius:8pt;padding:1pt 12pt;color:#fff;font-weight:800;font-size:10.2pt;line-height:17pt}
.rcl .rc i{font-style:normal;color:#f1c88b;font-weight:800}
/* قانون مور */
.mw{position:relative;background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:8pt;padding:7pt 10pt 8pt 10pt;margin:9pt 0 8pt 0}
.mw h5{margin:0 0 5pt 0;font-weight:800;font-size:10.2pt;color:var(--navy);line-height:1.45}
.mfig svg.moore{width:82%;height:auto;display:block;margin:0 auto}
.mfig{padding-top:8pt}
.mnote{font-weight:500;font-size:8.3pt;color:var(--muted);margin-right:10pt;padding-right:10pt;border-right:.75pt solid var(--line)}
.chal{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:8pt;margin:0 0 8pt 0}
.chal .ch2{background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:8pt;padding:7pt 9pt 7pt 9pt}
.chal h5{margin:0 0 5pt 0;font-weight:800;font-size:10pt;color:var(--navy);line-height:1.45}
.chal .cc2{display:flex;gap:7pt;align-items:flex-start;background:#fff;border:.75pt solid #dde5ef;border-radius:7pt;padding:5pt 7pt;margin-bottom:5pt}
.chal .cc2:last-child{margin-bottom:0}
.chal .ci svg{width:18pt;height:18pt;display:block}
.chal .cc2 b{font-weight:800;font-size:9.6pt;color:var(--navy)}
.chal p{font-size:8.8pt;line-height:13.2pt;color:var(--text)}
.chal .cc3{display:grid;grid-template-columns:repeat(3,1fr);gap:5pt}
.chal .cc3>div{display:flex;flex-direction:column;align-items:center;gap:3pt;background:#fff;border:.75pt solid #dde5ef;border-radius:7pt;padding:6pt 3pt;text-align:center;font-weight:700;font-size:8.8pt;line-height:12.5pt;color:var(--navy)}
.chal .cc3 span svg{width:18pt;height:18pt;display:block}
.chal .now p{margin-top:6pt}
.warn>div{flex:1}
.warn>div b{color:var(--navy2)}
/* التغيرات الاجتماعية */
.soc{padding:6pt 11pt 6pt 11pt}
.soc .sc{display:flex;gap:10pt;align-items:flex-start;padding:5pt 2pt 6pt 2pt;border-bottom:.75pt dashed #dde5ef}
.soc .si{flex:none;width:28pt;height:28pt;border-radius:50%;background:#eef2f8;display:flex;align-items:center;justify-content:center;margin-top:1pt}
.soc .si svg{width:16pt;height:16pt}
.soc .st{flex:1}
.soc h4{margin:0;font-weight:800;font-size:10.6pt;color:var(--navy);line-height:1.45}
.soc h4 small{font-size:8.2pt;font-weight:700;color:var(--gold2);margin-right:6pt}
.soc p{font-size:9.7pt;line-height:14.6pt;color:var(--text)}
.soc p.ex{font-size:9pt;color:var(--muted)}
.soc .cap{border-top:0;margin-top:4pt}
.soc .sl .sc{border-bottom:.75pt dashed #dde5ef}
.soc.cont{padding-top:6pt}
/* التقنيات الناشئة */
.emg{display:grid;grid-template-columns:1fr 1fr;gap:8pt;margin:0 0 8pt 0}
.emg .ec{display:grid;grid-template-columns:30pt 1fr;column-gap:8pt;align-content:start;background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:9pt;padding:7pt 10pt 8pt 10pt}
.emg .ei{grid-row:1 / 4;width:30pt;height:30pt;border-radius:50%;background:#fff;border:.75pt solid #dde5ef;display:flex;align-items:center;justify-content:center}
.emg .ei svg{width:17pt;height:17pt}
.emg h4{margin:0;font-weight:800;font-size:11pt;color:var(--navy);line-height:1.4}
.emg small{font-size:8pt;font-weight:700;color:var(--gold2);line-height:1.3}
.emg p{font-size:9.3pt;line-height:14.2pt;color:var(--text);margin-top:2pt}
.emg p b{color:var(--navy2)}
.steps.sd{margin-bottom:4pt}
.steps.sd .s{padding-bottom:9pt}
.steps .s p.sp{font-size:9.1pt;line-height:14pt;color:var(--text);margin-top:3pt;background:#f5f7fb;border-radius:6pt;padding:3pt 8pt}
.steps .s p.sp .fx{margin:0 0 0 5pt;vertical-align:1pt}
.steps .s .sl{color:var(--gold2);font-weight:800}
.steps .lnk{display:inline-block;margin-top:4pt;background:#eef2f8;border-radius:8pt;padding:0 9pt;font-weight:700;font-size:8.8pt;line-height:15pt;color:var(--gold2)}
.edge{padding:12pt 9pt 6pt 9pt}
.edge .e3{display:flex;align-items:stretch;gap:3pt}
.edge .es{flex:1;background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:8pt;padding:5pt 7pt 6pt 7pt;text-align:center}
.edge .es h6{margin:0 0 4pt 0;font-weight:800;font-size:9.6pt;color:var(--navy);line-height:1.4}
.edge .eic{display:flex;justify-content:center;align-items:center;gap:6pt;height:26pt}
.edge .eic svg{width:20pt;height:20pt}
.edge .eic.dec span{display:flex;flex-direction:column;align-items:center}
.edge .eic.dec svg{width:15pt;height:15pt}
.edge .eic.dec small{font-size:7.2pt;font-weight:700;color:var(--muted);line-height:1.1}
.edge .es p{font-size:8.5pt;line-height:12.5pt;color:var(--muted);margin-top:3pt}
.edge .ea{flex:none;align-self:center;font-style:normal;font-size:11pt}
.edge .evs{display:grid;grid-template-columns:1fr 1fr 88pt;gap:7pt;margin-top:8pt}
.edge .ep{background:#fff;border:.75pt solid #dde5ef;border-top:3pt solid #22375c;border-radius:8pt;padding:4pt 7pt 6pt 7pt}
.edge .ep.bad{border-top-color:#e29433}
.edge .eh{display:flex;align-items:center;justify-content:space-between}
.edge .et{font-weight:800;font-size:9.4pt;color:var(--navy)}
.edge .em{width:14pt;height:14pt;border-radius:50%;background:#22375c;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:9pt;line-height:1}
.edge .em svg{width:10pt;height:10pt}
.edge .bad .em{background:#e29433;color:#17263f}
.edge .ech{display:flex;align-items:flex-start;justify-content:space-between;margin:5pt 0 4pt 0}
.edge .ech span{display:flex;flex-direction:column;align-items:center;gap:1pt}
.edge .ech span svg{width:16pt;height:16pt}
.edge .ech small{font-size:7.2pt;font-weight:700;color:var(--muted);line-height:1.15;text-align:center}
.edge .ech i{font-style:normal;font-size:9pt;margin-top:3pt}
.edge .ep p{font-size:8.3pt;line-height:12.3pt;color:var(--text);border-top:.75pt dashed #dde5ef;padding-top:3pt}
.edge .ex14{background:#22375c;border-radius:8pt;padding:5pt 7pt;color:#fff;font-size:8.2pt;line-height:12.6pt}
.edge .ex14>b{display:block;color:#f1c88b;font-weight:800;font-size:8.8pt;margin-bottom:2pt}
.edge .ex14 .r{margin-top:3pt;padding-top:3pt;border-top:.75pt solid rgba(255,255,255,.25)}
.edge .ex14 .r b{color:#ffd08a}
.arvr .av2{display:grid;grid-template-columns:1fr 1fr;gap:12pt;width:100%;margin:0 auto}
.arvr .avp{border:.75pt solid #dde5ef;border-radius:8pt;overflow:hidden}
.arvr .avh{background:#22375c;color:#fff;font-weight:800;font-size:9.6pt;line-height:17pt;padding:0 9pt}
.arvr .avh b{display:inline-block;background:#e29433;color:#17263f;border-radius:5pt;padding:0 5pt;line-height:13pt;margin-left:6pt;font-size:8.4pt}
.arvr .avp svg{width:100%;height:auto;display:block}
.anl3{position:relative;display:grid;grid-template-columns:repeat(3,1fr);gap:8pt;margin:0 0 8pt 0}
.anl3>div{background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:8pt;padding:7pt 9pt 8pt 9pt}
.anl3 .ai svg{width:20pt;height:20pt;display:block}
.anl3 h5{margin:3pt 0 2pt 0;font-weight:800;font-size:10pt;color:var(--navy);line-height:1.4}
.anl3 h5 small{font-size:7.8pt;color:var(--gold2)}
.anl3 .tg{display:inline-block;background:#22375c;color:#fff;border-radius:7pt;font-size:7.6pt;font-weight:700;line-height:12.5pt;padding:0 6pt}
.anl3 p{font-size:9pt;line-height:13.8pt;color:var(--text);margin-top:3pt}
.qbf .qb2{display:grid;grid-template-columns:1fr 1fr;gap:10pt}
.qbf .qp{background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:8pt;overflow:hidden;text-align:center;padding-bottom:6pt}
.qbf .qh{background:#2e4a78;color:#fff;font-weight:800;font-size:10pt;line-height:17pt}
.qbf .qp.k .qh{background:#22375c}
.qbf .qs{font-weight:700;font-size:8.4pt;color:var(--gold2);margin-top:3pt}
.qbf .qp svg{width:50%;height:auto;display:block;margin:4pt auto 2pt auto}
.qbf .qp.k svg{width:34%}
.qbf .qp>b{display:block;font-weight:800;font-size:9.4pt;color:var(--navy);line-height:1.4}
.qbf .qp>small{display:block;font-size:8.4pt;color:var(--muted);line-height:1.35}
.qbf .qx{text-align:right;font-size:8.9pt;line-height:13.6pt;color:var(--text);margin:5pt 9pt 0 9pt;padding-top:5pt;border-top:.75pt dashed #dde5ef}
.qbf .qx .fx{margin:0 0 0 5pt;vertical-align:1pt}
.simply p .fx{vertical-align:1pt}
/* شارة «للفهم» اللي فوق البلوك ماتلزقش في الهيدر لو البلوك أول الصفحة */
.content>.pnl:first-child,.content>.strip:first-child,.content>.mw:first-child,.content>.chal:first-child,.content>.anl3:first-child,.content>.simply:first-child,.content>.fig.edge:first-child,.content>.verbs:first-child{margin-top:7pt}
.steps.sd.cont{padding-top:2pt}
.sdf svg.sdv{width:84%;height:auto;display:block;margin:0 auto}
.sdf{padding-top:8pt}
.qbf .qn{display:flex;align-items:center;gap:8pt;background:#fbf6e8;border:.75pt solid #eee0b8;border-radius:7pt;padding:4pt 10pt;margin-top:8pt}
.qbf .qn .ex{flex:none;width:15pt;height:15pt;border-radius:50%;background:#e29433;color:#fff;font-weight:800;font-size:9pt;display:flex;align-items:center;justify-content:center;line-height:1}
.qbf .qn p{font-size:9pt;line-height:13.6pt;color:var(--text2)}
.soc h4 em.fl{font-style:normal;font-size:7.8pt;font-weight:600;color:var(--muted2);background:#f5f7fb;border:.75pt solid #dde5ef;border-radius:6pt;padding:0 6pt;line-height:12pt;margin-right:6pt;vertical-align:1pt}
/* البنك */
.cmpw{position:relative}
.qcard.sol .sr.s1{margin-bottom:6pt}
.qcard.sol .sg{grid-template-columns:1.25fr 1fr}
ul.op li .arr{font-size:8.6pt;margin:0 1pt}
.check{padding:7pt 13pt 5pt 13pt}
.check .g2{margin-top:5pt}
.check li{margin-bottom:4pt}
/* 1-1: «مصطلحات أساسية» أضيق سنة عشان «اتأكد» يلحق آخر صفحة شرح */
.terms .t2{gap:4pt 6pt}
.terms .t2 div{padding:2pt 9pt;line-height:14pt}
.dark li{margin-bottom:2.5pt}
"""

body = (f'<body data-lesson="الدرس 1-1 — {TITLE}" data-start="{START}" data-total="{TOTAL}">\n<main class="flow">\n'
        + group_html("\n".join(E)) + "\n\n<!-- ===================== بنك الأسئلة ===================== -->\n" + "\n".join(B)
        + "\n</main>\n</body>\n</html>\n")
out = head.replace("</style>", EXTRA_CSS + FLAG_CSS + "</style>", 1) + body
out = out.replace("(el.firstElementChild && el.firstElementChild.tagName === 'H4')", "(el.firstElementChild && /^H[34]$/.test(el.firstElementChild.tagName))")
open(BASE + "lesson_1_1.html", "w", encoding="utf-8").write(out)
print("written", len(out), "| book", N_BOOK, "| mcq", len(MCQ), "| fill", len(FILL), "| tf", len(TF), "| cls", N_CLS, "| why", len(WHY), "| ess", N_ESS, "| tq", N_TQ)
