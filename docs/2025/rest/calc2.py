import json
CPI=116.6/81.5   # 2008→2025 (2016=95.8 역산, 2025=114.2×1.021)
U08={'살인':17319246667,'강간':217208694,'상해':22066382,'폭행':9429124}   # 박경래 외(2010), 2008년 기준 1건당
U={k:v*CPI for k,v in U08.items()}
N={'살인':(969-708)/4,'상해':(40679-39387)/4,'성폭력':(23613-21704)/4}   # 경찰청 2021~24 연평균(약물·정신병 상태)
RAPE=0.20  # 성폭력 중 강간 비중 가정, 나머지 추행 → 폭행 단가
SH={'하한':0.10,'기준':0.25,'상한':0.50}
def soc(sh):
    a=N['상해']*sh*U['상해']; b=N['성폭력']*sh*(RAPE*U['강간']+(1-RAPE)*U['폭행'])
    return a,b
out={'CPI':CPI,'U':U,'N':N,'sc':{}}
for s,sh in SH.items():
    a,b=soc(sh); h=N['살인']*sh*U['살인']
    out['sc'][s]=dict(상해=a,성폭력=b,사회혼란=a+b,예방=( (377-17)*0.5e8 if s=='하한' else (377-17)*1e8 if s=='기준' else 585e8),
                      살인참고=h,가족참고={'하한':9.3e8,'기준':23.2e8,'상한':46.4e8}[s])
json.dump(out,open('rest2.json','w'),ensure_ascii=False,indent=1)
print('CPI',CPI,{k:round(v/1e8,3) for k,v in U.items()})
for s,v in out['sc'].items(): print(s,{k:round(x/1e8,1) for k,x in v.items()}, '합(사회혼란+예방)',round((v['사회혼란']+v['예방'])/1e8,1))
