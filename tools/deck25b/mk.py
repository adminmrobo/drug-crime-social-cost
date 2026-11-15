import json,re
V=json.load(open('vals.json'))
V['b4ln_raw']=V['b4ln'].replace(',','')
PATCH2=[("'이 판의 기준연도: 2025년(시산, 없는 자료는 추정)', '2024년 확정판과 같은 방법'", "'이 판의 기준연도: 2025년(원고 반영, 고통비용은 추정)', '모든 항목 1명당 × N*'"), ("s.addNotes('2025년 시산판. 2025년 형사사건 처리 통계가 2026년 12월 확정 예정이라 일부 항목은 2024년 확정치에서 추정.');", "s.addNotes('2025년 원고 반영판. 형사사법(11. 8.)과 제3장 제1·2절(11. 6.) 원고의 실측값을 쓰고, 고통비용만 2024년 원단위에서 추정.');"), ("'2025년 시산 11건(실측 기반 5건·추정 6건), 추계 작업 중 4건'", "'2025년 원고 반영 11건(실측 10건·추정 1건), 추계 작업 중 4건'"), ("  ['의료·복지 비용', '59.2억 원', '추정(2024 환산)'],\n  ['생산성 손실', '773.3억 원', '추정(2024 환산)'],\n  ['고통비용 PGS', '2,435.9억 원', '치료보호 실측'],\n  ['경찰 형사사법비용', '1,416.8억 원', '추정(2024 환산)'],\n  ['검찰 형사사법비용', '214.5억 원', '2025 결산 실측'],\n  ['법원 형사사법비용', '100.8억 원', '추정(2024 환산)'],\n  ['교도소 형사사법비용', '962.8억 원', '2025 결산 실측'],\n  ['국립법무병원 비용', '9.9억 원', '추정(2024 환산)'],\n  ['보호관찰소 비용', '102.2억 원', '추정(2024 환산)'],", "  ['의료·복지 비용', '78.6억 원', '원고 11. 6.'],\n  ['생산성 손실', '815.0억 원', '원고 11. 6.'],\n  ['고통비용 PGS', '2,426.4억 원', '추정(원고 미수령)'],\n  ['경찰 형사사법비용', '1,381.0억 원', '원고 11. 8.'],\n  ['검찰 형사사법비용', '199.3억 원', '원고(2024 값)'],\n  ['법원 형사사법비용', '99.0억 원', '원고 11. 8.'],\n  ['교도소 형사사법비용', '1,953.3억 원', '원고 11. 8.'],\n  ['국립법무병원 비용', '5.1억 원', '원고 11. 8.'],\n  ['보호관찰소 비용', '90.5억 원', '원고 11. 8.'],"), ("colBox(M, LW, '2025년 시산 항목', '11건', HEX.teal);", "colBox(M, LW, '2025년 원고 반영 항목', '11건', HEX.teal);"), ("'사회적 혼란·기타 496.0억 원: 범죄 단가·예산·문헌으로 잠정 반영(암수율 미적용)'", "'사회적 혼란·기타 496.0억 원: 범죄 단가·예산·문헌으로 잠정 반영, 1명당 × N*(λ 10 4,960.4억)'"), ("'※ 2025년 미수령: 경찰 결산·검거, 마약류 1일 평균, 중독 사망자, 검찰 처리 인원 등. 추정 = 2024년 확정치 × 물가 1.021·결산 증가 1.037·단속 증가 1.0165'", "'※ 미수령: 고통비용 원고, 교정본부 마약류 수용인원 기준치, 검찰 2025 처리 인원, 2025 마약 예산. 고통비용 추정 = 2024년 원단위 × 물가 1.021'")]
src=open('/home/claude/deck/build2025.js').read().split('\n')
def seg(a,b): return '\n'.join(src[a-1:b])   # inclusive 1-based
def fill(t):
    def rep(m):
        k=m.group(1); return str(V[k])
    return re.sub(r'«([^»]+)»',rep,t)
