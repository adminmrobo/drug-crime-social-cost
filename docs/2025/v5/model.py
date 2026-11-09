import json
V=json.load(open('/home/claude/y2025/vals.json')); EX={int(k):v for k,v in json.load(open('/home/claude/v5/extra.json')).items()}
GROUPS=['형사사법','고통비용','생산성','의료·복지']
def fx(y):
    it=[]
    for x in V['items']:
        v=(x[2] if y==2024 else x[3]); tg=('실측' if y==2024 else x[8].replace('추계','추정'))
        if y==2025 and x[1]=='중독자 PGS': v=1649*1.1*1.021; tg='실측+추정'
        it.append(dict(g=x[0],n=x[1],v=v,tag=tg))
    N=23022 if y==2024 else 23403
    base=sum(i['v'] for i in it)
    e=EX[y]; ex=dict(이차=e['이차범죄']/1e8,예방=e['예방']/1e8,가족=e['가족']/1e8,운전=e['운전']/1e8,운전건수=e['운전건수'],
                    이차_lo=e['이차범죄_범위'][0]/1e8,이차_hi=e['이차범죄_범위'][1]/1e8)
    ex['합']=ex['이차']+ex['예방']+ex['가족']+ex['운전']
    d=dict(y=y,N=N,items=it,base=base,ex=ex,pc=base/N*1e4)
    d['grp']={g:sum(i['v'] for i in it if i['g']==g) for g in GROUPS}
    d['t1']=base+ex['합']; d['t10']=base*10+ex['합']; d['t28']=base*28.57+ex['합']
    # decomposition vs 2016 (4개 분야)
    cpi={2024:114.2,2025:114.2*1.021}[y]; ci=cpi/95.8; o=N/14214; b=22389; fin=base*10
    d['dec']=dict(cpi=cpi,ci=ci,o=o,p=b*(ci-1),a=b*ci*(o-1),r=fin-b*ci*o,inc=fin-b,exp=b*ci*o,bp=b*ci,ratio=fin/b,pc16=b*1e8/142140/1e4,pc16r=b*1e8/142140/1e4*ci)
    return d
if __name__=='__main__':
    for y in (2024,2025):
        d=fx(y); print(y, round(d['base'],1), round(d['t1'],1), round(d['t10'],1), round(d['t28'],1), round(d['pc'],1), {k:round(v,1) for k,v in d['grp'].items()}, {k:round(v,2) for k,v in d['ex'].items()})
        print({k:round(v,3) for k,v in d['dec'].items()})
