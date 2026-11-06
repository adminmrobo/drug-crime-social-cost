import json
d=json.load(open('life.json'))
css=open('/home/claude/y2025/tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
e=lambda x:f"{x/1e4:,.2f}"  # 만원→억
def jo(x):  # 억 → 조/억
    if x>=10000: j=int(x//10000); return f"{j}조 {x-j*10000:,.0f}억"
    return f"{x:,.0f}억"
br=''.join(f'<tr><td>{b[0]}</td><td class="n">{b[1]}년</td><td class="n">{e(b[2])}</td><td class="n">{e(b[3])}</td><td class="n"><b>{e(b[4])}</b></td><td class="n">{e(b[5])}</td><td class="n">{e(b[6])}</td></tr>' for b in d['br'])
sc=''
for s,v in d['sc'].items():
    w=v[0]; cls=' class="hl"' if s.startswith('B') else ''
    sc+=f'<tr{cls}><td>{s}</td>'+''.join(f'<td class="n">{x}%</td>' for x in w)+f'<td class="n">{v[1]:.2f}년</td><td class="n">{e(v[2])}</td><td class="n">{e(v[3])}</td><td class="n"><b>{e(v[4])}</b></td><td class="n">{e(v[5])}</td></tr>'
ag=''
for s,v in d['sc'].items():
    p=v[4]/1e4
    cls=' class="hl"' if s.startswith('B') else ''
    ag+=f'<tr{cls}><td>{s}</td><td class="n">{p:,.2f}억</td><td class="n">{jo(p*23403)}</td><td class="n">{jo(p*234030)}</td><td class="n">{jo(p*668624)}</td></tr>'
B=d['sc']['B 기준']
foot=lambda n:f'<div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 별지 생애비용(2025년 기준)</span><span>{n}</span></div>'
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>생애 사회적 비용</title><style>{css}</style></head><body>
<section class="page">
<div class="kicker">별지 · 2025년 기준 · 2026. 11. 6. 시산</div>
<h1>마약중독자 1명당 생애 사회적 비용<br>기준 시나리오 {e(B[4])}억 원(할인율 4.5%, 30년 상한)</h1>
<h2>1. 전제</h2>
<table>
<tr><th>항목</th><th>설정</th></tr>
<tr><td>연간 비용</td><td>2025년 1명당 사회적 비용 <b>2,231.5만 원</b>(형사사법 1,199.4 · 고통 676.4 · 생산성 330.4 · 의료·복지 25.3만 원). 1명이 발생할 때의 비용을 1년 발생 비용으로 본다</td></tr>
<tr><td>생애비용</td><td>재활기간 T년 동안 매년 같은 실질 비용(2025년 가격)이 발생한다고 보고 현재가치로 합산. PV = 2,231.5만 원 × Σ(t=1~T) 1/(1+r)ᵗ</td></tr>
<tr><td>할인율</td><td>기본 4.5%(본 연구 기준), 민감도 3%·5%. 모든 구간에 같은 할인율 적용</td></tr>
<tr><td>재활기간 구간</td><td>5년 이하 → 5년, 5~10년 → 10년, 10~15년 → 15년, 15년 이상 → 30년(상한). 각 구간 상한을 대표값으로 사용</td></tr>
</table>
<h2>2. 재활기간별 1명당 생애비용 (억 원)</h2>
<table>
<tr><th>재활기간</th><th class="n">대표값</th><th class="n">할인 전</th><th class="n">r 3%</th><th class="n">r 4.5% (기본)</th><th class="n">r 5%</th><th class="n">형사사법 1회만<br>(r 4.5%)</th></tr>{br}
</table>
<div class="note">형사사법 1회만 = 형사사법 1,199.4만 원은 첫해에만, 나머지 1,032.1만 원은 매년 발생한다고 본 민감도. 검거·기소·수용이 매년 반복되지는 않으므로 기본값은 상한 쪽 추정이다.</div>
<h2>3. 재활기간 분포 시나리오별 1명당 생애비용 (억 원)</h2>
<table style="font-size:8.8pt">
<tr><th>시나리오</th><th class="n">5년 이하</th><th class="n">5~10년</th><th class="n">10~15년</th><th class="n">15년 이상</th><th class="n">평균 기간</th><th class="n">할인 전</th><th class="n">r 3%</th><th class="n">r 4.5%</th><th class="n">r 5%</th></tr>{sc}
</table>
<div class="note">A 조기회복: 치료·재활 연계가 잘 되어 절반이 5년 안에 회복. B 기준: 첫 치료 후 지속 회복(1년 이상 단약)까지 중위 9년, 치료 3~4회(Dennis et al., 2005) 근거로 평균 10년 안팎이 되도록 설정. C 만성화: 첫 사용부터 지속 회복까지 중위 27년(같은 연구)을 반영해 15년 이상 비중 35%. 세 분포 모두 연구진 가정이다.</div>
{foot(1)}</section>
<section class="page">
<div class="kicker">별지 · 2025년 기준</div>
<h1>총량 환산과 해석상 유의점</h1>
<h2>4. 2025년 기준 총량 환산 (r 4.5%)</h2>
<table>
<tr><th>시나리오</th><th class="n">1명당</th><th class="n">단속 23,403명</th><th class="n">λ 10 (234,030명)</th><th class="n">λ 28.57 (668,624명)</th></tr>{ag}
</table>
<div class="note">총량 = 1명당 생애비용 × 인원. 현재 사용자 전원이 지금부터 재활기간 동안 비용을 발생시킨다고 볼 때의 값이다. 연간 사회적 비용(λ 10 5조 2,223.7억 원)과는 기준이 달라(연간 횡단 총액 대 생애 누적) 더하지 않는다.</div>
<h2>5. 과거 잠정 생애가치비용 10억 원과의 비교</h2>
<table>
<tr><th>구분</th><th class="n">1명당</th><th class="n">10억 원 대비</th></tr>
<tr><td>30년(상한), 할인 전</td><td class="n">{e(d['br'][3][2])}억 원</td><td class="n">{d['br'][3][2]/1e5*100:.0f}%</td></tr>
<tr><td>30년(상한), r 4.5%</td><td class="n">{e(d['br'][3][4])}억 원</td><td class="n">{d['br'][3][4]/1e5*100:.0f}%</td></tr>
<tr class="hl"><td>B 기준 시나리오, r 4.5%</td><td class="n">{e(B[4])}억 원</td><td class="n">{B[4]/1e5*100:.0f}%</td></tr>
</table>
<div class="note">2025년 연간 1명당 비용으로는 할인하지 않아도 약 45년이 지나야 10억 원에 이른다. 10억 원은 과거 기준 잠정 추계로 참고만 하고, 본 별지는 30년 상한을 둔 위 추계를 쓴다.</div>
<h2>6. 해석상 유의점</h2>
<div class="box" style="background:var(--navyBg);margin-top:2px"><ul>
<li><b>연간 비용의 반복 가정:</b> 형사사법(53.7%)과 사망 고통비용은 1회성 성격이 강하다. 매년 반복으로 보면 생애비용이 과대 쪽이다. 하한은 2절의 "형사사법 1회만" 값으로 본다.</li>
<li><b>재활기간 정의:</b> 재활기간은 비용이 계속 발생하는 기간(사용·재발·치료가 이어지는 기간)으로 본다. 기간 중 단약과 재발이 반복되는 경우는 연간 비용을 평균값으로 처리하였다.</li>
<li><b>분포 근거:</b> 국내 마약중독자 재활기간 분포 자료는 확인되지 않는다. 미국 장기 추적연구(Dennis et al., 2005, 1,271명)를 원용하였다. 서식 8(경과기간별 재복역)과 치료보호 추적자료가 오면 분포를 교체한다.</li>
<li><b>할인율:</b> 구간별로 다른 할인율을 쓰지 않고 4.5%를 일괄 적용하였다. 장기 구간에 체감 할인율(예: 3.5%)을 쓰면 15년 이상 구간 값이 커진다.</li>
<li><b>실질 증가 미반영:</b> 1명당 비용의 실질 증가(2016→2025년 연 약 1.7%)를 반영하지 않았다. 반영하면 할인율이 실질적으로 그만큼 낮아지는 효과가 있다.</li>
</ul></div>
<div class="note" style="margin-top:8px">자료: 본 연구 2025년 기준 시산(1명당 2,231.5만 원), Dennis, M. L., Scott, C. K., Funk, R., &amp; Foss, M. A.(2005). The duration and correlates of addiction and treatment careers. Journal of Substance Abuse Treatment, 28(Suppl 1), S51–S62, 박성수·백민석(2019), 연구진 계산</div>
{foot(2)}</section></body></html>'''
open('life.html','w').write(html)