head=seg(1,98).replace('// 중간보고 PPT — 2025년 기준 시산판','// 중간보고 PPT — 2025년 기준(원고 반영)판').replace("중간보고(2025년 기준 시산)","중간보고(2025년 기준, 원고 반영)")
G=['형사사법','고통비용','생산성','의료·복지','사회적 혼란·기타']
NEW1=fill(r'''
// ════════ 1. 표지 ════════
pres.addSection({ title: '표지' });
let s = pres.addSlide({ masterName: 'COVER', sectionTitle: '표지' });
s.addText('마약류범죄와 교정기관 중독재활 체계의\n사회적 비용 비교분석', { placeholder: 'title' });
s.addText([
  { text: '중간보고 · 2025년 기준 (원고 반영)', options: { bold: true, color: HEX.white, breakLine: true } },
  { text: ' ', options: { fontSize: 10, breakLine: true } },
  { text: '연구책임자  박성수 교수 (세명대학교 경찰학과)', options: { breakLine: true } },
  { text: '2026. 11.', options: {} },
], { placeholder: 'body' });
s.addNotes('표지. 2025년 기준판. 형사사법 원고(2026. 11. 8.)와 제3장 제1·2절 원고(2026. 11. 6.)의 2025년 실측값을 반영함. 고통비용은 원고 미수령으로 2024년 원단위에 물가를 곱한 추정.');

// ════════ 2. 목차 ════════
pres.addSection({ title: '개요' });
s = content('개요', '목차', '보고 순서와 장별 진행 상태');
const toc = [
  ['Ⅰ', '연구 배경', '마약류 범죄 현황과 처벌 중심 대응의 한계', 'done', '정리 완료'],
  ['Ⅱ', '연구 설계', '범위·방법·자료 확보 현황', 'done', '정리 완료'],
  ['Ⅲ', '이론 검토', '선행연구, 암수율과 실질 사용자 수 N*', 'done', '정리 완료'],
  ['Ⅳ', '사회적 비용 체계', '전체 체계도와 비용 산정의 주요 특징', 'done', '확정'],
  ['Ⅴ', '집계 비용', '2025년 원고 반영 총괄, 방침 점검, 1명당 생애비용', 'done', '원고 반영'],
  ['Ⅵ', '교정 재활 비용편익', '산출 구조와 잠정값, 자료 대기 항목', 'wip', '추계 작업 중'],
  ['Ⅶ', '향후 계획', '남은 추계와 협조 요청', 'plan', '계획'],
];
toc.forEach((r, i) => {
  const y = 1.65 + i * 0.68;
  R(s, { x: M, y, w: W - 2 * M, h: 0.58, fill: { color: i % 2 ? HEX.white : HEX.paper } });
  T(s, r[0], { x: M + 0.2, y, w: 0.6, h: 0.58, fontSize: 20, bold: true, color: C.accent1, valign: 'middle' });
  T(s, r[1], { x: M + 0.9, y, w: 3.2, h: 0.58, fontSize: 17, bold: true, valign: 'middle' });
  T(s, r[2], { x: M + 4.2, y, w: 6.0, h: 0.58, fontSize: 14, color: C.accent5, valign: 'middle' });
  chip(s, W - M - 1.4, y + 0.16, r[4], r[3], 1.2);
});
s.addNotes('Ⅰ~Ⅴ장 정리 완료. Ⅴ장은 2025년 원고 2건을 반영하고 1명당 생애비용을 더함. Ⅵ장은 교정본부 회신 대기 항목이 있어 추계 작업 중.');

// ════════ 3. 요약 ════════
s = content('개요', '중간보고 요약', '2025년 마약류 사회적 비용 «t10» 원 (암수율 10배)');
const sum = [
  ['«t10»', '사회적 비용 (λ 10)', '1명당 «pc»만 원 × 234,030명. 모든 항목에 λ 적용. 미반영 «tot»억 원', HEX.teal],
  ['«gl_형사사법»', '형사사법비용', '6개 기관 2025 실측(원고 11. 8.). 미반영 «g_형사사법»억 원', HEX.navy],
  ['«gl_고통비용»', '고통비용 (PGS)', '사망 58명 × 9.9억 + 치료보호 1,649명 × 1.12억 (원고 미수령, 추정)', HEX.red],
  ['«gl_생산성»', '생산성 손실', '조기사망 · 미취업 · 이환·입원 (원고 11. 6. 실측)', HEX.amber],
  ['«gl_사회적 혼란·기타» · «gl_의료·복지»', '사회적 혼란·기타 · 의료·복지', '2차 범죄·예방 예산·가족·운전 / 직접·간접 의료·정신건강 (원고 11. 6.)', HEX.slate],
];
sum.forEach((r, i) => {
  const cwid = (W - 2 * M - 4 * 0.18) / 5, x = M + i * (cwid + 0.18);
  RR(s, { x, y: 1.7, w: cwid, h: 2.6, fill: { color: HEX.paper } });
  T(s, r[0], { x: x + 0.15, y: 1.9, w: cwid - 0.2, h: 0.75, fontSize: i === 4 ? 14 : 18, bold: true, color: r[3], valign: 'bottom' });
  T(s, r[1], { x: x + 0.18, y: 2.75, w: cwid - 0.3, h: 0.4, fontSize: i === 4 ? 12 : 13.5, bold: true });
  T(s, r[2], { x: x + 0.18, y: 3.15, w: cwid - 0.3, h: 1.05, fontSize: 10.5, color: C.accent5 });
});
T(s, [
  { text: '주요 산출 내역', options: { bold: true, fontSize: 16, breakLine: true } },
  { text: '박성수(2018) 2조 2,389억 원 대비 «ratio»배. 같은 4개 분야 범위로는 «b4ratio»배(물가 «s_cpi»%, 검거 인원 «s_arr»%, 1명당 실질 «s_real»%)', options: { bullet: true, breakLine: true } },
  { text: '암수율 28.57배(민감도) «t28» 원. 교도소는 원고 기준(12. 31. 전체 수용자, 7,429 ÷ 64,626명). 연평균 추정이면 λ 10에서 «pr_diffl» 원(부록 4)', options: { bullet: true, breakLine: true } },
  { text: '방침 점검: 사회적 혼란·기타를 λ 없이 더하던 것을 1명당 «gp_사회적 혼란·기타»만 원 × N*로 바로잡음(+4,464.4억 원)', options: { bullet: true, breakLine: true } },
  { text: '중독자 1명당 생애 사회적 비용(기준) 현재가치 «lf_B_pv45»억 원, 명목 누계 «lf_B_nom»억 원. 하한 «floor»만 원, 상한 16억 원', options: { bullet: true } },
], { x: M, y: 4.5, w: W - 2 * M, h: 2.3, fontSize: 14, paraSpaceAfter: 5 });
s.addNotes('2025년 사회적 비용은 암수율 10배 기준 «t10» 원. 모든 항목을 검거 사범 1명당 값(합계 «pc»만 원)으로 바꾸고 실질 사용자 234,030명을 곱함. 형사사법과 사회적 혼란·기타에도 λ를 곱함. 미반영 «tot»억, 28.57배 «t28». 11. 9. 시산 대비 증가는 대부분 교도소 인원 기준(원고의 12. 31. 전체 수용자) 때문. 생애비용 기준 시나리오 현재가치 «lf_B_pv45»억 원.');
''')
NEW2=fill(r'''
s = content('Ⅲ. 이론 검토', 'Ⅲ. 이론 검토 — 선행연구', '선행 추계는 2016년 기준이 마지막');
const prev = [
  ['보건복지부 건강증진사업단 (2009)', '약 2조 5천억 원', '2008년 기준', '국내 첫 체계적 추계. 공식 검거 인원 중심이라 암수 반영이 약함'],
  ['박성수 (2018)', '2조 2,389억 원', '2016년 기준 · 암수율 10배', '의료·생산성·형사사법·무형비용 종합. 교정 재활의 비용 대비 효과는 분리하지 않음'],
  ['본 연구 (2026)', '«t10» 원', '2025년 · 암수율 10배', '선행연구와 같은 10배 기준. 고통비용·사회적 혼란 포함, 모든 항목 1명당 × N*. 4개 분야만 «b4l» 원'],
];
prev.forEach((r, i) => {
  const y = 1.65 + i * 1.55, last = i === 2;
  RR(s, { x: M, y, w: W - 2 * M, h: 1.35, fill: { color: last ? HEX.navyBg : HEX.paper } });
  T(s, r[0], { x: M + 0.3, y: y + 0.18, w: 3.8, h: 0.4, fontSize: 15, bold: true });
  T(s, r[2], { x: M + 0.3, y: y + 0.65, w: 3.8, h: 0.4, fontSize: 12, color: C.accent5 });
  T(s, r[1], { x: M + 4.2, y: last ? y + 0.08 : y + 0.2, w: 3.0, h: last ? 0.6 : 0.9, fontSize: last ? 21 : 24, bold: true, color: last ? C.accent3 : C.accent1, valign: 'middle' });
  if (last) T(s, [
    { text: '암수율 미반영: ', options: { bold: true, color: HEX.navy } }, { text: '«tot»억 원', options: { bold: true, color: HEX.ink, breakLine: true } },
    { text: '암수율 반영 λ 28.57: ', options: { bold: true, color: HEX.navy } }, { text: '«t28» 원', options: { bold: true, color: HEX.ink } },
  ], { x: M + 4.2, y: y + 0.66, w: 3.1, h: 0.62, fontSize: 11, valign: 'top' });
  T(s, r[3], { x: M + 7.3, y: y + 0.2, w: 4.5, h: 0.95, fontSize: 13, valign: 'middle' });
});
T(s, '단속 인원 2016년 14,214명 → 2025년 23,403명으로 증가, 현 시점 기준 비용 재계량 필요', { x: M, y: 6.3, w: W - 2 * M, h: 0.35, fontSize: 13, bold: true, color: C.accent1 });

// ── 선행연구 대비 차이 원인 ──
s = content('Ⅲ. 이론 검토', 'Ⅲ. 이론 검토 — 선행연구 대비 차이', '같은 4개 분야·10배 기준 «b4ratio»배: 검거 인원 «s_arr»%, 1명당 실질 «s_real»%');
{
  T(s, '총액 비교 (억 원, 명목, 암수율 10배, 4개 분야)', { x: M, y: 1.55, w: 5.4, h: 0.35, fontSize: 13, bold: true });
  const MX = «b4ln_raw», BW = 5.4;
  const bars = [
    ['박성수(2018), 2016년', 22389, '2조 2,389', HEX.slate],
    ['× 물가 1.217 (추계)', 27249.7, '2조 7,249.7', '8A97AA'],
    ['× 검거 인원 1.65', 44865.9, '4조 4,865.9', HEX.amber],
    ['본 연구 2025년', «b4ln_raw», '«b4l»', HEX.navy],
  ];
  bars.forEach((b, i) => {
    const y = 2.0 + i * 0.82;
    T(s, b[0], { x: M, y, w: 3.0, h: 0.3, fontSize: 12, bold: true });
    R(s, { x: M, y: y + 0.32, w: BW * b[1] / MX, h: 0.4, fill: { color: b[3] } });
    T(s, b[2], { x: M + 0.1, y: y + 0.32, w: 2.0, h: 0.4, fontSize: 13.5, bold: true, color: C.background1, valign: 'middle' });
  });
  RR(s, { x: M, y: 5.4, w: BW, h: 1.12, fill: { color: HEX.navyBg } });
  T(s, [
    { text: '사용자 1명당(4개 분야): 1,575.1만 원 → «b4pc»만 원', options: { bold: true, breakLine: true } },
    { text: '2025년 가격 환산 1,917.1만 원 대비 +«pcinc»%. 선행연구 = 2조 2,389억 ÷ (14,214명 × 10), 본 연구 = «b4»억 ÷ 23,403명', options: { fontSize: 10.5, color: HEX.slate } },
  ], { x: M + 0.15, y: 5.4, w: BW - 0.3, h: 1.12, fontSize: 12, valign: 'middle' });

  const X = M + 5.85, TW = W - M - X;
  T(s, '증가분 +«inc» 원의 기여 분해', { x: X, y: 1.55, w: TW, h: 0.35, fontSize: 13, bold: true });
  const segs = [[«s_cpi», '8A97AA', '물가 «s_cpi»%'], [«s_arr», HEX.amber, '검거 인원 «s_arr»%'], [«s_real», HEX.navy, '실질 «s_real»%']];
  let sx = X;
  segs.forEach(g => { const w = TW * g[0] / 100; R(s, { x: sx, y: 2.0, w, h: 0.5, fill: { color: g[1] } }); T(s, g[2], { x: sx, y: 2.0, w, h: 0.5, fontSize: 11.5, bold: true, color: C.background1, align: 'center', valign: 'middle' }); sx += w; });
  const rows = [
    ['물가상승 기여분 (추계)', '4,860.7억', '«s_cpi»%', '2조 2,389억 × (1.217 − 1). 소비자물가 2016년 95.8 → 2025년 116.6(추정)'],
    ['검거 인원 증가 기여분', '1조 7,616.2억', '«s_arr»%', '2조 7,250억 × (1.65 − 1). 단속 14,214 → 23,403명'],
    ['1명당 실질 비용 증가', '«d_real»', '«s_real»%', '① 교도소 인원 기준(12. 31. 전체 수용자) ② 치료보호 인원 증가(1,649명) ③ 고통비용 원단위 상승(사망 2.8억 → 9.7억)'],
  ];
  rows.forEach((r, i) => {
    const y = 2.7 + i * 0.95;
    R(s, { x: X, y, w: TW, h: 0.88, fill: { color: i % 2 ? HEX.white : HEX.paper } });
    T(s, r[0], { x: X + 0.12, y: y + 0.05, w: 2.6, h: 0.35, fontSize: 12.5, bold: true });
    T(s, r[1], { x: X + 2.7, y: y + 0.05, w: 1.6, h: 0.35, fontSize: 13, bold: true, color: C.accent2, align: 'right' });
    T(s, r[2], { x: X + TW - 0.95, y: y + 0.05, w: 0.85, h: 0.35, fontSize: 12.5, bold: true, align: 'right' });
    T(s, r[3], { x: X + 0.12, y: y + 0.4, w: TW - 0.24, h: 0.46, fontSize: 10, color: C.accent5 });
  });
  RR(s, { x: X, y: 5.65, w: TW, h: 0.87, fill: { color: HEX.navy } });
  T(s, '물가 → 검거 인원 순서의 단계 분해. 선행연구와 같은 4개 분야 기준(사회적 혼란·기타 «gl_사회적 혼란·기타» 제외). 전체 기준은 «ratio»배', { x: X + 0.15, y: 5.65, w: TW - 0.3, h: 0.87, fontSize: 11.5, bold: true, color: C.background1, valign: 'middle' });
  source(s, '박성수(2018), 통계청 소비자물가지수(2020=100, 2025년은 2024 × 1.021), 대검찰청(2026), 형사사법·제3장 원고(2026. 11.), 연구진 계산. 금액은 명목가격');
  s.addNotes('같은 10배·4개 분야 기준에서 2025년은 «b4l» 원으로 선행연구 2조 2,389억 원의 «b4ratio»배. 증가분 «inc» 원은 물가 4,860.7억(«s_cpi»%), 검거 인원 1조 7,616.2억(«s_arr»%), 1명당 실질 «d_real»(«s_real»%). 실질 비중이 커진 주된 이유는 원고가 교도소 인원을 12. 31. 전체 수용자 기준으로 쓴 것. 사범 수와 물가를 반영한 기대값 4조 4,865.9억 원의 «vsexp»배.');
}

s = content('Ⅲ. 이론 검토', 'Ⅲ. 이론 검토 — 암수율과 실질 사용자 수', '실질 사용자 23만 4천 명(λ 10, 기본) · 66만 9천 명(λ 28.57)');
const ahp = [['의료·재활 종사자', '0.319', '12.96배'], ['마약 범죄자', '0.292', '50.00배'], ['학계 전문가', '0.208', '16.81배'], ['관련 공무원', '0.181', '35.00배']];
T(s, '계층화분석법(AHP)으로 구한 집단별 가중치와 추정 배수', { x: M, y: 1.6, w: 6.0, h: 0.35, fontSize: 13, bold: true });
R(s, { x: M, y: 2.0, w: 6.0, h: 0.42, fill: { color: HEX.navy } });
[['응답 집단', 0.15, 2.5], ['가중치 w', 2.7, 1.5], ['추정 배수 X', 4.25, 1.6]].forEach(h => T(s, h[0], { x: M + h[1], y: 2.0, w: h[2], h: 0.42, fontSize: 12, bold: true, color: C.background1, valign: 'middle' }));
ahp.forEach((r, i) => {
  const y = 2.42 + i * 0.42;
  R(s, { x: M, y, w: 6.0, h: 0.42, fill: { color: i % 2 ? HEX.white : HEX.paper } });
  T(s, r[0], { x: M + 0.15, y, w: 2.5, h: 0.42, fontSize: 12, valign: 'middle' });
  T(s, r[1], { x: M + 2.7, y, w: 1.5, h: 0.42, fontSize: 12, valign: 'middle' });
  T(s, r[2], { x: M + 4.25, y, w: 1.6, h: 0.42, fontSize: 12, valign: 'middle' });
});
T(s, 'λ = Σ wᵢ·Xᵢ = 28.57배 (박성수·백민석, 2019). 관행적 10배의 약 2.9배', { x: M, y: 4.2, w: 6.0, h: 0.6, fontSize: 13 });
RR(s, { x: 7.1, y: 1.6, w: 5.63, h: 2.55, fill: { color: HEX.navy } });
T(s, 'N* = N검거 × λ', { x: 7.4, y: 1.8, w: 5.1, h: 0.45, fontSize: 16, color: C.accent6 });
T(s, '668,624명', { x: 7.4, y: 2.3, w: 5.1, h: 0.9, fontSize: 40, bold: true, color: C.background1 });
T(s, '2025년 단속 23,403명 × 28.57. λ 10이면 234,030명', { x: 7.4, y: 3.3, w: 5.1, h: 0.6, fontSize: 12, color: C.accent6 });
T(s, '암수율 적용 원칙: 모든 항목 1명당 비용 × N*', { x: 7.1, y: 4.35, w: 5.6, h: 0.35, fontSize: 14, bold: true });
const lam = [['형사사법비용', '적용', '검거 1명당 처리비용 × N*'], ['고통·생산성', '적용', '사범 1명당 손실 × N*'], ['의료·복지', '적용', '심평원 중독자 = 검거 사범 가정'], ['사회적 혼란·기타', '적용', '1명당 «gp_사회적 혼란·기타»만 원 × N* (11. 14. 수정)']];
lam.forEach((r, i) => {
  const y = 4.75 + i * 0.42;
  T(s, r[0], { x: 7.1, y, w: 1.75, h: 0.38, fontSize: 12, bold: true, valign: 'middle' });
  chip(s, 8.9, y + 0.06, r[1], 'done', 1.0);
  T(s, r[2], { x: 10.05, y, w: 2.7, h: 0.38, fontSize: 10.5, color: C.accent5, valign: 'middle' });
});
source(s, '박성수·백민석(2019), 대검찰청(2026) 표 3-21');
s.addNotes('범죄자 1명이 생길 때 퍼지는 비용을 원단위로 둔다. 검거 사범 1명당 비용 «pc»만 원(«tot»억 ÷ 23,403명)에 실질 사용자 N*를 곱한다. 형사사법과 사회적 혼란·기타를 포함한 모든 항목에 적용한다. 기본값은 λ 10(선행연구와 같음), 28.57은 민감도.');
''')
V['b4ln_raw']=V['b4ln'].replace(',','')
NEW2=NEW2.replace(V['b4ln'] if False else '«b4ln_raw»',V['b4ln_raw'])
# 체계도: orig 415-427 + new cols + orig 436-464 + new footnote
cols=fill(r'''const cols = [
  { t: '의료·복지', tag: 'DC', note: '«g_의료·복지»억', items: [['직접 의료비', '«i_직접 의료비»억 (청구 + 치료보호)', 'done'], ['간접의료비', '«i_간접의료비»억 (직접 × 38.1%)', 'done'], ['정신건강·복지 지원', '«i_정신건강·복지»억 (기관 운영)', 'done']] },
  { t: '생산성', tag: 'IC', note: '«g_생산성»억', items: [['조기 사망', '«i_조기사망»억 (사망 58명)', 'done'], ['이환·입원', '«i_이환·입원»억 (16,027일)', 'done'], ['노동력 상실·미취업', '«i_노동력 상실·미취업»억 (22,242명)', 'done']] },
  { t: '형사사법', tag: 'IC', note: '«g_형사사법»억', items: [['단속·수사', '경찰 «i_경찰»억 · 검찰 «i_검찰»억', 'done'], ['재판', '법원 «i_법원»억', 'done'], ['형 집행·교정', '교도소 «i_교도소»억 · 법무병원 «i_국립법무병원»억 · 보호관찰 «i_보호관찰소»억', 'done']] },
  { t: '피해자·주위', tag: 'IC·PGS', note: '2,547.5억', items: [['2차 범죄 피해', '«i_2차 범죄»억 (상해·성폭력, 범죄 단가)', 'wip'], ['고통비용 PGS', '«g_고통비용»억 (사망 «i_사망 PGS» · 중독자 «i_중독자 PGS»)', 'wip'], ['가족·주변인 케어', '«i_가족 돌봄»억 (가족 의료비, 최저)', 'wip']] },
  { t: '기타(사회적 혼란)', tag: 'DC·IC', note: '374.9억', items: [['예방·홍보·재활', '«i_예방·대응 예산»억 (2024 예산 값)', 'wip'], ['범죄 공포·방어 행동', '0원 (범죄 단가에 포함)', 'done'], ['마약 운전 교통사고', '«i_약물 운전»억 (2025년 33건)', 'done']] },
  { t: '종합', tag: 'SC', note: '«tot»억', items: [['총액 (λ 10)', '«t10» 원', 'done'], ['1명당 비용', '«pc»만 원 (전 항목 ÷ 23,403명)', 'done'], ['SCᵣ', '재복역 1건당 → 비용편익', 'wip']] },
];''')
tixi=seg(415,427)+'\n'+cols+'\n'+seg(436,464)+'\n'+fill(r'''T(s, '금액: 2025년, 억 원, 암수율 미반영. 모든 항목에 λ를 곱해 총액을 냄', { x: M, y: 6.66, w: 8, h: 0.3, fontSize: 10, color: C.accent5 });
s.addNotes('2025년 체계도. 초록 칸은 원고의 2025년 실측이 들어간 항목, 주황 칸은 추정이 남은 항목(고통비용, 2차 범죄, 예방 예산, 가족 돌봄). 미반영 합계 «tot»억 원, λ 10 «t10» 원.');''')
feats=fill(r'''
// ── 비용 산정의 주요 특징 ──
s = content('Ⅳ. 사회적 비용 체계', 'Ⅳ. 사회적 비용 체계 — 산정 원칙', '비용 산정의 주요 특징');
const feats = [
  ['1', '1명당 비용 구조', '모든 항목을 검거 사범 1명당 비용(«pc»만 원)으로 바꾸고 실질 사용자 N*에 곱함. 형사사법·사회적 혼란·기타 포함'],
  ['2', '기관 결산 × 마약류 비율', '기관 결산 총액 × 마약류 처리 인원 비율. 마약류 사범 1명의 비용이 평균 사범과 같다는 평균비용 가정'],
  ['3', '결산 전액을 범죄 대응으로 봄', '경찰·검찰·교정 결산 전액을 범죄 관련으로 간주(박경래 외, 2010 방식). 비범죄 업무 비율 공제는 민감도로 제시'],
  ['4', '이전지출 제외', '기초생활급여·불법 마약 구입비는 사회적 비용에서 제외. 제도 운영비만 계상(Single 외, 2001)'],
  ['5', '중복계상 방지', '치료보호↔건강보험, 치료감호·수용자 의료비, 구금↔미취업 손실은 한 곳에만 계상'],
  ['6', '연간 총액과 생애 비용 분리', '한 해 비용(횡단)과 중독자 1명의 생애 비용은 기준이 달라 더하지 않음. 생애비용은 1명당 값으로 따로 제시'],
  ['7', '기준연도·할인율', '2025년(원고 반영, 고통비용은 2024 환산). 조기사망은 원고의 할인율 4%·임금상승 4%, 생애·비용편익은 4.5%(민감도 3~5%)'],
  ['8', '1인당 값의 산식', '원고의 기관·항목별 1인당 값은 분모가 달라 합산하지 않음. N*에 곱하는 값은 총액 ÷ 검거 사범'],
];
feats.forEach((f, i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const x = M + col * 6.13, y = 1.55 + row * 1.25;
  R(s, { x, y: y + 0.05, w: 0.5, h: 0.5, fill: { color: i < 2 ? HEX.amber : HEX.navy } }, pres.shapes.OVAL);
  T(s, f[0], { x, y: y + 0.05, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: C.background1, align: 'center', valign: 'middle' });
  T(s, f[1], { x: x + 0.65, y, w: 5.3, h: 0.36, fontSize: 15, bold: true });
  T(s, f[2], { x: x + 0.65, y: y + 0.38, w: 5.3, h: 0.8, fontSize: 11.5, color: C.accent5 });
});
s.addNotes('1번: 연구 방침. 모든 비용을 1명당으로 만들고 암수율을 곱한다. 8번: 원고 <표 18>의 기관별 1인당 합(9,979.6만 원)은 N*에 곱하지 않음.');

// ════════ Ⅴ. 집계 비용 ════════
pres.addSection({ title: 'Ⅴ. 집계 비용' });
s = pres.addSlide({ masterName: 'SECTION', sectionTitle: 'Ⅴ. 집계 비용' });
s.addText('Ⅴ', { placeholder: 'num' }); s.addText('집계 비용', { placeholder: 'title' });
s.addText('2025년 총괄(원고 반영), 방침 점검, 1명당 생애비용', { placeholder: 'body' });
''')
# 총괄
def row5(k,desc): return f"['{k}', '{desc}', '{V['g_'+k]}', '{V['gl_n_'+k]}', '{V['gm_n_'+k]}']"
tot_slide=fill(r'''
// ── 사회적 비용 총괄 ──
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 총괄', '2025년 마약류 사회적 비용 «t10» 원 (암수율 10배)');
{
  const hd = ['분야', '항목', '암수율 미반영', 'λ = 10', 'λ = 28.57'];
  const rowsT = [
    @ROWS@
  ];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 12, align: j >= 2 ? 'right' : 'left' } }))].concat(
    rowsT.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: j === 1 ? 10.5 : 12.5, bold: j === 0 || j === 2, color: j === 2 ? HEX.teal : HEX.ink, fill: { color: i % 2 ? HEX.white : HEX.paper }, align: j >= 2 ? 'right' : 'left' } }))));
  tr.push(['합계(억 원)', '', '«tot»', '«t10n»', '«t28n»'].map((c, j) => ({ text: c, options: { bold: true, fontSize: 13, fill: { color: HEX.tealBg }, color: j >= 2 ? HEX.teal : HEX.ink, align: j >= 2 ? 'right' : 'left' } })));
  s.addTable(tr, { x: M, y: 1.55, w: 8.4, colW: [1.75, 3.15, 1.1, 1.15, 1.25], rowH: 0.58, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.04, 0.1, 0.04, 0.1] });
  RR(s, { x: 9.25, y: 1.55, w: 3.48, h: 2.3, fill: { color: HEX.navy } });
  T(s, '사회적 비용 (2025, 암수율 10배)', { x: 9.45, y: 1.7, w: 3.1, h: 0.35, fontSize: 12, color: C.accent6 });
  T(s, '«t10» 원', { x: 9.45, y: 2.05, w: 3.1, h: 0.75, fontSize: 23, bold: true, color: C.background1 });
  T(s, '형사사법 «sh_형사사법» · 고통비용 «sh_고통비용» · 생산성 «sh_생산성» · 사회적 혼란·기타 «sh_사회적 혼란·기타» · 의료·복지 «sh_의료·복지». 미반영 «tot»억 원', { x: 9.45, y: 2.9, w: 3.1, h: 0.8, fontSize: 11, color: C.accent6 });
  T(s, [
    { text: '검거 사범 1명당 «pc»만 원. 모든 항목 = 1명당 × 실질 사용자 N*(λ 10: 234,030명, λ 28.57: 668,624명)', options: { bullet: true, breakLine: true } },
    { text: '실측: 형사사법(원고 11. 8.), 생산성·의료·복지(원고 11. 6.). 추정: 고통비용, 사회적 혼란·기타 일부', options: { bullet: true, breakLine: true } },
    { text: '박성수(2018) 2조 2,389억 원 대비 «ratio»배(4개 분야 «b4ratio»배). 11. 9. 시산(6조 1,249.9억) 대비 +1조 4,191.8억 원', options: { bullet: true } },
  ], { x: 9.25, y: 4.0, w: 3.48, h: 2.5, fontSize: 11, paraSpaceAfter: 6 });
  source(s, '형사사법 원고(2026. 11. 8.), 제3장 제1·2절 원고(2026. 11. 6.), 대검찰청(2026), 한국교통연구원(2025), 연구진 계산. 억 원, 반올림으로 합이 0.1 다를 수 있음');
  s.addNotes('2025년, 암수율 10배 기준 «t10» 원. 형사사법 «gl_형사사법»(«sh_형사사법»), 고통비용 «gl_고통비용»(«sh_고통비용»), 생산성 «gl_생산성»(«sh_생산성»), 사회적 혼란·기타 «gl_사회적 혼란·기타»(«sh_사회적 혼란·기타»), 의료·복지 «gl_의료·복지»(«sh_의료·복지»). 미반영 «tot»억, 28.57배 «t28». 11. 9. 시산과의 차이는 교도소 인원 기준(+9,905억), 사회적 혼란·기타 λ 적용(+4,464억) 등.');
}

// ── 방침 점검 ──
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 방침 점검', '"모든 비용 1명당 × 암수율" 방침 점검 결과');
{
  const hd = ['대상', '1명당 정의', 'λ 처리', '판정', '조치'];
  const rows = [
    ['요약본·발표자료·엑셀: 4개 분야', '검거 사범 1명당 × N*', '형사사법 포함 적용', '준수', '-'],
    ['같은 자료: 사회적 혼란·기타', '총액을 그대로 더함', '미적용', '미준수', '1명당 «gp_사회적 혼란·기타»만 원 × N*로 수정(λ 10 «gl_사회적 혼란·기타»)'],
    ['별지: 사회적 혼란·미산정 비용', '총액', '"암수율 미적용" 명시', '미준수', '같은 방식으로 수정, 별지 문구 정정'],
    ['별지: 생애비용(11. 9.)', '2,231.5만 원(875명 기준)', '1명당 값', '기준 낡음', '이번 생애비용(1명당 «pc»만 원 기준)으로 대체'],
    ['형사사법 원고 <표 18>', '기관별 1인당 합 9,979.6만 원', '언급 없음', '정의 다름', 'N*에 곱하지 않음. 모형 1명당 «gp_형사사법»만 원 병기'],
    ['제3장 원고 제1·2절', '항목 대상자 1인당 합', '"암수율 미적용"', '표현 충돌', '"종합 절에서 1명당 × N*로 환산"으로 수정 권고'],
  ];
  const col = { '준수': HEX.teal, '미준수': HEX.red, '기준 낡음': HEX.red, '정의 다름': HEX.amber, '표현 충돌': HEX.amber };
  const tr = [hd.map(h => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 12 } }))].concat(
    rows.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: 11.5, bold: j === 0 || j === 3, color: j === 3 ? col[c] : HEX.ink, fill: { color: i % 2 ? HEX.white : HEX.paper } } }))));
  s.addTable(tr, { x: M, y: 1.5, w: W - 2 * M, colW: [2.9, 2.5, 1.75, 1.1, 3.88], rowH: 0.55, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.04, 0.1, 0.04, 0.1] });
  RR(s, { x: M, y: 5.5, w: W - 2 * M, h: 1.05, fill: { color: HEX.navyBg } });
  T(s, [
    { text: '4개 분야는 방침대로 만들었고 형사사법에도 λ를 곱하였다. 사회적 혼란·기타만 총액을 λ 없이 더하였다.', options: { bullet: true, breakLine: true } },
    { text: '11. 9. 시산(λ 10 6조 1,249.9억)을 방침대로 고치면 6조 5,714.1억 원. 원고 반영 후 «t10» 원.', options: { bullet: true, breakLine: true } },
    { text: '원고의 1인당 값에 N*를 곱하면 중복 계상(예: 생산성 7억 3,015만 원 × 234,030명 = 170조 원 초과).', options: { bullet: true } },
  ], { x: M + 0.2, y: 5.5, w: W - 2 * M - 0.4, h: 1.05, fontSize: 12, valign: 'middle', paraSpaceAfter: 3 });
  s.addNotes('연구 방침은 모든 비용을 검거 사범 1명당으로 만들고 암수율을 곱해 사회적 총비용을 내는 것. 점검 결과 4개 분야는 준수, 사회적 혼란·기타는 미준수였고 이번에 바로잡음. 원고의 1인당 값은 분모가 달라 N*에 곱하면 안 됨.');
}
''').replace('@ROWS@',',\n    '.join([
 row5('의료·복지',f"직접 의료비 {V['i_직접 의료비']} · 간접의료비 {V['i_간접의료비']} · 정신건강·복지 {V['i_정신건강·복지']}"),
 row5('생산성',f"조기사망 {V['i_조기사망']} · 이환·입원 {V['i_이환·입원']} · 노동력 상실·미취업 {V['i_노동력 상실·미취업']}"),
 row5('형사사법','경찰·검찰·법원·교도소(12. 31.)·국립법무병원·보호관찰소'),
 row5('고통비용',"사망 58명 × 9.9억 + 치료보호 1,649명 × 1.12억 (추정)"),
 row5('사회적 혼란·기타',f"2차 범죄 {V['i_2차 범죄']} · 예방 예산 {V['i_예방·대응 예산']} · 가족 돌봄 {V['i_가족 돌봄']} · 운전 사고 {V['i_약물 운전']}")]))
