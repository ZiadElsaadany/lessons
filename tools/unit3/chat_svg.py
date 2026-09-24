# واجهة دردشة بتلات حالات: html = هيكل بس، css = متنسقة، js = متنسقة + تفاعل
# ألوان المذكرة بس (مش ألوان أي تطبيق حقيقي)
def chat(mode):
    G='#b9c7da'; SK='#f5f7fb'; NV='#22375c'; GD='#e29433'; LN='#dde5ef'; IN='#eef2f8'; OUT='#fde9c8'
    css = mode in ('css', 'js')
    s=[f'<svg class="chat" viewBox="0 0 150 100" fill="none" stroke-linecap="round" stroke-linejoin="round">']
    # الإطار
    s.append(f'<rect x="1" y="1" width="148" height="98" rx="9" fill="{"#fff" if css else SK}" stroke="{NV if css else G}" stroke-width="1.3"/>')
    # الهيدر: صورة + اسم الشخص
    if css:
        s.append(f'<path d="M1 10 Q1 1 10 1 L140 1 Q149 1 149 10 L149 22 L1 22 Z" fill="{NV}"/>')
        s.append(f'<circle cx="135" cy="11.5" r="6.5" fill="{GD}"/><rect x="92" y="7" width="34" height="4.5" rx="2" fill="#fff"/><rect x="104" y="13.5" width="22" height="3" rx="1.5" fill="#8fa3c4"/>')
    else:
        s.append(f'<line x1="1" y1="22" x2="149" y2="22" stroke="{G}" stroke-width="1.2"/>')
        s.append(f'<circle cx="135" cy="11.5" r="6.5" stroke="{G}" stroke-width="1.2" stroke-dasharray="2.5 2"/><rect x="92" y="7" width="34" height="4.5" rx="1" stroke="{G}" stroke-width="1" stroke-dasharray="2.5 2"/>')
    # الرسائل
    bubbles=[(78,28,64,12,'in'),(8,44,62,12,'out'),(90,60,52,10,'in')]
    for x,y,w,h,k in bubbles:
        if css:
            fill = IN if k=='in' else OUT
            s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}"/>')
            s.append(f'<rect x="{x+6}" y="{y+h/2-1.3:.1f}" width="{w-12}" height="2.6" rx="1.3" fill="{"#9aa9c2" if k=="in" else "#d3a25a"}"/>')
        else:
            s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5" stroke="{G}" stroke-width="1.1" stroke-dasharray="2.5 2"/>')
            s.append(f'<line x1="{x+6}" y1="{y+h/2:.1f}" x2="{x+w-6}" y2="{y+h/2:.1f}" stroke="{G}" stroke-width="1.4"/>')
    # رسالة جديدة ظهرت بعد الضغط على إرسال (JavaScript)
    if mode=='js':
        s.append(f'<rect x="8" y="73" width="46" height="10" rx="5" fill="{OUT}" stroke="{GD}" stroke-width="1.2"/>')
        s.append(f'<rect x="14" y="76.7" width="34" height="2.6" rx="1.3" fill="#d3a25a"/>')
        for dx,dy,ex,ey in ((58,72,63,68),(59,78,65,78)):
            s.append(f'<line x1="{dx}" y1="{dy}" x2="{ex}" y2="{ey}" stroke="{GD}" stroke-width="1.3"/>')
    # مربع الكتابة + زر الإرسال
    if css:
        s.append(f'<rect x="26" y="86" width="116" height="9" rx="4.5" fill="#fff" stroke="{LN}" stroke-width="1"/>')
        s.append(f'<circle cx="14" cy="90.5" r="6.5" fill="{GD}"/><path d="M16.8 90.5 L11 87.6 L12.4 90.5 L11 93.4 Z" fill="#fff"/>')
    else:
        s.append(f'<rect x="26" y="86" width="116" height="9" rx="1.5" stroke="{G}" stroke-width="1.1" stroke-dasharray="2.5 2"/>')
        s.append(f'<rect x="7.5" y="84" width="13" height="13" rx="1.5" stroke="{G}" stroke-width="1.1" stroke-dasharray="2.5 2"/>')
    if mode=='js':
        # ضغطة على زر الإرسال
        s.append(f'<circle cx="14" cy="90.5" r="10" stroke="{GD}" stroke-width="1" opacity=".55"/>')
        # عداد الرسائل اتغير
        s.append(f'<circle cx="12" cy="11.5" r="7" fill="{GD}"/><text x="12" y="14.6" text-anchor="middle" font-size="9" font-weight="800" fill="{NV}" font-family="Baloo Bhaijaan 2">3</text>')
        # تنبيه
        s.append(f'<path d="M30 16 Q30 8 35 7.5 Q40 8 40 16 L41.5 17.5 L28.5 17.5 Z" fill="#fff"/><circle cx="35" cy="19" r="1.5" fill="#fff"/><circle cx="40.5" cy="7.5" r="2.4" fill="{GD}"/>')
    s.append('</svg>')
    return ''.join(s)
