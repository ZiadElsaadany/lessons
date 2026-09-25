# -*- coding: utf-8 -*-
"""u4conv — بيحوّل دروس الوحدة الرابعة (HTML متعمول بالإيد بصفحات ثابتة 1240px) لقالب المذكرة.

- التصميمات بتاعة الدرس نفسها بتفضل زي ما هي (نفس الـCSS والـmarkup)، بس:
  * كل الـclasses بتاخد بادئة «u-» عشان ماتتخانقش مع القالب، وكل الـselectors بتتحصر جوّه `.content`.
  * كل مقاسات الـpx بتتحول pt بمعامل FX_PT (عرض محتوى الصفحة 1132px عندهم = 532pt عندنا)، وأقل خط 8pt.
  * الشريط والفوتر بتوعهم بيتشالوا؛ القالب بيحط الهيدر والفوتر (باللوجو) والعلامة المائية والترقيم.
  * الصفحات الثابتة بتتفك: كل عنصر بقى بلوك في main.flow، والقالب بيقسّم على A4 لوحده.
- أسئلة «التقييمات الرسمية» بتتنقل للبنك: المكرر بياخد علامة «تقييمات» على سؤال البنك، والجديد بيتضاف
  في «اختر» أو في المقالي بعلامة «تقييمات». الترقيم والعدادات بيتحسبوا من جديد.
- «للفهم» بقت علم على الجنب (fxflag)، و«لخّص» في صفحة لوحدها، وعمود «التصحيح» في صح وخطأ اتشال.
"""
import re, os, sys, difflib
from bs4 import BeautifulSoup, NavigableString, Tag

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
from fxflag import FLAG_CSS, strip_style

FX_PT = 532 / 1132          # pt لكل px من التصميم الأصلي
MIN_FONT = 8.0              # أقل حجم خط بعد التحويل (pt)
P = "u-"                    # بادئة الـclasses

FXA = '<span class="fx abs">للفهم</span>'
BIDI = re.compile(r"\([A-Za-z][A-Za-z0-9 ./]*\s[–·:-]\s[A-Za-z0-9 ./-]+\)")


def _pt(v, font=False):
    x = float(v) * FX_PT
    if font and x < MIN_FONT: x = MIN_FONT
    return f"{x:.2f}pt".replace(".00pt", "pt")


def scale_decl(d):
    d = re.sub(r"(font-size\s*:\s*)(-?\d*\.?\d+)px", lambda m: m.group(1) + _pt(m.group(2), True), d)
    return re.sub(r"(-?\d*\.?\d+)px", lambda m: _pt(m.group(1)), d)


SKIP_SEL = re.compile(r"^\s*(html|body|\.stage|\.page|\.strip|\.foot|:root|\*)\b")


def conv_selector(sel):
    out = []
    for s in sel.split(","):
        s = s.strip()
        if not s or SKIP_SEL.match(s): continue
        s = re.sub(r"\.(-?[_a-zA-Z][\w-]*)", lambda m: "." + P + m.group(1), s)
        out.append(".content " + s)
    return ", ".join(out)


def conv_css(css):
    """CSS بسيط: قواعد + @media/@page (بيتشالوا)."""
    out, i, n = [], 0, len(css)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    n = len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0: break
        head = css[i:j].strip()
        if head.startswith("@"):
            depth, k = 1, j + 1
            while k < n and depth:
                depth += {"{": 1, "}": -1}.get(css[k], 0); k += 1
            i = k; continue
        k = css.find("}", j)
        body = css[j + 1:k]
        sel = conv_selector(head)
        if sel: out.append(sel + "{" + scale_decl(body) + "}")
        i = k + 1
    return "\n".join(out)


def cls(el): return el.get("class") or []


def has(el, c): return isinstance(el, Tag) and c in cls(el)


def txt(el): return re.sub(r"\s+", " ", el.get_text(" ", strip=True))


