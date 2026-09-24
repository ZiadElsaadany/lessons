import sys,re,html
from html.parser import HTMLParser
s=open(sys.argv[1],encoding='utf-8').read()
s=s[s.find('بنك الأسئلة ====='):] if 'بنك الأسئلة =====' in s else s[s.find('<main'):]
def txt(x): x=re.sub(r'<[^>]+>','',x); return re.sub(r'\s+',' ',html.unescape(x)).strip()
# split into top-level blocks by lines
for i,line in enumerate(s.split('\n')):
    if 'class="cat' in line: print('\n### ',txt(line)); continue
    if 'class="mrow"' in line:
        for m in re.finditer(r'<div class="mq"><div class="qq"><span class="k">(\d+)</span><p>(.*?)</p></div><ul class="op[^"]*">(.*?)</ul>',line):
            print(f'MCQ{m.group(1)}: {txt(m.group(2))} || {txt(m.group(3))[:90]}')
    elif 'class="frow"' in line:
        for m in re.finditer(r'<span class="k">(\d+)</span><p>(.*?)</p>',line): print(f'FILL{m.group(1)}: {txt(m.group(2))}')
    elif 'class="tfb"' in line:
        for m in re.finditer(r'<span class="k">(\d+)</span><span class="t">(.*?)</span>',line): print(f'TF{m.group(1)}: {txt(m.group(2))}')
    elif 'class="why' in line:
        m=re.search(r'<span class="k">(\d+)</span><p>(.*?)</p>',line); print(f'WHY{m.group(1)}{" ess" if "ess" in line[:40] else ""}: {txt(m.group(2))}')
    elif 'class="qcard' in line:
        print('CARD:',txt(line)[:400])
