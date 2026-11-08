import json
K=847.5/0.689*1.166   # 원/£ (PPP 2020 × 한국 CPI 2020→2025)
# Heeks 2019/20 단가 (£): anticipation(방어·보험), harm(신체·정서), other consequence(생산·의료·피해자지원·재산), response(경찰·사법)
H={'살인':dict(ant=68700,harm=2247260,oth=383630+1230+5070,resp=11710+629070),
   '상해(폭력 상해)':dict(ant=280+10,harm=9060,oth=3240+1060+20,resp=1100+940),
   '성폭력':dict(ant=130,harm=4210,oth=990+400+10,resp=670+140)}
KOTI_D=9.7e8*1.021
# 2021~24 경찰 검거: (주취·약물·정신병) − 음주 = 약물·정신병 상태, 연평균
N={'살인':(969-708)/4,'상해(폭력 상해)':(40679-39387)/4,'성폭력':(23613-21704)/4}
SH={'하한':0.10,'기준':0.25,'상한':0.50}
out={'K':K,'rows':[],'tot':{}}
for c in H:
    for s,sh in SH.items():
        n=N[c]*sh
        out['tot'].setdefault(s,{'4-1':0,'4-2a':0,'5-2b':0})
        out['tot'][s]['4-1']+=n*(H[c]['oth']+H[c]['resp'])*K
        out['tot'][s]['4-2a']+=n*(KOTI_D if c=='살인' else H[c]['harm']*K)
        out['tot'][s]['5-2b']+=n*H[c]['ant']*K
    hm=(KOTI_D if c=='살인' else H[c]['harm']*K)/1e8; o=(H[c]['oth']+H[c]['resp'])*K/1e8; a=H[c]['ant']*K/1e8
    out['rows'].append([c,N[c],N[c]*0.25,o+hm+a,o,hm,a])
# 4-3 가족 돌봄: 치료 중독자 875×1.0165(2025) × 주 h시간 × 52 × 최저임금 10,030
fam={k:875*1.0165*h*52*10030 for k,h in {'하한':2,'기준':5,'상한':10}.items()}
# 5-1 예방·홍보·재활(식약처 마약 예산 2024 377억; 2025 미확인) − 의료·복지 기존 반영 정신건강·복지 17억 중복 제거
pre={'하한':(377-17)*0.5e8,'기준':(377-17)*1e8,'상한':602e8-17e8}
# 5-2a 범죄 공포 WTP 참고: 성인 4,400만 × 연 1,000/3,000/5,000원
wtp={k:44e6*v for k,v in {'하한':1000,'기준':3000,'상한':5000}.items()}
for s in SH:
    out['tot'][s]['4-3']=fam[s]; out['tot'][s]['5-1']=pre[s]; out['tot'][s]['5-2a(참고)']=wtp[s]
json.dump(out,open('rest.json','w'),ensure_ascii=False,indent=1)
print('K',K)
for r in out['rows']: print(r[0],round(r[1],1),round(r[2],1),[round(x,2) for x in r[3:]])
for s,v in out['tot'].items():
    base=sum(x for k,x in v.items() if '참고' not in k)
    print(s,{k:round(x/1e8,1) for k,x in v.items()},'합(참고 제외)',round(base/1e8,1),'λ10 대비%',round(base/1e8/52223.7*100,2))