def norm(t):
    t = re.sub(r"[ً-ْـ]", "", t)
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


STOP = set("من في على إلى عن أن إن أو و ما هو هي التي الذي التالية التالي الآتي الآتية يلي مما كل بين مع ثم قد لا كيف لماذا ماذا أي اذكر اشرح وضح وضّح ناقش بيّن بين عرف تحدث قارن المقصود بمصطلح مصطلح يُعد يعد تعد تُعد أحد إحدى هل حسب الكتاب الدرس".split())
def words(t):
    out = set()
    for w in norm(t).split():
        for pre in ("وال", "بال", "لل", "ال", "و", "ب"):
            if w.startswith(pre) and len(w) - len(pre) >= 3: w = w[len(pre):]; break
        if w not in STOP and len(w) > 2: out.add(w)
    return out
def sim(a, b):
    A, B = words(a), words(b)
    j = len(A & B) / max(1, min(len(A), len(B)))
    return max(difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(), j * 0.95)


class Lesson:
    def __init__(self, src, lid, subs=()):
        self.lid = lid
        raw = open(src, encoding="utf-8").read()
        raw = raw.replace('<div class="unit">الوحدة الرابعة<br>', '<div class="unit">الفصل الرابع<br>')   # الكتاب بيقول «الفصل»
        raw = raw.replace("أي كلام عليه العلامة دي — هو والرسومات — مش موجود في الكتاب. أنا حاطّه عشان تفهم، مش عشان تحفظه. واللي من الكتاب هتلاقيه من غير علامة.",
                          "أي جزء عليه علامة «للفهم» هو شرح أو رسم إضافي للتوضيح، ومش مطلوب حفظه كنص من الكتاب.")
        for a, b in subs:        # تعديلات صياغة على نص المصدر — كل واحدة لازم تلاقي مكانها مرة واحدة بالظبط
            n = raw.count(a)
            if n != 1: raise SystemExit(f"subs: {n}× «{a[:70]}»")
            raw = raw.replace(a, b)
        self.soup = BeautifulSoup(raw, "html.parser")
        self.css = conv_css(self.soup.find("style").string)
        self.defs = self.soup.find("svg")                     # الـ<symbol> بتاعة الأيقونات
        self.defs.extract()
        blocks, mode = {"exp": [], "tq": [], "bank": []}, "exp"
        for pg in self.soup.select("div.page"):
            for c in list(pg.children):
                if not isinstance(c, Tag) or has(c, "strip") or has(c, "foot"): continue
                if has(c, "lhead"):
                    t = txt(c)
                    if "التقييمات" in t: mode = "tq"
                    elif "بنك الأسئلة" in t: mode = "bank"
                blocks[mode].append(c.extract())
        self.exp, self.tq, self.bank = blocks["exp"], blocks["tq"], blocks["bank"]
        self.log = []

    # ---------- مساعدات ----------
    def new(self, html):
        return BeautifulSoup(html, "html.parser").contents[0]

    def sec_index(self, key):
        for k, b in enumerate(self.bank):
            if has(b, "sec") and key in txt(b): return k
        return None

    def bank_range(self, key):
        a = self.sec_index(key)
        b = a + 1
        while b < len(self.bank) and not has(self.bank[b], "sec"): b += 1
        return a, b

    # ---------- التقييمات ← البنك ----------
    # ov: {("m"|"e", رقم السؤال في التقييمات من 1): "new" | "skip" | رقم سؤال البنك (اختر) / نص جزء من سؤال البنك (مقالي)}
    def merge_tq(self, ov=None, thr_m=0.62, thr_e=0.6):
        ov = ov or {}
        badge = lambda: self.new('<span class="tqbadge">تقييمات</span>')
        tq_mcq, tq_ess = [], []
        for b in self.tq:
            if not isinstance(b, Tag): continue
            if has(b, "tq"):
                h = b.find(class_="tqh"); q = h.find(class_="qn")
                if q: q.extract()
                tq_ess.append(txt(h))
            for m in b.select(".mcq"): tq_mcq.append(m)
        # --- اختر
        a, z = self.bank_range("اختر")
        grids = [b for b in self.bank[a:z] if has(b, "qgrid")]
        bank_mcq = [m for g in grids for m in g.select(".mcq")]
        n0 = len(bank_mcq); seen = []
        for i, m in enumerate(tq_mcq, 1):
            qh = m.find(class_="qh"); q = qh.find(class_="qn")
            if q: q.extract()
            t = txt(qh) + " " + " ".join(txt(o) for o in m.select(".opt"))
            dec = ov.get(("m", i))
            prev = max(seen, key=lambda x: sim(x[0], t)) if seen else None
            if dec is None and prev and sim(prev[0], t) >= 0.75: dec = "skip"
            if dec is None:
                best = max(range(n0), key=lambda k: sim(txt(bank_mcq[k]), t)) if n0 else None
                dec = best + 1 if best is not None and sim(txt(bank_mcq[best]), t) >= thr_m else "new"
            if dec == "skip":
                self.log.append(f"TQ-m{i} مكرر في التقييمات: «{txt(qh)[:55]}»"); continue
            if isinstance(dec, str) and dec != "new":          # سؤال في البنك برّه «اختر» (زي أسئلة الكتاب)
                tgt = next(x for b in self.bank if isinstance(b, Tag) for x in ([b] + b.select(".item, .sub, .c, .ecard")) if dec in txt(x))
                if not tgt.find(class_="tqbadge"): tgt.insert(0, badge())
                self.log.append(f"TQ-m{i} = «{txt(tgt)[:45]}»: «{txt(qh)[:40]}»"); continue
            if dec == "new":
                qh.insert(0, self.new('<span class="qn">0</span>')); m.insert(0, badge())
                grids[-1].append(m); bank_mcq.append(m); seen.append((t, m))
                self.log.append(f"TQ-m{i} اتضاف: «{txt(qh)[:60]}»")
            else:
                tgt = bank_mcq[dec - 1]
                if not tgt.find(class_="tqbadge"): tgt.insert(0, badge())
                seen.append((t, tgt))
                self.log.append(f"TQ-m{i} = اختر {dec}: «{txt(qh)[:40]}» ⇐ «{txt(tgt.find(class_='qh'))[:40]}»")
        for k, m in enumerate([m for g in grids for m in g.select(".mcq")], 1):
            m.find(class_="qn").string = str(k)
        self.n_mcq = len(bank_mcq)
        # --- المقالي (وعلّل والكتاب) — المكرر بياخد علامة، والجديد قبل «أنشطة»
        cand = []
        fa, fz = self.bank_range("أكمل")
        for k, b in enumerate(self.bank):
            if not isinstance(b, Tag) or fa <= k < fz: continue
            cand += [b] if (has(b, "item") or has(b, "ecard")) else b.select(".item, .ecard")
        act = self.sec_index("أنشطة")
        ins_at = act if act is not None else len(self.bank)
        new_items, seen = [], []
        for i, t in enumerate(tq_ess, 1):
            dec = ov.get(("e", i))
            prev = max(seen, key=lambda x: sim(x[0], t)) if seen else None
            if dec is None and prev and sim(prev[0], t) >= 0.72: dec = ("tq", prev[1])
            if dec is None:
                best = max(cand, key=lambda x: sim(txt(x), t)) if cand else None
                dec = best if best is not None and sim(txt(best), t) >= thr_e else "new"
            elif isinstance(dec, str) and dec not in ("new", "skip"):
                dec = next(x for x in cand if dec in txt(x))
            if dec == "skip": self.log.append(f"TQ-e{i} اتشال: «{t[:55]}»"); continue
            if isinstance(dec, tuple):
                self.log.append(f"TQ-e{i} مكرر في التقييمات: «{t[:55]}»"); continue
            if dec == "new":
                it = self.new(f'<div class="item"><span class="tqbadge">تقييمات</span><span class="qn">0</span>{t}</div>')
                ab = self.new('<div class="abox">' + '<div class="aline"></div>' * 3 + '</div>')
                new_items += [it, ab]; cand.append(it); seen.append((t, it))
                self.log.append(f"TQ-e{i} اتضاف: «{t[:60]}»")
            else:
                if not dec.find(class_="tqbadge"): dec.insert(0, badge())
                seen.append((t, dec))
                self.log.append(f"TQ-e{i} = «{txt(dec)[:45]}»: «{t[:45]}»")
        self.bank[ins_at:ins_at] = new_items
        ia = self.sec_index("مقالي")
        k = 0
        for b in self.bank[ia:]:
            if has(b, "item"):
                q = b.find(class_="qn")
                if q: k += 1; q.string = str(k)
        self.n_ess = k + len([b for b in self.bank[ia:self.sec_index("أنشطة") or len(self.bank)] if has(b, "sub")])
        self.n_badges = sum(len(b.select(".tqbadge")) + (1 if has(b, "tqbadge") else 0) for b in self.bank if isinstance(b, Tag))

    # ---------- مفتاح «اختر»: تطويل اختيارات غلط + تقرير ----------
    def mcq_key(self, key, lengthen=None):
        a, z = self.bank_range("اختر")
        ms = [m for b in self.bank[a:z] if has(b, "qgrid") for m in b.select(".mcq")]
        key = key.split(",") if isinstance(key, str) else key
        assert len(key) == len(ms), (len(key), len(ms))
        for q, rep in (lengthen or {}).items():
            for o in ms[q - 1].select(".opt"):
                ol = o.find(class_="ol"); t = txt(o)[len(txt(ol)):].strip()
                if t in rep:
                    for x in list(o.contents):
                        if x is not ol: x.extract()
                    o.append(rep[t])
        self.key, rep = key, []
        L4 = ["أ", "ب", "ج", "د"]
        for i, (m, k) in enumerate(zip(ms, key), 1):
            opts = [txt(o)[len(txt(o.find(class_="ol"))):].strip() for o in m.select(".opt")]
            c = opts[L4.index(k)]
            if len(c) == max(len(x) for x in opts) and [len(x) for x in opts].count(len(c)) == 1: rep.append(i)
        self.longest = rep
        return rep

    def fix_counts(self):
        for b in self.bank:
            if has(b, "counts"):
                for c in b.select(".cnt"):
                    t = txt(c.find(class_="t")); n = c.find(class_="n")
                    if t.startswith("اختر"): n.string = str(self.n_mcq)
                    if t.startswith("مقالي"): n.string = str(self.n_ess)
                b.append(self.new(f'<div class="cnt tqc"><div class="n">{self.n_badges}</div><div class="t"><span class="tqbadge">تقييمات</span></div></div>'))

    # ---------- صح وخطأ: من غير عمود التصحيح ----------
    def fix_tf(self, drop_rows=()):
        for b in self.bank:
            if b.name == "table" and has(b, "tf"):
                for tr in b.select("tr"):
                    cells = tr.find_all(["th", "td"], recursive=False)
                    if cells and ("التصحيح" in txt(cells[-1]) or cells[0].name == "td"):
                        if len(cells) == 4: cells[-1].extract()
                rows = [tr for tr in b.find_all("tr") if tr.find("td")]
                k = self.bank.index(b)
                for j in range(max(0, k - 3), k):
                    x = self.bank[j]
                    if has(x, "sec") and "صح وخطأ" in txt(x):
                        h = x.find("h2"); h.string = re.sub(r"صح وخطأ.*", "صح وخطأ", h.get_text())
                    if has(x, "inst"): x.string = "ضع علامة ○ أمام العبارة الصحيحة، وعلامة × أمام العبارة الخاطئة."
                for r in drop_rows: rows[r - 1].extract()
                for k, tr in enumerate([tr for tr in b.find_all("tr") if tr.find("td")], 1): tr.find("td").string = str(k)

    # ---------- «للفهم» ← علم ----------
    def flags(self):
        for b in self.exp + self.bank:
            if not isinstance(b, Tag): continue
            for t in b.select("span.tag"):
                if t.get_text(strip=True) != "للفهم" or has(b, "legend"): continue
                t.extract()
                b.insert(0, self.new(FXA))
            for l in b.select("span.lab"):
                s = l.get_text()
                if s.startswith("للفهم"):
                    l.string = s.replace("للفهم — ", "").replace("للفهم", "").strip() or "للفهم"
                    if not b.find(class_="fx"): b.insert(0, self.new(FXA))
            for s in b.select("span.lab"):
                if "للفهم — مش للحفظ" in s.get_text(): s.string = "مش للحفظ:"
        # شرح بالعامية مش من الكتاب: صندوق «ببساطة» ← علم · التعليق الرمادي جوه فقرة من الكتاب ← بادج صغير «للفهم»
        for b in self.exp:
            if not isinstance(b, Tag): continue
            for t in ([b] if has(b, "simple") else b.select(".simple")):
                if any("الكتاب" in l.get_text() for l in t.select("span.lab")): continue   # «مصطلحات الكتاب» = نص الكتاب
                anc, x = [t], t
                while x is not b and x.parent is not None: x = x.parent; anc.append(x)
                if not any(x.find(class_="fx", recursive=False) for x in anc): t.insert(0, self.new(FXA))
            for g in b.select("span.gl"):
                if not g.find(class_="fx"): g.insert(0, self.new('<span class="fx">للفهم</span> '))
        # سطر الشرح اللي تحت «خريطة الدرس» يفضل مع الخريطة نفسها (مايتفصلش عنها في آخر الصفحة)
        ex = [x for x in self.exp if isinstance(x, Tag)]
        for k, x in enumerate(ex[:-1]):
            if has(x, "sec") and "خريطة الدرس" in txt(x) and has(ex[k + 1], "lead") and "kwn" not in cls(ex[k + 1]):
                ex[k + 1]["class"] = cls(ex[k + 1]) + ["kwn"]
        # «مثال من حياتنا» ← علم على الصندوق اللي بعد العنوان
        for k, b in enumerate(self.exp):
            if has(b, "sec") and "مثال من حياتنا" in txt(b) and k + 1 < len(self.exp):
                nx = self.exp[k + 1]
                if isinstance(nx, Tag) and not nx.find(class_="fx"): nx.insert(0, self.new(FXA))
        # «أنشطة — فهم من الشرح» ← «أنشطة»
        for b in self.bank:
            if has(b, "sec"):
                h = b.find("h2")
                if h and "فهم من الشرح" in h.get_text(): h.string = h.get_text().replace(" — فهم من الشرح", "").replace("فهم من الشرح", "").strip(" —")

    # ---------- نص السؤال في عنصر واحد ----------
    def wrap_items(self):
        """.item / .qh معمولين flex: لو النص فيه <b> أو فراغ، كل حتة كانت بتبقى عمود لوحدها — نلمّ النص كله في span.qtx واحد جنب الرقم."""
        for b in self.exp + self.bank:
            if not isinstance(b, Tag): continue
            for it in ([b] if (has(b, "item") or has(b, "qh")) else []) + b.select(".item, .qh"):
                if it.find(class_="qtx", recursive=False): continue
                lead = [c for c in it.contents if isinstance(c, Tag) and (has(c, "qn") or has(c, "tqbadge"))]
                rest = [c for c in list(it.contents) if c not in lead]
                if not any((isinstance(c, Tag)) or str(c).strip() for c in rest): continue
                qt = self.soup.new_tag("span", attrs={"class": "qtx"})
                for c in rest: qt.append(c.extract())
                it.append(qt)

    # ---------- اللوجو في الهيدر ----------
    def logo(self):
        for b in self.exp + self.bank:
            if has(b, "lhead"):
                bar = b.find(class_="bar-h")
                if bar and not bar.find("img"):
                    bar.append(self.new('<img class="logo" src="assets/avatar.png" alt="">'))

    # ---------- «لخّص» في صفحة لوحدها ----------
    def summary_page(self):
        for k, b in enumerate(self.exp):
            if has(b, "sec") and "لخّص" in txt(b):
                self.exp.insert(k, self.new('<div class="pb"></div>'))
                for j in range(k + 1, len(self.exp)):
                    if has(self.exp[j], "lines"):
                        ln = self.exp[j]; ln.clear()
                        for _ in range(31): ln.append(self.new("<div></div>"))
                        self.exp.insert(j + 1, self.new('<div class="pb"></div>'))
                        break
                break

    # ---------- إدراج بلوكات جديدة ----------
    def raw(self, html):
        t = self.new(html); t["data-raw"] = "1"; return t

    def _hit(self, seq, key, nth):
        hits = [k for k, b in enumerate(seq) if isinstance(b, Tag) and not b.get("data-raw") and key in txt(b)]
        if not hits: raise KeyError(key)
        return hits[nth]

    def insert_after(self, where, key, html, nth=0):
        seq = self.exp if where == "exp" else self.bank
        seq.insert(self._hit(seq, key, nth) + 1, self.raw(html))

    def insert_before(self, where, key, html, nth=0):
        seq = self.exp if where == "exp" else self.bank
        seq.insert(self._hit(seq, key, nth), self.raw(html))

    def move(self, key, n, before=None):
        """يشيل n بلوكات من الشرح بادئة بالبلوك اللي فيه key ويحطهم قبل before (أو قبل «لخّص»)."""
        k = self._hit(self.exp, key, 0); grp = self.exp[k:k + n]; del self.exp[k:k + n]
        j = self._hit(self.exp, before or "لخّص الدرس بأسلوبك", 0)
        if self.exp[j - 1].name == "div" and has(self.exp[j - 1], "pb"): j -= 1
        self.exp[j:j] = grp

    def replace(self, where, key, html, nth=0):
        seq = self.exp if where == "exp" else self.bank
        k = self._hit(seq, key, nth); seq[k] = self.raw(html)

    # ---------- تجهيز للتقسيم على الصفحات ----------
    def prep(self, seq, bank=False):
        out, i = [], 0
        while i < len(seq):
            b = seq[i]
            if not isinstance(b, Tag): i += 1; continue
            if bank and has(b, "item"):
                grp = [b]; j = i + 1
                while j < len(seq) and isinstance(seq[j], Tag) and not (set(cls(seq[j])) & {"item", "sec", "sub", "inst"}) \
                        and seq[j].name != "table" and not has(seq[j], "pb") and not has(seq[j], "ecard"):
                    grp.append(seq[j]); j += 1
                w = self.new('<div class="grp"></div>')
                for g in grp: w.append(g)
                out.append(w); i = j; continue
            out.append(b); i += 1
        return out

    def render(self, blocks):
        html = []
        for b in blocks:
            if b.get("data-raw"):
                del b["data-raw"]; html.append(str(b)); continue
            for e in [b] + b.find_all(True):
                c = cls(e)
                keep = [x for x in c if x in ("fx", "abs", "pb", "rcl", "rl", "rc", "exs", "eh", "tq", "kwn")]
                c2 = [x if x in keep or x.startswith(P) else P + x for x in c]
                if c2: e["class"] = c2
                if e.get("style"): e["style"] = scale_decl(e["style"])
            for t in list(b.find_all(string=BIDI)):      # إنجليزي جنب إنجليزي بفاصل ← <bdi>
                if t.parent.name in ("bdi", "style", "script"): continue
                frag = BeautifulSoup(BIDI.sub(lambda m: f"<bdi>{m.group(0)}</bdi>", str(t)), "html.parser")
                t.replace_with(*list(frag.contents))
            if set(cls(b)) & {P + "sec", P + "sub", P + "inst", P + "tsub", P + "mainq", P + "qcard"}: b["class"] = cls(b) + ["kwn"]
            if set(cls(b)) & {P + "qgrid", P + "cls"}:
                b["class"] = cls(b) + ["split"]
            html.append(str(b))
        return "\n".join(html)


