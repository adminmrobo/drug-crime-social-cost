import json
d=json.load(open('vals.json'));I=d['items'];G=d['groups'];T=d['tot']
css=open('tpl.html').read();css=css[css.index('<style>')+7:css.index('</style>')]
f=lambda x:f"{x:,.1f}"
def ok(x):
    x=round(x,1)
    if x>=10000: j=int(x//10000); return f"{j}조 {x-j*10000:,.1f}"
    return f"{x:,.1f}"
tg={'추계':'<span class="tg e">추계</span>','실측+추계':'<span class="tg m">실측+추계</span>'}
rows=''
for g,v in G.items():
    a=v[0]*10;b=v[3]
    rows+=f'<tr class="hl"><td>{g}</td><td>소계</td><td class="n">{ok(a)}</td><td class="n">{ok(b)}</td><td class="n">+{f(b-a)}</td><td class="n">+{(b/a-1)*100:.1f}%</td><td class="n">{f(v[0]/2.3022)}</td><td class="n">{f(v[2])}</td><td class="n">{(v[2]/(v[0]/2.3022)-1)*100:+.1f}%</td><td></td></tr>'
    for x in I:
        if x[0]!=g: continue
        a=x[2]*10;b=x[5];p0=x[2]/2.3022
        rows+=f'<tr><td></td><td>{x[1]}</td><td class="n">{ok(a)}</td><td class="n">{ok(b)}</td><td class="n">+{f(b-a)}</td><td class="n">+{(b/a-1)*100:.1f}%</td><td class="n">{f(p0)}</td><td class="n">{f(x[4])}</td><td class="n">{(x[4]/p0-1)*100:+.1f}%</td><td>{tg[x[8]]}</td></tr>'
a=T[0]*10;b=T[3]
rows+=f'<tr class="tot"><td>합계</td><td></td><td class="n">{ok(a)}</td><td class="n">{ok(b)}</td><td class="n">+{f(b-a)}</td><td class="n">+{(b/a-1)*100:.1f}%</td><td class="n">{f(T[0]/2.3022)}</td><td class="n">{f(T[2])}</td><td class="n">+{(T[2]/(T[0]/2.3022)-1)*100:.1f}%</td><td></td></tr>'
foot=lambda n:f'<div class="foot"><span>마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 2024년 확정 대 2025년 시산</span><span>{n}</span></div>'
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>2024·2025 비교</title><style>{css}
table.c td{{padding:2.2px 5px}}table.c th{{padding:3px 5px}}.pr{{font-weight:700;color:var(--red)}}</style></head><body>
<section class="page">
<div class="kicker">2024년 확정 대 2025년 시산 · 2026. 11. 6.</div>
<h1>2025년 사회적 비용 5조 2,223.7억 원(λ 10)<br>2024년 대비 +2,013.8억 원(+4.0%)</h1>
<h2>1. 총괄 비교</h2>
<table>
<tr><th>구분</th><th class="n">2024 (확정)</th><th class="n">2025 (시산)</th><th class="n">증감</th></tr>
<tr><td>마약류 단속 인원</td><td class="n">23,022명</td><td class="n">23,403명</td><td class="n">+381명 (+1.65%)</td></tr>
<tr><td>실질 사용자 N* (λ 10)</td><td class="n">230,220명</td><td class="n">234,030명</td><td class="n">+3,810명</td></tr>
<tr><td>암수율 미반영</td><td class="n">5,021.0억 원</td><td class="n">5,222.4억 원</td><td class="n">+201.4억 원</td></tr>
<tr class="hl"><td>사회적 비용 (λ 10, 기본)</td><td class="n">5조 209.9억 원</td><td class="n">5조 2,223.7억 원</td><td class="n">+2,013.8억 원 (+4.0%)</td></tr>
<tr><td>사회적 비용 (λ 28.57, 민감도)</td><td class="n">14조 3,449.7억 원</td><td class="n">14조 9,203.1억 원</td><td class="n">+5,753.4억 원</td></tr>
<tr><td>검거 사범 1명당</td><td class="n">2,181.0만 원</td><td class="n">2,231.5만 원</td><td class="n">+50.5만 원 (+2.3%)</td></tr>
</table>
<div class="seg" style="margin-top:8px"><div style="width:41.3%;background:var(--amber)">단속 인원 증가 830.9억 (41.3%)</div><div style="width:58.7%;background:var(--navy)">1명당 비용 증가 1,182.8억 (58.7%)</div></div>
<div class="note">단속 인원 증가분 = 5조 209.9억 × (1.0165 − 1). 1명당 비용 증가분 = 나머지. 1명당 증가 2.3% 중 실측으로 확인된 것은 검찰(+5.9%)과 교도소(−0.2%)뿐이고, 나머지는 추계 가정(결산 +3.7%, 물가 +2.1%)이 그대로 반영된 값이다.</div>
<h2>2. 항목별 비교 (λ 10, 억 원)</h2>
<table class="c" style="font-size:8.3pt"><tr><th>부문</th><th>세부 항목</th><th class="n">2024</th><th class="n">2025</th><th class="n">증감</th><th class="n">증감률</th><th class="n">1명당 2024<br>(만 원)</th><th class="n">1명당 2025<br>(만 원)</th><th class="n">1명당<br>증감</th><th>2025 구분</th></tr>{rows}</table>
<div class="note">1명당 = 항목 비용(암수율 미반영) ÷ 단속 인원. 교도소는 2025 결산 +1.5%가 단속 증가 +1.65%보다 작아 1명당 비용이 줄었다. <span class="tg m">실측+추계</span> 2025 결산 실측 기반 <span class="tg e">추계</span> 2024 확정치 환산</div>
{foot(1)}</section>

<section class="page">
<div class="kicker">2025년 기준 · 자료 현황</div>
<h1>현재 추정한 자료와 확정 계산에 필요한 자료</h1>
<h2>3. 현재 추정한 자료 (2025년)</h2>
<table class="c" style="font-size:8.5pt">
<tr><th>항목</th><th>추정 대상</th><th>추정값·산식</th><th class="n">비중</th></tr>
<tr><td>경찰</td><td>결산, 전체·마약류 검거 인원</td><td>2024 비용 1,344.0억 × 1.037 × 1.0165 = 1,416.8억</td><td class="n">27.1%</td></tr>
<tr><td>교도소</td><td>마약류 수용자 1일 평균 인원</td><td>63,680명 × 5.67%(2024 비율) = 3,608명</td><td class="n">18.4%</td></tr>
<tr><td>검찰</td><td>전체 처리 인원(분모)</td><td>2024년 1,405,185명 대용</td><td class="n">4.1%</td></tr>
<tr><td>법원</td><td>형사소송 예산, 전체·마약류 사건</td><td>2024 95.6억 × 1.037 × 1.0165 = 100.8억</td><td class="n">1.9%</td></tr>
<tr><td>보호관찰소</td><td>결산, 전체·마약류 접수</td><td>2024 97.0억 × 1.037 × 1.0165 = 102.2억</td><td class="n">2.0%</td></tr>
<tr><td>국립법무병원</td><td>결산, 전체 1일 평균 인원</td><td>2024 9.4억 × 1.037 × 1.0165 = 9.9억</td><td class="n">0.2%</td></tr>
<tr><td>중독자 PGS</td><td>치료보호 인원, 원단위</td><td>875명 × 1.0165 × 1.1억 × 1.021 = 999.0억</td><td class="n">19.1%</td></tr>
<tr><td>사망 PGS</td><td>중독 사망자, 원단위</td><td>58명 × 1.0165 × 9.7억 × 1.021 = 583.9억</td><td class="n">11.2%</td></tr>
<tr><td>생산성 3항목</td><td>사망자·임금·고용·입원일수</td><td>2024 745.1억 × 1.021 × 1.0165 = 773.3억</td><td class="n">14.8%</td></tr>
<tr><td>의료·복지 3항목</td><td>진료 인원·진료비, 복지 예산</td><td>2024 57.0억 × 1.021 × 1.0165 = 59.2억</td><td class="n">1.1%</td></tr>
</table>
<div class="note">1.0165 = 단속 증가(23,403 ÷ 23,022). 1.037 = 형사사법 결산 증가 가정(실측 교정 +1.5%, 검찰 +5.9%). 1.021 = 2025년 소비자물가 상승률. 실측 기반은 교도소 결산·검찰 결산(합계 비중 22.5%)뿐이다.</div>
<h2>4. 확정 계산에 필요한 자료 (우선순위 순)</h2>
<table class="c" style="font-size:8.4pt">
<tr><th style="white-space:nowrap;width:9mm">순위</th><th>필요 자료 (2025년)</th><th>요청처·출처</th><th>2024 값 (참고)</th></tr>
<tr><td class="pr">1</td><td>경찰청 세출 결산 / 전체 검거 인원 / 마약류 검거 인원</td><td>경찰청 (경찰통계연보)</td><td>12조 9,777.1억 / 1,303,656명 / 13,501명</td></tr>
<tr><td class="pr">2</td><td>마약류 수용자 1일 평균 인원 (수형자·미결 구분)</td><td>교정본부</td><td>3,477명 (전체 61,366명)</td></tr>
<tr><td class="pr">3</td><td>치료보호 인원</td><td>대검찰청 (2026 마약류 범죄백서)·보건복지부</td><td>875명</td></tr>
<tr><td class="pr">4</td><td>마약류 중독 사망자 (X40–X44 등, 20~64세 연령별)</td><td>통계청 사망원인통계</td><td>58명</td></tr>
<tr><td>5</td><td>검찰 전체 처리 인원</td><td>대검찰청 (검찰연감)</td><td>1,405,185명</td></tr>
<tr><td>6</td><td>평균 임금·고용률, 마약류 입원 일수</td><td>고용노동부·통계청·심평원</td><td>생산성 745.1억</td></tr>
<tr><td>7</td><td>보호관찰소 결산 / 전체 접수 / 마약류 접수</td><td>범죄예방정책국</td><td>1,933.5억 / 41,643명 / 2,089명</td></tr>
<tr><td>8</td><td>형사소송 관련 예산 / 전체 형사 사건 / 마약류 사건</td><td>법원행정처 (사법연감)</td><td>2,288.1억 / 333,291명 / 13,926명</td></tr>
<tr><td>9</td><td>마약류 중독 진료 인원·진료비, 정신건강·복지 예산</td><td>건강보험심사평가원·보건복지부</td><td>의료·복지 57.0억</td></tr>
<tr><td>10</td><td>국립법무병원 결산 / 전체 1일 평균 인원</td><td>국립법무병원</td><td>445.9억 / 808명 (마약류 2025 연평균 24명 확보)</td></tr>
<tr><td>참고</td><td>고통비용 원단위 2025년 기준</td><td>한국교통연구원</td><td>사망 9.7억 (미공표 시 물가 환산 유지)</td></tr>
</table>
<div class="note">순위는 2025년 총액 비중 기준이다. 1~4순위 자료가 총액의 약 76%를 결정한다. 확보 완료(실측): 단속 23,403명, 교정 결산 1조 6,992.2억, 교정 1일 평균 63,680명, 검찰 결산 1조 2,879.5억, 법무병원 마약류 연평균 24명, 물가 2.1%, 1인당 GNI 5,241.6만 원.</div>
{foot(2)}</section></body></html>'''
open('out/cmp.html','w').write(html)
