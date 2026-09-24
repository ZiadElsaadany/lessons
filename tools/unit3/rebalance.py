# إعادة توزيع مكان الإجابة الصحيحة في «اختر» على أ/ب/ج/د بالتساوي تقريبًا
import random, re, ast, json, sys
L4 = ["أ", "ب", "ج", "د"]
def targets(n, seed):
    rnd = random.Random(seed)
    base = [i % 4 for i in range(n)]
    while True:
        rnd.shuffle(base)
        ok = all(not (base[i] == base[i-1] == base[i-2]) for i in range(2, n))
        ok = ok and sum(1 for i in range(1, n) if base[i] == base[i-1]) <= 3
        if ok: return list(base)
def perm(nopts, cur, tgt):
    order = list(range(nopts)); order[cur], order[tgt] = order[tgt], order[cur]
    return order  # new position k takes old option order[k]

def do_gen(path, key, seed):
    src = open(path, encoding='utf-8').read()
    tree = ast.parse(src)
    node = next(n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'MCQ')
    lines = src.split('\n')
    offs = [0]
    for l in lines: offs.append(offs[-1] + len(l.encode('utf-8')) + 1)
    b = src.encode('utf-8')
    def pos(ln, col): return offs[ln - 1] + col
    T = targets(len(node.value.elts), seed)
    edits = []; newkey = []
    for q, (tup, cur, tgt) in enumerate(zip(node.value.elts, key, T)):
        lst = tup.elts[1]
        segs = [b[pos(e.lineno, e.col_offset):pos(e.end_lineno, e.end_col_offset)].decode('utf-8') for e in lst.elts]
        order = perm(len(segs), cur, tgt)
        new = '[' + ', '.join(segs[k] for k in order) + ']'
        edits.append((pos(lst.lineno, lst.col_offset), pos(lst.end_lineno, lst.end_col_offset), new))
        newkey.append(L4[tgt])
    for a, z, new in sorted(edits, reverse=True):
        b = b[:a] + new.encode('utf-8') + b[z:]
    open(path, 'wb').write(b)
    return newkey

def do_html(path, key, seed):
    s = open(path, encoding='utf-8').read()
    start = s.rindex('<body data-lesson')
    pat = re.compile(r'(<div class="mq[^"]*"><div class="qq"><span class="k">(\d+)</span>.*?</div>)(<ul class="op[^"]*">)(.*?)(</ul>)', re.S)
    ms = list(pat.finditer(s, start))
    assert len(ms) == len(key), (len(ms), len(key))
    T = targets(len(ms), seed); newkey = []
    out = []; last = 0
    for m, cur, tgt in zip(ms, key, T):
        lis = re.findall(r'<li><b>(.*?)</b>(.*?)</li>', m.group(4))
        order = perm(len(lis), cur, tgt)
        new = ''.join(f'<li><b>{lis[k][0]}</b>{lis[order[k]][1]}</li>' for k in range(len(lis)))
        out.append(s[last:m.start(4)]); out.append(new); last = m.end(4)
        newkey.append(L4[tgt])
    out.append(s[last:])
    open(path, 'w', encoding='utf-8').write(''.join(out))
    return newkey
