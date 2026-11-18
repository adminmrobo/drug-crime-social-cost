# 생애가치 B/C · 정책 제언 별지 섹션 (gen.py, gen_report.py 공용)
import json
d = json.load(open('/home/claude/cba/cba.json')); r = d['res']; E = d['EFF']; EN = list(E)
PN = ['3년 한정', '5년 반감', '평생 유지']
DC = d['DC']

def bc(s, b, p, e): return r[f'{s}|{b}|{p}|{e}']['BC']
def cell(p, e): return f"{bc('B 기준','nom',p,e):.2f} ({bc('B 기준','pv',p,e):.2f})"
def es(p): return f"{r[f'B 기준|nom|{p}|estar']*100:.1f}% ({r[f'B 기준|pv|{p}|estar']*100:.1f}%)"

REFS = ("기획재정부(2017. 8. 11.). 예비타당성조사 사회적 할인율 4.5%로 인하 보도자료. · "
        "김도균·나종민(2025). 형사정책연구, 36(1), 65–99. · "
        "Cohen, M. A., &amp; Piquero, A. R.(2009). New evidence on the monetary value of saving a high risk youth. <i>Journal of Quantitative Criminology</i>, 25(1), 25–49. · "
        "Ettner, S. L., Huang, D., Evans, E., Ash, D. R., Hardy, M., Jourabchi, M., &amp; Hser, Y.-I.(2006). Benefit–cost in the California Treatment Outcome Project: Does substance abuse treatment \"pay for itself\"? <i>Health Services Research</i>, 41(1), 192–213. · "
        "Inciardi, J. A., Martin, S. S., &amp; Butzin, C. A.(2004). Five-year outcomes of therapeutic community treatment of drug-involved offenders after release from prison. <i>Crime &amp; Delinquency</i>, 50(1), 88–107. · "
        "Mitchell, O., Wilson, D. B., &amp; MacKenzie, D. L.(2006). The effectiveness of incarceration-based drug treatment on criminal behavior. <i>Campbell Systematic Reviews</i>, 2006:11. · "
        "National Institute on Drug Abuse(2006. 7. 24.). Principles of drug abuse treatment for criminal justice populations: A research-based guide. · "
        "Washington State Institute for Public Policy(2023). Benefit-cost results: Therapeutic communities for individuals with substance use disorders (incarceration).")

