import json
pi,g=0.021,0.017
CJ1=1199.4                    # 최초 검거 형사사법(교도소 기대 수용비 411.4 포함), 만원
REP=25.3+7.1+153.0+426.9      # 매년 반복분: 의료·복지 + 이환 + 미취업 + 중독자 PGS
q=58*23403/23022/23403        # 연 사망확률
DC=9.7e4*1.021+398.5e4/(58*23403/23022)  # 사망 1건 비용(사망PGS+조기사망), 만원
h=1-(1-0.363)**(1/3)          # 연 재복역 위험(2018 출소자 3년 36.3%)
CR=5036+605.4+43.1+43.7       # 재복역 1건 형사사법(장기수용 2.45년×85% 포함)
W={'가중 없음':[1,1,1,1],'가중 기본':[1,1.2,1.5,2.0],'가중 높음':[1,1.3,1.8,2.5]}
def w(t,k): v=W[k]; return v[0] if t<=5 else v[1] if t<=10 else v[2] if t<=15 else v[3]
def flows(T,k,recid=True):
    S=1.0
    for t in range(1,T+1):
        gr=(1+g)**(t-1)
        cj=CJ1 if t==1 else 0
        rep=REP*w(t,k)
        rc=(h*min(w(t,k),1/h*0.6)*CR) if recid else 0   # 재복역 확률 상한 60%
        dth=q*DC
        yield t,(cj+S*(rep+rc+dth))*gr, dict(cj=cj*gr,rep=S*rep*gr,rc=S*rc*gr,dth=S*dth*gr)
        S*=(1-q)
def agg(T,k,r=0.045,**a):
    nom=sum(v*(1+pi)**t for t,v,_ in flows(T,k,**a)); fix=None
    pv=lambda rr: sum(v/(1+rr)**t for t,v,_ in flows(T,k,**a))
    comp={}
    for t,v,c in flows(T,k,**a):
        for kk,x in c.items(): comp[kk]=comp.get(kk,0)+x/(1+r)**t
    return [nom,pv(0.03),pv(0.045),pv(0.05),comp]
br=[('5년 이하',5),('5~10년',10),('10~15년',15),('15년 이상',30)]
sc={'A 조기회복':[50,30,15,5],'B 기준':[30,35,20,15],'C 만성화':[15,25,25,35]}
out={'p':dict(REP=REP,q=q,DC=DC,h=h,CR=CR,CJ1=CJ1),'br':{},'sc':{},'norc':{}}
for k in W:
    out['br'][k]=[[n,T]+agg(T,k)[:4]+[agg(T,k)[4]] for n,T in br]
    out['norc'][k]=[agg(T,k,recid=False)[2] for n,T in br]
    for s,ws in sc.items():
        out['sc'][s+'|'+k]=[sum(x/100*b[i] for x,b in zip(ws,out['br'][k])) for i in range(2,6)]+[sum(x/100*v for x,v in zip(ws,out['norc'][k]))]
json.dump(out,open('life3.json','w'),ensure_ascii=False,indent=1)
print({k:round(v,4) for k,v in out['p'].items()})
for k in W:
    print(k)
    for b in out['br'][k]: print(' ',b[0],[round(x/1e4,2) for x in b[2:6]],{a:round(c/1e4,2) for a,c in b[6].items()})
for s,v in out['sc'].items(): print(s,[round(x/1e4,2) for x in v])
for k in W:
  for T in range(1,80):
    if agg(T,k)[2]>=1e5: print('PV10억',k,T);break
  for T in range(1,80):
    if agg(T,k)[0]>=1e5: print('nom10억',k,T);break
