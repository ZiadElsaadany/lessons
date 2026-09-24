# رسمة البيت (دور واحد): يمين = هيكل (HTML) · نص = تشطيب (CSS) · شمال = نور وكهرباء (JavaScript)
# المناطق متظبطة على عرض الكروت اللي فوقها (أعمدة .85fr 1.05fr 1.2fr + فجوة 7pt)
def house():
    G='#b9c7da'; NV='#22375c'; GD='#e29433'; CR='#ffffff'; LT='#ffe3a3'; SK='#f5f7fb'
    X0,B1,B2,X3=20,230,436,580      # حدود المناطق
    EV,RG,RX=62,26,300              # ارتفاع الحافة، قمة السقف، مكان القمة
    WT,GND=62,124                   # أعلى الحيطة، الأرض
    L,R=8,592                       # أطراف السقف
    def ry(x):
        return EV-(x-L)*(EV-RG)/(RX-L) if x<=RX else RG+(x-RX)*(EV-RG)/(R-RX)
    s=[f'<svg class="house" viewBox="0 0 600 130" fill="none" stroke-linecap="round" stroke-linejoin="round">']
    # ---- شمال: JavaScript
    s.append(f'<path d="M{L} {EV} L{B1} {ry(B1):.1f} L{B1} {WT} Z" fill="{NV}"/>')
    s.append(f'<rect x="{X0}" y="{WT}" width="{B1-X0}" height="{GND-WT}" fill="{CR}" stroke="{NV}" stroke-width="1.6"/>')
    for wx in (32,160):
        s.append(f'<rect x="{wx}" y="76" width="40" height="30" rx="2" fill="{LT}" stroke="{NV}" stroke-width="1.4"/>'
                 f'<line x1="{wx+20}" y1="76" x2="{wx+20}" y2="106" stroke="{NV}" stroke-width="1"/>')
    # مفتاح كهربا
    s.append(f'<rect x="210" y="84" width="10" height="15" rx="2" fill="#fff" stroke="{NV}" stroke-width="1.2"/>'
             f'<line x1="215" y1="88" x2="215" y2="93" stroke="{GD}" stroke-width="2"/>')
    # ---- نص: CSS
    s.append(f'<path d="M{B1} {WT} L{B1} {ry(B1):.1f} L{RX} {RG} L{B2} {ry(B2):.1f} L{B2} {WT} Z" fill="{NV}"/>')
    s.append(f'<rect x="{B1}" y="{WT}" width="{B2-B1}" height="{GND-WT}" fill="{CR}" stroke="{NV}" stroke-width="1.6"/>')
    for k in range(9):   # تكسية
        xx=362+k*7.6
        s.append(f'<line x1="{xx:.1f}" y1="{WT}" x2="{xx:.1f}" y2="{GND}" stroke="{GD}" stroke-width="1.1"/>')
    s.append(f'<rect x="248" y="76" width="54" height="30" rx="2" fill="#eef2f8" stroke="{NV}" stroke-width="1.4"/>'
             f'<line x1="275" y1="76" x2="275" y2="106" stroke="{NV}" stroke-width="1"/>')
    s.append(f'<rect x="316" y="80" width="30" height="{GND-80}" rx="2" fill="#e8c9a0" stroke="{NV}" stroke-width="1.4"/>'
             f'<circle cx="340" cy="104" r="1.8" fill="{NV}"/>')
    # ---- يمين: HTML (هيكل بس)
    s.append(f'<path d="M{B2} {ry(B2):.1f} L{R} {EV}" stroke="{G}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    for cx in (B2+6, 508, X3-6):
        s.append(f'<rect x="{cx-6}" y="{WT}" width="12" height="{GND-WT}" fill="{SK}" stroke="{G}" stroke-width="1.6"/>')
    s.append(f'<rect x="{B2}" y="{WT-4}" width="{X3-B2}" height="8" fill="{SK}" stroke="{G}" stroke-width="1.6"/>')
    # أرض
    s.append(f'<line x1="4" y1="{GND+1}" x2="596" y2="{GND+1}" stroke="{NV}" stroke-width="2"/>')
    # ---- موصّلات من نص كل كارت لحد منطقته
    for cx in (113, 333, 520):
        y=ry(cx) if cx<B2 else WT-4
        s.append(f'<path d="M{cx} 0 L{cx} {y-7:.1f}" stroke="{GD}" stroke-width="1.4" stroke-dasharray="3 3"/>'
                 f'<circle cx="{cx}" cy="{y-3:.1f}" r="3.6" fill="{GD}" stroke="#fff" stroke-width="1.2"/>')
    # لمبة متعلقة ومنوّرة جوه منطقة JavaScript
    bx,by=116,80
    s.append(f'<line x1="{bx}" y1="{WT}" x2="{bx}" y2="{by-6}" stroke="{NV}" stroke-width="1.2"/>'
             f'<path d="M{bx-7} {by-2} Q{bx} {by-10} {bx+7} {by-2} Z" fill="{NV}"/>')
    s.append(f'<circle cx="{bx}" cy="{by+2}" r="4.5" fill="{GD}"/>')
    for dx,dy in ((-1,.35),(1,.35),(0,1),(-.7,.8),(.7,.8)):
        s.append(f'<line x1="{bx+dx*9:.1f}" y1="{by+2+dy*9:.1f}" x2="{bx+dx*15:.1f}" y2="{by+2+dy*15:.1f}" stroke="{GD}" stroke-width="1.4"/>')
    s.append('</svg>')
    return ''.join(s)
