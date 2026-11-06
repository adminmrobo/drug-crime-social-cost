import json
d=json.load(open('life3.json')); P=d['p']
css=open('/home/claude/y2025/tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
css+="th.g{text-align:center;border-left:2px solid #fff}td.gl{border-left:2px solid var(--mist)}.bad{color:var(--red);font-weight:700}"
e=lambda x:f"{x/1e4:,.2f}"
hit=lambda x: f'<span class="bad">{e(x)}</span>' if x>=1e5 else e(x)
K=['가중 없음','가중 기본','가중 높음']
def brtab(k):
    r=''
    for b in d['br'][k]:
        c=b[6]; r+=f'<tr><td>{b[0]}</td><td class="n">{b[1]}년</td><td class="n gl">{hit(b[2])}</td><td class="n gl">{e(b[3])}</td><td class="n"><b>{e(b[4])}</b></td><td class="n">{e(b[5])}</td><td class="n gl">{e(c["cj"])}</td><td class="n">{e(c["rep"])}</td><td class="n">{e(c["rc"])}</td><td class="n">{e(c["dth"])}</td></tr>'
    return f'''<table style="font-size:8.6pt"><tr><th rowspan="2">재활기간</th><th rowspan="2" class="n">대표값</th><th class="g">총 누계비용</th><th colspan="3" class="g">현재가치 비용 (실질 할인율)</th><th colspan="4" class="g">현재가치 구성 (4.5%)</th></tr>
<tr><th class="n">명목</th><th class="n">3%</th><th class="n">4.5%</th><th class="n">5%</th><th class="n">최초<br>형사사법</th><th class="n">매년<br>반복분</th><th class="n">재복역<br>(장기수용)</th><th class="n">사망</th></tr>{r}</table>'''
sc={'A 조기회복':[50,30,15,5],'B 기준':[30,35,20,15],'C 만성화':[15,25,25,35]}
srows=''
for s,w in sc.items():
    for k in K:
        v=d['sc'][s+'|'+k]; cls=' class="hl"' if (s.startswith('B') and k=='가중 기본') else ''
        srows+=f'<tr{cls}><td>{s if k==K[0] else ""}</td><td>{" · ".join(map(str,w)) if k==K[0] else ""}</td><td>{k}</td><td class="n gl">{hit(v[0])}</td><td class="n gl">{e(v[1])}</td><td class="n"><b>{e(v[2])}</b></td><td class="n">{e(v[3])}</td><td class="n gl">{e(v[4])}</td></tr>'
B=d['sc']['B 기준|가중 기본']; Bc=[b[6] for b in d['br']['가중 기본']]
foot=lambda n:f'<div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 별지 생애비용(2025년 기준)</span><span>{n}</span></div>'
b30=d['br']['가중 기본'][3]
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>생애 사회적 비용</title><style>{css}</style></head><body>
<section class="page">
<div class="kicker">별지 · 2025년 기준 · 2026. 11. 6. 시산(구조 수정)</div>
<h1>마약중독자 1명당 생애 사회적 비용<br>기준 시나리오: 총 누계 {e(B[0])}억 원, 현재가치 {e(B[2])}억 원</h1>
<h2>1. 비용 구조와 전제</h2>
<table style="font-size:8.9pt">
<tr><th style="width:30mm">구성</th><th>산식 (2025년 1명당, 만 원)</th><th class="n">연간 기대값</th></tr>
<tr><td>① 최초 형사사법</td><td>첫해 1회. 경찰·검찰·법원·보호관찰·법무병원 + 교도소 기대 수용비 411.4</td><td class="n">1,199.4 (1회)</td></tr>
<tr><td>② 매년 반복분</td><td>의료·복지 25.3 + 이환 7.1 + 미취업 153.0 + 중독자 고통비용 426.9, × 장기화 가중 wₜ</td><td class="n">612.3 × wₜ</td></tr>
<tr><td>③ 재복역(장기수용)</td><td>연 재복역 확률 h {P["h"]*100:.1f}% × wₜ × 재복역 1건 {P["CR"]:,.1f}<br>1건 = 실형 2.45년 × 복역 85% × 수용 원가 + 검찰(5,036) + 경찰 605.4 + 법원 43.1 + 보호관찰 43.7</td><td class="n">{P["h"]*P["CR"]:,.1f} × wₜ</td></tr>
<tr><td>④ 사망</td><td>연 사망 확률 {P["q"]*100:.2f}% × 사망 1건 {P["DC"]/1e4:.2f}억(고통비용 9.90억 + 조기사망 6.76억). 생존자에게만 ②·③ 발생</td><td class="n">{P["q"]*P["DC"]:,.1f}</td></tr>
</table>
<div class="note">h = 1 − (1 − 0.363)^(1/3): 2018년 출소자 3년 내 재복역 36.3%(김도균·나종민, 2025)의 연 환산. wₜ = 1~5년차 1.0, 6~10년차 1.2, 11~15년차 1.5, 16~30년차 2.0(가중 기본, 잠정). 재복역 확률 × wₜ의 상한은 연 60%. 물가 π 2.1%는 명목 누계에만, 실질 증가율 g 1.7%는 누계·현재가치 모두 반영. 할인율은 실질 4.5%(민감도 3%·5%). 재활기간 대표값: 5·10·15·30년(상한)</div>
<h2>2. 재활기간별 1명당 생애비용 (가중 기본, 억 원)</h2>
{brtab('가중 기본')}
<div class="note"><span class="bad">붉은 숫자</span>는 10억 원 이상. 30년 지속 시 현재가치 {e(b30[4])}억 원 중 재복역(장기수용)이 {b30[6]["rc"]/b30[4]*100:.0f}%로 가장 크다.</div>
<h2>3. 장기화 가중 수준별 비교 (30년, 억 원)</h2>
<table>
<tr><th>가중 수준</th><th class="n">1~5 · 6~10 · 11~15 · 16~30년차</th><th class="n">총 누계(명목)</th><th class="n">현재가치 3%</th><th class="n">현재가치 4.5%</th><th class="n">현재가치 5%</th></tr>
{''.join(f'<tr><td>{k}</td><td class="n">{" · ".join(f"{x:.1f}" for x in w)}</td><td class="n">{hit(d["br"][k][3][2])}</td><td class="n">{e(d["br"][k][3][3])}</td><td class="n">{e(d["br"][k][3][4])}</td><td class="n">{e(d["br"][k][3][5])}</td></tr>' for k,w in zip(K,[[1,1,1,1],[1,1.2,1.5,2],[1,1.3,1.8,2.5]]))}
</table>
{foot(1)}</section>

<section class="page">
<div class="kicker">별지 · 2025년 기준</div>
<h1>재활기간 분포 시나리오별 생애비용과 10억 원 도달 조건</h1>
<h2>4. 시나리오 × 가중 수준별 1명당 생애비용 (억 원)</h2>
<table style="font-size:8.6pt">
<tr><th rowspan="2">시나리오</th><th rowspan="2">구간 비중(%)<br>5↓·5~10·10~15·15↑</th><th rowspan="2">장기화 가중</th><th class="g">총 누계</th><th colspan="3" class="g">현재가치 비용</th><th class="g">재복역 제외</th></tr>
<tr><th class="n">명목</th><th class="n">3%</th><th class="n">4.5%</th><th class="n">5%</th><th class="n">4.5%</th></tr>{srows}
</table>
<div class="note">A 조기회복: 절반이 5년 안에 회복. B 기준: 첫 치료 후 1년 이상 단약까지 중위 9년, 치료 3~4회(Dennis et al., 2005)를 반영해 평균 12.5년. C 만성화: 첫 사용부터 지속 회복까지 중위 27년(같은 연구)을 반영해 15년 이상 35%. 재복역 제외 = ③을 뺀 값으로, 장기수용이 생애비용에 더하는 몫을 보여 준다.</div>
<h2>5. 1인당 생애비용 10억 원 도달 조건</h2>
<table>
<tr><th>기준</th><th>10억 원 이상이 되는 경우</th><th>판단</th></tr>
<tr><td>총 누계(명목)</td><td>30년 지속 시 가중 없음 {e(d["br"]["가중 없음"][3][2])}억 · 기본 {e(b30[2])}억 · 높음 {e(d["br"]["가중 높음"][3][2])}억 원. 가중 기본이면 24년, 가중 높음이면 22년 지속 시 도달</td><td>장기 지속 사례 도달</td></tr>
<tr><td>현재가치(4.5%)</td><td>30년 지속 + 가중 높음도 {e(d["br"]["가중 높음"][3][4])}억 원. 지속기간을 늘려도 사망·할인으로 10억 원에 이르지 않음</td><td>미도달</td></tr>
<tr><td>시나리오 평균</td><td>현재가치 최대 {e(d["sc"]["C 만성화|가중 높음"][2])}억 원, 명목 최대 {e(d["sc"]["C 만성화|가중 높음"][0])}억 원(C 만성화 + 가중 높음)</td><td>미도달</td></tr>
</table>
<div class="note">재복역·사망을 확률로 나누고 생존을 반영하면서, 형사사법 매년 반복 가정(이전 판)보다 장기 구간 현재가치가 다소 낮아졌다. 장기수용 비용은 ③으로 반영되어 30년 지속 시 가장 큰 구성 요소이다.</div>
{foot(2)}</section>

<section class="page">
<div class="kicker">별지 · 검토 의견</div>
<h1>생애비용 추계에 대한 검토 의견</h1>
<div class="box" style="background:var(--navyBg)"><ul>
<li><b>① 장기수용 비용:</b> 최초 검거 시 수용비는 연간 비용의 교도소 기대값(411.4만 원)으로 ①에 들어가 있다. 재활기간 중 재범으로 다시 수용되는 비용은 ③ 재복역 1건 {P["CR"]:,.1f}만 원(실형 2.45년 × 복역 85% 포함)으로 반영하였다. 장기 지속 구간일수록 ③이 커진다.</li>
<li><b>② 재복역 확률의 적용 범위:</b> 연 {P["h"]*100:.1f}%는 출소자 기준이다. 최초 검거 후 실형을 받지 않은 사람에게 그대로 쓰면 ③이 과대 쪽이다. 서식 8(경과기간별 재복역)이 오면 출소자·비수용자를 나누어 다시 계산한다.</li>
<li><b>③ 물가와 할인율:</b> 4.5%는 실질 할인율이므로 물가는 명목 누계에만 반영하였다. 현재가치를 키우는 요인은 실질 증가율 g(1.7%)와 장기화 가중 wₜ이다.</li>
<li><b>④ 실질 증가율 1.7%의 지속성:</b> 2016→2025년 증가의 상당 부분은 고통비용 원단위 개정(사망 2.8억 → 9.7억 원)에서 왔다. g = 0~1%를 민감도로 둘 필요가 있다.</li>
<li><b>⑤ 장기화 가중의 근거:</b> 1.2·1.5·2.0 배수는 문헌 근거가 확인되지 않는 잠정치이다. 재범 확률 상승은 서식 8, 의료비 상승은 심평원 기간별 진료비로 근거를 보완한다.</li>
<li><b>⑥ 중독자 고통비용의 반복:</b> 중독자 고통비용(1.1억 원 × 치료보호 인원 ÷ 검거 인원)을 매년 반복분으로 넣었다. 고통비용이 1회 평가값인지 연간 값인지에 따라 ②가 크게 달라진다. 원 자료(한국교통연구원 중상 고통비용)는 1회 평가값이어서 반복 적용은 상한 쪽이다.</li>
<li><b>⑦ 구간 대표값:</b> 구간 상한(5·10·15·30년)을 써서 과대 쪽이다.</li>
<li><b>⑧ 10억 원 목표:</b> 목표 금액에 맞추어 가정을 고르면 신뢰성이 떨어진다는 우려가 있다. 그러나 "도달 조건"으로 제시하면 이를 피할 수 있다. 본 별지 기준으로 10억 원은 명목 누계로 22~24년 이상 지속 사례에서 도달한다. 과거 잠정치 10억 원의 기준(명목·현재가치, 기간)을 확인해야 비교가 성립한다.</li>
<li><b>⑨ 총량 환산:</b> 1명당 생애비용 × 인원은 연간 사회적 비용과 기준이 달라 더하지 않는다.</li>
</ul></div>
<h2>권고</h2>
<div class="box" style="background:var(--tealBg);margin-top:2px;line-height:1.6">본문 대표값은 <b>현재가치(실질 4.5%) B 기준 {e(B[2])}억 원</b>, 병기값은 <b>명목 총 누계 {e(B[0])}억 원</b>으로 한다. 10억 원은 "재활이 20년 이상 이어지는 만성 사례는 명목 누계로 10억 원을 넘는다"로 제시한다. 서식 8 회신 후 ③의 재복역 확률을, 원자료 확인 후 ⑥의 반복 여부를 확정한다.</div>
<div class="note" style="margin-top:8px">자료: 본 연구 2025년 기준 시산, 김도균·나종민(2025), 2025 마약류 범죄백서(평균 실형), 통계청 소비자물가지수, Dennis, M. L., Scott, C. K., Funk, R., &amp; Foss, M. A.(2005). Journal of Substance Abuse Treatment, 28(Suppl 1), S51–S62, 연구진 계산</div>
{foot(3)}</section></body></html>'''
open('life3.html','w').write(html)
