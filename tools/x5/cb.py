import json, math
# 서식8
S8={2019:(1605,512,17,205,416),2020:(1602,515,21,212,425),2021:(1386,415,12,141,310),2022:(1384,413,13,143,350)}
n=sum(v[0] for v in S8.values()); r3=sum(v[1] for v in S8.values()); m6=sum(v[2] for v in S8.values()); y1=sum(v[3] for v in S8.values()); y2=sum(v[4] for v in S8.values())
# 서식9 전체 rows
S9={2019:{'이수':(652,194),'미이수':(13,5),'탈락':(8,3)},2020:{'이수':(524,174),'미이수':(34,10),'탈락':(6,1)},2021:{'이수':(411,141),'미이수':(18,7),'탈락':(1,1)},2022:{'이수':(539,163),'미이수':(36,13),'탈락':(0,0)}}
def s(k): return sum(S9[y][k][0] for y in S9), sum(S9[y][k][1] for y in S9)
n1,x1=s('이수'); nm,xm=s('미이수'); nd,xd=s('탈락'); n0,x0=nm+nd,xm+xd
p1=x1/n1; p0=x0/n0; d=p0-p1; se=math.sqrt(p1*(1-p1)/n1+p0*(1-p0)/n0)
# 미지정(교육 미지정) = 서식8 전체 − 서식9 (모수 정의 다를 수 있음)
nu=n-n1-n0; xu=r3-x1-x0
# 과정별 이수
C={'기본':[(520,154),(365,106),(299,88),(369,91)],'집중':[(107,33),(116,51),(74,36),(125,54)],'심화':[(25,7),(43,17),(38,17),(45,18)]}
cr={k:(sum(a for a,b in v),sum(b for a,b in v)) for k,v in C.items()}
# D: 3년 내 재복역 시점 분포, r=4.5%, 연중 중간
sh=[y1/r3,(y2-y1)/r3,(r3-y2)/r3]; D=sum(w/1.045**t for w,t in zip(sh,[0.5,1.5,2.5]))
# ΔC
prog=59.99e8+16.98e8; done25=1545; UC06=prog/done25
SCr=5035.7e4; SCx=SCr+(3223.6-1593.0)*1e4
def bc(sc): B=d*sc*D; return dict(B=B,BC=B/UC06,NPV=B-UC06,dstar=UC06/(sc*D))
R=dict(n=n,r3=r3,r0all=r3/n,m6=m6,y1=y1,y2=y2,byyear={y:v[1]/v[0] for y,v in S8.items()},
 n1=n1,x1=x1,p1=p1,n0=n0,x0=x0,p0=p0,nm=nm,xm=xm,nd=nd,xd=xd,d=d,rel=d/p0,ci=(d-1.96*se,d+1.96*se),z=d/se,nu=nu,xu=xu,pu=xu/nu,
 cr={k:(a,b,b/a) for k,(a,b) in cr.items()},sh=sh,D=D,prog=prog,done25=done25,UC06=UC06,SCr=SCr,SCx=SCx,lo=bc(SCr),hi=bc(SCx),
 s4={'2024':dict(개시=1436,이수=1374,탈락=62),'2025':dict(개시=1599,이수=1545,탈락=54),'2026_9':dict(개시=1358,이수=1293,탈락=65),
     '2025과정':{'기본':(1283,1237,46),'집중':(163,160,3),'심화':(44,40,4),'회복이음':(109,108,1)}},
 s3={'2024':dict(기결=3477,향정=3153,신입=2503,출소=1569,형기=(39,145,1488,1805)),'2025':dict(기결=4188,향정=3793,신입=2362,출소=1751,형기=(42,188,1599,2359))},
 mig={'2024':6629-3477,'2025':7429-4188},prison=dict(tot=1953.313,gi=1953.313*4188/7429,mi=1953.313*3241/7429))
json.dump(R,open('cb.json','w'),ensure_ascii=False,indent=1)
print(f"서식8 n={n} r3={r3} {r3/n:.3f} 6m {m6} 1y {y1} 2y {y2}")
print(f"이수 {x1}/{n1}={p1:.4f} 미이수+탈락 {x0}/{n0}={p0:.4f} diff {d*100:.2f}%p rel {d/p0*100:.1f}% CI {R['ci'][0]*100:.1f}~{R['ci'][1]*100:.1f} z {d/se:.2f}")
print(f"미지정 {xu}/{nu}={xu/nu:.4f}", {k:f"{a}/{b}={c:.3f}" for k,(a,b,c) in R['cr'].items()})
print('D',round(D,4),'sh',[round(x,3) for x in sh],'UC06',round(UC06/1e4,1))
for k in ('lo','hi'): print(k,{a:round(b/1e4,1) if a in('B','NPV') else round(b,3) for a,b in R[k].items()})
print(R['prison'],R['mig'])
# ---- 확정판: 미회신 항목 추계치 ----
UC10=9.79e8/1835          # 서식7 미회신: 마약류 중독 외래 1인당 연간 진료비(제3장 원고) 대용
UC12=14.4e8/1649/1.045    # 별도요청 미회신: 치료보호 지원 1인당 예산, 출소 1년차 할인
dC=UC06+UC10+UC12
def bc2(sc,dd): B=dd*sc*D; return dict(B=B,BC=B/dC,NPV=B-dC,dstar=dC/(sc*D))
lit=p0*0.192   # 김도균·나종민(2025) 상대 감소율 19.2%를 실측 r0에 적용
F=dict(UC10=UC10,UC12=UC12,dC=dC,lo=bc2(SCr,d),hi=bc2(SCx,d),lit_d=lit,litlo=bc2(SCr,lit),lithi=bc2(SCx,lit),
       ci_lo=bc2(SCx,max(R['ci'][1],0)))
R['F']=F; json.dump(R,open('cb.json','w'),ensure_ascii=False,indent=1)
print('UC10',round(UC10/1e4,1),'UC12',round(UC12/1e4,1),'dC',round(dC/1e4,1))
for k in ('lo','hi','litlo','lithi','ci_lo'): print(k,{a:round(b/1e4,1) if a in('B','NPV') else round(b,3) for a,b in F[k].items()})
print('lit d',round(lit*100,2))
