import json
A=json.load(open('addon.json')); U=A['U']; R=A['res']
css=open('/home/claude/y2025/tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
css+="table.c td,table.c th{padding:3px 6px}.sm{font-size:8.6pt}"
e=lambda x:f"{x/1e8:.2f}"
SN=['A 조기회복','B 기준','C 만성화']
B=R['B 기준|nom']['tot']; Bp=R['B 기준|pv45']['tot']
foot=lambda n:f'<div class="foot"><span>별지 3 · 부가연구: 2016년 기준 마약사범(중독자) 1인당 생애 사회적 비용</span><span>{n}</span></div>'
t1=f"""<tr><td>1년차 비용</td><td>2조 2,389억 원 ÷ 실질 사용자 142,140명(14,214명 × 10)</td><td class='n'>{U['Y1']/1e4:,.1f}만 원</td><td>그대로 사용</td></tr>
<tr><td>의료·복지</td><td>1인당 진료비(입원 749.5만 + 외래 71.9만)</td><td class='n'>821.4만 원</td><td><b>가정:</b> 활동 중독자의 30%가 해마다 진료</td></tr>
<tr><td>중독 고통(PGS)</td><td>교통사고 중상자 평균 PGS(심재익 외, 2016)</td><td class='n'>7,362.7만 원</td><td><b>가정:</b> 활동 중독 1년마다 8% (약 12.5년에 걸쳐 나눔)</td></tr>
<tr><td>재검거 형사사법</td><td>형사사법 1인 비용(경찰·검찰·법원·교정)</td><td class='n'>5,451.5만 원</td><td>재검거 1회마다 (연 재검거 10%)</td></tr>
<tr><td>초과 사망 고통(PGS)</td><td>교통사고 사망자 PGS</td><td class='n'>2억 8,095.5만 원</td><td>초과 사망 1건마다</td></tr>
<tr><td>초과 사망 소득</td><td>조기사망 1인당 손실(사망 시 기대소득)</td><td class='n'>6억 623.1만 원</td><td>초과 사망 1건마다</td></tr>
<tr><td>노동능력 상실</td><td>연령별 연간 노동가치(2025년 값 ÷ 1.417)</td><td class='n'>-</td><td><b>가정:</b> 2025 노동가치를 물가·실질임금으로 2016년 환산</td></tr>"""
S=json.load(open('/home/claude/y2025b/life.json'))['param']['SC']
t2=''.join(f"<tr><td>{s}</td><td class='n'>{S[s]['med']}년</td><td class='n'>{S[s]['L']*100:.1f}%</td><td class='n'>{S[s]['rho']*100:.0f}%</td><td class='n'>{S[s]['ea']*100:.2f}%</td><td class='n'>{S[s]['er']*100:.1f}%</td><td class='n'>{S[s]['re']*100:.0f}%</td></tr>" for s in SN)

t3=''.join(f"<tr><td>{s}</td>"+''.join(f"<td class='n'>{e(R[s+'|'+m]['tot'])}</td>" for m in ['pv3','pv4','pv45','pv5','nom'])+f"<td class='n'>{R[s+'|nom']['tot']*1.217/1e8:.2f}</td></tr>" for s in SN)
CK=list(R['B 기준|nom']['comp'].keys())
t4=''.join(f"<tr><td>{k}</td><td class='n'>{e(R['B 기준|pv45']['comp'][k])}</td><td class='n'>{e(R['B 기준|nom']['comp'][k])}</td><td class='n'>{R['B 기준|nom']['comp'][k]/B*100:.1f}%</td></tr>" for k in CK)
t5=''.join(f"<tr><td>{a[0]}세</td><td class='n'>{a[1]:,}</td><td class='n'>{e(a[2])}</td><td class='n'>{e(a[3])}</td></tr>" for a in A['age']['B 기준'])
p1=f"""<section class="page">
<div class="kicker">별지 3 · 부가연구 · 2016년 기준 · 2026. 11.</div>
<h1>2016년 기준 마약사범(중독자) 1인당 생애 사회적 비용<br><span style="font-size:15pt;color:#1d6b3a">누적 기준(B) {e(B)}억 원 (현재가치 4.5% {e(Bp)}억 원, 2016년 가격)</span></h1>
<div class="box" style="background:var(--navyBg)"><ul>
<li><b>목적:</b> 박성수(2018)는 2016년 기준 마약류 사회적 비용을 연간 단위로 추계하였다(암수율 10배, 2조 2,389억 원). 그 연구는 1인당 생애 사회적 비용을 구하는 것을 목적으로 하지 않았다. 이 부가연구는 본 연구 별지 2의 생애비용 모형을 2016년 연구의 원단위에 적용해 2016년 기준 값을 추계하고, 연구의 연속선상에서 본 연구와 비교한다.</li>
<li><b>성격:</b> 연속선상의 비교를 위한 추계로, 본 연구(2025년 기준)의 연간 비용과는 따로 다룬다. 2016년 원단위를 그대로 적용하기 어려운 부분은 합리적인 범위의 보완 가정을 두어 추계하였다. 결과는 생애비용의 규모를 가늠하기 위한 참고값이다.</li>
<li><b>결과:</b> 생애비용은 누적 기준(B)으로 본다. 1인당 생애 사회적 비용은 누적 기준 {e(B)}억 원(현재가치 {e(Bp)}억 원)이다. 2025년 가격으로 바꾸면(× 1.217) 누적 기준 {B*1.217/1e8:.2f}억 원이다.</li></ul></div>
<h2>1. 2016년 연구 원단위의 적용 (박성수, 2018)</h2>
<table class="c sm"><tr><th>항목</th><th>2016년 연구 값</th><th class="n">원단위</th><th>생애 모형 적용</th></tr>{t1}</table>
<div class="note">초과 사망 소득과 초과 사망 고통은 2016년 연구의 사망 1건당 값을 그대로 썼다. 의료·복지와 중독 고통은 원단위가 "진료 1인", "중상 1건" 기준이라 해마다 전액을 쓰면 생애비용이 과대해진다(의료 100%·고통 100%이면 명목 32.3억 원). 그래서 비율 가정을 두었다.</div>
<h2>2. 생애 구조 (본 연구 별지 2와 같음)</h2>
<table class="c sm"><tr><th>시나리오</th><th class="n">잔여 중독기간 중앙값</th><th class="n">노동능력 상실</th><th class="n">회복 후 잔존</th><th class="n">초과 사망(활동)</th><th class="n">초과 사망(회복)</th><th class="n">연 재검거</th></tr>{t2}</table>
<div class="note">생존율은 통계청 2024년 생명표에 맞춘 곡선을 썼다(2016년 생명표 대신 적용한 보완 가정). 연령 분포는 2025년 검거 사범 분포를 썼다. 실질 단가 증가 1.7%, 할인율 4.5%(3~5%), 명목 누계는 물가 2.1% 반영·할인 없음. 근거: Dennis et al.(2005), Stockings et al.(2019), Lewer et al.(2020), 대검찰청(2026), 박성수(2018).</div>
<h2>3. 결과: 1인당 생애 사회적 비용 (단위: 억 원, 2016년 가격)</h2>
<table class="c"><tr><th>시나리오</th><th class="n">현재가치 3%</th><th class="n">4%</th><th class="n">4.5%(기본)</th><th class="n">5%</th><th class="n">명목 누계</th><th class="n">명목 누계(2025년 가격)</th></tr>{t3}</table>

{foot(1)}</section>"""
p2=f"""<section class="page">
<h2>4. 구성 (B 기준)</h2>
<table class="c sm"><tr><th>구성</th><th class="n">현재가치 4.5%</th><th class="n">명목 누계</th><th class="n">비중(명목)</th></tr>{t4}
<tr class="tot"><td>합계</td><td class="n">{e(Bp)}</td><td class="n">{e(B)}</td><td class="n">100%</td></tr></table>
<h2>5. 검거 연령별 (B 기준)</h2>
<table class="c sm"><tr><th>검거 연령(대표)</th><th class="n">사범 수(2025 분포)</th><th class="n">현재가치 4.5%</th><th class="n">명목 누계</th></tr>{t5}</table>
<h2>6. 본 연구(별지 2, 2025년 기준)와 비교</h2>
<table class="c sm"><tr><th>구분</th><th class="n">1년차 1인당</th><th class="n">B 현재가치</th><th class="n">B 명목 누계</th></tr>
<tr><td>부가연구: 2016년 기준(2016년 가격)</td><td class="n">{A['U']['Y1']/1e4:,.1f}만 원</td><td class="n">{e(Bp)}억 원</td><td class="n">{e(B)}억 원</td></tr>
<tr><td>본 연구 별지 2: 2025년 기준(2025년 가격)</td><td class="n">3,194.7만 원</td><td class="n">3.97억 원</td><td class="n">12.28억 원</td></tr></table>
<div class="box" style="background:var(--navyBg);margin-top:6px"><ul>
<li>2016년 기준 1인당 생애 사회적 비용은 누적 기준(B) 약 {B/1e8:.1f}억 원(현재가치 약 {Bp/1e8:.1f}억 원)이다.</li>
<li>2016년 연구의 "1인당 비용 10억 2,371만 원"은 항목마다 대상이 다른 1인당 값(사망 1인당 생산성 손실 6.06억 원, 사상자 1인당 고통비용 3.55억 원 등)을 더한 값이다. 중독자 1명의 생애 비용과는 개념이 다르다. 크기가 비슷한 것은 우연에 가깝다.</li>
<li>2016년 값이 작은 주된 이유는 가격 기준이다. 2025년 가격(× 1.217)으로 바꾸면 명목 누계 {B*1.217/1e8:.2f}억 원, 현재가치 {Bp*1.217/1e8:.2f}억 원으로 본 연구(12.28억, 3.97억 원)와 비슷하다.</li><li>1년차 비용은 2016년이 1,917.1만 원(2025년 가격)으로 본 연구 3,194.7만 원의 60.0%이다. ① 사망 고통비용 원단위가 2.81억 원(심재익 외, 2016)으로 2025년 9.7억 원보다 낮다. ② 2016년 연구는 사회적 혼란·기타 비용을 산정하지 않았다. ③ 2025년에는 교도소 비용을 미결 포함 연말 전체 수용자 기준으로 배분하였고, 치료보호 인원이 597명에서 1,649명으로 늘었다.</li><li>그럼에도 생애비용 차이가 작은 것은 2016년 연구의 사망 1건당 소득 손실(6.06억 원)이 커서 초과 사망 비용이 명목 누계의 {(R['B 기준|nom']['comp']['초과사망 고통(PGS)']+R['B 기준|nom']['comp']['초과사망 소득'])/B*100:.1f}%를 차지하기 때문이다.</li>
<li>한계: 의료 30%·중독 고통 8% 비율, 2016년 노동가치 환산, 2024년 생명표·2025년 연령 분포 적용은 보완 가정이다. 결과는 규모를 비교하는 참고값으로 활용한다.</li></ul></div>
<div class="note" style="margin-top:4px"><b>참고문헌</b> 박성수(2018). 마약류 등 유해약물의 사회적 비용 분석. 『치안정책연구』, 32(3), 217–253. · 심재익 외(2016). 2013년 교통사고비용 추정. 한국교통연구원. · 대검찰청(2026). 2025 마약류 범죄백서. · 통계청(2025). 2024년 생명표. · Dennis et al.(2005). · Stockings et al.(2019). · Lewer et al.(2020).</div>
{foot(2)}</section>"""
open('rep.html','w').write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>부가연구 생애비용</title><style>{css}</style></head><body>{p1}{p2}</body></html>')