# 의료·생산성 매칭: orig 524-569 with replaced rows
mp=seg(524,569)
mp=mp.replace("'의료·복지와 생산성 항목별 산식과 금액 (2025년, 2024년 확정치 환산)'","'의료·복지와 생산성 항목별 산식과 금액 (2025년, 제3장 원고)'")
old_rows=mp[mp.index("  const rows = ["):mp.index("  const groups")]
new_rows=fill(r'''  const rows = [
    ['직접 의료비', '청구 진료비 30.18억(입원 20.39 · 외래 9.79) + 치료보호 예산 14.4억(국비·지방비)', '«i_직접 의료비»'],
    ['간접의료비', '직접 의료비 × 38.1%(한국보건사회연구원, 1997)', '«i_간접의료비»'],
    ['정신건강·복지', '치료보호기관 운영 9.0억 · 우수기관 3.0억 · 기타 5.0억 (중복 제외)', '«i_정신건강·복지»'],
    ['조기사망', '사망 58명(20~64세) × 잔여 노동가치, 할인율 4%·임금상승 4%', '«i_조기사망»'],
    ['이환·입원', '입내원 손실 16,027일 × 연령별 일당', '«i_이환·입원»'],
    ['노동력 상실·미취업', '20세 이상 사범 22,242명 × 실직 25% × 조정 50% × 연간 노동가치', '«i_노동력 상실·미취업»'],
  ];
''')
mp=mp.replace(old_rows,new_rows)
mp=mp.replace("['의료·복지', [0, 1, 2], '59.2억 원'], ['생산성', [3, 4, 5], '773.3억 원']",fill("['의료·복지', [0, 1, 2], '«g_의료·복지»억 원'], ['생산성', [3, 4, 5], '«g_생산성»억 원']"))
ms=float(V['g_의료·복지'].replace(',',''))+float(V['g_생산성'].replace(',',''))
def jo(x): return f"{int(x//10000)}조 {x%10000:,.1f}억" if x>=10000 else f"{x:,.1f}억"
mp=mp.replace("'의료·복지·생산성 합계  832.5억 원'",f"'의료·복지·생산성 합계  {ms:,.1f}억 원'")
mp=mp.replace("'     암수율 미반영. 암수율 반영 시 λ 10: 8,324.7억, λ 28.57: 2조 3,783.7억'",f"'     암수율 미반영. 암수율 반영 시 λ 10: {jo(ms*10)}, λ 28.57: {jo(ms*28.57)}'")
mp=mp.replace("source(s, '2024년 확정치: 송도훈_2024년_사회적비용. 환산 계수: 통계청 소비자물가(2025년 2.1%), 대검찰청(2026) 단속 인원(23,022 → 23,403명)');","source(s, '「마약류 사용의 사회적 비용」 제3장 제1·2절 원고(2026. 11. 6.) <표 3-2>~<표 3-22>');")
mp=re.sub(r"s\.addNotes\('2025년 의료·복지와 생산성은.*?'\);",fill("s.addNotes('2025년 의료·복지와 생산성은 제3장 원고(11. 6.)의 실측값. 의료·복지 «g_의료·복지»억, 생산성 «g_생산성»억 원. 원고는 암수율 미적용이라 적었으나, 모형에서는 1명당 계수로 바꿔 N*를 곱함. 조기사망 할인율 4%는 프로젝트 기본 4.5%와 달라 연구진 확정 필요.');"),mp,flags=re.S)
# PGS slide
pg=seg(574,619)
for a,b in [("'고통비용 2,435.9억 원 (λ 10: 2조 4,359.1억 원)'",fill("'고통비용 «g_고통비용»억 원 (λ 10: «gl_고통비용» 원)'")),
 ("['사망 PGS', '59명', '9.9억 원', '583.9', '2024년 58명 × 단속 증가 1.0165 (2025 사망원인통계 미수령, 추정)',",fill("['사망 PGS', '58명', '9.9억 원', '«i_사망 PGS»', '2025년 사망 58명(20~64세, 제3장 원고 <표 3-16>)',")),
 ("'2,435.9', { x: M + 4.5",fill("'«g_고통비용»', { x: M + 4.5")),
 ("'λ 10: 2조 4,359.1억 · λ 28.57: 6조 9,594.0억 (1명당 × N*)'",fill("'λ 10: «gl_고통비용» · λ 28.57: 6조 9,322.4억 (1명당 × N*)'")),
 ("사망자는 2024년 통계에서 추정');","사망자는 제3장 원고(2025년 58명). 고통비용 원고는 미수령');")]:
    assert a in pg,a; pg=pg.replace(a,b)
