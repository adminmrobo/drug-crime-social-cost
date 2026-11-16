import json, math, sys
sys.path.insert(0,'/home/claude/y2025b')
L=json.load(open('/home/claude/y2025b/life.json')); P=L['param']
GA,GB=P['GA'],P['GB']; g=0.017; pi=0.021
qg=lambda x: 1-math.exp(-GA*math.exp(GB*x)*(math.exp(GB)-1)/GB)
W=1.217*1.017**9   # 2025→2016 임금 환산(물가 × 실질임금)
def Y(x):
    if x<20 or x>64: return 0.0
    return {2:19439784,3:39685728,4:45121128,5:40092300,6:15321336}[min(x//10,6)]/W
# 2016 연령분포(2016 백서 근사: 2025 분포 사용, 헐거운 가정)
AGE=[(17,674),(25,6913),(35,6986),(45,3925),(55,2428),(65,1990)]
U=dict(Y1=22389e8/142140, MED=8214000, PGSA=73627000, CJ=54515347, DPGS=280955000, DEARN=606230696)
def run(a0,p,U,r=0.045,nominal=False,share_pgs=1.0,med_share=1.0):
    h=math.log(2)/p['med']; Aa,Ar=1.0,0.0
    c=dict.fromkeys(['1년차','의료·복지','중독 고통(PGS)','재검거 형사사법','노동능력 상실','초과사망 고통(PGS)','초과사망 소득'],0.0); c['1년차']=U['Y1']
    for t in range(1,111-a0):
        x=a0+t; f=((1+g)*(1+pi))**t if nominal else (1+g)**t/(1+r)**t
        exA=Aa*p['ea']; exR=Ar*p['er']; rem=Aa*(1-qg(x)-p['ea'])*h
        Aa,Ar=Aa-Aa*(qg(x)+p['ea'])-rem, Ar-Ar*(qg(x)+p['er'])+rem
        c['의료·복지']+=Aa*U['MED']*med_share*f
        c['중독 고통(PGS)']+=Aa*U['PGSA']*share_pgs*f
        c['재검거 형사사법']+=Aa*p['re']*U['CJ']*f
        c['노동능력 상실']+=(Aa+Ar*p['rho'])*p['L']*Y(x)*f
        c['초과사망 고통(PGS)']+=(exA+exR)*U['DPGS']*f
        c['초과사망 소득']+=(exA*(1-p['L'])+exR*(1-p['L']*p['rho']))*U['DEARN']*f
    return c
SC=P['SC']
def wavg(s,**kw):
    tot=sum(n for _,n in AGE); comp={}
    for a,n in AGE:
        for k,v in run(a,SC[s],U,**kw).items(): comp[k]=comp.get(k,0)+v*n/tot
    return comp
import itertools
for ms,ps in [(0.3,0.08)]:
    for s in ['B 기준']:
        cn=wavg(s,nominal=True,share_pgs=ps,med_share=ms); cp=wavg(s,share_pgs=ps,med_share=ms)
        print(ms,ps,s,'nom',round(sum(cn.values())/1e8,2),'pv',round(sum(cp.values())/1e8,2),{k:round(v/1e8,2) for k,v in cn.items()})
MS,PS=0.3,0.08
OUT={'U':U,'MS':MS,'PS':PS,'W':W,'res':{},'age':{}}
for s in SC:
    for key,kw in [('pv3',dict(r=0.03)),('pv4',dict(r=0.04)),('pv45',{}),('pv5',dict(r=0.05)),('nom',dict(nominal=True))]:
        cmp=wavg(s,share_pgs=PS,med_share=MS,**kw); OUT['res'][s+'|'+key]=dict(tot=sum(cmp.values()),comp=cmp)
    OUT['age'][s]=[[a,n,sum(run(a,SC[s],U,share_pgs=PS,med_share=MS).values()),sum(run(a,SC[s],U,nominal=True,share_pgs=PS,med_share=MS).values())] for a,n in AGE]
OUT['life']={s:(L['w'][s+'|pv45']['e_gen'],L['w'][s+'|pv45']['e_add']) for s in SC}
json.dump(OUT,open('addon.json','w'),ensure_ascii=False,indent=1)
for k,v in OUT['res'].items(): print(k, round(v['tot']/1e8,2))
for a in OUT['age']['B 기준']: print(a[0],round(a[2]/1e8,2),round(a[3]/1e8,2))
print('Y1',U['Y1']/1e4)
