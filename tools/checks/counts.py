import sys,re,html
s=open(sys.argv[1],encoding='utf-8').read()
s=s[s.rindex('<body data-lesson'):]
def txt(x): x=re.sub(r'<[^>]+>','',x); return re.sub(r'\s+',' ',html.unescape(x)).strip()
# stats bar
m=re.search(r'<div class="qstats">(.*?)</div></div>',s,re.S)
print('STATS:', txt(re.sub(r'</div>',' | ',m.group(1))))
# sections by h2.cat
parts=re.split(r'(<h2 class="cat[^"]*">.*?</h2>)',s)
print('TQ badges total:', s.count('class="tq"') if 'class="tq"' in s else 'n/a')
for i in range(1,len(parts),2):
    h=txt(parts[i]); body=parts[i+1]
    cards=re.findall(r'<div class="qcard[^"]*">(?:<h4><span class="n">(\d+)</span>)?',body)
    nk=len(re.findall(r'<span class="k">',body))
    tables=body.count('class="cmp')
    whys=len(re.findall(r'<div class="why',body))
    mq=len(re.findall(r'<div class="mq',body))
    tq=len(re.findall(r'class="tq',body))
    print(f'{h}: cards={[c or "-" for c in cards]} k={nk} mq={mq} why={whys} cmp={tables} tq={tq}')
