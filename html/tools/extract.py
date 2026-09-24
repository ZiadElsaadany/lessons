import pymupdf, sys, re
ALEFS = set("اأإآ")
import os; doc = pymupdf.open(os.environ.get("SRC","unit3.pdf"))

def line_text(line):
    """Return (text_with_markup) for a line: reverse word order (visual->logical), fix ligature order."""
    toks = []  # list of (word, bold)
    cur = []; curb = None
    def flush():
        nonlocal cur, curb
        if cur:
            toks.append(("".join(cur), curb)); cur = []
    for s in line["spans"]:
        bold = ("ExtraBold" in s["font"]) or ("Black" in s["font"]) or ("Bold" in s["font"])
        chars = s["chars"]
        i = 0
        while i < len(chars):
            c = chars[i]["c"]; w = chars[i]["bbox"][2]-chars[i]["bbox"][0]
            if c == " ":
                flush(); curb=None; i += 1; continue
            if c in ALEFS and abs(w) < 0.01 and i+1 < len(chars) and chars[i+1]["c"] == "ل":
                # ligature lam-alef extracted reversed
                if curb is None: curb = bold
                cur.append("ل"); cur.append(c); i += 2; continue
            if curb is None: curb = bold
            if curb != bold:
                flush(); curb = bold
            cur.append(c); i += 1
    flush()
    toks.reverse()
    out = []
    for w, b in toks:
        out.append(("**"+w+"**") if b else w)
    return " ".join(out)

for pno in range(int(sys.argv[1])-1, int(sys.argv[2])):
    p = doc[pno]
    rd = p.get_text("rawdict")
    print(f"\n\n======== PAGE {pno+1} ========")
    lines = []
    for b in rd["blocks"]:
        if b["type"] != 0: continue
        for l in b["lines"]:
            if abs(l["dir"][1]) > 0.01: continue  # skip rotated watermark
            bb = l["bbox"]
            if bb[1] < 30 or bb[1] > 807: continue  # skip header/footer
            sizes = {round(s["size"],1) for s in l["spans"]}
            fonts = {s["font"].split("-")[0] for s in l["spans"]}
            t = line_text(l)
            if t.strip():
                lines.append((round(bb[1],1), round(bb[0],1), round(bb[2],1), sizes, fonts, t))
    lines.sort(key=lambda x: (x[0], -x[2]))
    for y, x0, x1, sizes, fonts, t in lines:
        print(f"[y={y:6.1f} x={x0:5.1f}-{x1:5.1f} {'/'.join(sorted(fonts))} {sorted(sizes)}] {t}")
