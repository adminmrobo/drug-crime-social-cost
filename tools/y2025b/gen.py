import json
R=json.load(open('r.json')); L=json.load(open('life.json'))
css=open('/home/claude/y2025/tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
css+="table.c td,table.c th{padding:3px 6px} .ok{color:#1d6b3a;font-weight:700}.ng{color:#b3261e;font-weight:700}.sm{font-size:8.6pt}"
def jo(x):  # 억 → 조·억 표기
    if abs(x)>=10000: return f"{int(x//10000)}조 {x%10000:,.1f}억"
    return f"{x:,.1f}억"
N=R['N']; g=R['grp']; O=R['old']
foot=lambda n:f'<div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 별지 2025년 원고 반영 재산정·방침 점검·1인당 생애비용 (2026. 11. 14.)</span><span>{n}</span></div>'
GO=['형사사법','고통비용','생산성','의료·복지','사회적 혼란·기타']
src={'형사사법':'원고 11.08 실측','고통비용':'2024 원단위×물가(원고 미수령)','생산성':'원고 11.06 실측','의료·복지':'원고 11.06 실측','사회적 혼란·기타':'별지 추계(11. 9.)'}
t1=''.join(f"<tr><td>{k}</td><td class='n'>{g[k]:,.1f}</td><td class='n'>{g[k]/N*1e4:,.1f}</td><td class='n'>{jo(g[k]*10)}</td><td class='n'>{g[k]/R['tot']*100:.1f}%</td><td class='n'>{g[k]-O[k]:+,.1f}</td><td>{src[k]}</td></tr>" for k in GO)
t1+=f"<tr class='tot'><td>합계</td><td class='n'>{R['tot']:,.1f}</td><td class='n'>{R['pc']:,.1f}</td><td class='n'>{jo(R['t10'])}</td><td class='n'>100.0%</td><td class='n'>{R['tot']-R['old_tot']:+,.1f}</td><td></td></tr>"
t2=''.join(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td class='n'>{r[2]:,.1f}</td><td class='n'>{r[3]:,.1f}</td><td class='n'>{jo(r[4])}</td><td class='n'>{jo(r[5])}</td></tr>" for r in R['rows'])
t2+=f"<tr class='tot'><td colspan=2>합계</td><td class='n'>{R['tot']:,.1f}</td><td class='n'>{R['pc']:,.1f}</td><td class='n'>{jo(R['t10'])}</td><td class='n'>{jo(R['t28'])}</td></tr>"
p1=f'''<section class="page">
<div class="kicker">별지 · 2025년 기준 · 2026. 11. 14.</div>
<h1>2025년 사회적 비용(λ 10): {jo(R['t10'])} 원<br>검거 사범 1명당 {R['pc']:,.1f}만 원 · 생애비용(기준) {L['w']['B 기준|pv45']['tot']/1e8:.2f}억 원</h1>
<div class="box" style="background:var(--navyBg)"><ul>
<li>형사사법 원고(2025, 11. 8.)와 제3장 제1·2절 원고(2025, 11. 6.)의 실측값을 반영하였다. 고통비용은 원고가 없어 2024년 원단위에 물가(1.021)를 곱한 추정이다.</li>
<li>모든 비용을 검거 사범 1명당 값(총액 ÷ {N:,}명)으로 바꾸고 암수율 λ를 곱하였다. 형사사법과 사회적 혼란·기타에도 λ를 곱하였다.</li>
<li>암수율 미반영 {jo(R['tot'])} 원, λ 10 {jo(R['t10'])} 원(N* {N*10:,}명), λ 28.57 {jo(R['t28'])} 원이다. 박성수(2018)의 2조 2,389억 원 대비 λ 10에서 {R['vs16']['ratio']:.2f}배이다.</li>
<li>11. 9. 시산(6,571.4억 원) 대비 {R['tot']-R['old_tot']:+,.1f}억 원이다. 교도소가 962.8억 원에서 1,953.3억 원으로 늘어난 몫(+990.5억 원)이 대부분이다. 원고가 교정본부 빅데이터 12. 31. 기준 전체 수용자(7,429 ÷ 64,626명)를 썼기 때문이다.</li></ul></div>
<h2>1. 분야별 총괄 (단위: 억 원, 1명당은 만 원)</h2>
<table class="c"><tr><th>분야</th><th class="n">암수율 미반영</th><th class="n">1명당</th><th class="n">λ 10</th><th class="n">구성비</th><th class="n">11. 9. 시산 대비</th><th>자료</th></tr>{t1}</table>
<div class="note">1명당 = 분야 총액 ÷ 2025년 검거 사범 {N:,}명(대검찰청, 2026). λ 10 = 1명당 × N* {N*10:,}명. 11. 9. 시산 값: 형사사법 2,807.0, 고통비용 2,435.9, 생산성 773.3, 의료·복지 59.2, 사회적 혼란·기타 496.0억 원.</div>
<h2>2. 원고 반영으로 바뀐 값</h2>
<table class="c sm"><tr><th>항목</th><th class="n">11. 9. 시산</th><th class="n">원고 반영</th><th>바뀐 이유</th></tr>
<tr><td>경찰</td><td class="n">1,416.8</td><td class="n">1,381.0</td><td>추정(2024×증가율) → 실측(결산 13조 3,558억 × 13,343 ÷ 1,290,412명)</td></tr>
<tr><td>검찰</td><td class="n">214.5</td><td class="n">199.3</td><td>원고는 2024년 예산·인원 사용(2025년 총검거인원 미공개)</td></tr>
<tr><td>법원</td><td class="n">100.8</td><td class="n">99.0</td><td>실측(형사소송 관련 2,483.9억 × 13,849 ÷ 347,473명)</td></tr>
<tr><td>교도소</td><td class="n">962.8</td><td class="n">1,953.3</td><td>3,608 ÷ 63,680명(추정) → 7,429 ÷ 64,626명(12. 31. 전체 수용자)</td></tr>
<tr><td>국립법무병원·보호관찰소</td><td class="n">112.1</td><td class="n">95.6</td><td>실측(9 ÷ 823명, 1,853 ÷ 41,138명)</td></tr>
<tr><td>조기사망·이환·미취업</td><td class="n">773.3</td><td class="n">815.0</td><td>실측(사망 58명, 할인율 4%·임금상승 4%; 20세 이상 사범 22,242명)</td></tr>
<tr><td>의료·복지</td><td class="n">59.2</td><td class="n">78.6</td><td>실측(청구 30.2억 + 치료보호 14.4억, 간접 38.1%, 기관 운영 17.0억)</td></tr>
<tr><td>사망 PGS</td><td class="n">583.9</td><td class="n">574.4</td><td>사망자 58명 실측 × 9.7억 원 × 1.021</td></tr></table>
{foot(1)}</section>'''
p2=f'''<section class="page">
<h2>3. 항목별 금액과 1명당 계수 (2025년, 단위: 억 원, 1명당은 만 원)</h2>
<table class="c sm"><tr><th>분야</th><th>항목</th><th class="n">암수율 미반영</th><th class="n">1명당</th><th class="n">λ 10</th><th class="n">λ 28.57</th></tr>{t2}</table>
<div class="note">형사사법은 마약류만 반영하였다(원고의 유해화학물질 포함 값과 5.6억 원 차이). 사회적 혼란·기타의 2차 범죄 하한(45.0억 원)을 쓰면 1명당 {R['pc_lo']:,.1f}만 원이다. 중독자 PGS = 치료보호 1,649명 × 1.1억 원 × 1.021. 사망 PGS = 58명 × 9.7억 원 × 1.021(한국교통연구원, 2025).</div>
<h2>4. 원고 1인당 비용과 모형 1명당 계수는 다르다</h2>
<table class="c sm"><tr><th>구분</th><th class="n">원고 1인당</th><th>원고의 분모</th><th class="n">모형 1명당</th></tr>
<tr><td>형사사법(원고 &lt;표 18&gt;)</td><td class="n">9,979.6만</td><td>기관마다 다름(경찰 13,343, 교도소 7,429, 법무병원 9명 등)의 1인당 합</td><td class="n">{g['형사사법']/N*1e4:,.1f}만</td></tr>
<tr><td>의료·복지(원고 &lt;표 3-9&gt;)</td><td class="n">1,013.9만</td><td>입원 393, 외래 1,835, 치료보호 1,649명의 1인당 합</td><td class="n">{g['의료·복지']/N*1e4:,.1f}만</td></tr>
<tr><td>생산성(원고 &lt;표 3-22&gt;)</td><td class="n">73,014.7만</td><td>사망자 58, 의료이용 2,080, 사범 22,242명의 1인당 합</td><td class="n">{g['생산성']/N*1e4:,.1f}만</td></tr></table>
<div class="note">원고의 1인당 값은 기관·항목마다 분모가 다른 값을 더한 것이다. 여기에 N*를 곱하면 중복 계상이 된다. 예를 들어 생산성 7억 3,015만 원 × 234,030명은 170조 원이 넘는다. 모형의 총비용은 분야 총액 ÷ 검거 사범 {N:,}명으로 만든 1명당 계수에 N*를 곱해야 한다. 원고 본문의 1인당 값은 "해당 항목 대상자 1인당"으로 이름을 바꿀 것을 권한다.</div>
{foot(2)}</section>'''
chk=[('요약본·발표자료·엑셀(2024·2025): 4개 분야','검거 사범 1명당 × N*','형사사법 포함 전 항목 λ','ok','준수','-'),
('같은 자료: 사회적 혼란·기타(481.4·496.0억)','총액을 그대로 더함','λ 미적용','ng','미준수','이번 별지에서 1명당 {0:,.1f}만 원 × N*로 바꿈'.format(g['사회적 혼란·기타']/N*1e4)),
('별지 사회적 혼란 잠정추계·나머지 미산정 비용','총액','"암수율 미적용" 명시','ng','미준수','같은 방식으로 바꿈. 별지 문구 수정 필요'),
('별지 생애비용(11. 9.)','1명당 2,231.5만 원(875명 기준, 사회적 혼란 제외)','1명당 값이라 λ 무관','ng','기준 낡음','이번 별지 5장으로 대체'),
('원고 11.08 형사사법 &lt;표 18&gt;','기관별 1인당 합 9,979.6만 원','λ 언급 없음','ng','정의 다름','모형 1명당 {0:,.1f}만 원 병기'.format(g['형사사법']/N*1e4)),
('원고 11.06 제1·2절','항목 대상자 1인당 합','"암수율은 적용하지 않았다"','ng','표현 충돌','"본 절은 관측 인원 기준 금액이며 종합 절에서 1명당 계수 × N*로 환산한다"로 수정 권고'),
('프로젝트 지침 문구','-','"형사사법비용에는 적용하지 않는다"','ng','지침 낡음','연구진 방침(형사사법 포함 전 항목 λ)으로 지침 수정 필요')]
t3=''.join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class='{d}'>{e}</td><td>{f}</td></tr>" for a,b,c,d,e,f in chk)
p3=f'''<section class="page">
<h2>5. "모든 비용 1명당 × 암수율" 방침 점검</h2>
<table class="c sm"><tr><th>산출물</th><th>1명당 정의</th><th>λ 처리</th><th>판정</th><th>조치</th></tr>{t3}</table>
<div class="box" style="background:var(--navyBg);margin-top:6px"><ul>
<li>4개 분야는 방침대로 만들었다. 형사사법에도 λ를 곱하였다.</li>
<li>사회적 혼란·기타는 1명당 계수로 바꾸지 않고 총액(2024년 481.4억, 2025년 496.0억 원)을 λ 없이 더하였다. 방침과 맞지 않는다. 바꾸면 2025년 λ 10에서 {jo(g['사회적 혼란·기타']*10)} 원으로 {jo(g['사회적 혼란·기타']*9)} 원 늘어난다. 2024년도 481.4억 원 → 4,814.0억 원으로 늘어난다.</li>
<li>11. 9.에 낸 2025년 시산(λ 10 6조 1,249.9억 원)을 방침대로 고치면 6조 5,714.1억 원이다. 이번 원고 반영 값은 {jo(R['t10'])} 원이다.</li></ul></div>
<h2>6. 원고에서 확인할 점</h2>
<table class="c sm"><tr><th>원고</th><th>위치</th><th>확인할 점</th></tr>
<tr><td>11.08</td><td>&lt;표 2&gt;·&lt;표 6&gt;</td><td>&lt;표 2&gt;는 검찰 2025년 결산 1조 2,879.5억 원인데 계산은 2024년 예산 1조 2,162.6억 원을 썼다. 2025년 결산에 2024년 비율을 쓰면 {R['cj_alt_검찰']:,.1f}억 원(+{R['cj_alt_검찰']-199.27:,.1f}억)이다.</td></tr>
<tr><td>11.08</td><td>보호관찰 본문</td><td>본문 총 접수인원 43,138명, &lt;표 3&gt;·&lt;표 16&gt;은 41,138명. 계산 결과(90.5억 원)는 41,138명과 맞는다.</td></tr>
<tr><td>11.08</td><td>교도소</td><td>12. 31. 기준 전체 수용자(미결 포함). 교정본부 담당자 기준치가 오면 그 값으로 바꾼다.</td></tr>
<tr><td>11.08</td><td>표 번호·숫자</td><td>&lt;표 3&gt;·&lt;표 11&gt;·&lt;표 15&gt; 번호 중복, &lt;표 18&gt; "373,384,780,,399" 쉼표 오류, 1장 "마약루" 오타.</td></tr>
<tr><td>11.06</td><td>&lt;표 3-15&gt;</td><td>조기사망 할인율 4%·임금상승 4%. 프로젝트 기본 할인율 4.5%와 다르다. 4.5%를 쓰면 금액이 줄어든다. 연구진 확정 필요.</td></tr>
<tr><td>11.06</td><td>&lt;표 3-22&gt;</td><td>조기사망 1인당(7억 2,740만 원)은 사망자 1인당이다. 검거 사범 1명당으로는 {421.89/N*1e4:,.1f}만 원이다.</td></tr></table>
{foot(3)}</section>'''
P=L['param']; S=P['SC']
def sc_row(lab,k): s=S[k]; return f"<tr><td>{lab}</td><td class='n'>{s['med']}년</td><td class='n'>{s['L']*100:.1f}%</td><td class='n'>{s['rho']*100:.0f}%</td><td class='n'>{s['ea']*100:.2f}%</td><td class='n'>{s['er']*100:.1f}%</td><td class='n'>{s['re']*100:.0f}%</td></tr>"
p4=f'''<section class="page">
<h2>7. 마약사범(중독자) 1명당 생애 사회적 비용: 모형</h2>
<div class="box" style="background:var(--navyBg)"><ul>
<li><b>범위:</b> 하한은 이 연구의 1년차 1명당 비용 {P['FLOOR']/1e4:,.1f}만 원(2차 범죄 하한 기준)이다. 상한은 16억 원이다.</li>
<li><b>대상:</b> 2025년 검거 사범의 연령 분포(10대 674, 20대 6,913, 30대 6,986, 40대 3,925, 50대 2,428, 60세 이상 1,990명)로 가중 평균한다(대검찰청, 2026).</li>
<li><b>시점:</b> 검거 해에 1년차 비용을 내고, 다음 해부터 사망할 때까지 매년 비용을 더한다. 2025년 불변가격, 실질 단가 증가 1.7%, 할인율 4.5%(민감도 3·4·5%)이다. 총 누계는 물가 2.1%를 더하고 할인하지 않은 명목 합계이다.</li></ul></div>
<div class="note" style="margin:4px 0"><b>생애비용</b> = 1년차 비용 + Σ<sub>t</sub> [ 활동 중독 확률 × (반복 비용 {P['REC']/1e4:,.0f}만 원 + 재검거 확률 × 형사사법 {P['CJ1']/1e4:,.0f}만 원) + (활동 + 회복 후 잔존) × 노동능력 상실 비율 × 연간 노동가치 + 초과 사망 확률 × (사망 PGS {P['DPGS']/1e8:.2f}억 원 + 잔여 근로소득) ] × 단가 증가 ÷ 할인</div>
<h2>8. 모수와 근거</h2>
<table class="c sm"><tr><th>시나리오</th><th class="n">잔여 중독기간 중앙값</th><th class="n">노동능력 상실</th><th class="n">회복 후 잔존</th><th class="n">초과 사망(활동)</th><th class="n">초과 사망(회복)</th><th class="n">연 재검거</th></tr>
{sc_row('A 조기회복','A 조기회복')}{sc_row('B 기준','B 기준')}{sc_row('C 만성화','C 만성화')}</table>
<table class="c sm" style="margin-top:6px"><tr><th>모수</th><th>근거</th></tr>
<tr><td>일반인 사망률</td><td>통계청 2024년 생명표 40세 기대여명(남 41.9, 여 47.4년)과 60세(남 23.7, 여 28.4년)의 남녀 평균에 맞춘 Gompertz 곡선</td></tr>
<tr><td>중독기간</td><td>첫 치료부터 1년 이상 단약까지 중앙값 9년, 첫 사용부터 중앙값 27년(Dennis et al., 2005). A는 5년으로 가정</td></tr>
<tr><td>초과 사망</td><td>암페타민류 사용자 조사망률 연 1.14%(95% CI 0.92~1.42), 표준화사망비 6.83(Stockings et al., 2019). 초과분 = 조사망률 × (1 − 1/6.83). 회복 후 값은 가정</td></tr>
<tr><td>기대수명 검증</td><td>아편류 의존자의 18세 기대여명은 일반인보다 남 14.7년, 여 15.8년 짧다(Lewer et al., 2020). 필로폰 중심인 국내에서는 이보다 짧은 격차를 기대한다</td></tr>
<tr><td>노동능력 상실</td><td>2025년 마약류 사범 무직 7,268명(31.1%)(대검찰청, 2026). B는 박성수(2018)의 조정비율 50%를 적용한 15.6%, A는 박성수(2018) 실직률 25% × 50% = 12.5%</td></tr>
<tr><td>연간 노동가치</td><td>제3장 원고 &lt;표 3-14&gt;(월임금 × 12 × 고용률, 20~64세)</td></tr>
<tr><td>반복 비용</td><td>중독자 PGS·의료·복지·이환·2차 범죄·가족·운전의 1명당 값. 미취업·조기사망·예방예산은 1년차에만 넣고 이후는 노동능력·초과 사망 항목으로 대신함(중복 방지)</td></tr>
<tr><td>재검거</td><td>마약류 재범률 34.5%(서울신문, 2025. 6. 27.)와 11. 9. 생애 별지의 연 10%를 기준으로 둠</td></tr></table>
<h2>8-1. 기대여명 근거와 한계</h2>
<table class="c sm"><tr><th>구분</th><th>내용</th></tr>
<tr><td style="white-space:nowrap">일반인 기대여명</td><td>통계청(2025. 12. 3.) 「2024년 생명표」의 40세(남 41.9, 여 47.4년)·60세(남 23.7, 여 28.4년) 기대여명. 남녀 평균(40세 44.65년, 60세 26.05년)에 맞춘 Gompertz 사망률 곡선을 일반인 사망률로 썼다.</td></tr>
<tr><td style="white-space:nowrap">중독자 기대여명</td><td>문헌 값을 그대로 쓰지 않고 계산하였다. 일반인 사망률 + 초과 사망률(활동 중독: Stockings et al., 2019; 회복 후: 가정 연 0.1~0.3%), 중독기간(Dennis et al., 2005). 단축 결과는 A 3.9년, B 6.3년, C 10.2년이다.</td></tr>
<tr><td>검증</td><td>호주 아편류 의존자의 기대여명은 일반인보다 남 14.7년, 여 15.8년 짧았다(Lewer et al., 2020). 필로폰 중심인 국내 사범은 이보다 작은 격차가 타당하다고 보았다.</td></tr>
<tr><td>한계</td><td>① 생명표 값은 보도 자료에서 옮겼다. KOSIS 생명표 원표로 확인할 필요가 있다. ② 남녀 평균을 썼다. 사범은 남성 비중이 높아 일반인 기대여명이 다소 길게 잡혔을 수 있다. 2025 범죄백서의 성별 인원으로 가중하면 더 정확하다. ③ 회복 후 초과 사망률은 근거가 없는 가정이다. ④ 국내 마약류 사용자의 사망률·기대여명을 다룬 연구는 확인되지 않는다. 국내 자료가 생기면 가장 먼저 바꿀 모수이다. ⑤ Lewer et al.(2020)은 권·쪽수를 확인하지 못하였다.</td></tr></table>
{foot(4)}</section>'''
def cell(k,m): return L['w'][k+'|'+m]['tot']/1e8
def clip(v): return min(max(v,P['FLOOR']/1e8),16)
SN=['A 조기회복','B 기준','C 만성화']
t5=''.join(f"<tr><td>{s}</td>"+''.join(f"<td class='n'>{cell(s,m):.2f}</td>" for m in ['pv3','pv4','pv45','pv5'])+f"<td class='n'>{cell(s,'nom'):.2f}</td><td class='n'><b>{clip(cell(s,'pv45')):.2f}</b> / {clip(cell(s,'nom')):.2f}</td></tr>" for s in SN)
def le(s): w=L['w'][s+'|pv45']; return w['e_gen'],w['e_add'],w['act']
t6=''.join(f"<tr><td>{s}</td><td class='n'>{le(s)[0]:.1f}년</td><td class='n'>{le(s)[1]:.1f}년</td><td class='n'>{le(s)[0]-le(s)[1]:.1f}년</td><td class='n'>{le(s)[2]:.1f}년</td></tr>" for s in SN)
CK=list(L['w']['B 기준|pv45']['comp'].keys())
t7=''.join(f"<tr><td>{c}</td>"+''.join(f"<td class='n'>{L['w'][s+'|pv45']['comp'][c]/1e8:.2f}</td>" for s in SN)+f"<td class='n'>{L['w']['B 기준|nom']['comp'][c]/1e8:.2f}</td></tr>" for c in CK)
t8=''.join(f"<tr><td>{a[0]}세</td><td class='n'>{a[1]:,}</td><td class='n'>{a[2]/1e8:.2f}</td><td class='n'>{b[2]/1e8:.2f}</td><td class='n'>{a[3]:.1f} → {a[4]:.1f}</td></tr>" for a,b in zip(L['age']['B 기준|pv45'],L['age']['B 기준|nom']))
B=cell('B 기준','pv45')
p5=f'''<section class="page">
<h2>9. 결과: 1명당 생애 사회적 비용 (단위: 억 원)</h2>
<table class="c"><tr><th>시나리오</th><th class="n">현재가치 3%</th><th class="n">4%</th><th class="n">4.5%(기본)</th><th class="n">5%</th><th class="n">총 누계(명목)</th><th class="n">범위 적용(현재가치/누계)</th></tr>{t5}</table>
<div class="note">범위 적용 = 하한 {P['FLOOR']/1e8:.2f}억 원, 상한 16억 원으로 자른 값. C의 명목 총 누계 {cell('C 만성화','nom'):.2f}억 원은 상한을 넘어 16억 원으로 둔다. 현재가치는 세 시나리오 모두 범위 안이다.</div>
<table class="c sm" style="margin-top:6px"><tr><th>시나리오</th><th class="n">일반인 잔여 기대여명</th><th class="n">중독자 잔여 기대여명</th><th class="n">단축</th><th class="n">활동 중독 기간(기대)</th></tr>{t6}</table>
<h2>10. 구성 (4.5% 현재가치, B는 명목 총 누계 병기)</h2>
<table class="c sm"><tr><th>구성</th><th class="n">A</th><th class="n">B</th><th class="n">C</th><th class="n">B 총 누계</th></tr>{t7}
<tr class="tot"><td>합계</td>{''.join(f"<td class='n'>{cell(s,'pv45'):.2f}</td>" for s in SN)}<td class='n'>{cell('B 기준','nom'):.2f}</td></tr></table>
<h2>11. 검거 연령별 (B 기준)</h2>
<table class="c sm"><tr><th>검거 연령(대표)</th><th class="n">사범 수</th><th class="n">현재가치 4.5%</th><th class="n">총 누계</th><th class="n">잔여 기대여명(일반 → 중독)</th></tr>{t8}</table>
<div class="box" style="background:var(--navyBg);margin-top:6px"><ul>
<li>기준(B) 1명당 생애비용은 현재가치 {B:.2f}억 원, 명목 총 누계 {cell('B 기준','nom'):.2f}억 원이다. 1년차 비용의 {B/(P['FLOOR']/1e8):.1f}배이다.</li>
<li>가장 큰 몫은 초과 사망의 고통(PGS)과 노동능력 상실이다. 사망 PGS 원단위(교통사고 9.7억 원)와 노동능력 상실 비율이 결과를 가장 크게 움직인다.</li>
<li>16억 원 상한은 C(만성화)의 명목 누계에서만 닿는다. 현재가치로 16억 원이 되려면 활동 중독이 사실상 평생 이어지고 할인율이 0에 가까워야 한다.</li>
<li>참고: 2025년 검거 사범 전원에 B를 곱하면 {23403*B/1e4:,.1f}조 원, λ 10이면 {234030*B/1e4:,.1f}조 원이다. 해마다 새로 생기는 사범의 생애 부담이므로 연간 사회적 비용과 더하지 않는다.</li></ul></div>
<div class="note" style="margin-top:4px"><b>참고문헌</b> 대검찰청(2026). 2025 마약류 범죄백서. · 박성수(2018). 마약류 사용의 사회적 비용 추계. · 통계청(2025. 12. 3.). 2024년 생명표(보도 기준, KOSIS 원표 확인 필요). · 한국교통연구원(2025. 7. 28.). 교통 사망사고 고통 비용 보도자료. · Dennis, M. L., Scott, C. K., Funk, R., &amp; Foss, M. A.(2005). The duration and correlates of addiction and treatment careers. <i>Journal of Substance Abuse Treatment</i>, 28(Suppl. 1), S51–S62. · Stockings, E., et al.(2019). Mortality among people with regular or problematic use of amphetamines: A systematic review and meta-analysis. <i>Addiction</i>, 114(10). doi:10.1111/add.14706. · Lewer, D., Jones, N. R., Hickman, M., Nielsen, S., &amp; Degenhardt, L.(2020). Life expectancy of people who are dependent on opioids: A cohort study in New South Wales, Australia. <i>Journal of Psychiatric Research</i>(2020 게재).</div>
{foot(5)}</section>'''
html=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>2025 원고 반영 재산정</title><style>{css}</style></head><body>{p1}{p2}{p3}{p4}{p5}</body></html>'
open('rep.html','w').write(html)
