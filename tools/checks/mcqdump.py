import sys,re,html
s=open(sys.argv[1],encoding='utf-8').read()
s=s[s.rindex('<body data-lesson'):]
def txt(x): x=re.sub(r'<[^>]+>','',x); return re.sub(r'\s+',' ',html.unescape(x)).strip()
for m in re.finditer(r'<div class="mq[^"]*"><div class="qq"><span class="k">(\d+)</span>(.*?)</div><ul class="op[^"]*">(.*?)</ul>',s,re.S):
    ops=re.findall(r'<li><b>(.*?)</b>(.*?)</li>',m.group(3))
    print(f'MCQ{m.group(1)}: {txt(m.group(2))}')
    for l,o in ops: print(f'    {l}) {txt(o)}')
