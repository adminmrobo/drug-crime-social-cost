import json, math, os
os.chdir('/home/claude/y2025b')
src=open('life.py').read(); src=src[:src.index("out={'param'")]
G={}; exec(src,G)
SC,AGE,qg,Y,REC,CJ1,DPGS,FLOOR,g,pi=[G[k] for k in ['SC','AGE','qg','Y','REC','CJ1','DPGS','FLOOR','g','pi']]
def stream(a0,s,r=0.045,nominal=False):
    p=SC[s]; h=math.log(2)/p['med']; Aa,Ar=1.0,0.0; out=[]
    for t in range(1,111-a0):
        x=a0+t
        f=((1+g)*(1+pi))**t if nominal else (1+g)**t/(1+r)**t
        exA=Aa*p['ea']; exR=Ar*p['er']; rem=Aa*(1-qg(x)-p['ea'])*h
        Aa,Ar=Aa-Aa*(qg(x)+p['ea'])-rem, Ar-Ar*(qg(x)+p['er'])+rem
        ep=sum(Y(k)*(1+g)**(k-x)*((1+pi)**(k-x) if nominal else 1/(1+r)**(k-x)) for k in range(x+1,65))
        c=Aa*REC+Aa*p['re']*CJ1+(Aa+Ar*p['rho'])*p['L']*Y(x)+(exA+exR)*DPGS+(exA*(1-p['L'])+exR*(1-p['L']*p['rho']))*ep
        out.append(c*f)
    return out
W=sum(n for _,n in AGE)
def avg_stream(s,**kw):
    L=max(111-a for a,_ in AGE); acc=[0.0]*L
    for a,n in AGE:
        for i,v in enumerate(stream(a,s,**kw)): acc[i]+=v*n/W
    return acc
PERS={'3년 한정':lambda t: 1.0 if t<=3 else 0.0,'5년 반감':lambda t: 0.5**((t-1)/5),'평생 유지':lambda t: 1.0}
EFF={'관측(교정본부)':0.0287/0.3448,'국내 문헌':0.192,'국외 메타분석':0.20}
DC=6351000.0
res={}
for s in SC:
    for basis,kw in [('pv',{}),('nom',dict(nominal=True)),('pv3',dict(r=0.03)),('pv5',dict(r=0.05))]:
        st=avg_stream(s,**kw); fut=sum(st)
        for pn,w in PERS.items():
            base=sum(v*w(t) for t,v in enumerate(st,1))
            for en,e in EFF.items():
                B=e*base; res[f'{s}|{basis}|{pn}|{en}']=dict(B=B,BC=B/DC,NPV=B-DC)
            res[f'{s}|{basis}|{pn}|estar']=DC/base
        res[f'{s}|{basis}|future']=fut
json.dump(dict(res=res,EFF=EFF,DC=DC),open('/home/claude/cba/cba.json','w'),ensure_ascii=False,indent=1)
for basis in ['pv','nom']:
    print('== B 기준',basis,'미래비용',round(res[f'B 기준|{basis}|future']/1e8,2))
    for pn in PERS:
        print(pn,{en:round(res[f'B 기준|{basis}|{pn}|{en}']['BC'],2) for en in EFF},'e*',round(res[f'B 기준|{basis}|{pn}|estar']*100,1),'%', 'B(억)',{en:round(res[f'B 기준|{basis}|{pn}|{en}']['B']/1e8,2) for en in EFF})
for s in ['A 조기회복','C 만성화']:
    print(s,'pv 5년반감',{en:round(res[f'{s}|pv|5년 반감|{en}']['BC'],2) for en in EFF})
for b in ['pv3','pv5']: print(b,'B 5년반감',{en:round(res[f'B 기준|{b}|5년 반감|{en}']['BC'],2) for en in EFF})
