import json
d=json.load(open('life3.json')); P=d['param']
css=open('/home/claude/y2025/tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
css+="th.g{text-align:center;border-left:2px solid #fff}td.gl{border-left:2px solid var(--mist)}.bad{color:var(--red);font-weight:700}table.c td{padding:2px 5px}"
e=lambda x:f"{x/1e4:,.2f}"
hit=lambda x:f'<span class="bad">{e(x)}</span>' if x>=1e5 else e(x)
K=['가중 없음','가중 기본','가중 높음']
HDR='''<tr><th rowspan="2">재활기간</th><th rowspan="2" class="n">대표값</th><th colspan="2" class="g">총 누계비용</th><th colspan="3" class="g">현재가치 비용 (실질 할인율)</th></tr>
<tr><th class="n">2025년 가격 고정</th><th class="n">명목(물가·실질증가)</th><th class="n">3%</th><th class="n">4.5% (기본)</th><th class="n">5%</th></tr>'''
def brt(src):
    return '<table class="c">'+HDR+''.join(f'<tr><td>{b[0]}</td><td class="n">{b[1]}년</td><td class="n gl">{e(b[2])}</td><td class="n">{hit(b[3])}</td><td class="n gl">{hit(b[4])}</td><td class="n"><b>{hit(b[5])}</b></td><td class="n">{hit(b[6])}</td></tr>' for b in src)+'</table>'
sc={'A 조기회복':[50,30,15,5],'B 기준':[30,35,20,15],'C 만성화':[15,25,25,35]}
def sct(src):
    r=''
    for s,w in sc.items():
        for k in K:
            v=src[s+'|'+k]; cls=' class="hl"' if (s.startswith('B') and k=='가중 기본') else ''
            r+=f'<tr{cls}><td>{s if k==K[0] else ""}</td><td>{" · ".join(map(str,w)) if k==K[0] else ""}</td><td>{k}</td><td class="n gl">{e(v[0])}</td><td class="n">{hit(v[1])}</td><td class="n gl">{e(v[2])}</td><td class="n"><b>{e(v[3])}</b></td><td class="n">{e(v[4])}</td></tr>'
    return '<table class="c" style="font-size:8.3pt"><tr><th rowspan="2">시나리오</th><th rowspan="2">구간 비중(%)<br>5↓·5~10·10~15·15↑</th><th rowspan="2">장기화 가중</th><th colspan="2" class="g">총 누계비용</th><th colspan="3" class="g">현재가치 비용</th></tr><tr><th class="n">2025 가격</th><th class="n">명목</th><th class="n">3%</th><th class="n">4.5%</th><th class="n">5%</th></tr>'+r+'</table>'
B=d['sc']['B 기준|가중 기본']; BI=d['inmate']['B 기준|가중 기본']
comp_order=['건강·생산성','사망','사건','수용']
def comprow(lab,v):
    r=''
    for i,(m,ml) in enumerate([('fixed','총 누계 · 2025년 가격'),('nom','총 누계 · 명목'),('pv','현재가치 4.5%')]):
        dd=v[5][m]; tot=sum(dd[c] for c in comp_order); cls=' class="hl"' if m=='nom' else ''
        r+=f'<tr{cls}><td>{lab if i==0 else ""}</td><td>{ml}</td>'+''.join(f'<td class="n">{e(dd[c])} ({dd[c]/tot*100:.0f}%)</td>' for c in comp_order)+f'<td class="n"><b>{hit(tot)}</b></td></tr>'
    return r
base_a=[B[0],B[1],B[3]]; base_i=[BI[0],BI[1],BI[3]]
sens=f'<tr class="hl"><td>기준값</td>'+''.join(f'<td class="n{" gl" if j==0 else ""}">{e(x)}</td>' for j,x in enumerate(base_a))+''.join(f'<td class="n{" gl" if j==0 else ""}">{e(x)}</td>' for j,x in enumerate(base_i))+'</tr>'
pairs=[('재범 위험 5%','재범 위험 5%'),('재범 위험 15%','재범 위험 15%'),('재범 시 실형 20%','재범 시 실형 30%'),('재범 시 실형 50%','재범 시 실형 70%'),('실질 증가 0%','실질 증가 0%'),('실질 증가 1%','실질 증가 1%')]
for a,b in pairs:
    lab=a if a==b else f'재범 시 실형 낮음/높음 ({a[-3:]} · {b[-3:]})'
    sens+=f'<tr><td>{lab}</td>'+''.join(f'<td class="n{" gl" if j==0 else ""}">{e(x)}</td>' for j,x in enumerate(d['sens'][a]))+''.join(f'<td class="n{" gl" if j==0 else ""}">{e(x)}</td>' for j,x in enumerate(d['sens_in'][b]))+'</tr>'

foot=lambda n:f'<div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 별지 생애비용(2025년 기준)</span><span>{n}</span></div>'
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>생애 사회적 비용</title><style>{css}</style></head><body>
<section class="page">
<div class="kicker">별지 · 2025년 기준 · 2026. 11. 6. 시산(구조 수정)</div>
<h1>마약중독자 1명당 생애 사회적 비용 (B 기준, 현재가치 4.5%)<br>검거 사범 평균 {e(B[3])}억 원 · 수형자 {e(BI[3])}억 원</h1>
<h2>1. 연간 비용의 성격별 분해 (2025년 1명당 2,231.5만 원)</h2>
<table class="c">
<tr><th>구분</th><th>구성</th><th class="n">금액</th><th>생애비용에서 발생 방식</th></tr>
<tr><td>건강·생산성 반복분</td><td>중독자 고통 · 미취업 · 이환 · 의료·복지</td><td class="n">{P['REP']:,.1f}만 원/년</td><td>재활기간 동안 매년(장기화 가중 w 적용)</td></tr>
<tr><td>사망 기대비용</td><td>사망 고통 · 조기사망 (연 사망 확률 × 1회 비용)</td><td class="n">{P['DTH']:,.1f}만 원/년</td><td>연간 기대값이므로 매년(w 적용, 신체손상 누적 반영)</td></tr>
<tr><td>사건 비용</td><td>경찰 · 검찰 · 법원 · 보호관찰 · 법무병원</td><td class="n">{P['EV']:,.1f}만 원/건</td><td>검거될 때마다 1회. 첫해 검거 1회 + 이후 매년 재범 확률 h × w</td></tr>
<tr class="hl"><td>수용 비용</td><td>실제 복역 {P['SERVE']:.2f}년 × 수용 1인 연간 원가 {P['UC01']:,.1f}만 원</td><td class="n">{P['PRI']:,.1f}만 원/실형</td><td>실형 시 형기 동안 연도별로 나누어 발생. 첫 검거 실형 확률 {P['p1']*100:.1f}%, 재범 시 {P['p2']*100:.0f}%</td></tr>
</table>
<div class="note">첫 검거 실형 확률 {P['p1']*100:.1f}% = 연간 1명당 교도소 비용 411.4만 원 ÷ 실형 1회 수용비({P['PRI']:,.1f}만 원). 평균 실형 2.448년(대검찰청, 2026: 표 3-69), 실제 복역 비율 85%(가정), 수용 1인 연간 원가(UC-01)는 교정 결산 기준. 재범 위험 h = 연 {P['h']*100:.0f}%(김도균·나종민(2025) 미이수 재복역률 50.2%, 추적 5~6.7년에 맞춘 가정). 물가 2.1%(명목 누계만), 실질 증가 1.7%, 실질 할인율 4.5%(민감도 3%·5%), 장기화 가중 w = 1~5년차 1.0, 6~10년차 1.2, 11~15년차 1.5, 16~30년차 2.0(잠정)</div>
<h2>2. 재활기간별 생애비용: 검거 사범 평균 (가중 기본, 억 원)</h2>
{brt(d['br']['가중 기본'])}
<h2>3. 재활기간별 생애비용: 수형자(실형 선고자) 경로 (가중 기본, 억 원)</h2>
{brt(d['inmate']['가중 기본'])}
<div class="note">수형자 경로 = 첫 검거에서 실형(확률 100%), 재범 시 실형 50%(가정). 교정본부 재활 대상 집단에 해당한다. <span class="bad">붉은 숫자</span>는 10억 원 이상</div>
{foot(1)}</section>

<section class="page">
<div class="kicker">별지 · 2025년 기준</div>
<h1>시나리오별 생애비용, 구성, 민감도</h1>
<h2>4. 재활기간 분포 시나리오별 1명당 생애비용: 검거 사범 평균 (억 원)</h2>
{sct(d['sc'])}
<h2>5. 같은 시나리오: 수형자 경로 (억 원)</h2>
{sct(d['inmate'])}
<div class="note">A 조기회복 평균 9.3년, B 기준 12.5년(첫 치료 후 지속 회복까지 중위 9년, Dennis et al., 2005), C 만성화 17.5년(첫 사용부터 지속 회복까지 중위 27년, 같은 연구). 분포·가중은 연구진 잠정 가정</div>
{foot(2)}</section>

<section class="page">
<div class="kicker">별지 · 2025년 기준</div>
<h1>비용 구성, 민감도, 이전 계산과의 비교 (총 누계·현재가치)</h1>
<h2>6. B 기준(가중 기본) 생애비용 구성: 총 누계와 현재가치 (억 원)</h2>
<table class="c"><tr><th>집단</th><th>기준</th><th class="n">건강·생산성</th><th class="n">사망</th><th class="n">사건</th><th class="n">수용</th><th class="n">합계</th></tr>
{comprow('검거 사범 평균',B)}{comprow('수형자 경로',BI)}</table>
<div class="note">총 누계 2025년 가격 = 증가·할인 없이 연도별 비용을 더한 값. 명목 = 물가 2.1%·실질 증가 1.7% 반영. 수형자 경로에서는 수용 비용이 가장 큰 단일 항목이 된다. 장기 수용은 실형을 받은 사람에게 집중되므로 검거 사범 평균에서는 비중이 작다.</div>
<h2>7. 민감도 (B 기준, 가중 기본, 억 원)</h2>
<table class="c" style="font-size:8.4pt"><tr><th rowspan="2">변경 가정</th><th colspan="3" class="g">검거 사범 평균</th><th colspan="3" class="g">수형자 경로</th></tr>
<tr><th class="n">누계 2025 가격</th><th class="n">누계 명목</th><th class="n">현재가치 4.5%</th><th class="n">누계 2025 가격</th><th class="n">누계 명목</th><th class="n">현재가치 4.5%</th></tr>{sens}</table>
<div class="note">기준값: 재범 위험 h 연 10%, 재범 시 실형 30%(검거 사범 평균)·50%(수형자), 실질 증가 1.7%. 재범 시 실형 민감도는 검거 사범 평균 20%·50%, 수형자 30%·70%. 실질 증가율을 바꿔도 2025년 가격 고정 누계는 변하지 않는다.</div>
<h2>8. 이전 계산(연간 비용 매년 반복)과의 비교 (B 기준, 가중 기본)</h2>
<table class="c"><tr><th>방식</th><th class="n">누계 2025 가격</th><th class="n">누계 명목</th><th class="n">현재가치 4.5%</th></tr>
<tr><td>이전: 2,231.5만 원 전체 매년 반복</td><td class="n">2.79</td><td class="n">5.80</td><td class="n">2.69</td></tr>
<tr class="hl"><td>수정: 성격별 분해 (검거 사범 평균)</td><td class="n">{e(B[0])}</td><td class="n">{e(B[1])}</td><td class="n">{e(B[3])}</td></tr>
<tr class="hl"><td>수정: 성격별 분해 (수형자 경로)</td><td class="n">{e(BI[0])}</td><td class="n">{e(BI[1])}</td><td class="n">{e(BI[3])}</td></tr></table>
<div class="note">이전 계산은 경찰·검찰·법원 비용(788.1만 원)이 매년 반복되어 과대였다. 수정 후 사건 비용은 검거 때만, 수용 비용은 실형 시 형기 동안 발생한다.</div>
<h2>9. 1인당 생애비용 10억 원 도달 여부</h2>
<div class="box" style="background:var(--navyBg);margin-top:2px"><ul>
<li><b>명목 총 누계:</b> 15년 이상 구간(30년)에서 도달. 검거 사범 평균 가중 기본 {e(d['br']['가중 기본'][3][3])}억 원, 수형자 경로 {e(d['inmate']['가중 기본'][3][3])}억 원</li>
<li><b>현재가치(4.5%):</b> 어느 구간·시나리오에서도 미도달. 최대는 수형자 경로 30년·가중 높음 {e(d['inmate']['가중 높음'][3][5])}억 원</li>
<li><b>보고서 표현:</b> "약 20년 이상 지속되는 만성 중독자는 명목 누계로 1인당 10억 원을 넘는다"로 제시한다. 대표값은 현재가치 B 기준으로 둔다.</li>
</ul></div>
<div class="note" style="margin-top:6px">자료: 본 연구 2025년 기준 시산, 대검찰청(2026) 마약류 범죄백서 표 3-69, 김도균·나종민(2025), 통계청 소비자물가지수, Dennis, M. L., Scott, C. K., Funk, R., &amp; Foss, M. A.(2005). Journal of Substance Abuse Treatment, 28(Suppl 1), S51–S62, 연구진 계산</div>
{foot(3)}</section></body></html>'''
open('life3.html','w').write(html)
