import json
d=json.load(open('rest2.json')); S=d['sc']; U=d['U']; N=d['N']
css=open('/home/claude/y2025/tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
css+="table.c td{padding:2.5px 6px}.tg{display:inline-block;font-size:7.3pt;font-weight:700;border-radius:3px;padding:0 4px;color:#fff}.tg.b{background:var(--teal)}.tg.c{background:var(--amber)}.tg.r{background:var(--red)}"
f=lambda x:f"{x/1e8:,.1f}"
tot={s:S[s]['사회혼란']+S[s]['예방'] for s in S}
sc10=52223.7e8
row=lambda lab,k,tag:f'<tr><td>{lab}</td><td>{tag}</td>'+''.join(f'<td class="n">{"<b>" if s=="기준" else ""}{f(S[s][k])}{"</b>" if s=="기준" else ""}</td>' for s in ('하한','기준','상한'))+'</tr>'
foot=lambda n:f'<div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 별지 사회적 혼란 비용 잠정 추계(2025년 기준)</span><span>{n}</span></div>'
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>사회적 혼란 비용</title><style>{css}</style></head><body>
<section class="page">
<div class="kicker">별지 · 2025년 기준 · 2026. 11. 8. 잠정(수정)</div>
<h1>사회적 혼란 비용 잠정 추계<br>기준 {f(tot['기준'])}억 원(범위 {f(tot['하한'])}~{f(tot['상한'])}억 원), 사회적 비용 λ 10의 {tot['기준']/sc10*100:.1f}%</h1>
<h2>1. 구성과 결과 (2025년, 억 원)</h2>
<table class="c"><tr><th>구성</th><th>근거</th><th class="n">하한</th><th class="n">기준</th><th class="n">상한</th></tr>
<tr class="hl"><td colspan="2">① 마약 상태 2차 범죄 피해 (대응·결과·예방 비용 포함)</td><td class="n">{f(S['하한']['사회혼란'])}</td><td class="n"><b>{f(S['기준']['사회혼란'])}</b></td><td class="n">{f(S['상한']['사회혼란'])}</td></tr>
{row('　상해','상해','<span class="tg b">한국형사정책연구원 단가</span>')}
{row('　성폭력 (강간 20% · 강제추행 등 80%)','성폭력','<span class="tg b">한국형사정책연구원 단가</span>')}
<tr class="hl"><td>② 예방·홍보·재활 대응 예산</td><td><span class="tg b">식약처 예산</span></td><td class="n">{f(S['하한']['예방'])}</td><td class="n"><b>{f(S['기준']['예방'])}</b></td><td class="n">{f(S['상한']['예방'])}</td></tr>
<tr class="tot"><td>사회적 혼란 비용 (① + ②)</td><td></td><td class="n">{f(tot['하한'])}</td><td class="n">{f(tot['기준'])}</td><td class="n">{f(tot['상한'])}</td></tr>
<tr><td colspan="5" style="background:var(--paper);font-weight:700">참고 (합계 제외)</td></tr>
{row('마약 상태 살인 (살인 평균 단가)','살인참고','<span class="tg r">상한 참고</span>')}
{row('가족·주변인 돌봄 시간','가족참고','<span class="tg c">가정</span>')}
</table>
<div class="note">하한·기준·상한은 경찰 통계의 "약물·정신병 상태" 피의자 중 마약 상태 비율을 10%·25%·50%로, 예산은 식약처 예산의 50%·100%·범정부 602억 원으로 둔 값이다.</div>
<h2>2. 살인을 합계에서 뺀 이유</h2>
<div class="box" style="background:var(--amberBg);margin-top:2px;line-height:1.55">한국형사정책연구원의 살인 1건당 사회적 비용은 2008년 173.2억 원(2025년 247.8억 원)이다. 이 가운데 약 170억 원이 정신적·육체적 고통에 대한 지불의사액이다. 마약 상태 살인을 이 단가로 계산하면 기준 {f(S['기준']['살인참고'])}억 원으로, 다른 항목을 모두 합친 것보다 크다. 마약 관련 사회적 혼란은 사회 전체를 공포에 빠뜨리는 묻지마 살인보다 낮게 본다는 연구진 판단에 따라 살인은 합계에서 빼고 상한 참고로만 둔다. 마약 상태 살인 건수가 범죄분석으로 확인되면 별도 항목으로 다시 검토한다.</div>
<h2>3. 사회적 비용 총액에 더할 때</h2>
<table class="c"><tr><th>구분</th><th class="n">2025 시산 (λ 10)</th><th class="n">사회적 혼란 기준</th><th class="n">합계</th></tr>
<tr><td>사회적 비용</td><td class="n">5조 2,223.7억 원</td><td class="n">+{f(tot['기준'])}억 원</td><td class="n"><b>5조 {(sc10+tot['기준'])/1e8-50000:,.1f}억 원</b></td></tr></table>
<div class="note"><b>암수율 λ는 곱하지 않는다.</b> 사회 전체에서 관찰된 사건 수와 예산 총액이기 때문이다. 1명당 계수로 바꾸면 기준 {tot['기준']/234030/1e4:,.1f}만 원(÷ N* 234,030명)이다.</div>
{foot(1)}</section>
<section class="page">
<div class="kicker">별지 · 산식과 근거</div>
<h1>산식, 원단위, 남은 자료</h1>
<h2>4. 원단위 (범죄 1건당 사회적 비용)</h2>
<table class="c"><tr><th>범죄</th><th class="n">2008년 (원)</th><th class="n">2025년 환산 (억 원)</th><th>적용</th></tr>
<tr><td>상해</td><td class="n">22,066,382</td><td class="n">{U['상해']/1e8:,.3f}</td><td>상해</td></tr>
<tr><td>강간</td><td class="n">217,208,694</td><td class="n">{U['강간']/1e8:,.3f}</td><td>성폭력의 20%(가정)</td></tr>
<tr><td>폭행</td><td class="n">9,429,124</td><td class="n">{U['폭행']/1e8:,.3f}</td><td>성폭력의 80%(강제추행 등, 가정)</td></tr>
<tr><td>살인</td><td class="n">17,319,246,667</td><td class="n">{U['살인']/1e8:,.1f}</td><td>참고만</td></tr></table>
<div class="note">자료: 박경래 외(2010), 「범죄 및 형사정책에 대한 법경제학적 접근: 범죄의 사회적 비용 추계」, 한국형사정책연구원(2008년 범죄 기준). 1건당 비용은 대응 비용(경찰·검찰·법원), 결과 비용(신체·정신적 고통, 의료, 재산 피해), 사회적 예방 비용(보안장비 등)을 합한 값이다. 그래서 2차 범죄 피해, 피해자 고통, 방어적 행동을 따로 더하지 않는다. 2025년 환산: 소비자물가 2008년 81.5 → 2025년 116.6(2020=100), 1.431배. 2008년 지수는 2016년 95.8을 연도별 상승률로 역산한 값이다.</div>
<h2>5. 건수와 예산</h2>
<table class="c"><tr><th>항목</th><th class="n">값</th><th>근거</th></tr>
<tr><td>약물·정신병 상태 상해 피의자</td><td class="n">연 {N['상해']:,.0f}명</td><td rowspan="3">경찰청 "범행 당시 피의자 상태" 2021~2024년 합계에서 (주취·약물·정신병) − (음주)를 4로 나눔(박정현 의원실 분석, 2025. 10. 보도)</td></tr>
<tr><td>약물·정신병 상태 성폭력 피의자</td><td class="n">연 {N['성폭력']:,.0f}명</td></tr>
<tr><td>약물·정신병 상태 살인 피의자</td><td class="n">연 {N['살인']:,.0f}명</td></tr>
<tr><td>식약처 마약 관련 예산</td><td class="n">377억 원 (2024)</td><td>예방교육·홍보·재활센터 등. 이미 의료·복지에 넣은 정신건강·복지 17억 원을 빼서 360억 원. 범정부 602억 원은 단속 예산이 섞여 형사사법과 겹치므로 상한에만 사용</td></tr></table>
<h2>6. 남은 자료</h2>
<div class="box" style="background:var(--navyBg);margin-top:2px"><ul>
<li><b>마약 상태 범죄 건수:</b> 경찰 통계는 약물과 정신병을 함께 집계한다. 대검찰청 범죄분석의 "범행 시 정신상태: 마약" 표를 받으면 10~50% 가정을 실측으로 바꿀 수 있다.</li>
<li><b>성폭력 중 강간 비중:</b> 20%는 가정이다. 범죄분석의 죄명별 인원으로 바꾼다.</li>
<li><b>2025년 예산:</b> 2025년 마약류 관리 시행계획의 예산표를 확인하지 못해 2024년 값을 썼다.</li>
<li><b>약물운전 사고:</b> 2025년 약물운전 면허취소 237건(경찰청)은 확인했으나 사고·사상자 자료가 없어 넣지 않았다.</li>
<li><b>범죄 공포:</b> 국내 지불의사액 자료가 없어 넣지 않았다. 한국형사정책연구원 단가의 고통비용에 일부 반영되어 있다.</li>
</ul></div>
<div class="note" style="margin-top:6px">자료: 박경래 외(2010), 한국형사정책연구원; 문화일보(2014. 2. 17.) 법무부 제출 자료(살인 1건당 약 173억 원); 경찰청 자료(시사저널·KPI뉴스, 2025. 10.); 이투데이(2023. 9. 7., 9. 12.); 헤럴드경제(2026. 6. 29.); 연구진 계산</div>
{foot(2)}</section></body></html>'''
open('rest2.html','w').write(html)
