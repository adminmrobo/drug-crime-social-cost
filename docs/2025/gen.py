import json
d=json.load(open('vals.json'))
def ok(x):  # 억 → 조/억 format
    x=round(x,1)
    if x>=10000:
        j=int(x//10000); r=x-j*10000
        return f"{j}조 {r:,.1f}억" if r>=0.05 else f"{j}조"
    return f"{x:,.1f}억"
def f1(x): return f"{x:,.1f}"
T=d['tot']; G=d['groups']; I=d['items']
cpi25,ci,o,ratio,base_p,base_po,p,a,rr,inc,sh,_=d['decomp']
pc16=22389e8/142140/1e4; pc16r=pc16*ci; pc25=T[2]
exp=base_po
gcol={'형사사법':'var(--navy)','고통비용':'var(--red)','생산성':'var(--amber)','의료·복지':'var(--teal)'}
seg=''.join(f'<div style="width:{G[g][5]:.1f}%;background:{gcol[g]}">{g+" " if G[g][5]>5 else ""}{G[g][5]:.1f}%</div>' if G[g][5]>5 else f'<div style="width:{G[g][5]:.1f}%;background:{gcol[g]}"></div>' for g in G)
detail={'형사사법':'경찰 {} · 교도소 {}','고통비용':'중독자 {} · 사망 {}','생산성':'조기사망 {} · 미취업 {}','의료·복지':'직접 의료 {} · 정신건강·복지 {}'}
it={x[1]:x for x in I}
dk={'형사사법':('경찰','교도소'),'고통비용':('중독자 PGS','사망 PGS'),'생산성':('조기사망','노동력 상실·미취업'),'의료·복지':('직접 의료비','정신건강·복지')}
grow=''.join(f'<tr><td><b>{g}</b></td><td class="n">{ok(G[g][0]*10)}</td><td class="n">{ok(G[g][1])}</td><td class="n"><b>{ok(G[g][3])}</b></td><td class="n">{f1(G[g][2])}만</td><td>{detail[g].format(ok(it[dk[g][0]][5]),ok(it[dk[g][1]][5]))}</td></tr>' for g in G)
tag=lambda s:{'추계':'<span class="tg e">추계</span>','실측+추계':'<span class="tg m">실측+추계</span>'}[s]
def apx(col,lab,n):
    rows=''
    for g in G:
        gv=G[g]; v= gv[3] if col==5 else gv[4]
        rows+=f'<tr class="hl"><td>{g}</td><td>소계</td><td class="n">{f1(gv[1])}</td><td class="n">{f1(gv[2])}</td><td class="n">{f1(v)}</td><td class="n">{gv[5]:.1f}%</td><td></td></tr>'
        for x in I:
            if x[0]==g: rows+=f'<tr><td></td><td>{x[1]}</td><td class="n">{f1(x[3])}</td><td class="n">{f1(x[4])}</td><td class="n">{f1(x[col])}</td><td class="n">{x[7]:.1f}%</td><td>{tag(x[8])}</td></tr>'
    tv=T[3] if col==5 else T[4]
    rows+=f'<tr class="tot"><td>합계</td><td></td><td class="n">{f1(T[1])}</td><td class="n">{f1(T[2])}</td><td class="n">{f1(tv)}</td><td class="n">100.0%</td><td></td></tr>'
    return f'<table class="t" style="font-size:7.8pt"><tr><th>부문</th><th>세부 항목</th><th class="n">암수율 미반영</th><th class="n">1명당(만 원)</th><th class="n">{lab} ({n})</th><th class="n">비중</th><th>구분</th></tr>{rows}</table>'
html=open('tpl.html').read()
rep={'{{T1}}':ok(T[1]),'{{T3}}':ok(T[3]),'{{T4}}':ok(T[4]),'{{PC}}':f1(pc25),'{{INC}}':ok(inc),'{{RATIO}}':f"{ratio:.2f}",
'{{SH0}}':f"{sh[0]:.1f}",'{{SH1}}':f"{sh[1]:.1f}",'{{SH2}}':f"{sh[2]:.1f}",'{{P}}':ok(p),'{{A}}':ok(a),'{{R}}':ok(rr),
'{{BP}}':ok(base_p),'{{EXP}}':ok(exp),'{{EXPR}}':f"{T[3]/exp:.2f}",'{{CI}}':f"{ci:.3f}",'{{CIP}}':f"{(ci-1)*100:.1f}",'{{O}}':f"{o:.3f}",
'{{PC16}}':f1(pc16),'{{PC16R}}':f1(pc16r),'{{PCN}}':f"{(pc25/pc16-1)*100:.1f}",'{{PCR}}':f"{(pc25/pc16r-1)*100:.1f}",'{{CPI25}}':f"{cpi25:.1f}",
'{{SEG}}':seg,'{{GROWS}}':grow,'{{V24}}':ok(50209.9),'{{D24}}':ok(T[3]-50209.9),'{{D24P}}':f"{(T[3]/50209.9-1)*100:.1f}",
'{{APX10}}':apx(5,'λ 10','234,030명'),'{{APX28}}':apx(6,'λ 28.57','668,624명'),
'{{CJ}}':ok(G['형사사법'][3]),'{{SHCJ}}':f"{G['형사사법'][5]:.1f}"}
for k,v in rep.items(): html=html.replace(k,v)
assert '{{' not in html, [l for l in html.split('\n') if '{{' in l][:3]
open('out/summary_2025.html','w').write(html)
print(rep['{{T3}}'],rep['{{INC}}'],sh, pc16, pc16r, pc25, exp)
