"""Extract vector drawings from a PDF page region as a standalone SVG (paths only)."""
import pymupdf

def hx(c):
    return None if c is None else '#%02x%02x%02x' % tuple(int(round(v*255)) for v in c[:3])

def drawings_to_svg(page, clip, pad=0.5, exclude_fill=None):
    x0, y0, x1, y1 = clip.x0-pad, clip.y0-pad, clip.x1+pad, clip.y1+pad
    out = []
    for d in page.get_drawings():
        r = d["rect"]
        if not clip.intersects(r):
            continue
        if exclude_fill and hx(d.get("fill")) in exclude_fill and r.width > clip.width*0.9:
            continue
        parts = []
        cur = None  # current pen position
        def P(pt): return f"{pt.x-x0:.3f} {pt.y-y0:.3f}"
        def same(a, b): return a is not None and abs(a.x-b.x) < 0.01 and abs(a.y-b.y) < 0.01
        for it in d["items"]:
            op = it[0]
            if op == "l":
                p1, p2 = it[1], it[2]
                if not same(cur, p1): parts.append("M" + P(p1))
                parts.append("L" + P(p2)); cur = p2
            elif op == "c":
                p1, c1, c2, p2 = it[1], it[2], it[3], it[4]
                if not same(cur, p1): parts.append("M" + P(p1))
                parts.append(f"C{P(c1)} {P(c2)} {P(p2)}"); cur = p2
            elif op == "re":
                rr = it[1]
                parts.append(f"M{rr.x0-x0:.3f} {rr.y0-y0:.3f} H{rr.x1-x0:.3f} V{rr.y1-y0:.3f} H{rr.x0-x0:.3f} Z"); cur = None
            elif op == "qu":
                q = it[1]
                parts.append(f"M{P(q.ul)} L{P(q.ur)} L{P(q.lr)} L{P(q.ll)} Z"); cur = None
        dstr = " ".join(parts)
        if d.get("closePath"):
            dstr += " Z"
        attrs = []
        t = d["type"]
        fill = hx(d.get("fill")) if "f" in t else None
        stroke = hx(d.get("color")) if "s" in t else None
        attrs.append(f'fill="{fill}"' if fill else 'fill="none"')
        if d.get("fill_opacity") not in (None, 1.0) and fill:
            attrs.append(f'fill-opacity="{d["fill_opacity"]:.3f}"')
        if stroke:
            attrs.append(f'stroke="{stroke}" stroke-width="{d.get("width") or 1:.3f}"')
            lc = d.get("lineCap"); lj = d.get("lineJoin")
            cap = {0:"butt",1:"round",2:"square"}
            join = {0:"miter",1:"round",2:"bevel"}
            if lc: attrs.append(f'stroke-linecap="{cap.get(lc[0] if isinstance(lc,(tuple,list)) else lc,"butt")}"')
            if lj is not None: attrs.append(f'stroke-linejoin="{join.get(lj,"miter")}"')
            if d.get("stroke_opacity") not in (None, 1.0):
                attrs.append(f'stroke-opacity="{d["stroke_opacity"]:.3f}"')
        if d.get("even_odd"):
            attrs.append('fill-rule="evenodd"')
        out.append(f'<path d="{dstr}" {" ".join(attrs)}/>')
    w, h = x1-x0, y1-y0
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.2f}pt" height="{h:.2f}pt">' + "".join(out) + '</svg>'

if __name__ == "__main__":
    import sys
    doc = pymupdf.open("unit3.pdf")
    jobs = {
        "robot": (1, pymupdf.Rect(278, 200, 318, 251)),
        "icon_front": (2, pymupdf.Rect(430, 292, 533, 382)),
        "icon_back": (2, pymupdf.Rect(249, 289, 347, 382)),
        "icon_db": (2, pymupdf.Rect(69, 286, 161, 386)),
    }
    for name, (pno, clip) in jobs.items():
        svg = drawings_to_svg(doc[pno], clip)
        open(f"assets/{name}.svg", "w").write(svg)
        print(name, len(svg))
