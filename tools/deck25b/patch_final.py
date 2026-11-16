import json
c=json.load(open('/home/claude/x5/cb.json')); F=c['F']; lo=F['lo']; hi=F['hi']; ll=F['litlo']; lh=F['lithi']; cu=F['ci_lo']
s=open('build.js').read()
def rep(a,b):
    global s
    assert a in s, a[:90]; s=s.replace(a,b)
def block(start,end,new):
    global s
    i=s.index(start); j=s.index(end,i+len(start)); s=s[:i]+new+s[j:]
m=lambda x:f"{x/1e4:,.1f}만 원"
BC=f"{lo['BC']:.2f}~{hi['BC']:.2f}"
# 공통 표기
rep("중간보고(2025년 기준, 원고 반영)","중간보고(2025년 기준, 확정판)")
rep("{ text: '중간보고 · 2025년 기준 (원고 반영)', options:","{ text: '중간보고 · 2025년 기준 (확정판)', options:")
rep("s.addNotes('표지. 2025년 기준판.","s.addNotes('표지. 2025년 기준 확정판. 회신되지 않은 자료는 추계치(추정치)를 썼고 해당 항목마다 표시함.")
# 목차
rep("['Ⅴ', '집계 비용', '2025년 원고 반영 총괄, 방침 점검, 1명당 생애비용', 'done', '원고 반영'],","['Ⅴ', '집계 비용', '2025년 총괄, 방침 점검, 1명당 생애비용', 'done', '확정'],")
rep("['Ⅵ', '교정 재활 비용편익', '서식 8·9·10 회신 반영, 잠정 B/C', 'wip', '잠정 산출'],","['Ⅵ', '교정 재활 비용편익', '재복역 실측 + 미회신 항목 추계치, B/C 확정', 'done', '확정'],")
rep("['Ⅶ', '향후 계획', '남은 추계와 협조 요청', 'plan', '계획'],","['Ⅶ', '추계치와 향후 계획', '추계치 목록, 최종보고서 작성', 'plan', '계획'],")
rep("Ⅵ장은 교정본부 회신(11. 16.)으로 재복역 자료를 반영해 잠정 B/C를 냄.');","Ⅵ장은 교정본부 회신(11. 16.)과 추계치로 B/C를 확정함. 회신되지 않은 자료는 추계치를 썼다고 표시함.');")
# 요약
rep(f"재활교육 잠정 B/C 0.27~0.36(재복역률 차 2.9%p, 유의하지 않음)",f"교정 재활 B/C {BC}(문헌 효과 적용 시 {ll['BC']:.2f}~{lh['BC']:.2f}). 미회신 자료는 추계치")
# Ⅱ 자료 확보 현황: 슬라이드 통째 교체
newII=f"""s = content('Ⅱ. 연구 설계', 'Ⅱ. 연구 설계 — 자료 확보 현황', '실측 13건, 미회신 자료는 추계치 9건으로 대체');
const got = [
  ['형사사법 6개 기관', '3,728.2억 원', '원고 11. 8.(검찰 제외)'],
  ['의료·복지', '78.6억 원', '원고 11. 6.'],
  ['생산성 손실', '815.0억 원', '원고 11. 6.'],
  ['사망 58명 · 치료보호 1,649명', 'PGS 인원', '원고 11. 6.'],
  ['마약 운전 사고', '33건', '경찰청(2026)'],
  ['단속 인원 · 실질 사용자', '23,403 · 234,030명', '대검찰청(2026)'],
  ['마약류 기결 · 미결', '4,188 · 3,241명', '서식 3(11. 16.)'],
  ['재활교육 개시·이수·탈락', '1,599 · 1,545 · 54명', '서식 4(11. 16.)'],
  ['출소자 3년 내 재복역', '31.0%', '서식 8(11. 16.)'],
  ['이수 · 미이수 재복역', '31.6% · 34.5%', '서식 9·10(11. 16.)'],
  ['재활예산 · 수용 원가', '59.99억 · 2,378.4만', '서식 6·1'],
];
const est = [
  ['고통비용 2,426.4억', '2024 원단위 × 물가 1.021', '원고 미수령'],
  ['검찰 199.3억', '2024 예산·인원', '2025 인원 미공개'],
  ['사회적 혼란·기타 496.0억', '범죄 단가·2024 예산·문헌 최저', '건수·예산 미확정'],
  ['전담인력 인건비 16.98억', '정원 × 봉급표 × 1.6 × 투입비율', '서식 5 비율'],
  ['UC-10 치료개입 {F['UC10']/1e4:,.1f}만', '중독 외래 1인당 진료비', '서식 7'],
  ['UC-12 사후관리 {F['UC12']/1e4:,.1f}만', '치료보호 1인당 예산 ÷ 1.045', '별도요청'],
  ['재활예산 성격', '집행액으로 간주', '서식 6 확인'],
  ['실제 복역 비율 85% · ΔM 0', '가석방 반영 · 수용기간 차이 없음', '가정'],
  ['생애비용 모수', '회복 후 초과 사망, 재검거 확률', '가정·문헌'],
];
const colBox = (x, w, head, n, col) => {{
  R(s, {{ x, y: 1.55, w, h: 0.5, fill: {{ color: col }} }});
  T(s, head, {{ x: x + 0.2, y: 1.55, w: w - 1.2, h: 0.5, fontSize: 15, bold: true, color: C.background1, valign: 'middle' }});
  T(s, n, {{ x: x + w - 1.0, y: 1.55, w: 0.85, h: 0.5, fontSize: 18, bold: true, color: C.background1, align: 'right', valign: 'middle' }});
}};
const LW = 6.0, RX = M + 6.25, RW = W - 2 * M - 6.25;
colBox(M, LW, '실측 (원고·회신·공개)', '', HEX.teal);
got.forEach((r, i) => {{
  const y = 2.05 + i * 0.4;
  R(s, {{ x: M, y, w: LW, h: 0.4, fill: {{ color: i % 2 ? HEX.white : HEX.tealBg }} }});
  T(s, r[0], {{ x: M + 0.15, y, w: 2.5, h: 0.4, fontSize: 11.5, bold: true, valign: 'middle' }});
  T(s, r[1], {{ x: M + 2.6, y, w: 1.75, h: 0.4, fontSize: 11.5, bold: true, color: C.accent2, align: 'right', valign: 'middle' }});
  T(s, r[2], {{ x: M + 4.45, y, w: 1.5, h: 0.4, fontSize: 9.5, color: C.accent5, valign: 'middle' }});
}});
colBox(RX, RW, '추계치 (자료 미회신·미공개)', '', HEX.amber);
est.forEach((r, i) => {{
  const y = 2.05 + i * 0.49;
  R(s, {{ x: RX, y, w: RW, h: 0.49, fill: {{ color: i % 2 ? HEX.white : HEX.amberBg }} }});
  T(s, r[0], {{ x: RX + 0.15, y, w: 2.45, h: 0.49, fontSize: 11.5, bold: true, valign: 'middle' }});
  T(s, r[1], {{ x: RX + 2.6, y, w: 2.2, h: 0.49, fontSize: 10, color: C.accent5, valign: 'middle' }});
  T(s, r[2], {{ x: RX + RW - 1.2, y, w: 1.1, h: 0.49, fontSize: 9.5, bold: true, color: C.accent3, align: 'right', valign: 'middle' }});
}});
T(s, '※ 추계치는 자료가 오면 엑셀 「1.입력값」만 바꿔 다시 계산한다. 슬라이드의 추계치 항목은 "추계치"로 표시', {{ x: M, y: 6.55, w: W - 2 * M, h: 0.3, fontSize: 10, color: C.accent5 }});
s.addNotes('확정판의 자료 구분. 실측은 원고·교정본부 회신·공개 통계. 회신되지 않았거나 공개되지 않은 자료 9건은 추계치(추정치)로 대체하고 산식과 근거를 밝힘.');

"""
block("s = content('Ⅱ. 연구 설계', 'Ⅱ. 연구 설계 — 자료 확보 현황'","// ════════ Ⅲ",newII)
# 체계도 범례
rep("['추정 포함', HEX.amberBg, null, 1.4]","['추계치 포함', HEX.amberBg, null, 1.5]")
rep("주황 칸은 추정이 남은 항목(고통비용, 2차 범죄, 예방 예산, 가족 돌봄).","주황 칸은 추계치를 쓴 항목(고통비용, 2차 범죄, 예방 예산, 가족 돌봄).")
rep("{ text: '= 형사사법(1건당) + 재중독 기간 의료·생산성 귀속분', options: {} },","{ text: '= 형사사법(1건당) + 비형사사법 1명당(의료·생산성·고통·혼란)', options: {} },")
# 원고 확인 노트
rep("교도소 기준은 교정본부 회신 대기.","교도소 기준은 교정본부 회신으로 확인(미결 포함 유지).")
# Ⅵ 섹션
rep("s.addText('교정 재활 비용편익 (잠정)', { placeholder: 'title' });","s.addText('교정 재활 비용편익 (확정)', { placeholder: 'title' });")
rep("s.addText('교정본부 회신(2026. 11. 16.) 반영: 재복역 자료와 잠정 B/C', { placeholder: 'body' });","s.addText('재복역 실측(교정본부 회신) + 미회신 항목 추계치로 B/C 확정', { placeholder: 'body' });")
rep("chip(s, W - M - 1.4, 0.36, '잠정 산출', 'wip', 1.4);","chip(s, W - M - 1.4, 0.36, '확정', 'done', 1.4);")
# 산출 구조
rep("// ── 비용편익 산출 구조(잠정) ──","// ── 비용편익 산출 구조(확정) ──")
rep("chip(s, W - M - 1.2, 0.36, '잠정', 'wip', 1.2);","chip(s, W - M - 1.2, 0.36, '확정', 'done', 1.2);")
rep("const SC = { got: [HEX.teal, '회신·공개'], est: [HEX.amber, '추계·가정'], lit: [HEX.slate, '문헌'], wait: [HEX.red, '자료 대기'] };","const SC = { got: [HEX.teal, '실측'], est: [HEX.amber, '추계치·가정'], lit: [HEX.slate, '문헌'] };")
rep("const x = W - M - 4 * 1.32 + i * 1.32;","const x = W - M - 3 * 1.32 + i * 1.32;")
rep("sb(LX, 1.88, 2.9, 0.98, '', '재활예산', '59.99억 원', '서식6 총액(예산·집행 구분 확인 중)', 'got');","sb(LX, 1.88, 2.9, 0.98, '', '재활예산', '59.99억 원', '서식6 총액(집행액으로 간주, 추계)', 'got');")
rep("sb(LX + 3.05, 1.88, 2.9, 0.98, '+', '전담인력 직접투입 인건비', '16.98억 원', '서식5 정원 × 2026 봉급표 × 1.6 × 투입비율', 'est');","sb(LX + 3.05, 1.88, 2.9, 0.98, '+', '전담인력 직접투입 인건비 (추계치)', '16.98억 원', '서식5 정원 × 2026 봉급표 × 1.6 × 투입비율', 'est');")
rep("sb(LX, 4.54, 1.9, 0.92, '+', 'UC-10 치료개입', '0', '서식7 미생산', 'wait');",f"sb(LX, 4.54, 1.9, 0.92, '+', 'UC-10 치료개입', '{F['UC10']/1e4:,.1f}만 원', '추계치: 중독 외래 1인당 진료비', 'est');")
rep("sb(LX + 2.02, 4.54, 1.9, 0.92, '+', 'UC-12 사후관리', '0', '별도요청 미회신', 'wait');",f"sb(LX + 2.02, 4.54, 1.9, 0.92, '+', 'UC-12 사후관리', '{F['UC12']/1e4:,.1f}만 원', '추계치: 치료보호 1인당 ÷ 1.045', 'est');")
rep("sb(LX, 5.58, PW, 0.62, '=', 'ΔC 증분비용 (하한)', '498.2만 원', '', 'est', HEX.navy);",f"sb(LX, 5.58, PW, 0.62, '=', 'ΔC 증분비용', '{F['dC']/1e4:,.1f}만 원', '', 'est', HEX.navy);")
rep("T(s, '+  재중독 기간 의료·생산성 귀속분: 1인당 값으로 추가 예정(추계 작업 중)', { x: RX2 + 0.18, y: 5.58, w: PW - 0.3, h: 0.62, fontSize: 11, color: C.accent5, valign: 'middle' });",
    f"T(s, '확장 SCᵣ = 하한 + 비형사사법 1명당 1,630.6만 = {c['SCx']/1e4:,.1f}만 원 (의료·생산성 따로 더하지 않음)', {{ x: RX2 + 0.18, y: 5.58, w: PW - 0.3, h: 0.62, fontSize: 11, color: C.accent5, valign: 'middle' }});")