pg=re.sub(r"s\.addNotes\('2025년 고통비용은.*?'\);",fill("s.addNotes('2025년 고통비용은 사망 58명 × 9.9억 = «i_사망 PGS»억, 치료보호 1,649명 × 1.12억 = «i_중독자 PGS»억, 합계 «g_고통비용»억 원. λ 10이면 «gl_고통비용» 원. 고통비용 원고는 아직 없어 2024년 원단위에 물가를 곱한 추정.');"),pg,flags=re.S)
# 형사사법 bar
cjv=[V['i_'+k].replace(',','') for k in ['교도소','경찰','검찰','법원','보호관찰소','국립법무병원']]
cj=fill(r'''
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 형사사법비용', '2025년 형사사법비용 «gl_형사사법» 원 (λ 10)');
s.addChart(pres.charts.BAR, [{ name: '마약류 비용', labels: ['교도소', '경찰', '검찰', '법원', '보호관찰소', '국립법무병원'], values: [@CJV@] }], {
  x: M, y: 1.5, w: 7.6, h: 4.9, barDir: 'bar', chartColors: [HEX.teal], showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '#,##0.0', dataLabelFontSize: 12, dataLabelColor: HEX.ink, dataLabelFontFace: '+mn-lt',
  catAxisLabelColor: HEX.ink, catAxisLabelFontSize: 13, catAxisLabelFontFace: '+mn-lt', catAxisOrientation: 'maxMin', valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' },
  showLegend: false, showTitle: true, title: '기관별 마약류 비용 (억 원, 2025, 암수율 미반영)', titleFontSize: 13, titleColor: HEX.ink, titleFontFace: '+mn-lt', barGapWidthPct: 40,
});
RR(s, { x: 8.55, y: 1.55, w: 4.18, h: 2.35, fill: { color: HEX.navy } });
T(s, '형사사법비용 (암수율 10배)', { x: 8.8, y: 1.7, w: 3.8, h: 0.35, fontSize: 13, color: C.accent6 });
T(s, '«gl_형사사법»', { x: 8.8, y: 2.05, w: 3.8, h: 0.8, fontSize: 30, bold: true, color: C.background1 });
T(s, '미반영 «g_형사사법»억 원. 6개 기관 2025 실측(검찰은 원고가 2024년 값 사용)', { x: 8.8, y: 2.95, w: 3.75, h: 0.8, fontSize: 12, color: C.accent6 });
T(s, [
  { text: '교도소 52.4%, 경찰 37.0%로 두 기관이 89.4% 차지', options: { bullet: true, breakLine: true } },
  { text: '검거 사범 1명당 형사사법 계수 «gp_형사사법»만 원. 원고 <표 18>의 1인 비용 9,979.6만 원은 기관별 1인당 합이라 쓰지 않음', options: { bullet: true, breakLine: true } },
  { text: '교도소를 연평균(추정 3,608 ÷ 63,680명)으로 하면 «cj_altl» 원(부록 4)', options: { bullet: true } },
], { x: 8.55, y: 4.1, w: 4.18, h: 2.4, fontSize: 12, paraSpaceAfter: 6 });
source(s, '「마약류 범죄의 형사사법 비용」 원고(2025년 기준, 2026. 11. 8.) <표 2>~<표 18>, 마약류만(유해화학물질 제외)');
s.addNotes('2025년: 교도소 «i_교도소»억(결산 1조 6,992.2억 × 7,429 ÷ 64,626명), 경찰 «i_경찰»억, 검찰 «i_검찰»억(2024년 예산·인원), 법원 «i_법원»억, 보호관찰소 «i_보호관찰소»억, 국립법무병원 «i_국립법무병원»억. 미반영 «g_형사사법»억, 암수율 10배 «gl_형사사법» 원.');
''').replace('@CJV@',', '.join(cjv))
# 매칭도
mt=seg(670,717)
old_rows=mt[mt.index("  const rows = ["):mt.index("  const ry")]
cj_sub1=float(V['i_경찰'].replace(',',''))+float(V['i_검찰'].replace(',',''))
cj_sub3=sum(float(V['i_'+k].replace(',','')) for k in ['교도소','국립법무병원','보호관찰소'])
new_rows=fill(r'''  const rows = [
    ['경찰', '결산 13조 3,558.3억 × 13,343 ÷ 1,290,412명', '«i_경찰»', '1인당 1,035.0만'],
    ['검찰', '2024 예산 1조 2,162.6억 × 23,022 ÷ 1,405,185명 (원고)', '«i_검찰»', '1인당 86.6만'],
    ['법원', '형사소송 2,483.9억 × 13,849 ÷ 347,473명', '«i_법원»', '1인당 71.5만'],
    ['교도소', '결산 1조 6,992.2억 × 7,429 ÷ 64,626명 (12. 31.)', '«i_교도소»', '1인당 2,629.3만'],
    ['국립법무병원', '결산 466.5억 × 9 ÷ 823명', '«i_국립법무병원»', '1인당 5,668.8만'],
    ['보호관찰소', '결산 2,009.3억 × 1,853 ÷ 41,138명', '«i_보호관찰소»', '1인당 488.4만'],
  ];
''')+f"  const groups = [['단속·수사', [0, 1], '{cj_sub1:,.1f}억 원', ''], ['재판', [2], '{V['i_법원']}억 원', ''], ['형 집행·교정', [3, 4, 5], '{cj_sub3:,.1f}억 원', '보호관찰 제외 {cj_sub3-float(V['i_보호관찰소'].replace(',','')):,.1f}억 원']];\n"
mt=mt.replace(old_rows,new_rows)
mt=mt.replace("'합계  2,807.0억 원 (λ 10: 2조 8,070.0억)  ·  보호관찰 제외 2,704.8억 원'",fill("'합계  «g_형사사법»억 원 (λ 10: «gl_형사사법»)  ·  1명당 «gp_형사사법»만 원'"))
mt=mt.replace("'     1인당 값은 기관마다 분모가 달라 합산하지 않음(평균비용 가정)'","'     기관별 1인당은 분모가 달라 합산하지 않음'")
mt=mt.replace("source(s, '2025 실측: 교정 결산·1일 평균(교정본부), 검찰 결산(대검 정보공개). 추정: 원고(2024년 기준) <표 2>~<표 18> × 결산 증가 1.037 × 단속 증가 1.0165');","source(s, '「마약류 범죄의 형사사법 비용」 원고(2026. 11. 8.) <표 2>~<표 18>. 기관별 1인당 = 마약류 비용 ÷ 기관 마약류 인원(참고)');")
mt=re.sub(r"s\.addNotes\('2025년 시산 매칭도\..*?'\);",fill("s.addNotes('2025년 매칭도(원고 반영). 6개 기관 모두 원고 실측값. 검찰만 2025년 총처리인원 미공개로 2024년 예산·인원 사용.');"),mt,flags=re.S)
iss=fill(r'''
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 원고 확인 사항', '원고 반영 시 확인할 점 다섯 가지');
const iss = [
  ['교도소 인원 기준: 12. 31. 전체 수용자(미결 포함)', '원고는 교정정보 빅데이터 7,429 ÷ 64,626명 사용. 연평균 추정(3,608 ÷ 63,680명)이면 λ 10에서 «pr_diffl» 원. 교정본부 기준치가 오면 그 값으로 바꿈(부록 4)', 'wip'],
  ['검찰: 표와 계산의 연도 차이', '<표 2>는 2025 결산 1조 2,879.5억 원, 계산은 2024 예산 1조 2,162.6억 원. 2025 결산 × 2024 비율이면 211.0억 원(+11.7억)', 'issue'],
  ['원고 1인당 값의 이름', '형사사법 9,979.6만, 의료·복지 1,013.9만, 생산성 7억 3,015만 원은 분모가 다른 1인당의 합. "해당 항목 대상자 1인당"으로 이름을 바꾸고 모형 1명당 값 병기', 'issue'],
  ['조기사망 할인율', '원고는 할인율 4%·임금상승 4%. 프로젝트 기본 4.5%와 다름. 연구진 확정 필요', 'plan'],
  ['오기', '보호관찰 접수 본문 43,138명(표 41,138명), 표 번호 중복(<표 3>·<표 11>·<표 15>), <표 18> 쉼표 오류, "마약루"', 'issue'],
];
iss.forEach((r, i) => {
  const y = 1.5 + i * 1.0;
  RR(s, { x: M, y, w: W - 2 * M, h: 0.9, fill: { color: HEX.paper } });
  chip(s, M + 0.25, y + 0.15, r[2] === 'issue' ? '수정' : (r[2] === 'wip' ? '회신 대기' : '확정 필요'), r[2], 1.0);
  T(s, r[0], { x: M + 1.45, y: y + 0.08, w: 10.5, h: 0.35, fontSize: 14.5, bold: true });
  T(s, r[1], { x: M + 1.45, y: y + 0.42, w: 10.6, h: 0.46, fontSize: 11.5, color: C.accent5 });
});
source(s, '형사사법 원고(2026. 11. 8.), 제3장 제1·2절 원고(2026. 11. 6.), 연구진 검토');
s.addNotes('원고 반영 시 확인할 점. 교도소 기준은 교정본부 회신 대기. 검찰 연도 차이와 1인당 값의 이름은 원고 수정 권고.');

// ── 1명당 생애 사회적 비용: 모형 ──
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 1명당 생애 사회적 비용 (모형)', '중독자 1명 생애비용: 하한 «floor»만~상한 16억 원');
{
  RR(s, { x: M, y: 1.5, w: W - 2 * M, h: 0.75, fill: { color: HEX.navy } });
  T(s, [
    { text: '생애비용 = 1년차 비용 + Σ ', options: { bold: true } },
    { text: '[활동 중독 × (반복 비용 + 재검거 × 형사사법) + 노동능력 상실 × 노동가치 + 초과 사망 × (사망 PGS + 잔여 소득)] ÷ 할인', options: {} },
  ], { x: M + 0.25, y: 1.5, w: W - 2 * M - 0.5, h: 0.75, fontSize: 13.5, color: C.background1, valign: 'middle' });
  const hd = ['시나리오', '잔여 중독기간', '노동능력 상실', '회복 후 잔존', '초과 사망(활동)', '초과 사망(회복)', '연 재검거'];
  const rows = [['A 조기회복', '5년', '12.5%', '0%', '0.79%', '0.1%', '5%'], ['B 기준', '9년', '15.6%', '50%', '0.97%', '0.2%', '10%'], ['C 만성화', '27년', '31.1%', '100%', '1.21%', '0.3%', '15%']];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.slate }, fontSize: 11.5, align: j ? 'right' : 'left' } }))].concat(
    rows.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: 12, bold: i === 1 || j === 0, fill: { color: i === 1 ? HEX.tealBg : HEX.white }, align: j ? 'right' : 'left' } }))));
  s.addTable(tr, { x: M, y: 2.4, w: W - 2 * M, colW: [2.0, 1.65, 1.65, 1.65, 1.75, 1.75, 1.68], rowH: 0.4, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.1, 0.03, 0.1] });
  const ev = [
    ['기대여명', '통계청 「2024년 생명표」 40세(남 41.9·여 47.4년)·60세(남 23.7·여 28.4년) 남녀 평균에 맞춘 Gompertz 곡선'],
    ['초과 사망', '암페타민류 사용자 조사망률 연 1.14%(0.92~1.42), SMR 6.83 (Stockings et al., 2019). 초과분 = 조사망률 × (1 − 1/6.83)'],
    ['중독기간', '첫 치료~단약 중앙값 9년, 첫 사용~단약 27년 (Dennis et al., 2005)'],
    ['노동능력 상실', '2025년 사범 무직 31.1%(대검찰청, 2026). B는 × 50%, A는 실직 25% × 50%(박성수, 2018)'],
    ['검증', '아편류 의존자 기대여명 일반인보다 남 14.7·여 15.8년 짧음(Lewer et al., 2020). 본 모형 단축 3.9~10.2년'],
  ];
  ev.forEach((r, i) => {
    const y = 4.15 + i * 0.44;
    R(s, { x: M, y, w: W - 2 * M, h: 0.4, fill: { color: i % 2 ? HEX.white : HEX.paper } });
    T(s, r[0], { x: M + 0.12, y, w: 1.6, h: 0.4, fontSize: 11.5, bold: true, valign: 'middle' });
    T(s, r[1], { x: M + 1.8, y, w: W - 2 * M - 1.9, h: 0.4, fontSize: 11, color: C.accent5, valign: 'middle' });
  });
  source(s, '2025년 검거 연령 분포 가중 평균. 2025년 불변가격, 실질 단가 증가 1.7%, 할인율 4.5%(3~5%), 총 누계는 물가 2.1% 반영·할인 없음. 한계: 생명표 보도 자료 인용(KOSIS 원표 확인 필요), 남녀 평균, 회복 후 초과 사망 가정, 국내 연구 없음');
  s.addNotes('1명당 생애비용 모형. 검거 해에 1년차 비용(하한 «floor»만 원)을 내고, 이후 사망 시까지 활동 중독 기간의 반복 비용과 재검거, 노동능력 상실, 초과 사망 비용을 더한다. 기대여명은 통계청 생명표에 초과 사망률(Stockings et al., 2019)을 더해 계산했고 Lewer et al.(2020)과 비교해 검증했다. 국내 마약류 사용자 사망률 연구는 확인되지 않아 국내 자료가 생기면 가장 먼저 바꿀 모수.');
}

// ── 1명당 생애 사회적 비용: 결과 ──
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 1명당 생애 사회적 비용 (결과)', '기준(B) 현재가치 «lf_B_pv45»억 · 명목 누계 «lf_B_nom»억 원');
{
  const hd = ['시나리오', 'PV 3%', 'PV 4%', 'PV 4.5%', 'PV 5%', '명목 누계', '기대여명 단축'];
  const rows = [
    ['A 조기회복', '«lf_A_pv3»', '«lf_A_pv4»', '«lf_A_pv45»', '«lf_A_pv5»', '«lf_A_nom»', '@LEA@년'],
    ['B 기준', '«lf_B_pv3»', '«lf_B_pv4»', '«lf_B_pv45»', '«lf_B_pv5»', '«lf_B_nom»', '@LEB@년'],
    ['C 만성화', '«lf_C_pv3»', '«lf_C_pv4»', '«lf_C_pv45»', '«lf_C_pv5»', '«lf_C_nom» → 16.00', '@LEC@년'],
  ];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 12, align: j ? 'right' : 'left' } }))].concat(
    rows.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: 13, bold: i === 1 || j === 3, color: j === 3 ? HEX.teal : HEX.ink, fill: { color: i === 1 ? HEX.tealBg : HEX.white }, align: j ? 'right' : 'left' } }))));
  s.addTable(tr, { x: M, y: 1.5, w: 7.4, colW: [1.5, 0.9, 0.9, 1.0, 0.9, 1.25, 0.95], rowH: 0.48, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  T(s, '단위 억 원/명. 하한 «floor_e»억 원·상한 16억 원 범위 적용. 현재가치는 모두 범위 안', { x: M, y: 3.5, w: 7.4, h: 0.3, fontSize: 10.5, color: C.accent5 });
  const comp = @COMP@;
  T(s, '구성 (B, 현재가치 4.5%, 억 원)', { x: M, y: 3.9, w: 7.4, h: 0.32, fontSize: 13, bold: true });
  const MXc = Math.max(...comp.map(c => c[1]));
  comp.forEach((c, i) => {
    const y = 4.27 + i * 0.36;
    T(s, c[0], { x: M, y, w: 2.3, h: 0.32, fontSize: 11, valign: 'middle' });
    R(s, { x: M + 2.35, y: y + 0.05, w: 4.3 * c[1] / MXc, h: 0.24, fill: { color: i === 0 ? HEX.slate : HEX.teal } });
    T(s, c[1].toFixed(2), { x: M + 2.45 + 4.3 * c[1] / MXc, y, w: 0.7, h: 0.32, fontSize: 11, bold: true, valign: 'middle' });
  });
  const X = 8.35, TW = W - M - X;
  T(s, '검거 연령별 (B)', { x: X, y: 1.5, w: TW, h: 0.32, fontSize: 13, bold: true });
  const ag = @AGE@;
  const tr2 = [['연령', '인원', 'PV', '누계'].map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.slate }, fontSize: 11, align: j ? 'right' : 'left' } }))].concat(
    ag.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: 11, fill: { color: i % 2 ? HEX.white : HEX.paper }, align: j ? 'right' : 'left' } }))));
  s.addTable(tr2, { x: X, y: 1.85, w: TW, colW: [0.9, 1.05, 1.0, 1.43], rowH: 0.34, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  RR(s, { x: X, y: 4.4, w: TW, h: 2.1, fill: { color: HEX.navyBg } });
  T(s, [
    { text: '초과 사망 고통(PGS)과 노동능력 상실이 가장 크게 움직임', options: { bullet: true, breakLine: true } },
    { text: '16억 원 상한은 C의 명목 누계에서만 닿음', options: { bullet: true, breakLine: true } },
    { text: '참고: 2025년 검거 전원 × B = «cohort»조 원(λ 10 «cohortl»조 원). 연간 사회적 비용과 더하지 않음', options: { bullet: true } },
  ], { x: X + 0.12, y: 4.4, w: TW - 0.24, h: 2.1, fontSize: 11, valign: 'middle', paraSpaceAfter: 4 });
  source(s, '통계청(2025), Stockings et al.(2019), Dennis et al.(2005), Lewer et al.(2020), 대검찰청(2026), 박성수(2018), 연구진 계산');
  s.addNotes('기준 시나리오 B의 1명당 생애 사회적 비용은 현재가치 4.5% «lf_B_pv45»억 원, 명목 총 누계 «lf_B_nom»억 원. A «lf_A_pv45»억, C «lf_C_pv45»억 원. C의 명목 누계 «lf_C_nom»억 원은 상한 16억 원으로 자름. 연간 총비용과는 기준이 달라 더하지 않음.');
}
''')
LE={k:V['le_'+k][2] for k in 'ABC'}
iss=iss.replace('@LEA@',LE['A']).replace('@LEB@',LE['B']).replace('@LEC@',LE['C'])
comp=[[k,float(v)] for k,v in V['lc_B'].items()]
iss=iss.replace('@COMP@',json.dumps(comp,ensure_ascii=False))
iss=iss.replace('@AGE@',json.dumps([[f"{a[0]}세",a[1],a[2],a[3]] for a in V['age']],ensure_ascii=False))
six=seg(734,818)
six=six.replace("['사회적 혼란', '2차 범죄 건수, 2025년 예산', '잠정 496.0억. 마약 상태 범죄 건수(범죄분석)와 예산표로 확정', 'final'],",fill("['사회적 혼란', '2차 범죄 건수, 2025년 예산', '잠정 496.0억(λ 10 «gl_사회적 혼란·기타»). 마약 상태 범죄 건수와 예산표로 확정', 'final'],"))
seven=seg(819,862).replace("{ text: '서식3: 마약류 1일 평균 수용인원(2024·2025). 12월 말 현원 기준의 민감도용', options: { bullet: true } },","{ text: '서식 3: 마약류 수용인원의 기관 기준치(2024·2025, 수형자·미결 구분)', options: { bullet: true } },")
seven=seven.replace("'고통비용 시나리오, 1명당 비용 계수, 구성비, 교도소 인원 수정, 암수율별 항목표'","'고통비용 시나리오, 1명당 비용 계수, 구성비, 교도소 인원 기준, 암수율별 항목표'")
assert '서식 3: 마약류 수용인원' in seven
# 부록 1
pg_rows=",\n    ".join(f"['{lab}', '{sh}', '{V['pg_'+k][0]}', '{V['pg_'+k][1]}', '{V['pg_'+k][2]}', '{V['pg_'+k][3]}', '{V['pg_'+k][4]}', {fl}]" for lab,sh,k,fl in [
 ('선행연구 시점 가구 구조 (2016)','27.9%','s16',0),('기본: 원단위 조사 시점 (2024)','36.1%','s24',1),('최근 가구 구조 (2025)','36.6%','s25',0),('참고: 본인 고통만 (가족 제외)','—','own',2),('참고: PGS 미반영','—','zero',2)])
