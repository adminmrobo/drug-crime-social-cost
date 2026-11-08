import json
d=json.load(open('rest.json')); T=d['tot']
css=open('/home/claude/y2025/tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
css+="table.c td{padding:2.5px 6px}.tg{display:inline-block;font-size:7.3pt;font-weight:700;border-radius:3px;padding:0 4px;color:#fff}.tg.b{background:var(--teal)}.tg.c{background:var(--amber)}.tg.r{background:var(--red)}"
f=lambda x:f"{x/1e8:,.1f}"
items=[('4-1','2차 범죄 직접 피해','사회적 혼란 · 불특정 다수','b','약물 상태 강력범죄 건수 × 범죄 1건당 생산손실·의료·피해자지원·경찰·사법 비용'),
('4-2a','2차 범죄 피해자 고통(PGS)','사회적 혼란 · 피해자','b','사망 피해자 × 9.9억(한국교통연구원 원단위, 2025년 환산), 상해·성폭력 × 신체·정서 피해 단가'),
('5-2b','방어적 행동','사회적 혼란 · 예상 비용','c','같은 범죄의 예상 비용(방어 지출·보험 관리비) 단가'),
('4-3','가족·주변인 돌봄','피해자·주위','c','치료 중독자 889명(875명 × 1.0165) × 가족 돌봄 주 2·5·10시간 × 52주 × 최저임금 10,030원'),
('5-1','예방·홍보·재활 예산','기타','b','식품의약품안전처 마약 예산 377억 원(2024) − 이미 반영한 정신건강·복지 17억 원')]
rows=''.join(f'<tr><td>{i}</td><td>{n}<br><span style="color:var(--slate);font-size:7.8pt">{g}</span></td><td><span class="tg {c}">{"공개자료·문헌" if c=="b" else "가정"}</span></td><td class="n">{f(T["하한"][i])}</td><td class="n"><b>{f(T["기준"][i])}</b></td><td class="n">{f(T["상한"][i])}</td></tr>' for i,n,g,c,_ in items)
tot={s:sum(v for k,v in T[s].items() if '참고' not in k) for s in T}
sc10=52223.7e8
rowsU=''.join(f'<tr><td>{r[0]}</td><td class="n">{r[1]:,.1f}</td><td class="n">{r[2]:,.1f}</td><td class="n">{r[4]:,.2f}</td><td class="n">{r[5]:,.2f}</td><td class="n">{r[6]:,.3f}</td><td class="n">{r[3]:,.2f}</td></tr>' for r in d['rows'])
meth=''.join(f'<tr><td>{i}</td><td>{m}</td></tr>' for i,n,g,c,m in items)
foot=lambda n:f'<div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 별지 미산출 항목 잠정 추계(2025년 기준)</span><span>{n}</span></div>'
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>미산출 항목 잠정 추계</title><style>{css}</style></head><body>
<section class="page">
<div class="kicker">별지 · 2025년 기준 · 2026. 11. 8. 잠정</div>
<h1>미산출 비용 항목 잠정 추계<br>기준 {f(tot['기준'])}억 원(범위 {f(tot['하한'])}~{f(tot['상한'])}억 원), 사회적 비용 λ 10의 {tot['기준']/sc10*100:.1f}%</h1>
<h2>1. 지금까지 산출하지 않은 항목</h2>
<table class="c"><tr><th>번호</th><th>항목</th><th>이번 처리</th></tr>
<tr><td>4-1 · 4-2a · 5-2b</td><td>사회적 혼란: 2차 범죄 피해, 피해자 고통, 방어적 행동</td><td>잠정 추계 (영국 범죄비용 단가 원용)</td></tr>
<tr><td>4-3</td><td>가족·주변인 돌봄</td><td>잠정 추계 (돌봄 시간 가정)</td></tr>
<tr><td>5-1</td><td>예방·홍보·재활 예산</td><td>잠정 추계 (식약처 예산)</td></tr>
<tr><td>5-2a</td><td>범죄 공포(지불의사액)</td><td>참고 시나리오만. 설문 없이 근거를 만들 수 없어 합계에서 제외</td></tr>
<tr><td>2-3a · 1-1c</td><td>구금 기간 생산성, 수용자 의료비</td><td>11. 5. 결정으로 제외 유지</td></tr>
</table>
<h2>2. 항목별 잠정 추계 (2025년, 억 원)</h2>
<table class="c"><tr><th>번호</th><th>항목</th><th>근거</th><th class="n">하한</th><th class="n">기준</th><th class="n">상한</th></tr>{rows}
<tr class="tot"><td></td><td>합계 (5-2a 제외)</td><td></td><td class="n">{f(tot['하한'])}</td><td class="n">{f(tot['기준'])}</td><td class="n">{f(tot['상한'])}</td></tr>
<tr><td>5-2a</td><td>범죄 공포 (참고)<br><span style="color:var(--slate);font-size:7.8pt">성인 4,400만 명 × 연 1,000·3,000·5,000원</span></td><td><span class="tg r">근거 없음</span></td><td class="n">{f(T['하한']['5-2a(참고)'])}</td><td class="n">{f(T['기준']['5-2a(참고)'])}</td><td class="n">{f(T['상한']['5-2a(참고)'])}</td></tr></table>
<div class="note">사회적 혼란(4-1·4-2a·5-2b) 기준 합계는 {f(T['기준']['4-1']+T['기준']['4-2a']+T['기준']['5-2b'])}억 원이다. 하한·상한은 약물·정신질환 상태 범죄 중 마약 상태 비율을 10%·25%·50%로, 가족 돌봄은 주 2·5·10시간으로, 예산은 식약처 예산의 50%·100%·범정부 602억 원으로 둔 값이다.</div>
<h2>3. 사회적 비용 총액에 더할 때</h2>
<table class="c"><tr><th>구분</th><th class="n">2025 시산 (λ 10)</th><th class="n">미산출 항목 기준</th><th class="n">합계</th></tr>
<tr><td>사회적 비용</td><td class="n">5조 2,223.7억 원</td><td class="n">+{f(tot['기준'])}억 원</td><td class="n"><b>5조 {(sc10+tot['기준'])/1e8-50000:,.1f}억 원</b></td></tr></table>
<div class="note"><b>암수율 λ는 곱하지 않는다.</b> 이 항목들은 검거 사범 1명당 비용이 아니라 사회 전체에서 관찰된 사건 수·예산·인구 단위 총액이다. 1명당 계수로 바꾸면 기준 {tot['기준']/234030/1e4:,.1f}만 원(÷ N* 234,030명)이다.</div>
{foot(1)}</section>
<section class="page">
<div class="kicker">별지 · 산식과 근거</div>
<h1>산식, 원단위, 남은 자료</h1>
<h2>4. 사회적 혼란: 2차 범죄 원단위 (2025년 원화, 억 원/건)</h2>
<table class="c" style="font-size:8.4pt"><tr><th>범죄</th><th class="n">약물·정신질환 상태<br>검거 (연평균)</th><th class="n">마약 상태<br>기준 25%</th><th class="n">직접 피해<br>(4-1)</th><th class="n">피해자 고통<br>(4-2a)</th><th class="n">방어 행동<br>(5-2b)</th><th class="n">1건 합계</th></tr>{rowsU}</table>
<div class="note">검거 인원: 2021~2024년 경찰청 "범행 당시 피의자 상태"에서 주취·약물·정신병 상태 인원 − 음주 상태 인원의 4년 평균(박정현 의원실 분석, 2025. 10. 보도). 이 인원에는 정신질환 상태가 섞여 있어 마약 상태 비율을 10·25·50%로 가정하였다. 원단위: 영국 내무부 범죄비용 단가(Heeks et al., 2018; 2019/20년 가격 개정판)의 결과 비용(생산손실·의료·피해자지원·재산)과 대응 비용(경찰·사법)을 4-1로, 신체·정서 피해를 4-2a로, 예상 비용(방어 지출·보험)을 5-2b로 나누었다. 살인 피해자의 고통은 본 연구 원단위와 맞추어 한국교통연구원 사망 9.7억 원 × 1.021을 썼다. 성폭력은 "기타 성범죄" 단가를 적용하였다(보수적). 환산: 구매력평가(2020년, 한국 847.5원/달러 ÷ 영국 0.689파운드/달러 = 1,230원/파운드) × 한국 소비자물가 2020→2025년 1.166 = 1파운드당 {d['K']:,.0f}원</div>
<h2>5. 나머지 항목의 산식</h2>
<table class="c"><tr><th>번호</th><th>산식·근거</th></tr>{meth}
<tr><td>5-2a</td><td>범죄 공포 지불의사액은 국내 조사가 확인되지 않는다. CVM 설문(1,000명) 전까지 합계에 넣지 않고 규모만 참고로 둔다.</td></tr></table>
<h2>6. 해석상 유의점과 남은 자료</h2>
<div class="box" style="background:var(--navyBg);margin-top:2px"><ul>
<li><b>살인이 사회적 혼란 비용의 대부분이다.</b> 기준값에서 살인 16.3건이 4-1·4-2a의 약 9할을 차지한다. 마약 상태 살인 건수를 확인하면 범위가 크게 좁혀진다. 대검찰청 범죄분석의 "범행 시 정신상태: 마약" 표가 필요하다.</li>
<li><b>영국 단가의 사법 비용:</b> 살인 1건의 경찰·사법 비용(약 9.2억 원)은 영국 기준이라 국내보다 클 수 있다. 국내 살인 사건 처리 비용으로 바꾸면 4-1이 줄어든다.</li>
<li><b>약물운전 사고:</b> 약물운전 면허취소는 2025년 237건(경찰청)이나 사고 건수·사상자 자료가 없어 넣지 않았다. 도로교통공단 교통사고분석시스템의 약물운전 사고 자료가 오면 한국교통연구원 원단위로 산정한다.</li>
<li><b>예방 예산 중복:</b> 범정부 마약 예산 602억 원(2024)에는 단속·수사 예산이 들어 있어 형사사법과 겹친다. 기준값은 단속 성격이 적은 식약처 예산만 썼다. 2025년 예산은 확인하지 못해 2024년 값을 썼다.</li>
<li><b>가족 돌봄:</b> 가족의 정신적 고통은 중독자 고통비용(한국교통연구원 원단위가 가족 고통 포함)에 이미 들어 있다. 여기서는 돌봄 시간만 더했다. 돌봄 시간은 국내 근거가 없는 가정이다.</li>
</ul></div>
<div class="note" style="margin-top:6px">자료: Heeks, M., Reed, S., Tafsiri, M., &amp; Prince, S.(2018). The economic and social costs of crime, second edition. Home Office Research Report 99; Home Office. Economic and social costs of crime 2019 to 2020(단가 개정판); 경찰청 자료(시사저널·KPI뉴스, 2025. 10.); 헤럴드경제(2026. 6. 29.) 약물운전 면허취소; 이투데이(2023. 9. 7., 9. 12.) 식약처·범정부 마약 예산; 한국교통연구원(2025. 7. 28.); 연구진 계산</div>
{foot(2)}</section></body></html>'''
open('rest.html','w').write(html)
