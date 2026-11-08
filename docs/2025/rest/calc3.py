import json
GBP=1.27*847.5/0.689*1.166        # £(2008) → 원(2025): 영국 CPI 2008→2020 × PPP 2020 × 한국 CPI 2020→2025
treated=875*1.0165; fam_ratio=140593/220043
fam=treated*fam_ratio*450*GBP
acc_unit=540595e8/1252433*(116.6/111.6)
drive=33*acc_unit
out=dict(GBP=GBP,treated=treated,fam_ratio=fam_ratio,fam_n=treated*fam_ratio,fam_unit=450*GBP,fam=fam,acc_unit=acc_unit,drive=drive,fear=0.0,
         soc=472.5e8, sc25=52223.7e8)
out['add']=fam+drive
json.dump(out,open('r3.json','w'),ensure_ascii=False,indent=1)
for k,v in out.items(): print(k, round(v/1e8,2) if v>1e6 else round(v,4))
