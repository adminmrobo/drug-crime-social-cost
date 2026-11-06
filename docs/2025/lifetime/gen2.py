import json
d=json.load(open('life2.json'))
css=open('/home/claude/y2025/tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
css+="th.g{text-align:center;border-left:2px solid #fff}td.gl{border-left:2px solid var(--mist)}.bad{color:var(--red);font-weight:700}"
e=lambda x:f"{x/1e4:,.2f}"
def hit(x): return f'<span class="bad">{e(x)}</span>' if x>=1e5 else e(x)
K=['가중 없음','가중 기본','가중 높음']
def brtab(k):
    r=''
    for b in d['br'][k]:
        r+=f'<tr><td>{b[0]}</td><td class="n">{b[1]}년</td><td class="n gl">{e(b[2])}</td><td class="n">{hit(b[3])}</td><td class="n gl">{hit(b[4])}</td><td class="n"><b>{hit(b[5])}</b></td><td class="n">{hit(b[6])}</td><td class="n">{e(b[7])}</td></tr>'
    return f'''<table><tr><th rowspan="2">재활기간</th><th rowspan="2" class="n">대표값</th><th colspan="2" class="g">총 누계비용</th><th colspan="3" class="g">현재가치 비용 (실질 할인율)</th><th rowspan="2" class="n">형사사법<br>1회만(4.5%)</th></tr>
<tr><th class="n">2025년 가격<br>고정</th><th class="n">명목<br>(물가·실질증가)</th><th class="n">3%</th><th class="n">4.5% (기본)</th><th class="n">5%</th></tr>{r}</table>'''
sc={'A 조기회복':[50,30,15,5],'B 기준':[30,35,20,15],'C 만성화':[15,25,25,35]}
srows=''
for s,w in sc.items():
    for k in K:
        v=d['sc'][s+'|'+k]; cls=' class="hl"' if (s.startswith('B') and k=='가중 기본') else ''
        srows+=f'<tr{cls}><td>{s if k==K[0] else ""}</td><td>{" · ".join(map(str,w)) if k==K[0] else ""}</td><td>{k}</td><td class="n gl">{e(v[0])}</td><td class="n">{hit(v[1])}</td><td class="n gl">{hit(v[2])}</td><td class="n"><b>{hit(v[3])}</b></td><td class="n">{hit(v[4])}</td><td class="n">{e(v[5])}</td></tr>'
B=d['sc']['B 기준|가중 기본']; C=d['sc']['C 만성화|가중 높음']
foot=lambda n:f'<div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 별지 생애비용(2025년 기준)</span><span>{n}</span></div>'
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>생애 사회적 비용</title><style>{css}</style></head><body>
<section class="page">
<div class="kicker">별지 · 2025년 기준 · 2026. 11. 6. 시산(수정)</div>
<h1>마약중독자 1명당 생애 사회적 비용<br>기준 시나리오: 총 누계 {e(B[1])}억 원, 현재가치 {e(B[3])}억 원</h1>
<h2>1. 전제</h2>
<table>
<tr><th style="width:27mm">항목</th><th>설정</th></tr>
<tr><td>연간 비용</td><td>2025년 1명당 <b>2,231.5만 원</b>(형사사법 1,199.4 · 고통 676.4 · 생산성 330.4 · 의료·복지 25.3만 원)을 1년 발생 비용으로 본다</td></tr>
<tr><td>물가상승률 π</td><td><b>2.1%</b>(2025년 소비자물가). 명목 누계비용에만 반영</td></tr>
<tr><td>실질 증가율 g</td><td><b>1.7%</b>: 1명당 비용의 2016→2025년 실질 연평균 증가(1,917.1만 → 2,231.5만 원, 2025년 가격). 누계·현재가치 모두 반영</td></tr>
<tr><td>장기화 가중 w</td><td>재활기간이 길수록 재범·신체손상이 누적되어 연간 비용이 커지는 정도(잠정). 1~5년차 1.0, 6~10년차 1.2, 11~15년차 1.5, 16~30년차 2.0(가중 기본)</td></tr>
<tr><td>할인율 r</td><td><b>실질 4.5%</b>(민감도 3%·5%). 명목으로 환산하면 (1.045 × 1.021) − 1 = 6.69%. 실질 비용을 실질 할인율로 할인한 값과 명목 비용을 명목 할인율로 할인한 값은 같다</td></tr>
<tr><td>산식</td><td>총 누계(명목) = Σ(t=1~T) 2,231.5만 × (1+g)ᵗ⁻¹ × wₜ × (1+π)ᵗ<br>현재가치 = Σ(t=1~T) 2,231.5만 × (1+g)ᵗ⁻¹ × wₜ ÷ (1+r)ᵗ</td></tr>
<tr><td>재활기간</td><td>5년 이하 → 5년, 5~10년 → 10년, 10~15년 → 15년, 15년 이상 → 30년(상한)</td></tr>
</table>
<h2>2. 재활기간별 1명당 생애비용 (가중 기본, 억 원)</h2>
{brtab('가중 기본')}
<div class="note"><span class="bad">붉은 숫자</span>는 10억 원 이상. 2025년 가격 고정 = 연간 비용 × 기간(증가·가중·할인 없음). 형사사법 1회만 = 형사사법 비용은 첫해에만 발생한다고 본 하한 쪽 민감도</div>
<h2>3. 장기화 가중 수준별 비교 (15년 이상 구간, 30년)</h2>
<table>
<tr><th>가중 수준</th><th class="n">1~5 · 6~10 · 11~15 · 16~30년차</th><th class="n">총 누계(명목)</th><th class="n">현재가치 3%</th><th class="n">현재가치 4.5%</th><th class="n">현재가치 5%</th></tr>
{''.join(f'<tr><td>{k}</td><td class="n">{" · ".join(f"{x:.1f}" for x in w)}</td><td class="n">{hit(d["br"][k][3][3])}</td><td class="n">{hit(d["br"][k][3][4])}</td><td class="n">{hit(d["br"][k][3][5])}</td><td class="n">{hit(d["br"][k][3][6])}</td></tr>' for k,w in zip(K,[[1,1,1,1],[1,1.2,1.5,2],[1,1.3,1.8,2.5]]))}
</table>
{foot(1)}</section>

<section class="page">
<div class="kicker">별지 · 2025년 기준</div>
<h1>재활기간 분포 시나리오별 생애비용과 10억 원 도달 조건</h1>
<h2>4. 시나리오 × 가중 수준별 1명당 생애비용 (억 원)</h2>
<table style="font-size:8.6pt">
<tr><th rowspan="2">시나리오</th><th rowspan="2">구간 비중(%)<br>5↓·5~10·10~15·15↑</th><th rowspan="2">장기화 가중</th><th colspan="2" class="g">총 누계비용</th><th colspan="3" class="g">현재가치 비용</th><th rowspan="2" class="n">형사사법<br>1회만</th></tr>
<tr><th class="n">2025 가격</th><th class="n">명목</th><th class="n">3%</th><th class="n">4.5%</th><th class="n">5%</th></tr>{srows}
</table>
<div class="note">A 조기회복: 절반이 5년 안에 회복. B 기준: 첫 치료 후 1년 이상 단약까지 중위 9년, 치료 3~4회(Dennis et al., 2005)를 반영해 평균 12.5년. C 만성화: 첫 사용부터 지속 회복까지 중위 27년(같은 연구)을 반영해 15년 이상 35%. 분포와 가중은 모두 연구진 잠정 가정이다.</div>
<h2>5. 1인당 생애비용 10억 원 도달 조건</h2>
<table>
<tr><th>기준</th><th>10억 원 이상이 되는 경우</th><th>판단</th></tr>
<tr><td>총 누계(명목)</td><td>15년 이상 구간(30년) 전 가중 수준: 12.43~26.20억 원. 시나리오 평균으로는 C 만성화 + 가중 높음 {e(C[1])}억 원. 가중 기본이면 약 20년, 가중 없음이면 약 27년 지속 시 도달</td><td>도달</td></tr>
<tr><td>현재가치(4.5%)</td><td>30년 지속 + 가중 높음도 7.98억 원. 가중 기본이면 53년, 가중 높음이면 40년이 필요</td><td>미도달</td></tr>
<tr><td>현재가치(3%)</td><td>30년 지속 + 가중 높음 10.17억 원</td><td>개별 구간만 도달</td></tr>
</table>
<div class="note">시나리오 평균(분포 가중)으로는 현재가치 기준 최대 {e(C[3])}억 원(C 만성화 + 가중 높음, 4.5%)이다. 1인당 생애비용 10억 원은 <b>명목 총 누계 기준의 장기 지속(약 20년 이상) 사례</b>에 해당하는 값으로 제시하는 것이 자료로 뒷받침되는 범위이다.</div>
{foot(2)}</section>

<section class="page">
<div class="kicker">별지 · 전문가 검토 의견</div>
<h1>생애비용 추계에 대한 검토 의견</h1>
<div class="box" style="background:var(--navyBg)"><ul>
<li><b>① 물가와 할인율의 관계:</b> 4.5%는 실질 사회적 할인율이므로 현재가치에 물가를 더하면 같은 효과를 두 번 빼거나 더하게 된다. 물가는 명목 총 누계에만 반영하고, 현재가치는 실질 기준으로 계산하였다. 따라서 물가 반영으로 현재가치는 달라지지 않는다. 현재가치를 키우는 요인은 실질 증가율 g(1.7%)와 장기화 가중 w이다.</li>
<li><b>② 실질 증가율 1.7%의 지속성:</b> 2016→2025년 실질 증가의 상당 부분은 고통비용 원단위 개정(사망 2.8억 → 9.7억 원)에서 왔다. 원단위 개정은 반복되는 추세라고 보기 어렵다. 보수적으로는 g = 0~1%를 민감도로 둘 필요가 있다.</li>
<li><b>③ 연간 비용의 반복 가정:</b> 1명당 연간 비용의 53.7%가 형사사법, 11.2%가 사망 고통비용이다. 사망은 1회 사건이고, 검거·기소·수용도 매년 반복되지 않는다. 엄밀한 생애비용은 연간 비용을 "매년 반복분(의료·생산성·중독자 고통) + 재범 확률 × 형사사법 + 사망 확률 × (사망 고통·조기사망)"으로 나누어야 한다. 현재 값은 상한 쪽이고, "형사사법 1회만" 값이 하한 쪽이다.</li>
<li><b>④ 장기화 가중의 근거:</b> 재범과 신체손상이 누적된다는 방향은 타당하다. 그러나 1.2·1.5·2.0 배수 자체는 문헌 근거가 확인되지 않는 잠정치이다. ③의 구조로 바꾸면 가중은 "재범 확률 상승"과 "의료비 상승"으로 나뉘어 근거를 붙일 수 있다(서식 8 재복역 자료, 심평원 연령·기간별 진료비).</li>
<li><b>⑤ 사망 위험 미반영:</b> 30년 동안 매년 비용이 발생한다는 가정은 생존을 전제로 한다. 중독자의 초과 사망률을 반영하면 장기 구간 값은 낮아진다. 반대로 사망 시 비용은 ③의 1회 비용으로 들어간다.</li>
<li><b>⑥ 구간 대표값:</b> 구간 상한(5·10·15·30년)을 대표값으로 써서 과대 쪽이다. 중간값(3·7.5·12.5·22.5년)을 쓰면 B 기준 현재가치가 낮아진다.</li>
<li><b>⑦ 10억 원 목표:</b> 목표 금액에 맞추어 가정을 고르면 보고서의 신뢰성이 떨어진다는 우려가 있다. 그러나 10억 원을 "도달 조건"으로 제시하면 이 우려를 피할 수 있다. 본 별지 기준으로 10억 원은 명목 총 누계에서는 약 20년 이상 지속 사례에서 도달하고, 현재가치(4.5%)에서는 30년 안에 도달하지 않는다. 과거 잠정치 10억 원이 명목 누계인지 현재가치인지, 몇 년을 가정했는지 확인해야 비교가 성립한다.</li>
<li><b>⑧ 총량 환산 시 유의:</b> 1명당 생애비용 × 인원은 연간 사회적 비용(λ 10 5조 2,223.7억 원)과 기준이 달라 더하지 않는다. 검거 1명당(λ 반영) 값을 쓰면 10억 원을 쉽게 넘지만, 이는 다른 사용자의 비용을 합친 것이어서 "1인당 생애비용"이 아니다.</li>
</ul></div>
<h2>권고</h2>
<div class="box" style="background:var(--tealBg);margin-top:2px;line-height:1.6">보고서 본문에는 <b>현재가치(실질 4.5%) 기준 B 시나리오 {e(B[3])}억 원</b>을 대표값으로 두고, <b>명목 총 누계 {e(B[1])}억 원</b>을 함께 적는다. 10억 원은 "장기 지속(약 20년 이상) 시 명목 누계로 10억 원을 넘는다"는 문장으로 제시한다. 최종보고 전에는 ③의 구조(반복분·재범 확률·사망 확률)로 연간 비용을 나누어 다시 계산한다.</div>
<div class="note" style="margin-top:8px">자료: 본 연구 2025년 기준 시산, 통계청 소비자물가지수, Dennis, M. L., Scott, C. K., Funk, R., &amp; Foss, M. A.(2005). The duration and correlates of addiction and treatment careers. Journal of Substance Abuse Treatment, 28(Suppl 1), S51–S62, 연구진 계산</div>
{foot(3)}</section></body></html>'''
open('life2.html','w').write(html)
