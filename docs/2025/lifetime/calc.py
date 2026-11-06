import json
c=2231.4954733585305  # 만원/년, 2025
cj=1199.4  # 형사사법 1명당 (만원)
br=[('5년 이하',5),('5~10년',10),('10~15년',15),('15년 이상',30)]
sc={'A 조기회복':[50,30,15,5],'B 기준':[30,35,20,15],'C 만성화':[15,25,25,35]}
def af(r,T): return sum((1+r)**-t for t in range(1,T+1)) if r>0 else T
rates=[0.03,0.045,0.05]
out={'c':c,'br':[],'sc':{}}
for nm,T in br:
    out['br'].append([nm,T,c*T]+[c*af(r,T) for r in rates]+[cj/(1.045)+(c-cj)*af(0.045,T)])
for s,w in sc.items():
    v=[sum(wi/100*b[i] for wi,b in zip(w,out['br'])) for i in range(2,7)]
    meanT=sum(wi/100*T for wi,(_,T) in zip(w,br))
    out['sc'][s]=[w,meanT]+v
json.dump(out,open('life.json','w'),ensure_ascii=False,indent=1)
for b in out['br']: print(b[0],[round(x/1e4,3) for x in b[2:]])
for s,v in out['sc'].items(): print(s,v[0],v[1],[round(x/1e4,3) for x in v[2:]])