import re
s=re.sub(r"T\(s, '편익 B = \(r0 [^']*',",f"T(s, '편익 B = (r0 {c['p0']*100:.1f}% − r1 {c['p1']*100:.1f}%) × SCᵣ × D {c['D']:.3f} = {lo['B']/1e4:,.1f}만 원   →   B/C {lo['BC']:.2f} (확장 SCᵣ {hi['BC']:.2f})',",s,count=1)
s=re.sub(r"s\.addNotes\('값은 2025 회신 기준의 잠정값\..*?'\);",f"s.addNotes('확정값. ΔC {F['dC']/1e4:,.1f}만 원 = 프로그램 498.2만 + 치료개입 {F['UC10']/1e4:,.1f}만(추계치) + 사후관리 {F['UC12']/1e4:,.1f}만(추계치). SCᵣ 하한 5,035.7만, 확장 {c['SCx']/1e4:,.1f}만 원. B/C {BC}.');",s,flags=re.S)
# 결과 슬라이드 통째 교체
newR=f"""// ── 비용편익 확정 결과 ──
s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 교정 재활 비용편익 — 결과', '교정 재활 B/C {BC}: 관측 효과로는 편익이 비용에 못 미침');
{{
  const hd = ['구분', '하한 (SCᵣ 형사사법분)', '확장 (SCᵣ 전 항목)'];
  const rows = [
    ['ΔC 증분비용 (프로그램 + 치료개입 + 사후관리)', '{m(F['dC'])}', '{m(F['dC'])}'],
    ['SCᵣ 재복역 1건당 사회적 비용', '{m(c['SCr'])}', '{m(c['SCx'])}'],
    ['B = (r0 − r1) × SCᵣ × D   [2.9%p × D 0.944]', '{m(lo['B'])}', '{m(hi['B'])}'],
    ['B/C (기본)', '{lo['BC']:.2f}', '{hi['BC']:.2f}'],
    ['NPV = B − ΔC', '{m(lo['NPV'])}', '{m(hi['NPV'])}'],
    ['손익분기 재복역률 차', '{lo['dstar']*100:.1f}%p', '{hi['dstar']*100:.1f}%p'],
    ['민감도: 문헌 효과(상대 19.2% → 6.6%p)', 'B/C {ll['BC']:.2f}', 'B/C {lh['BC']:.2f}'],
    ['민감도: 신뢰구간 상한 효과(11.7%p)', 'B/C {F['ci_lo']['BC']*c['SCr']/c['SCx']:.2f}', 'B/C {cu['BC']:.2f}'],
  ];
  const tr = [hd.map((h, j) => ({{ text: h, options: {{ bold: true, color: HEX.white, fill: {{ color: HEX.navy }}, fontSize: 12, align: j ? 'right' : 'left' }} }}))].concat(
    rows.map((r, i) => r.map((v, j) => ({{ text: v, options: {{ fontSize: 12, bold: i === 3 || j === 0, color: i === 3 && j ? HEX.teal : HEX.ink, fill: {{ color: i === 3 ? HEX.tealBg : (i >= 6 ? HEX.amberBg : (i % 2 ? HEX.white : HEX.paper)) }}, align: j ? 'right' : 'left' }} }}))));
  s.addTable(tr, {{ x: M, y: 1.5, w: 7.7, colW: [3.9, 1.8, 2.0], rowH: 0.47, border: {{ type: 'solid', color: HEX.mist, pt: 0.5 }}, fontFace: '맑은 고딕', valign: 'middle', margin: [0.04, 0.1, 0.04, 0.1] }});
  RR(s, {{ x: 8.55, y: 1.5, w: 4.18, h: 4.95, fill: {{ color: HEX.navyBg }} }});
  T(s, [
    {{ text: '결론', options: {{ bold: true, fontSize: 14, breakLine: true }} }},
    {{ text: '관측된 재복역률 차(2.9%p)로는 B/C {BC}로 편익이 비용에 못 미친다.', options: {{ bullet: true, breakLine: true }} }},
    {{ text: '손익분기는 재복역률 차 {hi['dstar']*100:.1f}~{lo['dstar']*100:.1f}%p. 이수자 재복역률을 {c['p0']*100-hi['dstar']*100:.1f}% 이하로 낮추면 B/C ≥ 1이다.', options: {{ bullet: true, breakLine: true }} }},
    {{ text: '관측 차이는 유의하지 않고(95% CI −6.0~11.7%p), 이수자는 형기가 길어 효과가 과소 추정됐을 수 있다. 상한 효과에서는 B/C {cu['BC']:.2f}.', options: {{ bullet: true, breakLine: true }} }},
    {{ text: '정책 함의: 재활 확대와 함께 효과 측정(비교군·사후관리 연계)이 필요하다.', options: {{ bullet: true, bold: true }} }},
  ], {{ x: 8.75, y: 1.6, w: 3.8, h: 4.75, fontSize: 11.5, valign: 'top', paraSpaceAfter: 6 }});
  source(s, '교정본부 회신(2026. 11. 16.) 서식 3·4·8·9·10, 서식 1·5·6, 제3장 원고(치료보호·외래 진료비), 김도균·나종민(2025), 연구진 계산. 추계치: UC-10·UC-12·인건비');
  s.addNotes('확정 B/C는 하한 {lo['BC']:.2f}, 확장 {hi['BC']:.2f}. ΔC {F['dC']/1e4:,.1f}만 원 중 치료개입·사후관리는 추계치. 문헌 효과를 쓰면 {ll['BC']:.2f}~{lh['BC']:.2f}, 신뢰구간 상한 효과면 확장 {cu['BC']:.2f}. 의료절감·생산성회복은 SCᵣ 안에 포함하고 따로 더하지 않음.');
}}
"""
block("// ── 잠정 비용편익 ──","s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 회신 현황과 남은 자료'",newR)
# 회신 현황 → 자료 구분
newW=f"""s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 자료 구분', '실측과 추계치: 회신되지 않은 자료는 추계치로 대체');
const wait = [
  ['서식 8 · 9 · 10', '재복역 코호트, 이수별 재복역, 인적특성', 'r0 34.5%, r1 31.6%, D 0.944', 'done'],
  ['서식 3 · 4', '마약류 기결수, 재활교육 실적', '기결 4,188명, 2025 이수 1,545명', 'done'],
  ['서식 1 · 6', '수용 원가, 재활예산', 'UC-01 2,378.4만 원, 재활예산 59.99억(집행액으로 간주)', 'done'],
  ['서식 5', '전담인력 투입비율', '추계치: 정원 × 봉급표 × 1.6 × 투입비율 → 16.98억', 'est'],
  ['서식 7', '치료개입 비용', '추계치: 중독 외래 1인당 진료비 {F['UC10']/1e4:,.1f}만 원', 'est'],
  ['별도요청', '치료보호·사후관리', '추계치: 치료보호 1인당 예산 ÷ 1.045 = {F['UC12']/1e4:,.1f}만 원', 'est'],
  ['서식 2', '전국 연말 기결수', '불필요: 미결 포함 기준(7,429 ÷ 64,626) 유지', 'done'],
];
R(s, {{ x: M, y: 1.55, w: W - 2 * M, h: 0.42, fill: {{ color: HEX.navy }} }});
[['자료', 0.15, 2.2], ['내용', 2.4, 3.3], ['반영 값', 5.8, 5.2], ['구분', 11.0, 1.1]].forEach(h => T(s, h[0], {{ x: M + h[1], y: 1.55, w: h[2], h: 0.42, fontSize: 12, bold: true, color: C.background1, valign: 'middle' }}));
wait.forEach((r, i) => {{
  const y = 1.97 + i * 0.62;
  R(s, {{ x: M, y, w: W - 2 * M, h: 0.62, fill: {{ color: i % 2 ? HEX.white : HEX.paper }} }});
  T(s, r[0], {{ x: M + 0.15, y, w: 2.2, h: 0.62, fontSize: 12.5, bold: true, valign: 'middle' }});
  T(s, r[1], {{ x: M + 2.4, y, w: 3.3, h: 0.62, fontSize: 12, valign: 'middle' }});
  T(s, r[2], {{ x: M + 5.8, y, w: 5.1, h: 0.62, fontSize: 11.5, color: C.accent5, valign: 'middle' }});
  chip(s, M + 11.0, y + 0.18, r[3] === 'done' ? '실측' : '추계치', r[3] === 'done' ? 'done' : 'wip', 1.05);
}});
s.addNotes('Ⅵ장의 자료 구분. 회신되지 않은 서식 5·7과 별도요청은 추계치로 대체하였다.');

"""
block("s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 회신 현황과 남은 자료'","// ════════ Ⅶ",newW)
# Ⅶ
newVII=f"""// ════════ Ⅶ. 향후 계획 ════════
pres.addSection({{ title: 'Ⅶ. 향후 계획' }});
s = content('Ⅶ. 향후 계획', 'Ⅶ. 추계치와 향후 계획', '확정값으로 최종보고서 작성, 추계치는 자료가 오면 교체');
const plan = [
  ['1', '최종보고서 작성', '2025년 확정값(λ 10 7조 5,441.7억 원) 기준으로 본문·표 정리'],
  ['2', '원고 수정', '1인당 값의 이름, 검찰 연도, 오기, "암수율 미적용" 문구'],
  ['3', '민감도 제시', 'λ 28.57, 할인율 3~5%, PGS 가구 구조, 교도소 기준'],
  ['4', '교정 재활 비용편익', 'B/C {BC}, 손익분기 {hi['dstar']*100:.1f}~{lo['dstar']*100:.1f}%p, 문헌·상한 효과 민감도'],
  ['5', '정책 제언', '재활 확대 규모, 효과 측정 체계, 사후관리 연계'],
];
plan.forEach((r, i) => {{
  const y = 1.6 + i * 0.95;
  R(s, {{ x: M, y: y + 0.08, w: 0.6, h: 0.6, fill: {{ color: i === 0 ? HEX.teal : HEX.navy }} }}, pres.shapes.OVAL);
  T(s, r[0], {{ x: M, y: y + 0.08, w: 0.6, h: 0.6, fontSize: 18, bold: true, color: C.background1, align: 'center', valign: 'middle' }});
  T(s, r[1], {{ x: M + 0.8, y: y + 0.02, w: 5.3, h: 0.38, fontSize: 15, bold: true }});
  T(s, r[2], {{ x: M + 0.8, y: y + 0.4, w: 5.3, h: 0.4, fontSize: 12, color: C.accent5 }});
}});
RR(s, {{ x: 7.1, y: 1.6, w: 5.63, h: 4.6, fill: {{ color: HEX.amberBg }} }});
T(s, '추계치를 쓴 항목 (자료가 오면 교체)', {{ x: 7.4, y: 1.8, w: 5.1, h: 0.42, fontSize: 16, bold: true, color: C.accent3 }});
T(s, [
  {{ text: '고통비용 2,426.4억: 2024 원단위 × 물가 (원고 미수령)', options: {{ bullet: true, breakLine: true }} }},
  {{ text: '검찰 199.3억: 2024 예산·인원 (2025 인원 미공개)', options: {{ bullet: true, breakLine: true }} }},
  {{ text: '사회적 혼란·기타 496.0억: 범죄 단가·2024 예산·문헌', options: {{ bullet: true, breakLine: true }} }},
  {{ text: '전담인력 인건비 16.98억: 투입비율 가정 (서식 5)', options: {{ bullet: true, breakLine: true }} }},
  {{ text: 'UC-10 {F['UC10']/1e4:,.1f}만 · UC-12 {F['UC12']/1e4:,.1f}만: 서식 7·별도요청 미회신', options: {{ bullet: true, breakLine: true }} }},
  {{ text: '재활예산 집행액 간주, 실제 복역 85%, ΔM 0', options: {{ bullet: true, breakLine: true }} }},
  {{ text: '생애비용: 회복 후 초과 사망, 재검거 확률', options: {{ bullet: true }} }},
], {{ x: 7.4, y: 2.3, w: 5.1, h: 3.8, fontSize: 12, paraSpaceAfter: 6 }});
s.addNotes('2025년 기준 값은 확정. 회신되지 않은 자료는 추계치를 썼고, 자료가 오면 엑셀 입력값만 바꿔 다시 계산한다.');

"""
block("// ════════ Ⅶ. 향후 계획 ════════","pres.addSection({ title: '맺음' });",newVII)
s=s.replace("중간보고_마약류사회적비용_2025기준_원고반영_2026-11-16.pptx","중간보고_마약류사회적비용_2025기준_확정판.pptx")
open('build.js','w').write(s); print('final patched')
s=open('build.js').read()
for a,b in [("(원고 미수령, 추정)', HEX.red]","(원고 미수령, 추계치)', HEX.red]"),
 ("'이 판의 기준연도: 2025년(원고 반영, 고통비용은 추정)'","'이 판의 기준연도: 2025년 확정(미회신 자료는 추계치)'"),
 ("s.addNotes('2025년 원고 반영판. 형사사법(11. 8.)과 제3장 제1·2절(11. 6.) 원고의 실측값을 쓰고, 고통비용만 2024년 원단위에서 추정.');","s.addNotes('2025년 확정판. 원고·교정본부 회신의 실측값을 쓰고, 회신되지 않은 자료는 추계치를 씀.');"),
 ("치료보호 1,649명 × 1.12억 (추정)', '2,426.4'","치료보호 1,649명 × 1.12억 (추계치)', '2,426.4'"),
 ("추정: 고통비용, 사회적 혼란·기타 일부'","추계치: 고통비용, 검찰(2024 대용), 사회적 혼란·기타'")]:
    assert a in s,a; s=s.replace(a,b)
open('build.js','w').write(s)
