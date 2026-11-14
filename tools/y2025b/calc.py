import json, math
N=23403; CPI=1.021
# ---- 2025 원고 반영(억 원) ----
CJ={'경찰':138100689019,'검찰':19926742438,'법원':9899724058,'교도소':195331338672,'국립법무병원':510193095,'보호관찰소':9050817841}
CJ={k:v/1e8 for k,v in CJ.items()}
MED={'직접 의료비':44.5789885,'간접의료비':16.98459462,'정신건강·복지':17.0}
PRD={'조기사망':421.8911316,'이환·입원':22.52245909,'노동력 상실·미취업':370.55281736}
PGS={'중독자 PGS':1649*1.1*CPI,'사망 PGS':58*9.7*CPI}
EX=json.load(open('/home/claude/v5/extra.json'))['2025']
SOC={'2차 범죄':EX['이차범죄']/1e8,'예방·대응 예산':EX['예방']/1e8,'가족 돌봄':EX['가족']/1e8,'약물 운전':EX['운전']/1e8}
SOC_LO=dict(SOC); SOC_LO['2차 범죄']=EX['이차범죄_범위'][0]/1e8
G=[('형사사법',CJ,'원고 11.08(실측)'),('고통비용',PGS,'추정(2024 원단위×물가)'),('생산성',PRD,'원고 11.06(실측)'),('의료·복지',MED,'원고 11.06(실측)'),('사회적 혼란·기타',SOC,'별지 추계(11.9)')]
OLD={'형사사법':2807.0,'고통비용':2435.9,'생산성':773.3,'의료·복지':59.2,'사회적 혼란·기타':496.0}  # 11.9 시산
rows=[];grp={}
for g,d,src in G:
    for k,v in d.items(): rows.append([g,k,v,v/N*1e4,v*10,v*28.57,src])
    grp[g]=sum(d.values())
base4=sum(grp[g] for g in ['형사사법','고통비용','생산성','의료·복지'])
tot=sum(grp.values()); totlo=tot-SOC['2차 범죄']+SOC_LO['2차 범죄']
R=dict(N=N,rows=rows,grp=grp,old=OLD,base4=base4,tot=tot,pc=tot/N*1e4,pc_lo=totlo/N*1e4,pc4=base4/N*1e4,
 t10=tot*10,t28=tot*28.57,old_tot=sum(OLD.values()),old_t10_nonc=6075.4*10+496.0,
 cj_alt_검찰=12879.48927480*23022/1405185, ms_pc_cj=99796054, ms_pc_med=10139211, ms_pc_prd=730147319)
# 박성수(2018) 대비
ci=114.2*CPI/95.8; R['vs16']=dict(ratio=R['t10']/22389, o=N/14214, ci=ci)
json.dump(R,open('r.json','w'),ensure_ascii=False,indent=1)
print({k:round(v,1) for k,v in grp.items()}); print('base4',round(base4,1),'tot',round(tot,1),'pc',round(R['pc'],1),'pc_lo',round(R['pc_lo'],1))
print('λ10',round(R['t10'],1),'λ28.57',round(R['t28'],1),'ratio',round(R['vs16']['ratio'],2),'검찰 alt',round(R['cj_alt_검찰'],1))
