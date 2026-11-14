import json, math
R=json.load(open('r.json')); N=R['N']
rows={r[1]:r[2] for r in R['rows']}
pp=lambda k: rows[k]/N*1e8            # 원/명
CJ1=sum(pp(k) for k in ['경찰','검찰','법원','교도소','국립법무병원','보호관찰소'])
REC=pp('중독자 PGS')+pp('직접 의료비')+pp('간접의료비')+pp('정신건강·복지')+pp('이환·입원')+pp('2차 범죄')+pp('가족 돌봄')+pp('약물 운전')
DPGS=9.7e8*1.021
FLOOR=R['pc_lo']*1e4; CAP=16e8
# 생명표 2024(남녀 평균) Gompertz 적합: e40=44.65, e60=26.05
def life(a,b,x0):
    S=1.0;e=0.0;x=x0
    while x<110:
        q=1-math.exp(-a*math.exp(b*x)*(math.exp(b)-1)/b); S*=1-q; e+=S; x+=1
    return e+0.5
best=None
for bi in range(700,1300):
    b=bi/10000
    lo,hi=1e-7,1e-2
    for _ in range(60):
        m=(lo*hi)**.5
        if life(m,b,40)>44.65: lo=m
        else: hi=m
    d=abs(life(m,b,60)-26.05)
    if best is None or d<best[0]: best=(d,m,b)
_,GA,GB=best
qg=lambda x: 1-math.exp(-GA*math.exp(GB*x)*(math.exp(GB)-1)/GB)
def Y(x):
    if x<20 or x>64: return 0.0
    return {2:19439784,3:39685728,4:45121128,5:40092300,6:15321336}[min(x//10,6)]
AGE=[(17,674),(25,6913),(35,6986),(45,3925),(55,2428),(65,1990)]
SC={'A 조기회복':dict(med=5,L=0.125,rho=0.0,ea=0.0092*(1-1/6.83),er=0.001,re=0.05),
    'B 기준':   dict(med=9,L=0.311*0.5,rho=0.5,ea=0.0114*(1-1/6.83),er=0.002,re=0.10),
    'C 만성화': dict(med=27,L=0.311,rho=1.0,ea=0.0142*(1-1/6.83),er=0.003,re=0.15)}
g=0.017; pi=0.021
def earnPV(x,r):   # 사망 시점 x에서 잃는 잔여 근로소득(x+1~64)의 x시점 가치
    return sum(Y(k)*(1+g)**(k-x)/(1+r)**(k-x) for k in range(x+1,65))
def run(a0,s,r=0.045,nominal=False):
    p=SC[s]; h=math.log(2)/p['med']
    Aa,Ar=1.0,0.0; c={'1년차':FLOOR,'반복(고통·의료·혼란)':0,'재검거 형사사법':0,'노동능력 상실':0,'초과사망(PGS)':0,'초과사망(소득)':0}
    ya=0;yr=0;e_add=0.5
    for t in range(1,111-a0):
        x=a0+t
        if nominal: f=((1+g)*(1+pi))**t
        else: f=(1+g)**t/(1+r)**t
        dA=Aa*(qg(x)+p['ea']); dR=Ar*(qg(x)+p['er'])
        exA=Aa*p['ea']; exR=Ar*p['er']
        rem=Aa*(1-qg(x)-p['ea'])*h
        Aa,Ar=Aa-dA-rem, Ar-dR+rem
        e_add+=Aa+Ar
        c['반복(고통·의료·혼란)']+=Aa*REC*f
        c['재검거 형사사법']+=Aa*p['re']*CJ1*f
        c['노동능력 상실']+=(Aa+Ar*p['rho'])*p['L']*Y(x)*f
        ex=exA+exR
        c['초과사망(PGS)']+=ex*DPGS*f
        ep = sum(Y(k)*(1+g)**(k-x)*((1+pi)**(k-x) if nominal else 1/(1+r)**(k-x)) for k in range(x+1,65))
        c['초과사망(소득)']+=(exA*(1-p['L'])+exR*(1-p['L']*p['rho']))*ep*f
        ya+=Aa
    tot=sum(c.values())
    return dict(c=c,tot=tot,clip=min(max(tot,FLOOR),CAP),act=ya,e_add=e_add,e_gen=life(GA,GB,a0))
out={'param':dict(CJ1=CJ1,REC=REC,DPGS=DPGS,FLOOR=FLOOR,CAP=CAP,GA=GA,GB=GB,e40=life(GA,GB,40),e60=life(GA,GB,60),SC=SC,g=g,pi=pi),'age':{},'w':{}}
W=sum(n for _,n in AGE)
for s in SC:
    for key,kw in [('pv45',{}),('pv3',dict(r=0.03)),('pv4',dict(r=0.04)),('pv5',dict(r=0.05)),('nom',dict(nominal=True))]:
        res=[run(a,s,**kw) for a,_ in AGE]
        out['age'][s+'|'+key]=[[a,n,x['tot'],x['e_gen'],x['e_add'],x['act'],x['c']] for (a,n),x in zip(AGE,res)]
        comp={k:sum(n*x['c'][k] for (a,n),x in zip(AGE,res))/W for k in res[0]['c']}
        out['w'][s+'|'+key]=dict(tot=sum(n*x['tot'] for (a,n),x in zip(AGE,res))/W,comp=comp,
            e_gen=sum(n*x['e_gen'] for (a,n),x in zip(AGE,res))/W,e_add=sum(n*x['e_add'] for (a,n),x in zip(AGE,res))/W,
            act=sum(n*x['act'] for (a,n),x in zip(AGE,res))/W, mx=max(x['tot'] for x in res), mn=min(x['tot'] for x in res))
json.dump(out,open('life.json','w'),ensure_ascii=False,indent=1)
P=out['param'];print('CJ1',round(CJ1/1e4),'REC',round(REC/1e4),'FLOOR',round(FLOOR/1e4),'Gompertz',GA,GB,round(P['e40'],2),round(P['e60'],2))
for k,v in out['w'].items(): print(k, round(v['tot']/1e8,2), 'e',round(v['e_gen'],1),round(v['e_add'],1),'act',round(v['act'],1),{a:round(b/1e8,2) for a,b in v['comp'].items()})
for a in out['age']['B 기준|pv45']: print(a[0], round(a[2]/1e8,2), round(a[3],1), round(a[4],1))
for a in out['age']['C 만성화|nom']: print('Cnom',a[0], round(a[2]/1e8,2))
