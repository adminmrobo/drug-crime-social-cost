import json
# 2025 1명당(만원) 항목
it={'경찰':605.4,'검찰':91.7,'법원':43.1,'교도소':411.4,'법무병원':4.2,'보호관찰':43.7,'중독자PGS':426.9,'사망PGS':249.5,'조기사망':170.3,'미취업':153.0,'이환':7.1,'직접':12.8,'정신':7.5,'간접':4.9}
EV=sum(it[k] for k in ['경찰','검찰','법원','보호관찰','법무병원'])      # 사건 비용(검거 1회)
REP=sum(it[k] for k in ['중독자PGS','미취업','이환','직접','정신','간접'])  # 매년 반복(건강·생산성·고통)
DTH=it['사망PGS']+it['조기사망']                                            # 연간 기대 사망비용(사망확률×비용)
UC01=2378.4; SERVE=2.448*0.85; PRI=SERVE*UC01                                # 실형 1회 수용비
p1=it['교도소']/PRI                                                         # 첫 검거 실형 확률(연간 교도소비와 정합)
P=dict(h=0.10,p2=0.30,g=0.017,pi=0.021)
W={'가중 없음':[1,1,1,1],'가중 기본':[1.0,1.2,1.5,2.0],'가중 높음':[1.0,1.3,1.8,2.5]}
def w(t,k): return W[k][0] if t<=5 else W[k][1] if t<=10 else W[k][2] if t<=15 else W[k][3]
def flows(T,k,h=None,p2=None):
    h=P['h'] if h is None else h; p2=P['p2'] if p2 is None else p2
    f={}  # year -> dict of components (2025 real, before growth)
    def add(t,c,v): f.setdefault(t,{}).setdefault(c,0); f[t][c]+=v
    for t in range(1,T+1):
        add(t,'건강·생산성',REP*w(t,k)); add(t,'사망',DTH*w(t,k))
        arr = 1.0 if t==1 else h*w(t,k); pp = p1 if t==1 else p2
        add(t,'사건',arr*EV)
        yrs=SERVE; s=t
        while yrs>0:
            frac=min(1,yrs); add(s,'수용',arr*pp*UC01*frac); yrs-=frac; s+=1
    return f
def agg(T,k,**a):
    f=flows(T,k,**a); g,pi=P['g'],P['pi']
    comp={}; nom=0; pv={0.03:0,0.045:0,0.05:0}; fixed=0
    for t,d in f.items():
        for c,v in d.items():
            real=v*(1+g)**(t-1); fixed+=v; nom+=real*(1+pi)**t
            for r in pv: pv[r]+=real/(1+r)**t
            comp[c]=comp.get(c,0)+real/(1.045)**t
    return dict(fixed=fixed,nom=nom,pv3=pv[0.03],pv45=pv[0.045],pv5=pv[0.05],comp=comp)
br=[('5년 이하',5),('5~10년',10),('10~15년',15),('15년 이상',30)]
sc={'A 조기회복':[50,30,15,5],'B 기준':[30,35,20,15],'C 만성화':[15,25,25,35]}
out={'param':dict(EV=EV,REP=REP,DTH=DTH,UC01=UC01,SERVE=SERVE,PRI=PRI,p1=p1,**P),'br':{},'sc':{},'sens':{}}
keys=['fixed','nom','pv3','pv45','pv5']
for k in W:
    out['br'][k]=[[n,T]+[agg(T,k)[x] for x in keys]+[agg(T,k)['comp']] for n,T in br]
    for s,ws in sc.items():
        v=[sum(x/100*b[2+i] for x,b in zip(ws,out['br'][k])) for i in range(5)]
        comp={}
        for x,b in zip(ws,out['br'][k]):
            for c,vv in b[7].items(): comp[c]=comp.get(c,0)+x/100*vv
        out['sc'][s+'|'+k]=v+[comp]
# 민감도: B 기준, 가중 기본
def scen(s,k,**a):
    return sum(x/100*agg(T,k,**a)['pv45'] for x,(_,T) in zip(sc[s],br)), sum(x/100*agg(T,k,**a)['nom'] for x,(_,T) in zip(sc[s],br))
for lab,a in [('재범 위험 5%',dict(h=0.05)),('재범 위험 15%',dict(h=0.15)),('재범 시 실형 20%',dict(p2=0.20)),('재범 시 실형 50%',dict(p2=0.50))]:
    out['sens'][lab]=scen('B 기준','가중 기본',**a)
for lab,gg in [('실질 증가 0%',0.0),('실질 증가 1%',0.01)]:
    P['g']=gg; out['sens'][lab]=scen('B 기준','가중 기본'); P['g']=0.017
json.dump(out,open('life3.json','w'),ensure_ascii=False,indent=1)
print('EV',EV,'REP',REP,'DTH',DTH,'PRI',PRI,'p1',p1)
for k in W:
    print(k)
    for b in out['br'][k]: print(' ',b[0],[round(x/1e4,2) for x in b[2:7]],{c:round(v/1e4,2) for c,v in b[7].items()})
for s,v in out['sc'].items(): print(s,[round(x/1e4,2) for x in v[:5]])
for s,v in out['sens'].items(): print(s,[round(x/1e4,2) for x in v])
# 수형자(실형 선고자) 경로: 첫 검거 실형 확정, 재범 시 실형 50%
import copy
p1_save=p1
p1=1.0
out['inmate']={}
for k in W:
    out['inmate'][k]=[[n,T]+[agg(T,k,p2=0.5)[x] for x in keys]+[agg(T,k,p2=0.5)['comp']] for n,T in br]
    for s,ws in sc.items():
        v=[sum(x/100*b[2+i] for x,b in zip(ws,out['inmate'][k])) for i in range(5)]
        comp={}
        for x,b in zip(ws,out['inmate'][k]):
            for c,vv in b[7].items(): comp[c]=comp.get(c,0)+x/100*vv
        out['inmate'][s+'|'+k]=v+[comp]
p1=p1_save
json.dump(out,open('life3.json','w'),ensure_ascii=False,indent=1)
print('--inmate')
for b in out['inmate']['가중 기본']: print(b[0],[round(x/1e4,2) for x in b[2:7]],{c:round(v/1e4,2) for c,v in b[7].items()})
for s in sc:
  for k in W: print(s,k,[round(x/1e4,2) for x in out['inmate'][s+'|'+k][:5]])
