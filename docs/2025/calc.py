import json
r=23403/23022; g=1.037; c=1.021
v24={'경찰':134400492696,'검찰':19926742438,'법원':9560539468,'교도소':94856159046,'국립법무병원':938143946,'보호관찰소':9699306569,
'중독자 PGS':96250000000,'사망 PGS':56260000000,'조기사망':38395534968,'노동력 상실·미취업':34499311294,'이환·입원':1612178477,
'직접 의료비':2896893330,'정신건강·복지':1700000000,'간접의료비':1103716359}
grp={'경찰':'형사사법','검찰':'형사사법','법원':'형사사법','교도소':'형사사법','국립법무병원':'형사사법','보호관찰소':'형사사법','중독자 PGS':'고통비용','사망 PGS':'고통비용','조기사망':'생산성','노동력 상실·미취업':'생산성','이환·입원':'생산성','직접 의료비':'의료·복지','정신건강·복지':'의료·복지','간접의료비':'의료·복지'}
v25={};how={}
for k,v in v24.items():
    if k=='검찰': v25[k]=1287949000000*23403/1405185; how[k]=('실측+추계','2025 결산 1조 2,879.5억(실측) × 23,403 ÷ 1,405,185명(2024 처리인원)')
    elif k=='교도소': v25[k]=1699217000000*(3477/61366); how[k]=('실측+추계','2025 결산 1조 6,992.2억(실측) × 3,608 ÷ 63,680명(1일 평균 마약류 추계)')
    elif grp[k]=='형사사법': v25[k]=v*g*r; how[k]=('추계','2024 × 1.037(결산 증가 가정) × 1.0165(단속 증가)')
    else: v25[k]=v*c*r; how[k]=('추계','2024 × 1.021(물가) × 1.0165(단속 증가)')
N=23403
tot=sum(v25.values()); tot24=sum(v24.values())
out={'items':[],'groups':{}}
for k in v24:
    out['items'].append([grp[k],k,v24[k]/1e8,v25[k]/1e8,v25[k]/N/1e4,v25[k]*10/1e8,v25[k]*28.57/1e8,v25[k]/tot*100,how[k][0],how[k][1]])
for gname in ['형사사법','고통비용','생산성','의료·복지']:
    a=sum(v24[k] for k in v24 if grp[k]==gname); b=sum(v25[k] for k in v25 if grp[k]==gname)
    out['groups'][gname]=[a/1e8,b/1e8,b/N/1e4,b*10/1e8,b*28.57/1e8,b/tot*100]
out['tot']=[tot24/1e8,tot/1e8,tot/N/1e4,tot*10/1e8,tot*28.57/1e8]
cpi25=114.2*1.021; ci=cpi25/95.8; o=23403/14214
base=22389; fin=tot*10/1e8
p=base*(ci-1); a=base*ci*(o-1); rr=fin-base*ci*o
out['decomp']=[cpi25,ci,o,fin/base,base*ci,base*ci*o,p,a,rr,fin-base,[x/(fin-base)*100 for x in (p,a,rr)], (tot/N)/(22389e8/142140/ci) ]
out['vs24']=[50209.9, fin, fin/50209.9-1]
json.dump(out,open('vals.json','w'),ensure_ascii=False,indent=1)
for it in out['items']: print(it[1], *[f"{x:,.1f}" for x in it[2:8]], it[8])
for g,vv in out['groups'].items(): print(g,[round(x,1) for x in vv])
print('tot',[round(x,1) for x in out['tot']])
print('decomp',[round(x,3) if isinstance(x,float) else [round(y,1) for y in x] for x in out['decomp']])
print('vs24', out['vs24'])
