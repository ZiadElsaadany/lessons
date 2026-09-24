"""Convert PyMuPDF get_drawings() items inside a clip rect into an SVG (vector)."""
import pymupdf, sys

def col(c, op=1.0):
    if c is None: return "none"
    return '#%02x%02x%02x' % tuple(int(round(v*255)) for v in c[:3])

def path_d(items):
    d = []
    cur = None
    for it in items:
        k = it[0]
        if k == 'l':
            p1, p2 = it[1], it[2]
            if cur is None or (abs(cur.x-p1.x) > 1e-6 or abs(cur.y-p1.y) > 1e-6):
                d.append(f"M{p1.x:.3f} {p1.y:.3f}")
            d.append(f"L{p2.x:.3f} {p2.y:.3f}")
            cur = p2
        elif k == 'c':
            p1, c1, c2, p2 = it[1], it[2], it[3], it[4]
            if cur is None or (abs(cur.x-p1.x) > 1e-6 or abs(cur.y-p1.y) > 1e-6):
                d.append(f"M{p1.x:.3f} {p1.y:.3f}")
            d.append(f"C{c1.x:.3f} {c1.y:.3f} {c2.x:.3f} {c2.y:.3f} {p2.x:.3f} {p2.y:.3f}")
            cur = p2
        elif k == 're':
            r = it[1]
            d.append(f"M{r.x0:.3f} {r.y0:.3f}H{r.x1:.3f}V{r.y1:.3f}H{r.x0:.3f}Z")
            cur = None
        elif k == 'qu':
            q = it[1]
            d.append(f"M{q.ul.x:.3f} {q.ul.y:.3f}L{q.ur.x:.3f} {q.ur.y:.3f}L{q.lr.x:.3f} {q.lr.y:.3f}L{q.ll.x:.3f} {q.ll.y:.3f}Z")
            cur = None
    return ' '.join(d)

def drawings_to_svg(page, clip, pad=0.5, filt=None):
    clip = pymupdf.Rect(clip)
    out = []
    for dr in page.get_drawings():
        r = dr["rect"]
        if not clip.contains(r): continue
        if filt and not filt(dr): continue
        d = path_d(dr["items"])
        if dr.get("closePath"): d += " Z"
        fill = col(dr.get("fill")) if dr["type"] in ("f", "fs") else "none"
        stroke = col(dr.get("color")) if dr["type"] in ("s", "fs") else "none"
        attrs = [f'd="{d}"', f'fill="{fill}"']
        if dr.get("even_odd"): attrs.append('fill-rule="evenodd"')
        if dr.get("fill_opacity") not in (None, 1, 1.0) and fill != "none": attrs.append(f'fill-opacity="{dr["fill_opacity"]:.3f}"')
        if stroke != "none":
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{dr.get("width") or 1:.3f}"')
            lc = {0:"butt",1:"round",2:"square"}.get((dr.get("lineCap") or (0,))[0], "butt")
            lj = {0:"miter",1:"round",2:"bevel"}.get(dr.get("lineJoin") or 0, "miter")
            attrs.append(f'stroke-linecap="{lc}" stroke-linejoin="{lj}"')
            if dr.get("stroke_opacity") not in (None, 1, 1.0): attrs.append(f'stroke-opacity="{dr["stroke_opacity"]:.3f}"')
            if dr.get("dashes") and dr["dashes"] not in ("[] 0", "[]"): attrs.append(f'stroke-dasharray="{dr["dashes"].split("]")[0].strip("[ ")}"')
        out.append("<path " + " ".join(attrs) + "/>")
    x0, y0 = clip.x0 - pad, clip.y0 - pad
    w, h = clip.width + 2*pad, clip.height + 2*pad
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {y0:.3f} {w:.3f} {h:.3f}" '
           f'width="{w:.3f}pt" height="{h:.3f}pt">' + "".join(out) + "</svg>")
    return svg, (w, h)

if __name__ == "__main__":
    doc = pymupdf.open("unit3.pdf")
    svg, wh = drawings_to_svg(doc[1], (278, 200, 318, 251))
    open("assets/robot.svg", "w").write(svg)
    print("robot", wh, len(svg))
