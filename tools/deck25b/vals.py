import json
R=json.load(open('/home/claude/y2025b/r.json')); L=json.load(open('/home/claude/y2025b/life.json'))
N=R['N']; it={r[1]:r[2] for r in R['rows']}; g=R['grp']
def jo(x):
    s='-' if x<0 else ''; x=abs(x)
    return s+(f"{int(x//10000)}조 {x%10000:,.1f}억" if x>=10000 else f"{x:,.1f}억")
f1=lambda x:f"{x:,.1f}"
pc=lambda x:x/N*1e4
V={}
for k,v in it.items(): V['i_'+k]=f1(v); V['p_'+k]=f1(pc(v)); V['l_'+k]=f1(v*10); V['m_'+k]=f1(v*28.57)
for k,v in g.items(): V['g_'+k]=f1(v); V['gp_'+k]=f1(pc(v)); V['gl_'+k]=jo(v*10); V['gl_n_'+k]=f1(v*10); V['gm_n_'+k]=f1(v*28.57); V['sh_'+k]=f"{v/R['tot']*100:.1f}%"
V.update(tot=f1(R['tot']),pc=f1(R['pc']),t10=jo(R['t10']),t28=jo(R['t28']),t10n=f1(R['t10']),t28n=f1(R['t28']),ratio=f"{R['t10']/22389:.2f}")
b4=R['base4']; V.update(b4=f1(b4),b4pc=f1(pc(b4)),b4l=jo(b4*10),b4ln=f1(b4*10),b4m=f1(b4*28.57),b4ratio=f"{b4*10/22389:.2f}")
inc=b4*10-22389; cpi=27249.7; arr=44865.9
V.update(inc=jo(inc),d_cpi='4,860.7',d_arr='1조 7,616.2',d_real=jo(b4*10-arr),s_cpi=f"{4860.7/inc*100:.1f}",s_arr=f"{17616.2/inc*100:.1f}",s_real=f"{(b4*10-arr)/inc*100:.1f}",vsexp=f"{b4*10/arr:.2f}",pcinc=f"{(pc(b4)/1917.1-1)*100:.1f}")
# PGS 시나리오
P=g['고통비용']; base4_noP=b4-P
for key,fac in [('s16',0.35+0.65*(1-0.279)/(1-0.361)),('s24',1.0),('s25',0.35+0.65*(1-0.366)/(1-0.361)),('own',0.35),('zero',0)]:
    p=P*fac; t=base4_noP+p
    V['pg_'+key]=[f1(p),f1(t),f1(t*10),f1(t*28.57),f1(pc(t))+'만 원']
V['pg_lo']=jo((base4_noP+P*(0.35+0.65*(1-0.366)/(1-0.361)))*10); V['pg_hi']=jo((base4_noP+P*(0.35+0.65*(1-0.279)/(1-0.361)))*10)
V['pg_d16']=f1(P*(0.35+0.65*(1-0.279)/(1-0.361))-P); V['pg_d16l']=f1((P*(0.35+0.65*(1-0.279)/(1-0.361))-P)*10); V['pg_d25']=f1(P-P*(0.35+0.65*(1-0.366)/(1-0.361)))
# share range of PGS across scenarios (λ10 total incl soc)
def shr(fac): p=P*fac; return p/(R['tot']-P+p)*100
V['pg_shr']=f"{shr(0.35+0.65*(1-0.366)/(1-0.361)):.1f}~{shr(0.35+0.65*(1-0.279)/(1-0.361)):.1f}%"
# 교도소 대안(연평균 추정)
alt=16992.17*3608/63680
V.update(pr_alt=f1(alt),pr_diff=f1(alt-it['교도소']),pr_diffl=jo((alt-it['교도소'])*10),cj_alt=f1(g['형사사법']-it['교도소']+alt),cj_altl=jo((g['형사사법']-it['교도소']+alt)*10),tot_altl=jo((R['tot']-it['교도소']+alt)*10),pr_share=f"{it['교도소']*10/16992.17*100:.1f}%",pr_share_alt=f"{alt*10/16992.17*100:.1f}%")
# 생애
w=L['w']
for s,k in [('A 조기회복','A'),('B 기준','B'),('C 만성화','C')]:
    for m in ['pv3','pv4','pv45','pv5','nom']: V[f'lf_{k}_{m}']=f"{w[s+'|'+m]['tot']/1e8:.2f}"
    V[f'le_{k}']=[f"{w[s+'|pv45']['e_gen']:.1f}",f"{w[s+'|pv45']['e_add']:.1f}",f"{w[s+'|pv45']['e_gen']-w[s+'|pv45']['e_add']:.1f}",f"{w[s+'|pv45']['act']:.1f}"]
    V[f'lc_{k}']={c:f"{v/1e8:.2f}" for c,v in w[s+'|pv45']['comp'].items()}
V['lc_Bnom']={c:f"{v/1e8:.2f}" for c,v in w['B 기준|nom']['comp'].items()}
V['floor']=f"{L['param']['FLOOR']/1e4:,.1f}"; V['floor_e']=f"{L['param']['FLOOR']/1e8:.2f}"
V['age']=[[a[0],f"{a[1]:,}",f"{a[2]/1e8:.2f}",f"{b[2]/1e8:.2f}",f"{a[3]:.1f}",f"{a[4]:.1f}"] for a,b in zip(L['age']['B 기준|pv45'],L['age']['B 기준|nom'])]
V['Bx']=f"{w['B 기준|pv45']['tot']/L['param']['FLOOR']:.1f}"
V['cohort']=f"{23403*w['B 기준|pv45']['tot']/1e12:,.1f}"; V['cohortl']=f"{234030*w['B 기준|pv45']['tot']/1e12:,.1f}"
json.dump(V,open('vals.json','w'),ensure_ascii=False,indent=0)
for k in ['t10','t28','pc','ratio','b4','b4pc','b4l','b4ratio','inc','d_real','s_cpi','s_arr','s_real','vsexp','pcinc','pg_lo','pg_hi','pg_shr','pr_alt','pr_diff','pr_diffl','cj_altl','tot_altl','pr_share','pr_share_alt','Bx']: print(k,V[k])
print({k:V['sh_'+k] for k in g}, {k:V['gl_'+k] for k in g}, {k:V['gp_'+k] for k in g})
for k in ['s16','s24','s25','own','zero']: print(k,V['pg_'+k])