ap1=seg(863,893)
ap1=ap1.replace("'가구 구조별 4개 분야 λ 10: 6조 630.0억~6조 2,785.7억 원'",fill("'가구 구조별 4개 분야 λ 10: «pg_lo»~«pg_hi» 원'"))
a=ap1.index("  const rows = [")+len("  const rows = [\n"); b=ap1.index("  ];",a)
ap1=ap1[:a]+"    "+pg_rows+"\n"+ap1[b:]
ap1=ap1.replace("1인가구 증가(27.9% → 36.6%)로 가족 고통 몫이 줄어 PGS는 2016년 구조 대비 215.6억 원(λ 10 2,155.7억) 감소",fill("1인가구 증가(27.9% → 36.6%)로 가족 고통 몫이 줄어 PGS는 2016년 구조 대비 «pg_d16»억 원(λ 10 «pg_d16l»억) 감소"))
ap1=ap1.replace("원단위 조사(2024)와 최근(2025)의 차이는 12.4억 원으로 작음",fill("원단위 조사(2024)와 최근(2025)의 차이는 «pg_d25»억 원으로 작음"))
ap1=re.sub(r"s\.addNotes\('2025년 시산 PGS.*?'\);",fill("s.addNotes('2025년 PGS «g_고통비용»억 원 기준의 가구 구조 시나리오. 4개 분야 λ 10은 2016년 구조 «pg_hi», 기본 «b4l», 2025년 구조 «pg_lo» 원. 본인 고통 비중 35%는 가정이며 원보고서 확인 필요.');"),ap1,flags=re.S)
# 부록 2
def P_(k): return V['p_'+k]
ap2=fill(r'''
// 부록 2. 중독자 1명당 비용 계수
s = content('부록', '부록 2 — 중독자 1명당 비용 계수', '중독자(검거 사범) 1명이 늘 때 사회적 비용 «pc»만 원');
{
  const L = [
    ['형사사법', '«gp_형사사법»', [['교도소', '«p_교도소»'], ['경찰', '«p_경찰»'], ['검찰', '«p_검찰»'], ['법원', '«p_법원»'], ['보호관찰소', '«p_보호관찰소»'], ['국립법무병원', '«p_국립법무병원»']], HEX.navy],
    ['고통비용 (PGS)', '«gp_고통비용»', [['중독자 PGS', '«p_중독자 PGS»'], ['사망 PGS', '«p_사망 PGS»']], HEX.red],
    ['생산성', '«gp_생산성»', [['조기사망', '«p_조기사망»'], ['노동력 상실·미취업', '«p_노동력 상실·미취업»'], ['이환·입원', '«p_이환·입원»']], HEX.amber],
    ['사회적 혼란·기타', '«gp_사회적 혼란·기타»', [['예방·대응 예산', '«p_예방·대응 예산»'], ['2차 범죄', '«p_2차 범죄»'], ['약물 운전', '«p_약물 운전»'], ['가족 돌봄', '«p_가족 돌봄»']], HEX.slate],
    ['의료·복지', '«gp_의료·복지»', [['직접 의료비', '«p_직접 의료비»'], ['정신건강·복지', '«p_정신건강·복지»'], ['간접의료비', '«p_간접의료비»']], HEX.teal],
  ];
  const cw = (W - 2 * M - 4 * 0.12) / 5;
  L.forEach((g, i) => {
    const x = M + i * (cw + 0.12);
    R(s, { x, y: 1.55, w: cw, h: 0.95, fill: { color: g[3] } });
    T(s, g[0], { x: x + 0.12, y: 1.6, w: cw - 0.24, h: 0.35, fontSize: 12.5, bold: true, color: C.background1 });
    T(s, g[1] + '만 원', { x: x + 0.12, y: 1.95, w: cw - 0.24, h: 0.5, fontSize: 19, bold: true, color: C.background1 });
    g[2].forEach((it, j) => {
      const y = 2.6 + j * 0.46;
      R(s, { x, y, w: cw, h: 0.42, fill: { color: j % 2 ? HEX.white : HEX.paper } });
      T(s, it[0], { x: x + 0.1, y, w: 1.45, h: 0.42, fontSize: 10.5, valign: 'middle' });
      T(s, it[1] + '만', { x: x + 1.4, y, w: cw - 1.5, h: 0.42, fontSize: 11.5, bold: true, align: 'right', valign: 'middle' });
    });
  });
  RR(s, { x: M, y: 5.55, w: W - 2 * M, h: 0.95, fill: { color: HEX.navy } });
  T(s, [
    { text: '합계 «pc»만 원 / 1명', options: { bold: true, fontSize: 16, breakLine: true } },
    { text: '계수 = 2025년 항목별 비용 ÷ 검거 사범 23,403명. 암수율 반영 값 = 계수 × 실질 사용자 N*(λ 10: 234,030명, λ 28.57: 668,624명). 사회적 혼란·기타 포함 모든 항목에 적용. 기관별 계수는 평균비용 가정', options: { fontSize: 10.5, color: HEX.mist } },
  ], { x: M + 0.25, y: 5.55, w: W - 2 * M - 0.5, h: 0.95, color: C.background1, valign: 'middle' });
  source(s, '형사사법·제3장 원고(2026. 11.), 한국교통연구원(2025), 대검찰청(2026), 연구진 계산. 단위 만 원/명');
  s.addNotes('2025년 1명당 비용 계수. 형사사법 «gp_형사사법»만, 고통비용 «gp_고통비용»만, 생산성 «gp_생산성»만, 사회적 혼란·기타 «gp_사회적 혼란·기타»만, 의료·복지 «gp_의료·복지»만, 합계 «pc»만 원. 세부로는 교도소 «p_교도소»만, 중독자 PGS «p_중독자 PGS»만, 경찰 «p_경찰»만 원 순.');
}

// 부록 3. 비용 비중
s = content('부록', '부록 3 — 사회적 비용 구성비', '형사사법 «sh_형사사법» · 고통비용 «sh_고통비용» · 생산성 «sh_생산성» (λ 10)');
{
  s.addChart(pres.charts.DOUGHNUT, [{ name: '구성비', labels: ['형사사법', '고통비용(PGS)', '생산성', '사회적 혼란·기타', '의료·복지'], values: [@DV@] }], {
    x: M, y: 1.45, w: 6.4, h: 5.1, holeSize: 52, chartColors: [HEX.navy, HEX.red, HEX.amber, HEX.slate, HEX.teal],
    showPercent: true, showValue: false, showLegend: false, dataLabelColor: HEX.white, dataLabelFontSize: 13, dataLabelFontBold: true, dataLabelPosition: 'bestFit',
  });
  T(s, [{ text: '«t10»', options: { bold: true, fontSize: 20, breakLine: true } }, { text: 'λ 10', options: { fontSize: 11, color: HEX.slate } }], { x: M + 1.95, y: 3.55, w: 2.5, h: 0.9, align: 'center', valign: 'middle' });
  const leg = [['형사사법', '«gl_형사사법»', '«sh_형사사법»', HEX.navy], ['고통비용 (PGS)', '«gl_고통비용»', '«sh_고통비용»', HEX.red], ['생산성', '«gl_생산성»', '«sh_생산성»', HEX.amber], ['사회적 혼란·기타', '«gl_사회적 혼란·기타»', '«sh_사회적 혼란·기타»', HEX.slate], ['의료·복지', '«gl_의료·복지»', '«sh_의료·복지»', HEX.teal]];
  leg.forEach((l, i) => {
    const y = 1.6 + i * 0.66;
    R(s, { x: 7.6, y: y + 0.1, w: 0.32, h: 0.32, fill: { color: l[3] } });
    T(s, l[0], { x: 8.05, y, w: 2.2, h: 0.52, fontSize: 14, bold: true, valign: 'middle' });
    T(s, l[1], { x: 10.0, y, w: 1.6, h: 0.52, fontSize: 14, align: 'right', valign: 'middle' });
    T(s, l[2], { x: 11.6, y, w: 1.1, h: 0.52, fontSize: 14, bold: true, color: l[3], align: 'right', valign: 'middle' });
  });
  RR(s, { x: 7.6, y: 5.0, w: 5.13, h: 1.4, fill: { color: HEX.paper } });
  T(s, [
    { text: '모든 항목에 같은 λ를 곱하므로 구성비는 λ와 무관', options: { bullet: true, breakLine: true } },
    { text: '교도소 인원 기준(12. 31.)으로 형사사법 비중이 커짐', options: { bullet: true, breakLine: true } },
    { text: 'PGS 시나리오(부록 1)에 따라 고통비용 비중 «pg_shr»', options: { bullet: true } },
  ], { x: 7.75, y: 5.0, w: 4.9, h: 1.4, fontSize: 11, valign: 'middle', paraSpaceAfter: 2 });
  source(s, '형사사법·제3장 원고(2026. 11.), 한국교통연구원(2025), 연구진 계산');
  s.addNotes('2025년, 암수율 10배 기준 «t10» 원의 구성비. 형사사법 «sh_형사사법», 고통비용 «sh_고통비용», 생산성 «sh_생산성», 사회적 혼란·기타 «sh_사회적 혼란·기타», 의료·복지 «sh_의료·복지».');
}

// 부록 4. 교도소 인원 기준
s = content('부록', '부록 4 — 교도소 인원 기준 비교', '12. 31. 전체 수용자(원고) vs 연평균 추정: λ 10에서 «pr_diffl» 원 차이');
{
  const hd = ['구분', '12. 31. 전체 수용자 (원고 반영)', '연평균 (추정)', '차이'];
  const rows = [
    ['교도소 마약류 인원 ÷ 전체 수용', '7,429 ÷ 64,626명', '3,608(추정) ÷ 63,680명', ''],
    ['마약류 비율', '11.50%', '5.67%', '−5.83%p'],
    ['교도소 비용 (결산 1조 6,992.2억 × 비율)', '«i_교도소»억', '«pr_alt»억', '«pr_diff»억'],
    ['형사사법 6개 기관 (암수율 미반영)', '«g_형사사법»억', '«cj_alt»억', '«pr_diff»억'],
    ['형사사법 (λ 10)', '«gl_형사사법»', '«cj_altl»', '«pr_diffl»'],
    ['사회적 비용 전체 (λ 10)', '«t10»', '«tot_altl»', '«pr_diffl»'],
    ['교도소 λ 10 금액 ÷ 교정 결산', '«pr_share»', '«pr_share_alt»', ''],
  ];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 12, align: j ? 'right' : 'left' } }))].concat(
    rows.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: 12.5, bold: i === 4 || i === 5 || j === 1, color: j === 3 ? HEX.red : (j === 1 ? HEX.teal : HEX.ink), fill: { color: i === 5 ? HEX.tealBg : (i % 2 ? HEX.white : HEX.paper) }, align: j ? 'right' : 'left' } }))));
  s.addTable(tr, { x: M, y: 1.55, w: W - 2 * M, colW: [4.4, 2.6, 2.6, 2.53], rowH: 0.48, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.04, 0.12, 0.04, 0.12] });
  RR(s, { x: M, y: 5.6, w: W - 2 * M, h: 0.92, fill: { color: HEX.amberBg } });
  T(s, [
    { text: '현재 처리  ', options: { bold: true } },
    { text: '원고는 교정본부 교정정보 빅데이터의 12. 31. 전체 수용자(미결 포함)를 썼다. 교정통계연보 2024년 3,477명은 12. 31. 수형자다. 교정본부에 기관 기준치(2024·2025)를 요청하였고, 회신이 오면 그 값으로 바꾼다', options: {} },
  ], { x: M + 0.2, y: 5.6, w: W - 2 * M - 0.4, h: 0.92, fontSize: 11.5, valign: 'middle' });
  source(s, '형사사법 원고(2026. 11. 8.) <표 12>, 교정본부 회신(2025 결산, 1일 평균 63,680명), 교정통계연보(2024 비율), 연구진 계산');
  s.addNotes('원고 기준(7,429 ÷ 64,626명)이면 교도소 «i_교도소»억 원, 연평균 추정(3,608 ÷ 63,680명)이면 «pr_alt»억 원. 암수율 10배에서 «pr_diffl» 원 차이. 교정본부 기준치 회신 대기.');
}
''').replace('@DV@',', '.join(V['gl_n_'+k].replace(',','') for k in ['형사사법','고통비용','생산성','사회적 혼란·기타','의료·복지']))
# 부록 5
def ii(k): return float(V['i_'+k].replace(',',''))
def tri(ks,f): return ' · '.join(f(k) for k in ks)
fi=lambda k:V['i_'+k]; fp=lambda k:V['p_'+k]; fl=lambda k:V['l_'+k]; fm=lambda k:V['m_'+k]
def grp(name,ksets,lab):
    out=[f"['{name}', '소계', '{V['g_'+lab]}', '{V['gp_'+lab]}', '{V['gl_n_'+lab]}', '{V['gm_n_'+lab]}', '{V['sh_'+lab]}', 1]"]
    for desc,ks in ksets: out.append(f"['', '{desc}', '{tri(ks,fi)}', '{tri(ks,fp)}', '{tri(ks,fl)}', '{tri(ks,fm)}', '', 0]")
    return out
