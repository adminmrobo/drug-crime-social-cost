import json
C=2231.4954733585305; CJ=1199.4; NC=C-CJ  # 만원
pi=0.021
p0=1-(1-0.363)**(1/3)   # 3년 내 재복역 36.3% → 연간
W={'가중 없음':[1,1,1,1],'가중 기본':[1.0,1.2,1.5,2.0],'가중 높음':[1.0,1.3,1.8,2.5]}
def w(t,k): v=W[k]; return v[0] if t<=5 else v[1] if t<=10 else v[2] if t<=15 else v[3]
def flows(T,k,g=0.017,p=p0,mode='구조'):
    for t in range(1,T+1):
        gr=(1+g)**(t-1)
        if mode=='구조':
            cj=CJ if t==1 else CJ*min(1,p*w(t,k))
            yield t,(NC*w(t,k)+cj)*gr
        else: yield t,C*w(t,k)*gr
def nom(T,k,**a): return sum(v*(1+pi)**t for t,v in flows(T,k,**a))
def pv(T,k,r=0.045,**a): return sum(v/(1+r)**t for t,v in flows(T,k,**a))
up=[5,10,15,30]; mid=[3,7.5,12.5,22.5]
sc={'A 조기회복':[50,30,15,5],'B 기준':[30,35,20,15],'C 만성화':[15,25,25,35]}
def mix(f,ws,Ts):
    tot=0
    for x,T in zip(ws,Ts):
        if T==int(T): tot+=x/100*f(int(T))
        else: tot+=x/100*(f(int(T))+f(int(T)+1))/2
    return tot
out={'p0':p0,'br':{},'sc':{},'sens':{}}
for k in W:
    out['br'][k]=[[T, C*T, nom(T,k), pv(T,k,0.03), pv(T,k), pv(T,k,0.05), pv(T,k,mode='반복')] for T in up]
    for s,ws in sc.items():
        out['sc'][s+'|'+k]=[mix(lambda T:C*T,ws,up), mix(lambda T:nom(T,k),ws,up), mix(lambda T:pv(T,k,0.03),ws,up), mix(lambda T:pv(T,k),ws,up), mix(lambda T:pv(T,k,0.05),ws,up), mix(lambda T:pv(T,k,mode='반복'),ws,up)]
B=sc['B 기준']; k='가중 기본'
S={}
S['기준(구조, g 1.7%, p 14.0%, 상한값)']=(mix(lambda T:nom(T,k),B,up),mix(lambda T:pv(T,k),B,up))
for g in (0,0.01): S[f'실질 증가 g {g*100:.0f}%']=(mix(lambda T:nom(T,k,g=g),B,up),mix(lambda T:pv(T,k,g=g),B,up))
S['재범 확률 p 25%']=(mix(lambda T:nom(T,k,p=0.25),B,up),mix(lambda T:pv(T,k,p=0.25),B,up))
S['구간 중간값(3·7.5·12.5·22.5년)']=(mix(lambda T:nom(T,k),B,mid),mix(lambda T:pv(T,k),B,mid))
S['연간 비용 매년 반복(직전 별지)']=(mix(lambda T:nom(T,k,mode='반복'),B,up),mix(lambda T:pv(T,k,mode='반복'),B,up))
out['sens']=S
# 10억 도달 연수 (구조)
yrs={}
for kk in W:
    T=1
    while nom(T,kk)<1e5 and T<150: T+=1
    T2=1
    while pv(T2,kk)<1e5 and T2<150: T2+=1
    yrs[kk]=(T,T2)
out['yrs']=yrs
json.dump(out,open('life3.json','w'),ensure_ascii=False,indent=1)
print('p0',p0)
for kk in W: print(kk,[[round(x/1e4,2) for x in b[1:]] for b in out['br'][kk]])
for s,v in out['sc'].items(): print(s,[round(x/1e4,2) for x in v])
for s,v in S.items(): print(s,[round(x/1e4,2) for x in v])
print(yrs)
