import json
U08={'강간':217208694,'상해':22066382,'폭행':9429124}
N={'상해':(40679-39387)/4,'성폭력':(23613-21704)/4}
CPI={2024:114.2,2025:114.2*1.021}; C08=81.5
GBP25=1.27*847.5/0.689*1.166
def calc(y,sh=0.25):
    k=CPI[y]/C08
    sang=N['상해']*sh*U08['상해']*k
    sex=N['성폭력']*sh*(0.2*U08['강간']+0.8*U08['폭행'])*k
    prev=360e8
    treated=(875 if y==2024 else 1649)
    fam=treated*(140593/220043)*450*GBP25*(CPI[y]/CPI[2025])
    acc=540595e8/1252433*(CPI[y]/111.6)
    ncase={2024:70*33/153,2025:33}[y]
    drive=ncase*acc
    return dict(상해=sang,성폭력=sex,이차범죄=sang+sex,예방=prev,사회혼란=sang+sex+prev,가족=fam,운전=drive,운전건수=ncase,기타=fam+drive,합=sang+sex+prev+fam+drive,
                하한=None)
out={}
for y in (2024,2025):
    b=calc(y); lo=calc(y,0.10); hi=calc(y,0.50)
    b['이차범죄_범위']=[lo['이차범죄'],hi['이차범죄']]
    out[y]=b
json.dump(out,open('extra.json','w'),ensure_ascii=False,indent=1)
for y,v in out.items(): print(y,{k:(round(x/1e8,1) if isinstance(x,float) and x>1e6 else x) for k,x in v.items()})