R5=[]
R5+=grp('형사사법',[('교도소 · 경찰 · 검찰',['교도소','경찰','검찰']),('법원 · 보호관찰소 · 국립법무병원',['법원','보호관찰소','국립법무병원'])],'형사사법')
R5+=grp('고통비용',[('중독자(1,649명) · 사망(58명)',['중독자 PGS','사망 PGS'])],'고통비용')
R5+=grp('생산성',[('조기사망 · 미취업 · 이환·입원',['조기사망','노동력 상실·미취업','이환·입원'])],'생산성')
R5+=grp('의료·복지',[('직접 의료 · 간접 · 정신건강·복지',['직접 의료비','간접의료비','정신건강·복지'])],'의료·복지')
R5+=grp('사회혼란 등',[('예방 · 2차 범죄',['예방·대응 예산','2차 범죄']),('운전 · 가족',['약물 운전','가족 돌봄'])],'사회적 혼란·기타')
R5.append(f"['합계', '', '{V['tot']}', '{V['pc']}', '{V['t10n']}', '{V['t28n']}', '100%', 2]")
ap5=seg(977,1001)
a=ap5.index("  const R5 = [")+len("  const R5 = [\n"); b=ap5.index("  ];",a)
ap5=ap5[:a]+"    "+",\n    ".join(R5)+",\n"+ap5[b:]
ap5=ap5.replace("rowH: 0.34","rowH: 0.31")
ap5=ap5.replace("'1명당 계수 = 2025년 항목 비용 ÷ 검거 사범 23,403명. 암수율 반영 금액 = 1명당 계수 × 실질 사용자. 비중은 λ 10 기준. 사회적 혼란·기타는 암수율 미적용'","'1명당 계수 = 2025년 항목 비용 ÷ 검거 사범 23,403명. 암수율 반영 금액 = 1명당 계수 × 실질 사용자. 비중은 λ 10 기준. 모든 항목에 암수율 적용'")
ap5=ap5.replace("source(s, '2025년 시산(실측 + 2024년 확정치 환산), 한국교통연구원(2025), 대검찰청(2026), 박성수·백민석(2019), 연구진 계산');","source(s, '형사사법·제3장 원고(2026. 11.), 한국교통연구원(2025), 대검찰청(2026), 박성수·백민석(2019), 연구진 계산');")
ap5=re.sub(r"s\.addNotes\('2025년 시산, 암수율 10배와.*?'\);",fill("s.addNotes('2025년, 암수율 10배와 28.57배의 항목별 금액. 10배 합계 «t10» 원, 28.57배 «t28» 원. 사회적 혼란·기타 포함 모든 항목에 λ 적용.');"),ap5,flags=re.S)
tail=seg(1002,1010).replace("중간보고_마약류사회적비용_2025기준_시산.pptx","중간보고_마약류사회적비용_2025기준_원고반영.pptx").replace("'/home/claude/deck/","'/home/claude/deck25b/")
mid=seg(157,319)
for a,b in PATCH2: 
    assert a in mid,a; mid=mid.replace(a,b)
out='\n'.join([head,NEW1,mid,NEW2,tixi,feats,tot_slide,mp,'',pg,cj,mt,iss,six,seven,ap1,ap2,ap5,tail])
assert '«' not in out, re.findall('«[^»]*»',out)[:5]
open('build.js','w').write(out); print('ok',len(out.split('\n')))
