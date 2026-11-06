import json
c=2231.4954733585305; cj=1199.4
pi=0.021; g=0.017  # 물가(2025 실적, 향후 가정), 1명당 실질증가(2016→2025 연평균)
W={'가중 없음':[1,1,1,1],'가중 기본':[1.0,1.2,1.5,2.0],'가중 높음':[1.0,1.3,1.8,2.5]}
def w(t,k): return W[k][0] if t<=5 else W[k][1] if t<=10 else W[k][2] if t<=15 else W[k][3]
def path(T,k,gr=g,first_cj=False):
    for t in range(1,T+1):
        base=c if not first_cj else ((c) if t==1 else c-cj)
        yield t, base*(1+gr)**(t-1)*w(t,k)
def nom(T,k,**a): return sum(v*(1+pi)**t for t,v in path(T,k,**a))
def pv(T,k,r=0.045,**a): return sum(v/(1+r)**t for t,v in path(T,k,**a))
br=[('5년 이하',5),('5~10년',10),('10~15년',15),('15년 이상',30)]
sc={'A 조기회복':[50,30,15,5],'B 기준':[30,35,20,15],'C 만성화':[15,25,25,35]}
out={'br':{},'sc':{}}
for k in W:
    out['br'][k]=[[n,T,c*T,nom(T,k),pv(T,k,0.03),pv(T,k),pv(T,k,0.05),pv(T,k,first_cj=True)] for n,T in br]
    for s,ws in sc.items():
        out['sc'][s+'|'+k]=[sum(x/100*b[i] for x,b in zip(ws,out['br'][k])) for i in range(2,8)]
json.dump(out,open('life2.json','w'),ensure_ascii=False,indent=1)
for k in W:
    print(k); [print(' ',b[0],[round(x/1e4,2) for x in b[2:]]) for b in out['br'][k]]
for s,v in out['sc'].items(): print(s,[round(x/1e4,2) for x in v])
# 10억 조건: 30년, PV4.5 가중기본 → 필요 배수
for k in W: print('30y need mult',k, 1e5/pv(30,k))
# years to 10억 PV under 가중 기본
for k in W:
  T=1
  while pv(T,k)<1e5 and T<200: T+=1
  print('PV10억 years',k,T)
  T=1
  while nom(T,k)<1e5 and T<200: T+=1
  print('nom10억 years',k,T)