def pages(n1, n2, foot_a, foot_b, title_suffix=''):
    rows = ''.join(f"<tr{' class=\"tot\"' if p=='5년 반감' else ''}><td>{p}{' (기준)' if p=='5년 반감' else ''}</td>" + ''.join(f"<td class='n'>{cell(p,e)}</td>" for e in EN) + f"<td class='n'>{es(p)}</td></tr>" for p in PN)
    sens = ''.join(f"<tr><td>{lab}</td>" + ''.join(f"<td class='n'>{bc(s,b,'5년 반감',e):.2f}</td>" for e in EN) + "</tr>"
                   for lab, s, b in [('A 조기회복 (현재가치 4.5%)', 'A 조기회복', 'pv'), ('B 기준 (현재가치 4.5%)', 'B 기준', 'pv'), ('C 만성화 (현재가치 4.5%)', 'C 만성화', 'pv'), ('B 기준, 할인율 3%', 'B 기준', 'pv3'), ('B 기준, 할인율 5%', 'B 기준', 'pv5')])
    fut_n = r['B 기준|nom|future']/1e8; fut_p = r['B 기준|pv|future']/1e8
    o = lambda b, e: r[f'B 기준|{b}|5년 반감|{e}']
    coh = lambda b, e: o(b, e)['NPV']*1545/1e8
    lit = [
        ('Cohen &amp; Piquero(2009)', '고위험 청소년 1명의 생애 외부비용. 중증 약물사용자 84만~110만 달러(14세 시점 현재가치)', '생애가치 편익 개념'),
        ('Mitchell 외(2006)', '교정시설 약물치료 66개 평가 메타분석. 재범 OR 1.37(35%→28%), 치료공동체 1.38', '국외 효과 20%'),
        ('김도균·나종민(2025)', '국내 마약류사범 재범 감소 효과(상대 19.2%)', '국내 효과 19.2%'),
        ('Inciardi 외(2004)', '교정 치료공동체 후 출소 사후관리 5년 추적. 수료자의 재체포·약물사용이 낮음', '효과 지속 근거'),
        ('WSIPP(2023)', '교정시설 치료공동체 B/C 9.56, 순편익 10,429달러', '결과 비교'),
        ('Ettner 외(2006)', '치료비 1,583달러 대비 편익 11,487달러(약 7:1)', '결과 비교'),
        ('NIDA(2006)', '치료 1달러당 범죄 관련 비용 4~7달러 절감, 치료 연속성 강조', '결과 비교·제언'),
        ('기획재정부(2017)', '사회적 할인율 5.5% → 4.5%', '현재가치 할인'),
    ]
    lt = ''.join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in lit)
    pa = f"""<section class="page">
<h2>{n1}. 생애가치 기준 교정 재활 비용편익{title_suffix}</h2>
<div class="box" style="background:var(--navyBg)"><ul>
<li><b>모형:</b> 편익 B = e × Σ<sub>t≥1</sub> w(t) × C(t). C(t)는 1인당 생애비용(B 시나리오)의 t년차 비용이고, 1년차 이후 합계는 누적 {fut_n:.2f}억 원(현재가치 {fut_p:.2f}억 원)이다. 비용 ΔC는 {DC/1e4:,.1f}만 원으로 재복역 1건 기준과 같다.</li>
<li><b>효과 e(상대 감소):</b> 관측 {E[EN[0]]*100:.1f}%(교정본부 자료, 2.87%p ÷ 34.5%, 유의하지 않음), 국내 문헌 19.2%(김도균·나종민, 2025), 국외 메타분석 20%(Mitchell 외, 2006).</li>
<li><b>지속 w(t):</b> 3년 한정(재복역 추적 기간), 5년 반감(기준), 평생 유지(상한 참고). 할인율 4.5%(기획재정부, 2017).</li>
<li>재복역 1건 기준 B/C 0.22~0.28은 출소 후 3년 재복역만 본 하한이다. 생애가치 기준은 효과가 남은 생애의 중독 관련 비용을 같은 비율로 줄인다고 본다.</li></ul></div>
<table class="c sm" style="margin-top:6px"><tr><th>B/C: 누적 기준 (현재가치)</th>{''.join(f"<th class='n'>{x}</th>" for x in ['관측 8.3%','국내 19.2%','국외 20%','손익분기 e*'])}</tr>{rows}</table>
<table class="c sm" style="margin-top:6px"><tr><th>민감도 (5년 반감)</th><th class="n">관측</th><th class="n">국내</th><th class="n">국외</th></tr>{sens}</table>
<div class="box" style="background:var(--navyBg);margin-top:6px"><ul>
<li>효과가 5년마다 절반으로 줄어도 관측 효과로 B/C {bc('B 기준','nom','5년 반감',EN[0]):.2f}(현재가치 {bc('B 기준','pv','5년 반감',EN[0]):.2f})이다. 손익분기 효과는 {es('5년 반감')}이다.</li>
<li>이수자 1인당 순편익(5년 반감)은 관측 효과 {o('nom',EN[0])['NPV']/1e4:,.1f}만 원(현재가치 {o('pv',EN[0])['NPV']/1e4:,.1f}만 원)이다. 2025년 이수 1,545명 기준 {coh('nom',EN[0]):,.1f}억 원(현재가치 {coh('pv',EN[0]):,.1f}억 원), 국외 효과로는 {coh('nom',EN[2]):,.1f}억 원(현재가치 {coh('pv',EN[2]):,.1f}억 원)이다.</li>
<li>효과가 3년에 그치면 관측 효과의 현재가치 B/C는 {bc('B 기준','pv','3년 한정',EN[0]):.2f}로 손익분기에 가깝다. 만성화 위험이 높은 C 시나리오는 {bc('C 만성화','pv','5년 반감',EN[0]):.2f}, 조기회복 A는 {bc('A 조기회복','pv','5년 반감',EN[0]):.2f}이다.</li>
<li><b>전제와 한계:</b> 관측 효과는 통계적으로 유의하지 않다. 효과가 모든 중독 관련 비용에 같은 비율로 미친다고 가정하였다. 판정은 현재가치 기준으로 한다.</li></ul></div>
<table class="c sm" style="margin-top:6px"><tr><th>선행연구·기준</th><th>내용</th><th>활용</th></tr>{lt}</table>
<div class="note">국외 결과(WSIPP 9.56, Ettner 외 약 7, NIDA 4~7)와 비교하면 현재가치 B/C {bc('B 기준','pv','5년 반감',EN[0]):.2f}~{bc('B 기준','pv','5년 반감',EN[2]):.2f}는 보수적인 범위이다. 국외 값은 통화·연도·편익 범위가 달라 직접 비교할 수 없고 방향만 참고한다.</div>
{foot_a}</section>"""
    pol = [
        ('1. 출소 전후 연속 처우', f"효과 3년 한정 B/C {cell('3년 한정',EN[0])} → 5년 반감 {cell('5년 반감',EN[0])}",
         ['교정 재활, 출소, 지역사회 치료를 한 사례 경로로 잇는다.', '출소 전후 일정 기간을 전환 구간으로 정해 지역 치료기관에 직접 인계한다.', '인계에 필요한 최소 정보만 본인 동의를 받아 공유한다.']),
        ('2. 효과 측정과 성과관리', '관측 효과 2.9%p, 95% CI −6.0~11.7%p(비교군 116명)',
         ['교육 지정자 가운데 비교군을 두는 평가 설계를 도입한다.', '재복역 외에 재검거, 치료 유지, 취업을 공동 성과지표로 둔다.', '교정·보호관찰·치료기관 자료를 개인 단위로 연계해 추적한다.']),
        ('3. 고위험군 우선 배정', f"현재가치 B/C(관측) A {bc('A 조기회복','pv','5년 반감',EN[0]):.2f} · B {bc('B 기준','pv','5년 반감',EN[0]):.2f} · C {bc('C 만성화','pv','5년 반감',EN[0]):.2f}",
         ['만성화 위험이 높을수록 줄일 수 있는 생애비용이 크다.', '위험·욕구 평가로 과정 강도를 정하고 고위험군을 우선 배정한다.', '집중·심화 과정 이수자의 사후관리를 강화한다.']),
        ('4. 재활 규모 확대', f"손익분기 효과 {es('5년 반감')}",
         ['낮은 손익분기 효과를 고려해 이수 인원을 단계적으로 늘린다.', '확대와 평가를 함께 설계해 효과가 확인되는 과정부터 넓힌다.', '중도탈락(3.4%) 사유를 관리한다.']),
        ('5. 치료 지향 보호관찰', '출소 후 감독이 치료 유지로 이어져야 효과가 남는다',
         ['출소 후 위험·욕구를 다시 평가해 감독 강도와 치료 수준을 맞춘다.', '약물검사 양성은 제재에 앞서 치료 연계의 계기로 쓴다.', '마약류 전담 보호관찰 인력과 교육을 늘린다.']),
        ('6. 지역사회 수용 능력', '연속 처우의 받침: 주거, 치료, 동료 지원',
         ['출소자가 머물며 치료를 이어 갈 중간 단계의 회복 주거를 확충한다.', '치료보호 기관의 인력·병상과 진료 보상을 현실화한다.', '회복 경험자의 동료 지원과 민간 단체 연계를 제도화한다.']),
        ('7. 법적 근거와 부처 협력', '교정·보호관찰·보건복지·지자체가 한 경로를 공유',
         ['기관 간 인계와 정보 공유의 법적 근거를 둔다.', '부처 간 조정 협의체와 공동 예산·성과관리를 운영한다.', '수사·재판 초기에 치료 필요를 선별해 치료 연계를 넓힌다.']),
    ]
    pt = ''.join(f"<tr><td><b>{a}</b><div class='sm' style='color:#6B7A90'>{b}</div></td><td><ul style='margin:0;padding-left:14px'>{''.join(f'<li>{x}</li>' for x in c)}</ul></td></tr>" for a, b, c in pol)
    pb = f"""<section class="page">
<h2>{n2}. 정책 제언</h2>
<div class="box" style="background:var(--navyBg)"><ul>
<li>생애가치 기준 B/C는 효과의 지속 기간에 가장 민감하다(관측 효과 현재가치 3년 한정 {bc('B 기준','pv','3년 한정',EN[0]):.2f} → 5년 반감 {bc('B 기준','pv','5년 반감',EN[0]):.2f} → 평생 유지 {bc('B 기준','pv','평생 유지',EN[0]):.2f}). 제언 1~4는 이 결과에서 나온 교정시설 안의 과제이다.</li>
<li>제언 5~7은 그 효과가 출소 뒤에도 남도록 하는 지역사회의 조건이다. 교정시설 치료에 출소 후 사후관리가 더해질 때 재범 감소가 크다는 국외 연구와 같은 방향이다(Inciardi 외, 2004; Mitchell 외, 2006; NIDA, 2006).</li></ul></div>
<table class="c" style="margin-top:6px"><tr><th style="width:36%">제언 · 근거</th><th>과제</th></tr>{pt}</table>
<div class="note" style="margin-top:6px"><b>참고문헌(비용편익·정책 제언)</b> {REFS}</div>
{foot_b}</section>"""
    return pa, pb
