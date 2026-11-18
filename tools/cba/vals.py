import json
d=json.load(open('/home/claude/cba/cba.json')); r=d['res']; E=d['EFF']; DC=d['DC']
EN=list(E); PN=['3년 한정','5년 반감','평생 유지']
V={}
for pn in PN:
    for i,en in enumerate(EN):
        for b in ['pv','nom']:
            x=r[f'B 기준|{b}|{pn}|{en}']; V[f'bc|{pn}|{i}|{b}']=f"{x['BC']:.2f}"; V[f'b|{pn}|{i}|{b}']=x['B']; V[f'npv|{pn}|{i}|{b}']=x['NPV']
    for b in ['pv','nom']: V[f'es|{pn}|{b}']=f"{r[f'B 기준|{b}|{pn}|estar']*100:.1f}%"
V['eff']=[f"{E[e]*100:.1f}%" for e in EN]
V['A']=f"{r['A 조기회복|pv|5년 반감|관측(교정본부)']['BC']:.2f}"; V['C']=f"{r['C 만성화|pv|5년 반감|관측(교정본부)']['BC']:.2f}"
V['A2']=f"{r['A 조기회복|pv|5년 반감|국외 메타분석']['BC']:.2f}"; V['C2']=f"{r['C 만성화|pv|5년 반감|국외 메타분석']['BC']:.2f}"
V['r3']=f"{r['B 기준|pv3|5년 반감|관측(교정본부)']['BC']:.2f}"; V['r5']=f"{r['B 기준|pv5|5년 반감|관측(교정본부)']['BC']:.2f}"
V['fut_pv']=r['B 기준|pv|future']; V['fut_nom']=r['B 기준|nom|future']
V['npvpp_obs']=r['B 기준|pv|5년 반감|관측(교정본부)']['NPV']; V['npvpp_lit']=r['B 기준|pv|5년 반감|국외 메타분석']['NPV']; V['npvpp_kr']=r['B 기준|pv|5년 반감|국내 문헌']['NPV']
V['B_obs']=r['B 기준|pv|5년 반감|관측(교정본부)']['B']
json.dump(V,open('/home/claude/cba/v.json','w'),ensure_ascii=False,indent=1)
print(V['bc|5년 반감|0|pv'],V['bc|5년 반감|2|pv'],V['es|5년 반감|pv'],V['A'],V['C'],V['r3'],V['r5'],round(V['npvpp_obs']*1545/1e8,1),round(V['npvpp_lit']*1545/1e8,1),round(V['npvpp_obs']*4188/1e8,1),round(V['npvpp_lit']*4188/1e8,1))
