import json
d=json.load(open('r3.json'))
css=open('/home/claude/y2025/tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
css+="table.c td{padding:3px 6px}"
e=lambda x:f"{x/1e8:,.1f}"
tot_add=d['add']; soc=d['soc']; sc=d['sc25']
final=sc+soc+tot_add
foot=lambda n:f'<div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 별지 나머지 미산정 비용 최저 추계(2025년 기준)</span><span>{n}</span></div>'
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>나머지 미산정 비용</title><style>{css}</style></head><body>
<section class="page">
<div class="kicker">별지 · 2025년 기준 · 2026. 11. 8. 최저 수준 추계</div>
<h1>나머지 미산정 비용 최저 추계: {e(tot_add)}억 원<br>사회적 비용(λ 10) 전 항목 합계 5조 {final/1e8-50000:,.1f}억 원</h1>
<h2>1. 항목별 최저 추계 (2025년)</h2>
<table class="c"><tr><th>항목</th><th>산식 (최저 수준)</th><th class="n">금액</th><th>출처</th></tr>
<tr><td>가족·주변인 돌봄</td><td>치료 중독자 {d['treated']:,.0f}명 × 동거 가족 {d['fam_ratio']:.2f}명 × 가족 1명당 의료비 £450 (= {d['fam_unit']/1e4:,.1f}만 원)</td><td class="n"><b>{e(d['fam'])}억 원</b></td><td>Copello, Templeton &amp; Powell(2010)</td></tr>
<tr><td>마약류 투약 운전 교통사고</td><td>2025년 33건 × 교통사고 1건당 평균 사회적 비용 {d['acc_unit']/1e4:,.0f}만 원</td><td class="n"><b>{e(d['drive'])}억 원</b></td><td>한국교통연구원(2025), 경찰청(2026)</td></tr>
<tr><td>범죄 공포</td><td>추가 0원. 공포·불안에 대한 고통과 예방 비용은 사회적 혼란의 범죄 1건당 단가(박경래 외, 2010)에 들어 있음</td><td class="n"><b>0원</b></td><td>박경래 외(2010); Cohen et al.(2004)</td></tr>
<tr class="tot"><td>합계</td><td></td><td class="n">{e(tot_add)}억 원</td><td></td></tr></table>
<h2>2. 최저 수준으로 본 근거</h2>
<div class="box" style="background:var(--navyBg);margin-top:2px"><ul>
<li><b>가족 돌봄:</b> 원 연구의 가족 1명당 연간 비용은 £9,497(2008년 가격)이다. 일상 지출 £2,330, 약물 관련 부수 비용 £1,165, 가족이 입은 범죄 피해 £2,840, 고용 기회 상실 £2,712, 의료비 £450로 구성된다. 이 가운데 가장 작은 의료비 £450만 썼다. 가족 수는 치료 중인 사용자 1명당 동거 성인 가족 0.64명(140,593 ÷ 220,043명)을 썼다. 가족의 정신적 고통(불행감)은 원 연구도 합계에서 뺐고, 본 연구에서는 중독자 고통비용(한국교통연구원 원단위가 가족 고통 포함)에 들어 있다.</li>
<li><b>교통사고:</b> 경찰청 집계 2025년 마약류 투약 후 교통사고는 33건, 사망 2명, 부상 53명이다. 사상자별 원단위 대신 전체 교통사고 1건당 평균 비용(2023년 54조 595억 원 ÷ 125만 2,433건 = 4,316만 원, 2025년 물가 환산)을 써서 하한으로 두었다. 사망 2명에 사망 원단위를 적용하면 금액은 이보다 커진다. 약물운전 전체 사고(2025년 153건)에는 마약 외 의약품이 섞여 있어 쓰지 않았다.</li>
<li><b>범죄 공포:</b> 범죄 감소에 대한 가구 지불의사액 연구(Cohen et al., 2004)는 특정 범죄를 10% 줄이는 데 가구당 연 100~150달러를 낸다고 보고하였다. 이를 국내 가구 수에 적용하면 조 원 단위가 되어 최저 수준이라는 원칙에 맞지 않는다. 마약에 특정한 국내 지불의사액 연구는 확인되지 않는다. 따라서 이미 반영한 범죄 단가 안의 고통·예방 비용 외에는 더하지 않았다.</li>
</ul></div>
<h2>3. 사회적 비용 전 항목 합계 (2025년, 암수율 λ 10)</h2>
<table class="c"><tr><th>구성</th><th class="n">금액</th><th>비고</th></tr>
<tr><td>기존 4개 분야 (형사사법·고통·생산성·의료·복지)</td><td class="n">5조 2,223.7억 원</td><td>1명당 2,231.5만 원 × N* 234,030명</td></tr>
<tr><td>사회적 혼란 (2차 범죄 피해 + 예방·홍보·재활 예산)</td><td class="n">{e(soc)}억 원</td><td>λ 미적용, 살인 제외</td></tr>
<tr><td>나머지 미산정 비용 (가족 돌봄 + 마약 운전 사고 + 범죄 공포)</td><td class="n">{e(tot_add)}억 원</td><td>λ 미적용, 최저 수준</td></tr>
<tr class="tot"><td>합계</td><td class="n">5조 {final/1e8-50000:,.1f}억 원</td><td>추가분은 전체의 {(soc+tot_add)/final*100:.1f}%</td></tr></table>
<div class="note">환산: 영국 2008년 파운드 → 2020년(영국 소비자물가 1.27배, 근사) → 원화(2020년 구매력평가 1,230원/파운드) → 2025년(한국 소비자물가 1.166배) = 1파운드당 {d['GBP']:,.0f}원. 교통사고 1건당 비용은 한국 소비자물가 2023년 111.6 → 2025년 116.6으로 환산. 환산 계수는 연구진 확인 필요.</div>
<div class="note" style="margin-top:6px"><b>참고문헌</b><br>
Copello, A., Templeton, L., &amp; Powell, J.(2010). The impact of addiction on the family: Estimates of prevalence and costs. <i>Drugs: Education, Prevention and Policy</i>, 17(sup1), 63–74. (원자료: Copello, A., Templeton, L., &amp; Powell, J.(2009). <i>Adult family members and carers of dependent drug users: Prevalence, social cost, resource savings and treatment responses</i>. UK Drug Policy Commission.)<br>
Cohen, M. A., Rust, R. T., Steen, S., &amp; Tidd, S. T.(2004). Willingness-to-pay for crime control programs. <i>Criminology</i>, 42(1), 89–109.<br>
박경래 외(2010). 범죄 및 형사정책에 대한 법경제학적 접근: 범죄의 사회적 비용 추계. 한국형사정책연구원.<br>
한국교통연구원(2025). 2023년 도로교통사고비용(보도: 다음뉴스, 2025. 8. 17.). 경찰청 자료(정춘생 의원실, 서울신문 2026. 8. 17.).</div>
{foot(1)}</section></body></html>'''
open('r3.html','w').write(html)