def build(src, lid, title, start, total, out, extra_css="", hook=None, tf_drop=(), ov=None, subs=()):
    L = Lesson(src, lid, subs)
    L.merge_tq(ov); L.fix_counts(); L.fix_tf(tf_drop); L.flags(); L.logo(); L.summary_page()
    if hook: hook(L)
    L.wrap_items()
    body_html = L.render(L.prep(L.exp)) + "\n\n<!-- ===================== بنك الأسئلة ===================== -->\n" \
        + L.render([L.new('<div class="pb"></div>')] + L.prep(L.bank, bank=True))
    base = os.path.dirname(TOOLS) + "/"
    tpl = open(base + "lesson_3_1.html", encoding="utf-8").read()
    head = strip_style(tpl[:tpl.index("<body data-lesson=")])
    head = head.replace("<title>الدرس 3-1 — البنية العامة لتطبيقات الويب</title>", f"<title>الدرس {lid} — {title}</title>")
    head = head.replace("الدرس 3-1 (الشرح)", f"الدرس {lid} (الشرح + بنك الأسئلة)")
    css = "\n/* ---------- تصميمات الدرس الأصلية (u4conv) ---------- */\n" + L.css + "\n" + U4_CSS + extra_css
    defs = str(L.defs)
    doc = (head.replace("</style>", css + FLAG_CSS + "</style>", 1)
           + f'<body data-lesson="الدرس {lid} — {title}" data-start="{start}" data-total="{total}">\n{defs}\n<main class="flow">\n'
           + body_html + "\n</main>\n</body>\n</html>\n")
    doc = doc.replace("(el.firstElementChild && el.firstElementChild.tagName === 'H4')", "(el.firstElementChild && /^H[34]$/.test(el.firstElementChild.tagName))")
    open(base + out, "w", encoding="utf-8").write(doc)
    return L


