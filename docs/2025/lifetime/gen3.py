import json
d=json.load(open('life3.json'))
css=open('/home/claude/y2025/tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
css+="th.g{text-align:center;border-left:2px solid #fff}td.gl{border-left:2px solid var(--mist)}.bad{color:var(--red);font-weight:700}.ok{color:var(--teal);font-weight:700}"
e=lambda x:f"{x/1e4:,.2f}"
hit=lambda x:f'<span class="bad">{e(x)}</span>' if x>=1e5 else e(x)
K=['가중 없음','가중 기본','가중 높음']; WV=[[1,1,1,1],[1,1.2,1.5,2],[1,1.3,1.8,2.5]]
nm=['5년 이하','5~10년','10~15년','15년 이상']
r=''
for n,b in zip(nm,d['br']['가중 기본']):
    r+=f'<tr><td>{n}</td><td class="n">{b[0]}년</td><td class="n gl">{e(b[1])}</td><td class="n">{hit(b[2])}</td><td class="n gl">{e(b[3])}</td><td class="n"><b>{e(b[4])}</b></td><td class="n">{e(b[5])}</td><td class="n gl">{e(b[6])}</td></tr>'
br=f'''<table><tr><th rowspan="2">재활기간</th><th rowspan="2" class="n">대표값</th><th colspan="2" class="g">총 누계비용</th><th colspan="3" class="g">현재가치 비용 (실질 할인율)</th><th rowspan="2" class="n g">참고: 매년<br>반복(4.5%)</th></tr>
<tr><th class="n">2025년 가격<br>고정</th><th class="n">명목<br>(물가·실질증가)</th><th class="n">3%</th><th class="n">4.5% (기본)</th><th class="n">5%</th></tr>{r}</table>'''
cmp=''.join(f'<tr><td>{k}</td><td class="n">{" · ".join(f"{x:.1f}" for x in w)}</td><td class="n">{hit(d["br"][k][3][2])}</td><td class="n">{e(d["br"][k][3][3])}</td><td class="n">{e(d["br"][k][3][4])}</td><td class="n">{e(d["br"][k][3][5])}</td><td class="n">{d["yrs"][k][0]}년</td></tr>' for k,w in zip(K,WV))
sc={'A 조기회복':[50,30,15,5],'B 기준':[30,35,20,15],'C 만성화':[15,25,25,35]}
srows=''
for s,w in sc.items():
    for k in K:
        v=d['sc'][s+'|'+k]; cls=' class="hl"' if (s.startswith('B') and k=='가중 기본') else ''
        srows+=f'<tr{cls}><td>{s if k==K[0] else ""}</td><td>{" · ".join(map(str,w)) if k==K[0] else ""}</td><td>{k}</td><td class="n gl">{e(v[0])}</td><td class="n">{hit(v[1])}</td><td class="n gl">{e(v[2])}</td><td class="n"><b>{e(v[3])}</b></td><td class="n">{e(v[4])}</td><td class="n gl">{e(v[5])}</td></tr>'
sens=''.join(f'<tr{" class=\"hl\"" if i==0 else ""}><td>{k}</td><td class="n">{e(v[0])}</td><td class="n">{e(v[1])}</td></tr>' for i,(k,v) in enumerate(d['sens'].items()))
B=d['sc']['B 기준|가중 기본']; Cm=d['sc']['C 만성화|가중 높음']; b30=d['br']['가중 기본'][3]; h30=d['br']['가중 높음'][3]
foot=lambda n:f'<div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 별지 생애비용(2025년 기준)</span><span>{n}</span></div>'
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>생애 사회적 비용</title><style>{css}</style></head><body>
<section class="page">
<div class="kicker">별지 · 2025년 기준 · 2026. 11. 6. 시산(검토 의견 반영)</div>
<h1>마약중독자 1명당 생애 사회적 비용<br>기준 시나리오: 현재가치 {e(B[3])}억 원, 총 누계 {e(B[1])}억 원</h1>
<h2>1. 전제</h2>
<table>
<tr><th style="width:27mm">항목</th><th>설정</th></tr>
<tr><td>연간 비용 구조</td><td>2025년 1명당 2,231.5만 원을 둘로 나눈다. <b>① 매년 반복분 1,032.1만 원</b>(의료·복지 25.3, 생산성 330.4, 고통 676.4. 사망 관련은 연간 사망 확률을 곱한 기대값) <b>② 형사사법 1,199.4만 원</b>: 첫해 1회, 2년차부터는 재범 확률 p를 곱한 값</td></tr>
<tr><td>재범 확률 p</td><td><b>연 14.0%</b>: 3년 내 재복역 36.3%(김도균·나종민, 2025, 2018년 출소자)를 연 단위로 환산. 1 − (1 − 0.363)^(1/3). 재복역 기준이라 재검거보다 낮은 쪽</td></tr>
<tr><td>장기화 가중 w</td><td>재범·신체손상 누적(잠정). 1~5년차 1.0, 6~10년차 1.2, 11~15년차 1.5, 16~30년차 2.0. ① 반복분과 재범 확률 p에 곱한다</td></tr>
<tr><td>실질 증가율 g</td><td><b>1.7%</b>(1명당 비용 2016→2025년 실질 연평균 증가). 민감도 0%·1%</td></tr>
<tr><td>물가상승률 π</td><td><b>2.1%</b>(2025년 소비자물가). 명목 총 누계에만 반영</td></tr>
<tr><td>할인율 r</td><td><b>실질 4.5%</b>(민감도 3%·5%). 명목 환산 시 6.69%. 실질 할인율이므로 현재가치에는 물가를 더하지 않는다</td></tr>
<tr><td>산식</td><td>연간 비용 cₜ = [1,032.1만 × wₜ + 1,199.4만 × (t=1이면 1, 아니면 p × wₜ)] × (1+g)ᵗ⁻¹<br>총 누계(명목) = Σ cₜ × (1+π)ᵗ, 현재가치 = Σ cₜ ÷ (1+r)ᵗ, t = 1~T</td></tr>
</table>
<h2>2. 재활기간별 1명당 생애비용 (가중 기본, 억 원)</h2>
{br}
<div class="note"><span class="bad">붉은 숫자</span>는 10억 원 이상. 참고: 매년 반복 = 직전 별지 방식(형사사법도 매년 발생), 상한 쪽 값</div>
<h2>3. 장기화 가중 수준별 비교 (15년 이상 구간, 30년)</h2>
<table>
<tr><th>가중 수준</th><th class="n">1~5 · 6~10 · 11~15 · 16~30년차</th><th class="n">총 누계(명목)</th><th class="n">현재가치 3%</th><th class="n">현재가치 4.5%</th><th class="n">현재가치 5%</th><th class="n">명목 10억 도달</th></tr>{cmp}
</table>
{foot(1)}</section>

<section class="page">
<div class="kicker">별지 · 2025년 기준</div>
<h1>재활기간 분포 시나리오, 민감도, 10억 원 도달 조건</h1>
<h2>4. 시나리오 × 가중 수준별 1명당 생애비용 (억 원)</h2>
<table style="font-size:8.6pt">
<tr><th rowspan="2">시나리오</th><th rowspan="2">구간 비중(%)<br>5↓·5~10·10~15·15↑</th><th rowspan="2">장기화 가중</th><th colspan="2" class="g">총 누계비용</th><th colspan="3" class="g">현재가치 비용</th><th rowspan="2" class="n g">참고: 매년<br>반복(4.5%)</th></tr>
<tr><th class="n">2025 가격</th><th class="n">명목</th><th class="n">3%</th><th class="n">4.5%</th><th class="n">5%</th></tr>{srows}
</table>
<div class="note">A 조기회복: 절반이 5년 안에 회복. B 기준: 첫 치료 후 1년 이상 단약까지 중위 9년, 치료 3~4회(Dennis et al., 2005)를 반영해 평균 12.5년. C 만성화: 첫 사용부터 지속 회복까지 중위 27년(같은 연구)을 반영해 15년 이상 35%. 분포와 가중은 연구진 잠정 가정이다.</div>
<h2>5. 민감도 (B 기준·가중 기본, 억 원)</h2>
<table><tr><th>변경 조건</th><th class="n">총 누계(명목)</th><th class="n">현재가치 4.5%</th></tr>{sens}</table>
<h2>6. 1인당 생애비용 10억 원 도달 조건</h2>
<table>
<tr><th>기준</th><th>내용</th><th>판단</th></tr>
<tr><td>총 누계(명목)</td><td>30년 지속 + 장기화 가중 시 {e(b30[2])}~{e(h30[2])}억 원. 가중 기본이면 약 {d["yrs"]["가중 기본"][0]}년, 가중 높음이면 약 {d["yrs"]["가중 높음"][0]}년 지속 시 도달. 가중이 없으면 약 {d["yrs"]["가중 없음"][0]}년</td><td class="ok">장기 지속 사례만 도달</td></tr>
<tr><td>현재가치(4.5%)</td><td>30년 지속 + 가중 높음도 {e(h30[4])}억 원. 실질 할인율 4.5%가 실질 증가율 1.7%보다 커서 기간을 늘려도 10억 원에 수렴하지 않는다</td><td class="bad">미도달</td></tr>
<tr><td>시나리오 평균</td><td>최대 C 만성화 + 가중 높음: 명목 누계 {e(Cm[1])}억 원, 현재가치 {e(Cm[3])}억 원</td><td class="bad">미도달</td></tr>
</table>
{foot(2)}</section>

<section class="page">
<div class="kicker">별지 · 검토 의견과 반영 내용</div>
<h1>검토 의견 반영 결과와 보고서 서술안</h1>
<table style="font-size:8.8pt">
<tr><th style="width:38mm">검토 의견</th><th>반영 내용</th></tr>
<tr><td>① 물가와 할인율</td><td>물가는 명목 총 누계에만 반영. 현재가치는 실질 4.5%로 할인</td></tr>
<tr><td>② 실질 증가율 지속성</td><td>g 0%·1% 민감도 추가(5절). 기준 현재가치 {e(B[3])}억 → g 0%면 {e(d["sens"]["실질 증가 g 0%"][1])}억 원</td></tr>
<tr><td>③ 연간 비용 반복 가정</td><td>형사사법을 첫해 1회 + 재범 확률(연 14.0%)로 바꿈. 사망 관련은 연간 사망 확률 기대값이라 매년 반영 유지. 기준 현재가치 2.69억 → {e(B[3])}억 원</td></tr>
<tr><td>④ 장기화 가중 근거</td><td>가중을 반복분(의료·생산성 손상 누적)과 재범 확률 상승에 나누어 적용. 배수는 잠정치로 명시</td></tr>
<tr><td>⑤ 사망 위험</td><td>연간 사망 확률(0.25%)이 낮아 생존 가중의 영향은 작다. 사망 비용은 기대값으로 반영</td></tr>
<tr><td>⑥ 구간 대표값</td><td>중간값(3·7.5·12.5·22.5년) 민감도 추가: 현재가치 {e(d["sens"]["구간 중간값(3·7.5·12.5·22.5년)"][1])}억 원</td></tr>
<tr><td>⑦ 10억 원 목표</td><td>추계값이 아니라 "도달 조건"으로 제시(6절)</td></tr>
<tr><td>⑧ 총량 환산</td><td>연간 사회적 비용과 합산하지 않음. 검거 1명당(λ 반영) 값은 1인당 생애비용으로 쓰지 않음</td></tr>
</table>
<h2>보고서 서술안</h2>
<div class="box" style="background:var(--tealBg);margin-top:2px;line-height:1.7;font-size:9.6pt">
마약중독자 1명의 생애 사회적 비용은 현재가치 기준 {e(B[3])}억 원으로 추계하였다(2025년 가격, 실질 할인율 4.5%, 기준 시나리오). 같은 조건의 명목 총 누계비용은 {e(B[1])}억 원이다. 연간 비용은 매년 반복분 1,032.1만 원과 형사사법비용 1,199.4만 원으로 나누고, 형사사법비용은 첫해 1회와 이후 재범 확률(연 14.0%)만큼 반영하였다. 재활기간 분포는 조기회복·기준·만성화의 세 시나리오로 두었으며, 현재가치는 {e(d["sc"]["A 조기회복|가중 기본"][3])}억~{e(d["sc"]["C 만성화|가중 기본"][3])}억 원이다. 재활기간이 30년에 이르고 재범·신체손상이 누적되면 명목 총 누계비용은 {e(b30[2])}억 원으로 10억 원을 넘는다. 다만 재활기간 분포와 장기화 가중은 국내 자료로 확인되지 않은 잠정 가정이다.
</div>
<h2>남은 확인 사항</h2>
<div class="note" style="font-size:8.8pt;color:var(--ink);line-height:1.6">· 과거 잠정치 10억 원의 산정 기준(명목 누계 또는 현재가치, 가정 기간) · 재범 확률: 서식 8(경과기간별 재복역) 회신 시 교체 · 재활기간 분포: 치료보호·재활 추적자료 확보 시 교체 · 장기화 가중: 심평원 기간별 진료비로 근거 보완</div>
<div class="note" style="margin-top:8px">자료: 본 연구 2025년 기준 시산, 김도균·나종민(2025), 통계청 소비자물가지수, Dennis, M. L., Scott, C. K., Funk, R., &amp; Foss, M. A.(2005). The duration and correlates of addiction and treatment careers. Journal of Substance Abuse Treatment, 28(Suppl 1), S51–S62, 연구진 계산</div>
{foot(3)}</section></body></html>'''
open('life3.html','w').write(html)
