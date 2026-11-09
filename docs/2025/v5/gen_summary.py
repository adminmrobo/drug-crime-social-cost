import sys, json
from model import fx, GROUPS
CSS=open('/home/claude/summary_a4/summary_a4.html').read(); CSS=CSS[CSS.index('<style>')+7:CSS.index('</style>')]
CSS+=".tg{display:inline-block;font-size:7pt;font-weight:700;border-radius:3px;padding:0 4px;color:#fff;white-space:nowrap}.tg.s{background:var(--teal)}.tg.m{background:var(--navy)}.tg.e{background:var(--amber)}"
def ok(x,u='억'):
    x=round(x,1)
    if abs(x)>=10000: j=int(x//10000); r=x-j*10000; return f"{j}조 {r:,.1f}{u}" if r>=0.05 else f"{j}조"
    return f"{x:,.1f}{u}"
f1=lambda x:f"{x:,.1f}"
TAG=lambda t:{'실측':'<span class="tg s">실측</span>','실측+추정':'<span class="tg m">실측+추정</span>','추정':'<span class="tg e">추정</span>'}[t]
GC={'형사사법':'var(--navy)','고통비용':'var(--red)','생산성':'var(--amber)','의료·복지':'var(--teal)','사회적 혼란·기타':'var(--slate)'}
def build(y):
    d=fx(y); N=d['N']; L10=N*10; L28=N*28.57; ex=d['ex']; D=d['dec']; it={i['n']:i for i in d['items']}
    t10=d['t10']; share=lambda v:v/t10*100
    G={g:d['grp'][g] for g in GROUPS}
    pr={2024:dict(eN=6629,eT=62961,aN=3477,aT=61366,bud=16741.28,aTag=''),2025:dict(eN=7429,eT=64626,aN=3477/61366*63680,aT=63680,bud=16992.17,aTag=' (마약류 인원 추정)')}[y]
    pe=pr['bud']*pr['eN']/pr['eT']; pa=pr['bud']*pr['aN']/pr['aT']; dd=pe-pa
    cj_e=G['형사사법']-it['교도소']['v']+pe
    est=(y==2025)
    kick=f"중간보고 요약 · {y}년 기준" + (" · 2026. 11. 9. 시산(없는 자료는 추정)" if est else " · 2026. 11. 9. 확정(사회적 혼란·기타 반영)")
    seg=''.join(f'<div style="width:{share(v):.1f}%;background:{GC[g]}">{g+" " if share(v)>8 else ""}{share(v):.1f}%</div>' if share(v)>4 else f'<div style="width:{share(v):.1f}%;background:{GC[g]}"></div>' for g,v in list(((g,G[g]*10) for g in GROUPS))+[('사회적 혼란·기타',ex['합'])])
    det={'형사사법':('경찰','교도소'),'고통비용':('중독자 PGS','사망 PGS'),'생산성':('조기사망','노동력 상실·미취업'),'의료·복지':('직접 의료비','정신건강·복지')}
    lab={'경찰':'경찰','교도소':'교도소','중독자 PGS':'중독자','사망 PGS':'사망','조기사망':'조기사망','노동력 상실·미취업':'미취업','직접 의료비':'직접 의료','정신건강·복지':'정신건강·복지'}
    grow=''.join(f'<tr><td><b>{g}</b></td><td class="n">{ok(G[g])}</td><td class="n"><b>{ok(G[g]*10)}</b></td><td class="n">{f1(G[g]/N*1e4)}만</td><td>{lab[det[g][0]]} {ok(it[det[g][0]]["v"]*10)} · {lab[det[g][1]]} {ok(it[det[g][1]]["v"]*10)}</td></tr>' for g in GROUPS)
    grow+=f'<tr><td><b>사회적 혼란·기타</b></td><td class="n">{ok(ex["합"])}</td><td class="n"><b>{ok(ex["합"])}</b></td><td class="n">—</td><td>예방 예산 {ok(ex["예방"])} · 2차 범죄 {ok(ex["이차"])} (λ 미적용)</td></tr>'
    # institution formulas
    if y==2024:
        F=[('경찰','결산 12조 9,777.1억 × 13,501 ÷ 1,303,656명(검거)','실측'),('교도소','결산 1조 6,741.3억 × 3,477 ÷ 61,366명(1일 평균)','실측'),('검찰','결산 1조 2,162.6억 × 23,022 ÷ 1,405,185명(처리)','실측'),
           ('보호관찰소','결산 1,933.5억 × 2,089 ÷ 41,643명(접수)','실측'),('법원','형사소송 관련 예산 2,288.1억 × 13,926 ÷ 333,291명','실측'),('국립법무병원','결산 445.9억 × 17 ÷ 808명(12. 31.)','실측')]
    else:
        F=[('경찰','2024년 1,344.0억 × 1.037(결산 증가 가정) × 1.0165(단속 증가)','추정'),('교도소','결산 1조 6,992.2억(실측) × 3,608(추정) ÷ 63,680명(실측, 1일 평균)','실측+추정'),('검찰','결산 1조 2,879.5억(실측) × 23,403 ÷ 1,405,185명(2024 처리 인원 대용)','실측+추정'),
           ('보호관찰소','2024년 97.0억 × 1.037 × 1.0165','추정'),('법원','2024년 95.6억 × 1.037 × 1.0165','추정'),('국립법무병원','2024년 9.4억 × 1.037 × 1.0165','추정')]
    frows=''.join(f'<tr><td>{n}</td><td>{t}</td><td class="n">{ok(it[n]["v"])}</td><td class="n">{ok(it[n]["v"]*10)}</td>{"<td>"+TAG(tg)+"</td>" if est else ""}</tr>' for n,t,tg in F)
    # social disruption block
    soc=f'''<table>
    <tr><th>구분</th><th>산식</th><th class="n">금액</th><th>출처</th></tr>
    <tr><td>2차 범죄 피해 (상해·성폭력)</td><td>약물·정신병 상태 피의자(2021~24 연평균 상해 323명·성폭력 477명) × 마약 상태 25% × 범죄 1건당 사회적 비용(상해 2,207만·강간 2.17억·폭행 943만 원, 2008년) × 물가 {D['cpi']/81.5:.3f}</td><td class="n">{ok(ex['이차'])}</td><td>박경래 외(2010); 경찰청(2025)</td></tr>
    <tr><td>예방·홍보·재활 예산</td><td>식약처 마약 예산 377억 원(2024) − 이미 반영한 정신건강·복지 17억 원{" (2025 예산 미확인, 2024년 값)" if est else ""}</td><td class="n">{ok(ex['예방'])}</td><td>식약처(2023. 9.)</td></tr>
    <tr><td>가족·주변인 돌봄</td><td>치료 중독자 {(1649 if est else 875):,}명 × 동거 가족 0.64명 × 가족 의료비 £450(최저 구성 항목)</td><td class="n">{ok(ex['가족'])}</td><td>Copello et al.(2010)</td></tr>
    <tr><td>마약 운전 교통사고</td><td>{"2025년 33건(경찰청)" if est else "2024년 15.1건(추정: 약물운전 사고 70건 × 2025년 마약 비중 21.6%)"} × 교통사고 1건당 평균 비용</td><td class="n">{ok(ex['운전'])}</td><td>한국교통연구원(2025); 경찰청(2026)</td></tr>
    <tr><td>범죄 공포·방어 행동</td><td>범죄 1건당 단가의 고통·예방 비용에 포함</td><td class="n">0원</td><td>박경래 외(2010)</td></tr>
    <tr class="tot"><td>합계</td><td>암수율 미적용(사회 전체 총액)</td><td class="n">{ok(ex['합'])}</td><td></td></tr></table>
    <div class="note">마약 상태 살인(살인 1건당 173억 원, 2008년)은 묻지마 살인보다 낮게 본다는 판단으로 제외. 2차 범죄 피해 범위 {ok(ex['이차_lo'])}~{ok(ex['이차_hi'])}(마약 상태 비율 10~50%)</div>'''
    # appendix
    def apx(mult,lab):
        rows=''
        for g in GROUPS:
            rows+=f'<tr class="hl"><td>{g}</td><td>소계</td><td class="n">{f1(G[g])}</td><td class="n">{f1(G[g]/N*1e4)}</td><td class="n">{f1(G[g]*mult)}</td><td class="n">{G[g]*mult/(d["base"]*mult+ex["합"])*100:.1f}%</td>{"<td></td>" if est else ""}</tr>'
            for i in d['items']:
                if i['g']==g: rows+=f'<tr><td></td><td>{i["n"]}</td><td class="n">{f1(i["v"])}</td><td class="n">{f1(i["v"]/N*1e4)}</td><td class="n">{f1(i["v"]*mult)}</td><td class="n">{i["v"]*mult/(d["base"]*mult+ex["합"])*100:.1f}%</td>{"<td>"+TAG(i["tag"])+"</td>" if est else ""}</tr>'
        tot=d['base']*mult+ex['합']
        rows+=f'<tr class="hl"><td>사회적 혼란·기타</td><td>2차 범죄·예방 예산·가족 돌봄·운전 사고</td><td class="n">{f1(ex["합"])}</td><td class="n">—</td><td class="n">{f1(ex["합"])}</td><td class="n">{ex["합"]/tot*100:.1f}%</td>{"<td>"+TAG("추정")+"</td>" if est else ""}</tr>'
        rows+=f'<tr class="tot"><td>합계</td><td></td><td class="n">{f1(d["t1"])}</td><td class="n">{f1(d["pc"])}</td><td class="n">{f1(tot)}</td><td class="n">100%</td>{"<td></td>" if est else ""}</tr>'
        return f'<table class="t" style="font-size:7.9pt"><tr><th>부문</th><th>세부 항목</th><th class="n">암수율 미반영</th><th class="n">1명당 계수(만 원)</th><th class="n">{lab}</th><th class="n">비중</th>{"<th>구분</th>" if est else ""}</tr>{rows}</table>'
    sideextra=f'<div><span>4개 분야 (λ 10)</span><b>{ok(d["base"]*10)} 원</b></div><div><span>사회적 혼란·기타 (λ 미적용)</span><b>{ok(ex["합"])} 원</b></div>'
    estbox=''
    if est:
        estbox='''<div class="box" style="background:var(--amberBg);margin-top:7px;font-size:8.6pt;line-height:1.5">2025년 실적은 단속 인원(23,403명), 치료보호 인원(1,649명), 교정·검찰 결산, 교정 1일 평균 수용 인원(63,680명)을 확보하였다. 나머지는 2024년 확정치를 물가(1.021)·결산 증가 가정(1.037)·단속 증가(1.0165)로 추정하였다. 항목별 구분은 부록 표의 <span class="tg s">실측</span><span class="tg m">실측+추정</span><span class="tg e">추정</span> 표지로 표시한다.</div>'''
    miss=''
    if est:
        miss='''<h2>9. 미수령 자료와 현재 추정값</h2><table style="font-size:8.5pt"><tr><th>미수령 자료 (2025년)</th><th>요청처·출처</th><th>현재 추정</th></tr>
        <tr><td>경찰 결산, 전체·마약류 검거 인원</td><td>경찰청(경찰통계연보)</td><td>2024년 × 1.037 × 1.0165</td></tr>
        <tr><td>마약류 수용자 1일 평균 인원</td><td>교정본부</td><td>3,608명 = 63,680 × 5.67%(2024 비율)</td></tr>
        <tr><td>중독 사망자(20~64세)</td><td>통계청 사망원인통계</td><td>58명 × 1.0165</td></tr>
        <tr><td>검찰 전체 처리 인원</td><td>대검찰청(검찰연감)</td><td>2024년 1,405,185명 대용</td></tr>
        <tr><td>보호관찰·법원·국립법무병원 결산과 인원</td><td>범죄예방정책국·법원행정처·국립법무병원</td><td>2024년 × 1.037 × 1.0165</td></tr>
        <tr><td>심평원 진료비, 임금·고용</td><td>건강보험심사평가원·고용노동부</td><td>2024년 × 1.021 × 1.0165</td></tr>
        <tr><td>2025년 마약 예산, 마약 상태 범죄 건수</td><td>국무조정실 시행계획·대검찰청 범죄분석</td><td>2024년 예산 360억 원, 2021~24 경찰 평균</td></tr></table>'''
    html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>사회적 비용 요약본 {y}</title><style>{CSS}</style></head><body>
<section class="page">
  <div class="kicker">{kick}</div>
  <h1>마약류 사회적 비용 {ok(t10)} 원(암수율 10배)<br>4개 분야 2016년 대비 +{ok(D['inc'])} 원, 검거 인원 증가 기여 {D['a']/D['inc']*100:.1f}%</h1>
  <div class="hero">
    <div><div class="lab">{y}년 사회적 비용 · 암수율 λ 10 (기본)</div><div class="big">{ok(t10)} 원</div>
      <div style="font-size:8.8pt;color:#E6ECF4;margin-top:4px">4개 분야(의료·생산성·형사사법·고통) + 사회적 혼란·기타. 단속 {N:,}명 × 10 = 실질 사용자 {L10:,}명</div></div>
    <div class="side">{sideextra}<div><span>암수율 미반영</span><b>{ok(d['t1'])} 원</b></div><div><span>λ 28.57 (민감도)</span><b>{ok(d['t28'])} 원</b></div></div>
  </div>{estbox}
  <h2>1. 2016년(선행연구) 대비 {y}년 (4개 분야, 같은 범위)</h2>
  <table>
    <tr><th>구분</th><th class="n">2016 (박성수, 2018)</th><th class="n">{y} (본 연구)</th><th class="n">증감</th></tr>
    <tr><td>검거(단속) 인원</td><td class="n">14,214명</td><td class="n">{N:,}명</td><td class="n up">+{(N/14214-1)*100:.1f}%</td></tr>
    <tr class="hl"><td>사회적 비용 (λ 10, 4개 분야)</td><td class="n">2조 2,389억 원</td><td class="n">{ok(d['base']*10)} 원</td><td class="n up">{D['ratio']:.2f}배</td></tr>
    <tr><td>소비자물가지수 (2020=100)</td><td class="n">95.8</td><td class="n">{D['cpi']:.1f}{" (추정)" if est else ""}</td><td class="n">+{(D['ci']-1)*100:.1f}%</td></tr>
    <tr><td>사범 수·물가 반영 기대값</td><td class="n">{ok(D['exp'])} 원</td><td class="n">{ok(d['base']*10)} 원</td><td class="n up">{d['base']*10/D['exp']:.2f}배</td></tr>
    <tr><td>사용자 1명당 ({y}년 가격)</td><td class="n">{f1(D['pc16r'])}만 원</td><td class="n">{f1(d['pc'])}만 원</td><td class="n up">+{(d['pc']/D['pc16r']-1)*100:.1f}%</td></tr>
  </table>
  <div class="note">선행연구와 같은 4개 분야·암수율 10배 기준 비교. 사회적 혼란·기타 {ok(ex['합'])} 원은 선행연구 범위 밖이라 비교에서 제외</div>
  <h2>2. 증가분 +{ok(D['inc'])} 원의 기여 분해</h2>
  <div class="seg"><div style="width:{D['p']/D['inc']*100:.1f}%;background:#8A97AA">물가 {D['p']/D['inc']*100:.1f}%</div><div style="width:{D['a']/D['inc']*100:.1f}%;background:var(--amber)">검거 인원 증가 {D['a']/D['inc']*100:.1f}%</div><div style="width:{D['r']/D['inc']*100:.1f}%;background:var(--navy)">1명당 실질 {D['r']/D['inc']*100:.1f}%</div></div>
  <table>
    <tr><th>기여 요인</th><th class="n">금액</th><th class="n">비중</th><th>산식</th></tr>
    <tr><td>물가상승 기여분 (추계)</td><td class="n">{ok(D['p'])} 원</td><td class="n">{D['p']/D['inc']*100:.1f}%</td><td>2조 2,389억 × ({D['ci']:.3f} − 1)</td></tr>
    <tr><td>검거 인원 증가 기여분</td><td class="n">{ok(D['a'])} 원</td><td class="n">{D['a']/D['inc']*100:.1f}%</td><td>{ok(D['bp'])} × ({D['o']:.3f} − 1)</td></tr>
    <tr><td>1명당 실질 비용 증가</td><td class="n">{ok(D['r'])} 원</td><td class="n">{D['r']/D['inc']*100:.1f}%</td><td>{ok(d['base']*10)} − {ok(D['exp'])}</td></tr>
  </table>
  <h2>3. 부문별 비용 (λ 10)</h2>
  <div class="seg">{seg}</div>
  <table>
    <tr><th>부문</th><th class="n">암수율 미반영</th><th class="n">λ 10</th><th class="n">1명당</th><th>주요 세부 (λ 10)</th></tr>{grow}
    <tr class="tot"><td>합계</td><td class="n">{ok(d['t1'])}</td><td class="n">{ok(t10)}</td><td class="n">{f1(d['pc'])}만</td><td>세부 전체는 부록</td></tr>
  </table>
  <div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 중간보고 요약 ({y}년 기준)</span><span>1</span></div>
</section>
<section class="page">
  <div class="kicker">중간보고 요약 · 산정 기준</div>
  <h1>형사사법비용 산식과 사회적 혼란·기타</h1>
  <h2>4. 교도소 인원 기준: 연말 현원 → 연평균</h2>
  <table>
    <tr><th>구분</th><th class="n">연말 현원 기준</th><th class="n">연평균 기준{pr['aTag']}</th><th class="n">차이</th></tr>
    <tr><td>교도소 마약류 인원 ÷ 전체 수용</td><td class="n">{pr['eN']:,} ÷ {pr['eT']:,}명</td><td class="n">{pr['aN']:,.0f} ÷ {pr['aT']:,}명</td><td class="n"></td></tr>
    <tr><td>교도소 비용 (결산 {ok(pr['bud'])} × 비율)</td><td class="n">{ok(pe)}</td><td class="n">{ok(pa)}</td><td class="n">−{ok(dd)}</td></tr>
    <tr><td>형사사법 6개 기관 (암수율 미반영)</td><td class="n">{ok(cj_e)}</td><td class="n">{ok(G['형사사법'])}</td><td class="n">−{ok(dd)}</td></tr>
    <tr class="hl"><td>형사사법 (λ 10)</td><td class="n">{ok(cj_e*10)}</td><td class="n">{ok(G['형사사법']*10)}</td><td class="n">−{ok(dd*10)}</td></tr>
  </table>
  <div class="note">연간 비용에는 연평균(1일 평균) 인원을 쓰는 것이 원칙이다. 연평균 기준이면 λ 10에서 교도소 비용({ok(pa*10)})은 교정 결산의 {pa*10/pr['bud']*100:.1f}%이다(연말 기준 {pe*10/pr['bud']*100:.1f}%).</div>
  <h2>5. 형사사법 기관별 산식 ({y}년)</h2>
  <table style="font-size:8.8pt"><tr><th>기관</th><th>산식</th><th class="n">미반영</th><th class="n">λ 10</th>{"<th>구분</th>" if est else ""}</tr>{frows}</table>
  <h2>6. 사회적 혼란·기타 ({y}년, 암수율 미적용)</h2>
  {soc}
  <div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 중간보고 요약 ({y}년 기준)</span><span>2</span></div>
</section>
<section class="page">
  <div class="kicker">중간보고 요약 · 가정과 자료</div>
  <h1>산정 가정, 자료{", 미수령 자료" if est else ""}</h1>
  <h2>7. 산정 가정</h2>
  <div class="box" style="background:var(--navyBg);margin-top:2px"><ul>
    <li><b>암수율:</b> 4개 분야는 검거 사범 1명당 비용({f1(d['pc'])}만 원) × 실질 사용자 N*. 기본 λ 10(선행연구와 같음), 민감도 λ 28.57(박성수·백민석, 2019). 사회적 혼란·기타는 사회 전체 총액이라 곱하지 않는다</li>
    <li><b>의료비:</b> 심평원 중독 진료자와 검거 사범을 같은 대상으로 가정</li>
    <li><b>고통비용(PGS):</b> 사망 PGS 9.7억 원(한국교통연구원, 2025){" × 1.021" if est else ""}, 중독자는 중상 2.2억 원의 50%(1.1억 원){" × 1.021" if est else ""}, 치료보호 {"1,649명(2025 실측, 2024년 875명에서 증가: 2024. 7. 치료보호 건강보험 적용 등 제도 변화 영향)" if est else "875명"}</li>
    <li><b>조기사망:</b> 20~64세 중독 사망 58명{" × 1.0165" if est else ""}, 임금상승률 4%·할인율 4%(박성수, 2018 방식)</li>
    <li><b>사회적 혼란·기타:</b> 출처가 분명한 국내 범죄 단가와 예산, 해외 논문의 최저 구성 항목만 사용. 마약 상태 살인과 범죄 공포 지불의사액은 더하지 않음</li>
  </ul></div>
  <h2>8. 자료</h2>
  <div class="note" style="font-size:8.6pt;color:var(--ink);line-height:1.6">박성수_최종2024년(「마약류 범죄의 형사사법 비용」 &lt;표 18&gt;) · 송도훈_2024년_사회적비용 · 한국교통연구원(2025. 7. 28.; 2025. 8.) · 대검찰청(2026) 「2025 마약류 범죄백서」 · 통계청 사망원인통계, 소비자물가지수 · 법무부 교정통계연보 · 박성수(2018), 치안정책연구 32(3) · 박성수·백민석(2019) · 박경래 외(2010) 「범죄의 사회적 비용 추계」, 한국형사정책연구원 · Copello, Templeton &amp; Powell(2010), Drugs: Education, Prevention and Policy 17(sup1) · 경찰청 자료(2025. 10.; 2026. 8.) · 식품의약품안전처 예산(2023. 9.){" · 교정본부 회신(2026. 9.), 대검찰청 정보공개(2026. 10.)" if est else ""}</div>
  {miss}
  <div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 중간보고 요약 ({y}년 기준)</span><span>3</span></div>
</section>
<section class="page">
  <div class="kicker">부록</div>
  <h1>암수율별 항목 비용표 ({y}년, 단위: 억 원)</h1>
  <h2>부록 1. 암수율 10배 (기본)</h2>{apx(10,f'λ 10 ({L10:,}명)')}
  <h2>부록 2. 암수율 28.57배 (민감도)</h2>{apx(28.57,f'λ 28.57 ({round(L28):,}명)')}
  <div class="note">1명당 계수 = 4개 분야 항목 비용 ÷ 검거 사범 {N:,}명. 암수율 반영 금액 = 1명당 계수 × 실질 사용자. 사회적 혼란·기타는 암수율 미적용. 교도소는 연평균 인원 기준</div>
  <div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 중간보고 요약 ({y}년 기준)</span><span>4</span></div>
</section></body></html>'''
    fn=f'/home/claude/v5/summary_{y}.html'; open(fn,'w').write(html); return fn
if __name__=='__main__':
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page()
        for y in (2024,2025):
            fn=build(y); pg.goto('file://'+fn); pg.wait_for_timeout(400)
            print(y,pg.evaluate("[...document.querySelectorAll('.page')].map(s=>s.scrollHeight+'/'+s.clientHeight)"))
            pg.pdf(path=f'/home/claude/v5/요약본_마약류사회적비용_{y}_A4.pdf',format='A4',print_background=True)
        b.close()