def recall(items):
    return ('<div class="rcl keep"><span class="rl">ثبّت الصفحة في 10 ثواني</span><div class="rc">'
            + '<i>·</i>'.join(f'<span>{t}</span>' for t in items) + '</div></div>')


def exs(t): return f'<div class="exs"><span class="fx abs">للفهم</span><span class="eh">مثال للتبسيط:</span>{t}</div>'


def terms(rows):
    return ('<div class="terms keep"><div class="th"><h3>مصطلحات أساسية</h3></div><div class="t2">'
            + "".join(f'<div class="full"><b>{a}</b> – {b}</div>' for a, b in rows) + '</div></div>')


U4_CSS = """
/* ---------- إضافات u4conv ---------- */
.content .u-lhead .u-bar-h{position:relative}
.content .u-lhead img.u-logo{width:40pt;height:40pt;border-radius:9pt;border:1.2pt solid rgba(255,255,255,.35);flex:none;margin-right:8pt}
.content .u-counts{grid-template-columns:repeat(8,1fr)!important}
.content .u-counts .u-tqc .u-tqbadge{position:static;display:inline-block}
.content .u-grp{margin:0}
.content .u-mcq{position:relative}
.content .u-item{position:relative}
.content .u-item>.u-tqbadge,.content .u-mcq>.u-tqbadge,.content .u-ecard>.u-tqbadge{position:absolute;top:-6pt;left:10pt}
.content>.u-grp:first-child>.u-item>.u-tqbadge,.content>.u-qgrid:first-child .u-mcq>.u-tqbadge{top:-3pt}
/* مسافة فوق نص السؤال اللي عليه بادج «تقييمات» عشان البادج مايغطيش أول سطر */
.content .u-mcq:has(>.u-tqbadge){padding-top:8.5pt}
.content .u-item:has(>.u-tqbadge){padding-top:7pt}
.content .u-ecard:has(>.u-tqbadge){padding-top:10pt}
.content .u-ecard:has(>.u-marks)>.u-tqbadge{left:56pt}
.content .u-qtx{flex:1;min-width:0}
.content>.u-grp:first-child>.u-item:has(>.u-tqbadge){padding-top:11pt}
.content>.u-qgrid:first-child .u-mcq:has(>.u-tqbadge){padding-top:11pt}   /* جنب «6 درجات» مش تحتها */
.rcl{display:flex;align-items:center;gap:10pt;background:#1F2A47;border-radius:10pt;padding:7pt 12pt;margin:0 0 10pt 0}
.rcl .rl{flex:none;background:#DA9C3B;color:#17263f;font-weight:800;font-size:9.6pt;line-height:18pt;padding:0 11pt;border-radius:8pt}
.rcl .rc{flex:1;display:flex;align-items:center;justify-content:center;gap:8pt;flex-wrap:wrap}
.rcl .rc span{background:#2e3b5e;border:.75pt solid #4a5a82;border-radius:8pt;padding:1pt 12pt;color:#fff;font-weight:800;font-size:10.2pt;line-height:17pt}
.rcl .rc i{font-style:normal;color:#f1c88b;font-weight:800}
.exs{position:relative;background:#fffdf8;border:.75pt dashed #DA9C3B;border-radius:9pt;padding:5pt 12pt;margin:5pt 0 8pt 0;font-size:9.6pt;line-height:15pt;color:#3A466A;text-wrap:pretty}
.exs .eh{font-weight:800;color:#b07a22;margin-left:5pt}
.exs b{color:#1F2A47}
.u4v{position:relative;border:.75pt solid #E3E7EF;border-radius:10pt;background:#fff;padding:9pt 12pt 8pt 12pt;margin:4pt 0 10pt 0}
.u4v .vh{font-weight:800;font-size:10.4pt;color:#1F2A47;margin:0 0 6pt 0}
.u4v .vh em{font-style:normal;color:#b07a22}
.u4v .vg{display:grid;gap:7pt}
.u4v .vc{border-radius:8pt;background:#F6F7FB;border:.75pt solid #E3E7EF;padding:6pt 8pt;text-align:center}
.u4v .vc b{display:block;font-weight:800;font-size:10pt;color:#1F2A47;line-height:1.35}
.u4v .vc small{display:block;font-size:8.8pt;line-height:13pt;color:#3A466A;margin-top:2pt;text-wrap:pretty}
.u4v .vc .tg{display:inline-block;margin-top:4pt;border-radius:7pt;padding:0 7pt;font-size:8.2pt;font-weight:800;line-height:14pt;background:#fff;border:.75pt solid #E8D9B8;color:#b07a22}
.u4v .vc.hot{background:#FFF8EC;border-color:#E8D9B8}
.u4v .vc.ok{background:#EEF8F2;border-color:#BFE3CE} .u4v .vc.no{background:#FDF0EE;border-color:#F0C9C2}
.u4v .vf{margin-top:6pt;padding-top:5pt;border-top:.75pt dashed #E3E7EF;text-align:center;font-size:9.2pt;line-height:14pt;color:#3A466A}
.u4v .vf b{color:#1F2A47}
.content .terms .t2 .full{grid-column:1/-1}
.content .terms .t2{gap:4pt 6pt}
"""
