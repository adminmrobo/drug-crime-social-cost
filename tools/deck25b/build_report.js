// 중간보고 PPT — 2025년 기준 보고용
const pptxgen = require('pptxgenjs');
const { applyTheme } = require('/mnt/skills/public/pptx/scripts/apply_theme.js');

const THEME = {
  name: 'Drug Social Cost Interim',
  headFontFace: '맑은 고딕',
  bodyFontFace: '맑은 고딕',
  colors: {
    dk1: '1B2433', lt1: 'FFFFFF', dk2: '1F3552', lt2: 'EEF1F5',
    accent1: '1F3552', accent2: '1F7A6B', accent3: 'B8721A', accent4: '9A3B34', accent5: '6B7A90', accent6: 'C9D3E0',
    hlink: '1F3552', folHlink: '6B7A90',
  },
};
const HEX = { navy: '1F3552', teal: '1F7A6B', amber: 'B8721A', red: '9A3B34', slate: '6B7A90', mist: 'C9D3E0', ink: '1B2433', paper: 'EEF1F5', white: 'FFFFFF',
  tealBg: 'E2F1EE', amberBg: 'FBF0DF', navyBg: 'E6ECF4', redBg: 'F6E4E2' };

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = '마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 — 중간보고';
pres.author = '박성수(세명대학교 경찰학과)';
pres.subject = '중간보고';
const C = pres.SchemeColor;
const W = 13.333, M = 0.6;
const FOOT = '중간보고(2025년 기준) · 마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석';

// ── 레이아웃 ──
pres.defineSlideMaster({
  title: 'COVER', background: { color: HEX.navy },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: M, y: 2.0, w: W - 2 * M, h: 1.7, fontSize: 36, bold: true, color: C.background1, valign: 'top', margin: 0, align: 'left' }, text: '' } },
    { placeholder: { options: { name: 'body', type: 'body', x: M, y: 4.0, w: W - 2 * M, h: 2.4, fontSize: 18, color: C.accent6, valign: 'top', margin: 0, align: 'left' }, text: '' } },
  ],
});
pres.defineSlideMaster({
  title: 'SECTION', background: { color: HEX.navy },
  objects: [
    { placeholder: { options: { name: 'num', type: 'body', x: M, y: 2.2, w: 3, h: 1.2, fontSize: 60, bold: true, color: C.accent3, margin: 0, align: 'left' }, text: '' } },
    { placeholder: { options: { name: 'title', type: 'title', x: M, y: 3.45, w: W - 2 * M, h: 1.0, fontSize: 36, bold: true, color: C.background1, margin: 0, align: 'left' }, text: '' } },
    { placeholder: { options: { name: 'body', type: 'body', x: M, y: 4.55, w: W - 2 * M, h: 1.2, fontSize: 18, color: C.accent6, margin: 0, valign: 'top', align: 'left' }, text: '' } },
  ],
});
pres.defineSlideMaster({
  title: 'CONTENT', background: { color: HEX.white },
  margin: [0.5, 0.6, 0.6, 0.6],
  objects: [
    { placeholder: { options: { name: 'kicker', type: 'body', x: M, y: 0.32, w: 9, h: 0.32, fontSize: 12, bold: true, color: C.accent5, margin: 0, align: 'left' }, text: '' } },
    { placeholder: { options: { name: 'title', type: 'title', x: M, y: 0.62, w: W - 2 * M, h: 0.72, fontSize: 28, bold: true, color: C.text1, margin: 0, valign: 'top', align: 'left' }, text: '' } },
    { text: { text: FOOT, options: { x: M, y: 7.05, w: 9, h: 0.28, fontSize: 9, color: C.accent5, margin: 0 } } },
  ],
  slideNumber: { x: W - M - 0.6, y: 7.05, w: 0.6, h: 0.28, fontSize: 9, color: HEX.slate, align: 'right' },
});

// ── 도우미 ──
let n = 0;
const SUBS = { 'ᵣ': ['r', 'sub'], 'ₜ': ['t', 'sub'], 'ᵢ': ['i', 'sub'], 'ᵗ': ['t', 'sup'] };
function runs(txt) {
  const arr = typeof txt === 'string' ? [{ text: txt, options: {} }] : txt;
  const out = [];
  arr.forEach(r => {
    const parts = r.text.split(/([ᵣₜᵢᵗ])/);
    let first = true;
    parts.forEach((p, i) => {
      if (!p) return;
      const o = Object.assign({}, r.options);
      const last = i === parts.length - 1 || parts.slice(i + 1).every(x => !x);
      if (!last) delete o.breakLine;
      if (!first) { delete o.bullet; delete o.paraSpaceAfter; delete o.paraSpaceBefore; delete o.align; }
      first = false;
      if (SUBS[p]) { o.subscript = SUBS[p][1] === 'sub'; o.superscript = SUBS[p][1] === 'sup'; out.push({ text: SUBS[p][0], options: o }); }
      else out.push({ text: p, options: o });
    });
  });
  return out;
}
const T = (s, txt, o) => s.addText(runs(txt), Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: C.text1, valign: 'top' }, o, { objectName: 't' + (++n) }));
const R = (s, o, shape) => s.addShape(shape || pres.shapes.RECTANGLE, Object.assign({ line: { type: 'none' } }, o, { objectName: 'r' + (++n) }));
const RR = (s, o) => R(s, Object.assign({ rectRadius: 0.08 }, o), pres.shapes.ROUNDED_RECTANGLE);
function content(section, kicker, title) {
  const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: section });
  s.addText(kicker, { placeholder: 'kicker' });
  s.addText(title, { placeholder: 'title' });
  return s;
}
function chip(s, x, y, label, kind, w) {
  const map = { prog: [HEX.navy, HEX.white], done: [HEX.teal, HEX.white], wip: [HEX.amber, HEX.white], new: [HEX.white, HEX.ink], plan: [HEX.slate, HEX.white], issue: [HEX.red, HEX.white] };
  const [bg, fg] = map[kind];
  RR(s, { x, y, w: w || 0.9, h: 0.26, fill: { color: bg }, line: kind === 'new' ? { color: HEX.ink, width: 0.75, dashType: 'dash' } : { type: 'none' }, rectRadius: 0.13 });
  T(s, label, { x, y, w: w || 0.9, h: 0.26, fontSize: 10, bold: true, color: fg, align: 'center', valign: 'middle' });
}
function stat(s, x, y, w, big, label, sub, color) {
  T(s, big, { x, y, w, h: 0.75, fontSize: 34, bold: true, color: color || C.accent1, valign: 'bottom' });
  T(s, label, { x, y: y + 0.82, w, h: 0.34, fontSize: 14, bold: true });
  if (sub) T(s, sub, { x, y: y + 1.16, w, h: 0.5, fontSize: 11, color: C.accent5 });
}
function source(s, txt) { T(s, '자료: ' + txt, { x: M, y: 6.66, w: W - 2 * M, h: 0.3, fontSize: 10, color: C.accent5 }); }


// ════════ 1. 표지 ════════
pres.addSection({ title: '표지' });
let s = pres.addSlide({ masterName: 'COVER', sectionTitle: '표지' });
s.addText('마약류범죄와 교정기관 중독재활 체계의\n사회적 비용 비교분석', { placeholder: 'title' });
s.addText([
  { text: '중간보고 · 2025년 기준', options: { bold: true, color: HEX.white, breakLine: true } },
  { text: ' ', options: { fontSize: 10, breakLine: true } },
  { text: '연구책임자  박성수 교수 (세명대학교 경찰학과)', options: { breakLine: true } },
  { text: '2026. 11.', options: {} },
], { placeholder: 'body' });
s.addNotes('표지. 2025년 기준.');

// ════════ 2. 목차 ════════
pres.addSection({ title: '개요' });
s = content('개요', '목차', '보고 순서와 장별 진행 상태');
const toc = [
  ['Ⅰ', '연구 배경', '마약류 범죄 현황과 처벌 중심 대응의 한계', 'done', '정리 완료'],
  ['Ⅱ', '연구 설계', '범위·방법·자료 확보 현황', 'done', '정리 완료'],
  ['Ⅲ', '이론 검토', '선행연구, 암수율과 실질 사용자 수 N*', 'done', '정리 완료'],
  ['Ⅳ', '사회적 비용 체계', '전체 체계도와 비용 산정의 주요 특징', 'done', '확정'],
  ['Ⅴ', '집계 비용', '2025년 총괄, 항목별 비용, 1인당 생애비용', 'done', '확정'],
  ['Ⅵ', '교정 재활 비용편익', '재복역 실측과 증분비용, B/C', 'done', '확정'],
  ['Ⅶ', '향후 계획', '최종보고서 작성과 정책 제언', 'plan', '계획'],
];
toc.forEach((r, i) => {
  const y = 1.65 + i * 0.68;
  R(s, { x: M, y, w: W - 2 * M, h: 0.58, fill: { color: i % 2 ? HEX.white : HEX.paper } });
  T(s, r[0], { x: M + 0.2, y, w: 0.6, h: 0.58, fontSize: 20, bold: true, color: C.accent1, valign: 'middle' });
  T(s, r[1], { x: M + 0.9, y, w: 3.2, h: 0.58, fontSize: 17, bold: true, valign: 'middle' });
  T(s, r[2], { x: M + 4.2, y, w: 6.0, h: 0.58, fontSize: 14, color: C.accent5, valign: 'middle' });
  chip(s, W - M - 1.4, y + 0.16, r[4], r[3], 1.2);
});
s.addNotes('Ⅰ~Ⅵ장은 2025년 기준으로 확정. 1인당 생애비용은 별지 2로 함께 제출.');

// ════════ 3. 요약 ════════
s = content('개요', '중간보고 요약', '2025년 마약류 사회적 비용 7조 5,441.7억 원 (암수율 10배)');
const sum = [
  ['7조 5,441.7억', '사회적 비용 (λ 10)', '1명당 3,223.6만 원 × 234,030명. 모든 항목에 λ 적용. 미반영 7,544.2억 원', HEX.teal],
  ['3조 7,282.0억', '형사사법비용', '6개 기관 2025 실측(형사사법 추계). 미반영 3,728.2억 원', HEX.navy],
  ['2조 4,264.1억', '고통비용 (PGS)', '사망 58명 × 9.9억 + 치료보호 1,649명 × 1.12억', HEX.red],
  ['8,149.7억', '생산성 손실', '조기사망 · 미취업 · 이환·입원 (의료·생산성 추계 실측)', HEX.amber],
  ['4,960.4억 · 785.6억', '사회적 혼란·기타 · 의료·복지', '2차 범죄·예방 예산·가족·운전 / 직접·간접 의료·정신건강 (의료·생산성 추계)', HEX.slate],
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
  { text: '박성수(2018) 2조 2,389억 원 대비 3.37배. 같은 4개 분야 범위로는 3.15배(물가 10.1%, 검거 인원 36.6%, 1명당 실질 53.3%)', options: { bullet: true, breakLine: true } },
  { text: '암수율 28.57배(민감도) 21조 5,537.0억 원. 교도소 7,429명 = 기결 4,188 + 미결 3,241명(교정본부 확인). 교정 재활 B/C 0.22~0.28(문헌 효과 적용 시 0.50~0.66).', options: { bullet: true, breakLine: true } },
  { text: '마약사범(중독자) 1인당 생애 사회적 비용: B 기준 명목 누계 12.28억 원(현재가치 3.97억 원). 별지 2', options: { bullet: true } },
], { x: M, y: 4.5, w: W - 2 * M, h: 2.3, fontSize: 14, paraSpaceAfter: 5 });
s.addNotes('2025년 사회적 비용은 암수율 10배 기준 7조 5,441.7억 원. 모든 항목을 검거 사범 1명당 값(합계 3,223.6만 원)으로 바꾸고 실질 사용자 234,030명을 곱함. 미반영 7,544.2억, 28.57배 21조 5,537.0억. 1인당 생애비용은 B 기준 명목 누계 12.28억 원(현재가치 3.97억 원).');


// ════════ Ⅰ. 연구 배경 ════════
pres.addSection({ title: 'Ⅰ. 연구 배경' });
s = pres.addSlide({ masterName: 'SECTION', sectionTitle: 'Ⅰ. 연구 배경' });
s.addText('Ⅰ', { placeholder: 'num' }); s.addText('연구 배경', { placeholder: 'title' });
s.addText('마약류 범죄 현황과 처벌 중심 대응의 한계', { placeholder: 'body' });

s = content('Ⅰ. 연구 배경', 'Ⅰ. 연구 배경 — 마약류 범죄 현황', '단속 인원 3년 연속 2만 명대');
s.addChart(pres.charts.BAR, [{ name: '단속 인원', labels: ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'], values: [12613, 16044, 18050, 16153, 18395, 27611, 23022, 23403] }], {
  x: M, y: 1.55, w: 7.6, h: 4.9, barDir: 'col', chartColors: [HEX.mist, HEX.mist, HEX.mist, HEX.mist, HEX.mist, HEX.navy, HEX.navy, HEX.teal],
  invertedColors: [HEX.mist], showValue: true, dataLabelPosition: 'outEnd', dataLabelFontSize: 11, dataLabelColor: HEX.ink, dataLabelFormatCode: '#,##0', dataLabelFontFace: '+mn-lt',
  catAxisLabelColor: HEX.ink, catAxisLabelFontSize: 12, catAxisLabelFontFace: '+mn-lt', valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' },
  showLegend: false, showTitle: true, title: '마약류 사범 단속 인원 (명)', titleFontSize: 13, titleColor: HEX.ink, titleFontFace: '+mn-lt', barGapWidthPct: 45,
});
stat(s, 8.75, 1.65, 4.0, '23,403명', '2025년 단속 인원', '2024년 23,022명 대비 +1.65%', HEX.teal);
stat(s, 8.75, 3.35, 4.0, '59.4%', '20·30대 비중 (2025)', '23,403명 중 13,899명. 10대 674명', HEX.navy);
T(s, '2023년 27,611명(최다) 이후 2024년 23,022명, 2025년 23,403명으로 2만 명대 지속', { x: 8.75, y: 5.2, w: 4.0, h: 1.0, fontSize: 13 });
source(s, '대검찰청(2026), 「2025 마약류 범죄백서」 표 3-1·3-21·3-6');

s = content('Ⅰ. 연구 배경', 'Ⅰ. 연구 배경 — 처벌 중심 대응의 한계', '재범률 30% 안팎, 치료 연계 인원은 소수 (2025)');
const lim = [
  ['29.8%', '마약류 사범 재범률 (2025)', '입건 전과 기준(대검찰청). 2024년 34.5%', HEX.red],
  ['7,429명', '교정시설 마약류 수용인원', '2025. 12. 말 전체 64,626명의 11.5%', HEX.navy],
  ['1,649명', '치료보호 인원 (2025)', '외래 1,422명 · 입원 227명. 2024년 875명', HEX.amber],
  ['7명', '치료감호 인원 (2025)', '2024년 16명에서 감소', HEX.amber],
];
lim.forEach((r, i) => {
  const x = M + (i % 2) * 3.4, y = 1.65 + Math.floor(i / 2) * 2.35;
  RR(s, { x, y, w: 3.15, h: 2.1, fill: { color: HEX.paper } });
  T(s, r[0], { x: x + 0.22, y: y + 0.15, w: 2.8, h: 0.75, fontSize: 32, bold: true, color: r[3], valign: 'bottom' });
  T(s, r[1], { x: x + 0.22, y: y + 0.98, w: 2.8, h: 0.35, fontSize: 14, bold: true });
  T(s, r[2], { x: x + 0.22, y: y + 1.33, w: 2.8, h: 0.65, fontSize: 11, color: C.accent5 });
});
T(s, [
  { text: '연구 문제', options: { bold: true, fontSize: 16, breakLine: true } },
  { text: '단속 인원 2만 명대 지속, 재범률 30% 안팎', options: { bullet: true, breakLine: true } },
  { text: '검거 사범 중 치료 연계 인원은 일부: 2024년 조건부 기소유예 치료 11명, 선도 521명, 교육 773명', options: { bullet: true, breakLine: true } },
  { text: '재활 확대는 예산 판단의 문제: 재활 비용과 재범 감소에 따른 사회적 비용 절감을 같은 단위로 비교한 근거 필요', options: { bullet: true } },
], { x: 7.6, y: 1.65, w: 5.1, h: 4.6, fontSize: 14, paraSpaceAfter: 10 });
source(s, '대검찰청(2026) 표 3-82·3-84·3-85~3-87·3-89, 교정본부 자료(2025. 12. 말 수용자 수, 교정본부 자료)');

s = content('Ⅰ. 연구 배경', 'Ⅰ. 연구 배경 — 연구 목적', '두 분석을 하나의 기준으로 연결');
RR(s, { x: M, y: 1.7, w: 5.4, h: 2.75, fill: { color: HEX.navyBg } });
T(s, '분석 1  사회적 비용 추계', { x: M + 0.3, y: 1.9, w: 4.9, h: 0.45, fontSize: 18, bold: true, color: C.accent1 });
T(s, [
  { text: '마약류로 사회가 1년 동안 잃는 비용의 총액과 1인당 값', options: { bullet: true, breakLine: true } },
  { text: '의료·생산성·형사사법·피해·기타 6개 분야', options: { bullet: true, breakLine: true } },
  { text: '선행연구 2조 2,389억 원(2016년, 암수율 10배) 갱신', options: { bullet: true } },
], { x: M + 0.3, y: 2.45, w: 4.9, h: 2.6, fontSize: 14, paraSpaceAfter: 8 });
RR(s, { x: 7.33, y: 1.7, w: 5.4, h: 2.75, fill: { color: HEX.tealBg } });
T(s, '분석 2  교정 재활 비용편익', { x: 7.63, y: 1.9, w: 4.9, h: 0.45, fontSize: 18, bold: true, color: C.accent2 });
T(s, [
  { text: '재활교육 이수자 1인에게 추가로 드는 비용(ΔC)', options: { bullet: true, breakLine: true } },
  { text: '재복역 감소로 줄어드는 사회적 비용(B)', options: { bullet: true, breakLine: true } },
  { text: 'B/C, NPV, 손익분기 재범감소율 Δr*', options: { bullet: true } },
], { x: 7.63, y: 2.45, w: 4.9, h: 2.6, fontSize: 14, paraSpaceAfter: 8 });
R(s, { x: 6.1, y: 2.85, w: 1.13, h: 0.5, fill: { color: HEX.amber } }, pres.shapes.RIGHT_ARROW);
RR(s, { x: M, y: 4.75, w: W - 2 * M, h: 1.0, fill: { color: HEX.white }, line: { color: HEX.amber, width: 1.25 } });
T(s, [
  { text: '연결 고리  SCᵣ (재복역 1건당 사회적 비용)  ', options: { bold: true, color: HEX.amber } },
  { text: '분석 1의 1인당 값을 분석 2의 편익에 투입. 의료절감·생산성회복은 별도 가산하지 않아 이중계상 방지', options: {} },
], { x: M + 0.3, y: 4.85, w: W - 2 * M - 0.6, h: 0.8, fontSize: 14, valign: 'middle' });
s.addNotes('두 분석이 SCᵣ 하나로 연결되는 것이 본 연구의 구조적 특징.');

// ════════ Ⅱ. 연구 설계 ════════
pres.addSection({ title: 'Ⅱ. 연구 설계' });
s = pres.addSlide({ masterName: 'SECTION', sectionTitle: 'Ⅱ. 연구 설계' });
s.addText('Ⅱ', { placeholder: 'num' }); s.addText('연구 설계', { placeholder: 'title' });
s.addText('범위 · 방법 · 자료 확보 현황', { placeholder: 'body' });

s = content('Ⅱ. 연구 설계', 'Ⅱ. 연구 설계 — 연구 범위', '내용·시간·공간 범위');
const scope = [
  ['내용', [
    '사회적 비용 추계: 직접·간접·무형비용', '교정 재활 투입 비용: 프로그램 운영비, 전담인력 인건비, 시설', '재활 편익: 재복역 감소에 따른 사회적 비용 절감']],
  ['시간', [
    '기준연도: 2025년', '모든 항목 1명당 × N*', '추세 비교: 2021~2025년', '편익 기간: 출소 후 3년, 할인율 4.5%(민감도 3~5%)']],
  ['공간', [
    '전국 마약류 단속·처리 실적', '교정시설 52곳, 마약사범재활과 4곳(화성·부산·청주여자·광주)', '국립법무병원 치료감호, 보호관찰소']],
];
scope.forEach((c, i) => {
  const x = M + i * 4.1;
  RR(s, { x, y: 1.65, w: 3.85, h: 3.9, fill: { color: HEX.paper } });
  T(s, c[0], { x: x + 0.25, y: 1.85, w: 3.4, h: 0.5, fontSize: 20, bold: true, color: C.accent1 });
  T(s, c[1].map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < c[1].length - 1 } })), { x: x + 0.25, y: 2.5, w: 3.4, h: 3.7, fontSize: 14, paraSpaceAfter: 10 });
});
s.addNotes('기준연도 2025년.');

s = content('Ⅱ. 연구 설계', 'Ⅱ. 연구 설계 — 연구 방법', '자료 수집에서 정책 제언까지 다섯 단계');
const steps = [
  ['1', '문헌·제도 검토', 'Single 외(2001) 국제 지침, 박성수(2018) 수정 인적자본접근, 해외 비용편익 사례'],
  ['2', '자료 수집', '교정본부 자료요청 13건, 정보공개, 범죄백서·교정통계연보·결산서'],
  ['3', '규모 보정', '암수율 λ = 28.57(박성수·백민석, 2019)로 실질 사용자 N* 추정. 항목별 적용 여부 구분'],
  ['4', '비용 추계·비용편익', '6개 분야 사회적 비용, 재복역 1건당 SCᵣ, 증분비용 ΔC, B/C·NPV·Δr*'],
  ['5', '검증·제언', '전문가 자문, 민감도 분석, 산출 근거 대장 공개'],
];
steps.forEach((r, i) => {
  const x = M + i * 2.46;
  R(s, { x: x + 0.75, y: 1.75, w: 0.7, h: 0.7, fill: { color: i === 3 ? HEX.amber : HEX.navy } }, pres.shapes.OVAL);
  T(s, r[0], { x: x + 0.75, y: 1.75, w: 0.7, h: 0.7, fontSize: 20, bold: true, color: C.background1, align: 'center', valign: 'middle' });
  if (i < 4) R(s, { x: x + 1.55, y: 2.03, w: 1.25, h: 0.14, fill: { color: HEX.mist } });
  T(s, r[1], { x, y: 2.65, w: 2.2, h: 0.45, fontSize: 16, bold: true, align: 'center' });
  T(s, r[2], { x: x + 0.05, y: 3.15, w: 2.1, h: 2.2, fontSize: 12, color: C.accent5 });
});
RR(s, { x: M, y: 4.85, w: W - 2 * M, h: 1.0, fill: { color: HEX.paper } });
T(s, [
  { text: '산출 근거 대장  ', options: { bold: true, color: C.accent1 } },
  { text: '모든 투입값의 출처와 산식을 산출 근거 대장으로 관리하고, 예산·인원이 바뀌면 같은 산식으로 다시 계산', options: {} },
], { x: M + 0.3, y: 4.95, w: W - 2 * M - 0.6, h: 0.8, fontSize: 13, valign: 'middle' });

s = content('Ⅱ. 연구 설계', 'Ⅱ. 연구 설계 — 자료 확보 현황', '실측 자료 13건과 원단위·문헌 적용 항목');
const got = [
  ['형사사법 6개 기관', '3,728.2억 원', '형사사법 추계(검찰 제외)'],
  ['의료·복지', '78.6억 원', '의료·생산성 추계'],
  ['생산성 손실', '815.0억 원', '의료·생산성 추계'],
  ['사망 58명 · 치료보호 1,649명', 'PGS 인원', '의료·생산성 추계'],
  ['마약 운전 사고', '33건', '경찰청(2026)'],
  ['단속 인원 · 실질 사용자', '23,403 · 234,030명', '대검찰청(2026)'],
  ['마약류 기결 · 미결', '4,188 · 3,241명', '교정본부 자료'],
  ['재활교육 개시·이수·탈락', '1,599 · 1,545 · 54명', '교정본부 자료'],
  ['출소자 3년 내 재복역', '31.0%', '교정본부 자료'],
  ['이수 · 미이수 재복역', '31.6% · 34.5%', '교정본부 자료'],
  ['재활예산 · 수용 원가', '59.99억 · 2,378.4만', '교정본부 자료'],
];
const est = [
  ['고통비용 2,426.4억', '2024 원단위 × 물가 1.021', ''],
  ['검찰 199.3억', '2024 예산·인원', ''],
  ['사회적 혼란·기타 496.0억', '범죄 단가·2024 예산·문헌 최저', ''],
  ['전담인력 인건비 16.98억', '정원 × 봉급표 × 1.6 × 투입비율', ''],
  ['UC-10 치료개입 53.4만', '중독 외래 1인당 진료비', ''],
  ['UC-12 사후관리 83.6만', '치료보호 1인당 예산 ÷ 1.045', ''],
  ['재활예산 성격', '집행액으로 간주', ''],
  ['실제 복역 비율 85% · ΔM 0', '가석방 반영 · 수용기간 차이 없음', '가정'],
  ['생애비용 모수', '회복 후 초과 사망, 재검거 확률', '가정·문헌'],
];
const colBox = (x, w, head, n, col) => {
  R(s, { x, y: 1.55, w, h: 0.5, fill: { color: col } });
  T(s, head, { x: x + 0.2, y: 1.55, w: w - 1.2, h: 0.5, fontSize: 15, bold: true, color: C.background1, valign: 'middle' });
  T(s, n, { x: x + w - 1.0, y: 1.55, w: 0.85, h: 0.5, fontSize: 18, bold: true, color: C.background1, align: 'right', valign: 'middle' });
};
const LW = 6.0, RX = M + 6.25, RW = W - 2 * M - 6.25;
colBox(M, LW, '실측 (연구진 추계·교정본부·공개 통계)', '', HEX.teal);
got.forEach((r, i) => {
  const y = 2.05 + i * 0.4;
  R(s, { x: M, y, w: LW, h: 0.4, fill: { color: i % 2 ? HEX.white : HEX.tealBg } });
  T(s, r[0], { x: M + 0.15, y, w: 2.5, h: 0.4, fontSize: 11.5, bold: true, valign: 'middle' });
  T(s, r[1], { x: M + 2.6, y, w: 1.75, h: 0.4, fontSize: 11.5, bold: true, color: C.accent2, align: 'right', valign: 'middle' });
  T(s, r[2], { x: M + 4.45, y, w: 1.5, h: 0.4, fontSize: 9.5, color: C.accent5, valign: 'middle' });
});
colBox(RX, RW, '원단위·문헌 적용', '', HEX.amber);
est.forEach((r, i) => {
  const y = 2.05 + i * 0.49;
  R(s, { x: RX, y, w: RW, h: 0.49, fill: { color: i % 2 ? HEX.white : HEX.amberBg } });
  T(s, r[0], { x: RX + 0.15, y, w: 2.45, h: 0.49, fontSize: 11.5, bold: true, valign: 'middle' });
  T(s, r[1], { x: RX + 2.6, y, w: 2.2, h: 0.49, fontSize: 10, color: C.accent5, valign: 'middle' });
  T(s, r[2], { x: RX + RW - 1.2, y, w: 1.1, h: 0.49, fontSize: 9.5, bold: true, color: C.accent3, align: 'right', valign: 'middle' });
});
s.addNotes('실측은 연구진 추계, 교정본부 자료, 공개 통계. 나머지 항목은 원단위·문헌 값을 적용하고 산식과 근거를 밝힘.');

// ════════ Ⅲ. 이론 검토 ════════
pres.addSection({ title: 'Ⅲ. 이론 검토' });
s = pres.addSlide({ masterName: 'SECTION', sectionTitle: 'Ⅲ. 이론 검토' });
s.addText('Ⅲ', { placeholder: 'num' }); s.addText('이론 검토', { placeholder: 'title' });
s.addText('선행연구와 암수율, 실질 사용자 수 N*', { placeholder: 'body' });


s = content('Ⅲ. 이론 검토', 'Ⅲ. 이론 검토 — 선행연구', '선행 추계는 2016년 기준이 마지막');
const prev = [
  ['보건복지부 건강증진사업단 (2009)', '약 2조 5천억 원', '2008년 기준', '국내 첫 체계적 추계. 공식 검거 인원 중심이라 암수 반영이 약함'],
  ['박성수 (2018)', '2조 2,389억 원', '2016년 기준 · 암수율 10배', '의료·생산성·형사사법·무형비용 종합. 교정 재활의 비용 대비 효과는 분리하지 않음'],
  ['본 연구 (2026)', '7조 5,441.7억 원', '2025년 · 암수율 10배', '선행연구와 같은 10배 기준. 고통비용·사회적 혼란 포함, 모든 항목 1명당 × N*. 4개 분야만 7조 481.3억 원'],
];
prev.forEach((r, i) => {
  const y = 1.65 + i * 1.55, last = i === 2;
  RR(s, { x: M, y, w: W - 2 * M, h: 1.35, fill: { color: last ? HEX.navyBg : HEX.paper } });
  T(s, r[0], { x: M + 0.3, y: y + 0.18, w: 3.8, h: 0.4, fontSize: 15, bold: true });
  T(s, r[2], { x: M + 0.3, y: y + 0.65, w: 3.8, h: 0.4, fontSize: 12, color: C.accent5 });
  T(s, r[1], { x: M + 4.2, y: last ? y + 0.08 : y + 0.2, w: 3.0, h: last ? 0.6 : 0.9, fontSize: last ? 21 : 24, bold: true, color: last ? C.accent3 : C.accent1, valign: 'middle' });
  if (last) T(s, [
    { text: '암수율 미반영: ', options: { bold: true, color: HEX.navy } }, { text: '7,544.2억 원', options: { bold: true, color: HEX.ink, breakLine: true } },
    { text: '암수율 반영 λ 28.57: ', options: { bold: true, color: HEX.navy } }, { text: '21조 5,537.0억 원', options: { bold: true, color: HEX.ink } },
  ], { x: M + 4.2, y: y + 0.66, w: 3.1, h: 0.62, fontSize: 11, valign: 'top' });
  T(s, r[3], { x: M + 7.3, y: y + 0.2, w: 4.5, h: 0.95, fontSize: 13, valign: 'middle' });
});
T(s, '단속 인원 2016년 14,214명 → 2025년 23,403명으로 증가, 현 시점 기준 비용 재계량 필요', { x: M, y: 6.3, w: W - 2 * M, h: 0.35, fontSize: 13, bold: true, color: C.accent1 });

// ── 선행연구 대비 차이 원인 ──
s = content('Ⅲ. 이론 검토', 'Ⅲ. 이론 검토 — 선행연구 대비 차이', '4개 분야 기준 3.15배: 검거 인원 36.6%, 1명당 실질 53.3%');
{
  T(s, '총액 비교 (억 원, 명목, 암수율 10배, 4개 분야)', { x: M, y: 1.55, w: 5.4, h: 0.35, fontSize: 13, bold: true });
  const MX = 70481.3, BW = 5.4;
  const bars = [
    ['박성수(2018), 2016년', 22389, '2조 2,389', HEX.slate],
    ['× 물가 1.217', 27249.7, '2조 7,249.7', '8A97AA'],
    ['× 검거 인원 1.65', 44865.9, '4조 4,865.9', HEX.amber],
    ['본 연구 2025년', 70481.3, '7조 481.3억', HEX.navy],
  ];
  bars.forEach((b, i) => {
    const y = 2.0 + i * 0.82;
    T(s, b[0], { x: M, y, w: 3.0, h: 0.3, fontSize: 12, bold: true });
    R(s, { x: M, y: y + 0.32, w: BW * b[1] / MX, h: 0.4, fill: { color: b[3] } });
    T(s, b[2], { x: M + 0.1, y: y + 0.32, w: 2.0, h: 0.4, fontSize: 13.5, bold: true, color: C.background1, valign: 'middle' });
  });
  RR(s, { x: M, y: 5.4, w: BW, h: 1.12, fill: { color: HEX.navyBg } });
  T(s, [
    { text: '사용자 1명당(4개 분야): 1,575.1만 원 → 3,011.6만 원', options: { bold: true, breakLine: true } },
    { text: '2025년 가격 환산 1,917.1만 원 대비 +57.1%. 선행연구 = 2조 2,389억 ÷ (14,214명 × 10), 본 연구 = 7,048.1억 ÷ 23,403명', options: { fontSize: 10.5, color: HEX.slate } },
  ], { x: M + 0.15, y: 5.4, w: BW - 0.3, h: 1.12, fontSize: 12, valign: 'middle' });

  const X = M + 5.85, TW = W - M - X;
  T(s, '증가분 +4조 8,092.3억 원의 기여 분해', { x: X, y: 1.55, w: TW, h: 0.35, fontSize: 13, bold: true });
  const segs = [[10.1, '8A97AA', '물가 10.1%'], [36.6, HEX.amber, '검거 인원 36.6%'], [53.3, HEX.navy, '실질 53.3%']];
  let sx = X;
  segs.forEach(g => { const w = TW * g[0] / 100; R(s, { x: sx, y: 2.0, w, h: 0.5, fill: { color: g[1] } }); T(s, g[2], { x: sx, y: 2.0, w, h: 0.5, fontSize: 11.5, bold: true, color: C.background1, align: 'center', valign: 'middle' }); sx += w; });
  const rows = [
    ['물가상승 기여분', '4,860.7억', '10.1%', '2조 2,389억 × (1.217 − 1). 소비자물가 2016년 95.8 → 2025년 116.6'],
    ['검거 인원 증가 기여분', '1조 7,616.2억', '36.6%', '2조 7,250억 × (1.65 − 1). 단속 14,214 → 23,403명'],
    ['1명당 실질 비용 증가', '2조 5,615.4억', '53.3%', '① 교도소 인원 기준(12. 31. 전체 수용자) ② 치료보호 인원 증가(1,649명) ③ 고통비용 원단위 상승(사망 2.8억 → 9.7억)'],
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
  T(s, '물가 → 검거 인원 순서의 단계 분해. 선행연구와 같은 4개 분야 기준(사회적 혼란·기타 4,960.4억 제외). 전체 기준은 3.37배', { x: X + 0.15, y: 5.65, w: TW - 0.3, h: 0.87, fontSize: 11.5, bold: true, color: C.background1, valign: 'middle' });
  source(s, '박성수(2018), 통계청 소비자물가지수(2020=100, 2025년은 2024 × 1.021), 대검찰청(2026), 연구진 추계(2026), 연구진 계산. 금액은 명목가격');
  s.addNotes('같은 10배·4개 분야 기준에서 2025년은 7조 481.3억 원으로 선행연구 2조 2,389억 원의 3.15배. 증가분 4조 8,092.3억 원은 물가 4,860.7억(10.1%), 검거 인원 1조 7,616.2억(36.6%), 1명당 실질 2조 5,615.4억(53.3%). 실질 비중이 커진 주된 이유는 교도소 인원을 12. 31. 전체 수용자(미결 포함) 기준으로 쓴 것. 사범 수와 물가를 반영한 기대값 4조 4,865.9억 원의 1.57배.');
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
const lam = [['형사사법비용', '적용', '검거 1명당 처리비용 × N*'], ['고통·생산성', '적용', '사범 1명당 손실 × N*'], ['의료·복지', '적용', '심평원 중독자 = 검거 사범 가정'], ['사회적 혼란·기타', '적용', '1명당 212.0만 원 × N*']];
lam.forEach((r, i) => {
  const y = 4.75 + i * 0.42;
  T(s, r[0], { x: 7.1, y, w: 1.75, h: 0.38, fontSize: 12, bold: true, valign: 'middle' });
  chip(s, 8.9, y + 0.06, r[1], 'done', 1.0);
  T(s, r[2], { x: 10.05, y, w: 2.7, h: 0.38, fontSize: 10.5, color: C.accent5, valign: 'middle' });
});
source(s, '박성수·백민석(2019), 대검찰청(2026) 표 3-21');
s.addNotes('범죄자 1명이 생길 때 퍼지는 비용을 원단위로 둔다. 검거 사범 1명당 비용 3,223.6만 원(7,544.2억 ÷ 23,403명)에 실질 사용자 N*를 곱한다. 형사사법과 사회적 혼란·기타를 포함한 모든 항목에 적용한다. 기본값은 λ 10(선행연구와 같음), 28.57은 민감도.');

// ════════ Ⅳ. 사회적 비용 체계 ════════
pres.addSection({ title: 'Ⅳ. 사회적 비용 체계' });
s = pres.addSlide({ masterName: 'SECTION', sectionTitle: 'Ⅳ. 사회적 비용 체계' });
s.addText('Ⅳ', { placeholder: 'num' }); s.addText('사회적 비용 체계', { placeholder: 'title' });
s.addText('전체 체계도와 비용 산정의 주요 특징', { placeholder: 'body' });

// ── 비용 전체 체계도 ──
s = content('Ⅳ. 사회적 비용 체계', 'Ⅳ. 사회적 비용 체계 — 전체 체계도', '마약류범죄의 사회적 비용 전체 체계도');
R(s, { x: M, y: 1.45, w: W - 2 * M, h: 0.55, fill: { color: HEX.navy } });
T(s, [
  { text: '사회적 비용 SC', options: { bold: true, fontSize: 16 } },
  { text: '   =  유형비용 TC + 무형비용 PGS  =  (직접비용 DC + 간접비용 IC) + PGS', options: { fontSize: 13 } },
], { x: M + 0.25, y: 1.45, w: W - 2 * M - 0.5, h: 0.55, color: C.background1, valign: 'middle' });
const cols = [
  { t: '의료·복지', tag: 'DC', note: '78.6억', items: [['직접 의료비', '44.6억 (청구 + 치료보호)', 'done'], ['간접의료비', '17.0억 (직접 × 38.1%)', 'done'], ['정신건강·복지 지원', '17.0억 (기관 운영)', 'done']] },
  { t: '생산성', tag: 'IC', note: '815.0억', items: [['조기 사망', '421.9억 (사망 58명)', 'done'], ['이환·입원', '22.5억 (16,027일)', 'done'], ['노동력 상실·미취업', '370.6억 (22,242명)', 'done']] },
  { t: '형사사법', tag: 'IC', note: '3,728.2억', items: [['단속·수사', '경찰 1,381.0억 · 검찰 199.3억', 'done'], ['재판', '법원 99.0억', 'done'], ['형 집행·교정', '교도소 1,953.3억 · 법무병원 5.1억 · 보호관찰 90.5억', 'done']] },
  { t: '피해자·주위', tag: 'IC·PGS', note: '2,547.5억', items: [['2차 범죄 피해', '112.5억 (상해·성폭력, 범죄 단가)', 'wip'], ['고통비용 PGS', '2,426.4억 (사망 574.4 · 중독자 1,852.0)', 'wip'], ['가족·주변인 케어', '8.6억 (가족 의료비, 최저)', 'wip']] },
  { t: '기타(사회적 혼란)', tag: 'DC·IC', note: '374.9억', items: [['예방·홍보·재활', '360.0억 (2024 예산 값)', 'wip'], ['범죄 공포·방어 행동', '0원 (범죄 단가에 포함)', 'done'], ['마약 운전 교통사고', '14.9억 (2025년 33건)', 'done']] },
  { t: '종합', tag: 'SC', note: '7,544.2억', items: [['총액 (λ 10)', '7조 5,441.7억 원', 'done'], ['1명당 비용', '3,223.6만 원 (전 항목 ÷ 23,403명)', 'done'], ['SCᵣ', '재복역 1건당 → 비용편익', 'wip']] },
];
const cw = (W - 2 * M - 5 * 0.14) / 6;
cols.forEach((c, i) => {
  const x = M + i * (cw + 0.14);
  R(s, { x: x + cw / 2 - 0.01, y: 2.0, w: 0.02, h: 0.18, fill: { color: HEX.slate } });
  const done = c.items.every(it => it[2] === 'done') || (c.t === '종합');
  R(s, { x, y: 2.18, w: cw, h: 0.72, fill: { color: done ? HEX.teal : HEX.paper } });
  T(s, c.t, { x: x + 0.1, y: 2.22, w: cw - 0.2, h: 0.36, fontSize: 12.5, bold: true, color: done ? C.background1 : C.text1 });
  T(s, c.tag + (c.note ? ' · ' + c.note : ''), { x: x + 0.1, y: 2.55, w: cw - 0.2, h: 0.3, fontSize: 10.5, color: done ? C.background1 : C.accent5 });
  c.items.forEach((it, j) => {
    const y = 3.02 + j * 0.98;
    const bg = it[2] === 'done' ? HEX.tealBg : (it[2] === 'excl' ? HEX.paper : HEX.amberBg);
    const ln = it[2] === 'excl' ? { color: HEX.slate, width: 1, dashType: 'dash' } : { type: 'none' };
    R(s, { x, y, w: cw, h: 0.88, fill: { color: bg }, line: ln });
    T(s, it[0], { x: x + 0.1, y: y + 0.07, w: cw - 0.2, h: 0.3, fontSize: 11.5, bold: true });
    T(s, it[1], { x: x + 0.1, y: y + 0.38, w: cw - 0.2, h: 0.48, fontSize: 10, color: it[2] === 'done' ? C.accent2 : C.accent5, bold: it[2] === 'done' });
  });
});
RR(s, { x: M, y: 6.0, w: W - 2 * M, h: 0.58, fill: { color: HEX.white }, line: { color: HEX.navy, width: 1.25 } });
T(s, [
  { text: 'SCᵣ  ', options: { bold: true, color: HEX.amber } },
  { text: '= 형사사법(1건당) + 비형사사법 1명당(의료·생산성·고통·혼란)', options: {} },
  { text: '   →   교정 재활 B/C = (r0 × Δr × SCᵣ × D) ÷ ΔC', options: { bold: true, color: HEX.navy } },
], { x: M + 0.25, y: 6.0, w: W - 2 * M - 0.5, h: 0.58, fontSize: 12.5, valign: 'middle' });
// 범례
[['실측 기반', HEX.tealBg, null, 1.2], ['원단위·문헌 적용', HEX.amberBg, null, 1.7]].forEach((l, i, a) => {
  const x = 7.6 + a.slice(0, i).reduce((t, v) => t + v[3], 0);
  R(s, { x, y: 0.4, w: 0.28, h: 0.2, fill: { color: l[1] }, line: l[2] ? { color: l[2], width: 1, dashType: 'dash' } : { color: HEX.mist, width: 0.5 } });
  T(s, l[0], { x: x + 0.34, y: 0.36, w: l[3] - 0.3, h: 0.28, fontSize: 10, color: C.accent5 });
});
T(s, '금액: 2025년, 억 원, 암수율 미반영. 모든 항목에 λ를 곱해 총액을 냄', { x: M, y: 6.66, w: 8, h: 0.3, fontSize: 10, color: C.accent5 });
s.addNotes('2025년 체계도. 초록 칸은 2025년 실측이 들어간 항목, 주황 칸은 원단위·문헌 값을 적용한 항목(고통비용, 2차 범죄, 예방 예산, 가족 돌봄). 미반영 합계 7,544.2억 원, λ 10 7조 5,441.7억 원.');

// ── 비용 산정의 주요 특징 ──
s = content('Ⅳ. 사회적 비용 체계', 'Ⅳ. 사회적 비용 체계 — 산정 원칙', '비용 산정의 주요 특징');
const feats = [
  ['1', '1명당 비용 구조', '모든 항목을 검거 사범 1명당 비용(3,223.6만 원)으로 바꾸고 실질 사용자 N*에 곱함. 형사사법·사회적 혼란·기타 포함'],
  ['2', '기관 결산 × 마약류 비율', '기관 결산 총액 × 마약류 처리 인원 비율. 마약류 사범 1명의 비용이 평균 사범과 같다는 평균비용 가정'],
  ['3', '결산 전액을 범죄 대응으로 봄', '경찰·검찰·교정 결산 전액을 범죄 관련으로 간주(박경래 외, 2010 방식). 비범죄 업무 비율 공제는 민감도로 제시'],
  ['4', '이전지출 제외', '기초생활급여·불법 마약 구입비는 사회적 비용에서 제외. 제도 운영비만 계상(Single 외, 2001)'],
  ['5', '중복계상 방지', '치료보호↔건강보험, 치료감호·수용자 의료비, 구금↔미취업 손실은 한 곳에만 계상'],
  ['6', '연간 총액과 생애 비용 분리', '한 해 비용(횡단)과 중독자 1명의 생애 비용은 기준이 달라 더하지 않음. 생애비용은 1명당 값으로 따로 제시'],
  ['7', '기준연도·할인율', '2025년(고통비용은 2024 원단위 환산). 조기사망은 할인율 4%·임금상승 4%, 생애·비용편익은 4.5%(민감도 3~5%)'],
  ['8', '민감도 제시', 'λ 28.57, 할인율 3~5%, PGS 가구 구조, 교도소 인원 기준을 민감도로 제시'],
];
feats.forEach((f, i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const x = M + col * 6.13, y = 1.55 + row * 1.25;
  R(s, { x, y: y + 0.05, w: 0.5, h: 0.5, fill: { color: i < 2 ? HEX.amber : HEX.navy } }, pres.shapes.OVAL);
  T(s, f[0], { x, y: y + 0.05, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: C.background1, align: 'center', valign: 'middle' });
  T(s, f[1], { x: x + 0.65, y, w: 5.3, h: 0.36, fontSize: 15, bold: true });
  T(s, f[2], { x: x + 0.65, y: y + 0.38, w: 5.3, h: 0.8, fontSize: 11.5, color: C.accent5 });
});
s.addNotes('1번: 모든 비용을 1명당으로 만들고 암수율을 곱한다. 8번: 주요 가정은 민감도로 제시한다.');

// ════════ Ⅴ. 집계 비용 ════════
pres.addSection({ title: 'Ⅴ. 집계 비용' });
s = pres.addSlide({ masterName: 'SECTION', sectionTitle: 'Ⅴ. 집계 비용' });
s.addText('Ⅴ', { placeholder: 'num' }); s.addText('집계 비용', { placeholder: 'title' });
s.addText('2025년 총괄, 항목별 비용, 1인당 생애비용', { placeholder: 'body' });


// ── 사회적 비용 총괄 ──
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 총괄', '2025년 마약류 사회적 비용 7조 5,441.7억 원 (암수율 10배)');
{
  const hd = ['분야', '항목', '암수율 미반영', 'λ = 10', 'λ = 28.57'];
  const rowsT = [
    ['의료·복지', '직접 의료비 44.6 · 간접의료비 17.0 · 정신건강·복지 17.0', '78.6', '785.6', '2,244.6'],
    ['생산성', '조기사망 421.9 · 이환·입원 22.5 · 노동력 상실·미취업 370.6', '815.0', '8,149.7', '23,283.6'],
    ['형사사법', '경찰·검찰·법원·교도소(12. 31.)·국립법무병원·보호관찰소', '3,728.2', '37,282.0', '106,514.5'],
    ['고통비용', '사망 58명 × 9.9억 + 치료보호 1,649명 × 1.12억', '2,426.4', '24,264.1', '69,322.4'],
    ['사회적 혼란·기타', '2차 범죄 112.5 · 예방 예산 360.0 · 가족 돌봄 8.6 · 운전 사고 14.9', '496.0', '4,960.4', '14,171.8']
  ];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 12, align: j >= 2 ? 'right' : 'left' } }))].concat(
    rowsT.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: j === 1 ? 10.5 : 12.5, bold: j === 0 || j === 2, color: j === 2 ? HEX.teal : HEX.ink, fill: { color: i % 2 ? HEX.white : HEX.paper }, align: j >= 2 ? 'right' : 'left' } }))));
  tr.push(['합계(억 원)', '', '7,544.2', '75,441.7', '215,537.0'].map((c, j) => ({ text: c, options: { bold: true, fontSize: 13, fill: { color: HEX.tealBg }, color: j >= 2 ? HEX.teal : HEX.ink, align: j >= 2 ? 'right' : 'left' } })));
  s.addTable(tr, { x: M, y: 1.55, w: 8.4, colW: [1.75, 3.15, 1.1, 1.15, 1.25], rowH: 0.58, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.04, 0.1, 0.04, 0.1] });
  RR(s, { x: 9.25, y: 1.55, w: 3.48, h: 2.3, fill: { color: HEX.navy } });
  T(s, '사회적 비용 (2025, 암수율 10배)', { x: 9.45, y: 1.7, w: 3.1, h: 0.35, fontSize: 12, color: C.accent6 });
  T(s, '7조 5,441.7억 원', { x: 9.45, y: 2.05, w: 3.1, h: 0.75, fontSize: 23, bold: true, color: C.background1 });
  T(s, '형사사법 49.4% · 고통비용 32.2% · 생산성 10.8% · 사회적 혼란·기타 6.6% · 의료·복지 1.0%. 미반영 7,544.2억 원', { x: 9.45, y: 2.9, w: 3.1, h: 0.8, fontSize: 11, color: C.accent6 });
  T(s, [
    { text: '검거 사범 1명당 3,223.6만 원. 모든 항목 = 1명당 × 실질 사용자 N*(λ 10: 234,030명, λ 28.57: 668,624명)', options: { bullet: true, breakLine: true } },
    { text: '자료: 연구진 추계, 대검찰청(2026), 한국교통연구원(2025), 교정본부 자료', options: { bullet: true, breakLine: true } },
    { text: '박성수(2018) 2조 2,389억 원 대비 3.37배(같은 4개 분야 3.15배)', options: { bullet: true } },
  ], { x: 9.25, y: 4.0, w: 3.48, h: 2.5, fontSize: 11, paraSpaceAfter: 6 });
  source(s, '연구진 형사사법비용 추계(2026), 연구진 의료·생산성 추계(2026), 대검찰청(2026), 한국교통연구원(2025), 연구진 계산. 억 원, 반올림으로 합이 0.1 다를 수 있음');
  s.addNotes('2025년, 암수율 10배 기준 7조 5,441.7억 원. 형사사법 3조 7,282.0억(49.4%), 고통비용 2조 4,264.1억(32.2%), 생산성 8,149.7억(10.8%), 사회적 혼란·기타 4,960.4억(6.6%), 의료·복지 785.6억(1.0%). 미반영 7,544.2억, 28.57배 21조 5,537.0억.');
}

// ── 의료·생산성 산출 매칭도 ──
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 의료·생산성 산출 매칭도', '의료·복지와 생산성 항목별 산식과 금액 (2025년, 연구진 추계)');
{
  const A = { x: M, w: 1.85 }, B = { x: M + 2.3, w: 4.85 }, Cc = { x: M + 7.6, w: 1.75 }, D = { x: M + 9.8, w: 2.33 };
  const y0 = 1.85, step = 0.72, h = 0.58;
  [['체계도 항목', A], ['항목 · 산식', B], ['금액 (억 원)', Cc], ['분야 소계', D]].forEach(t =>
    T(s, t[0], { x: t[1].x, y: 1.45, w: t[1].w, h: 0.32, fontSize: 11, bold: true, color: C.accent5 }));
  const rows = [
    ['직접 의료비', '청구 진료비 30.18억(입원 20.39 · 외래 9.79) + 치료보호 예산 14.4억(국비·지방비)', '44.6'],
    ['간접의료비', '직접 의료비 × 38.1%(한국보건사회연구원, 1997)', '17.0'],
    ['정신건강·복지', '치료보호기관 운영 9.0억 · 우수기관 3.0억 · 기타 5.0억 (중복 제외)', '17.0'],
    ['조기사망', '사망 58명(20~64세) × 잔여 노동가치, 할인율 4%·임금상승 4%', '421.9'],
    ['이환·입원', '입내원 손실 16,027일 × 연령별 일당', '22.5'],
    ['노동력 상실·미취업', '20세 이상 사범 22,242명 × 실직 25% × 조정 50% × 연간 노동가치', '370.6'],
  ];
  const groups = [['의료·복지', [0, 1, 2], '78.6억 원'], ['생산성', [3, 4, 5], '815.0억 원']];
  const ry = i => y0 + i * step;
  rows.forEach((r, i) => {
    const y = ry(i), cy = y + h / 2;
    R(s, { x: B.x, y, w: B.w, h, fill: { color: HEX.paper } });
    T(s, r[0], { x: B.x + 0.12, y, w: 1.5, h, fontSize: 12, bold: true, valign: 'middle' });
    T(s, r[1], { x: B.x + 1.6, y, w: B.w - 1.65, h, fontSize: 9.5, color: C.accent5, valign: 'middle' });
    R(s, { x: Cc.x, y, w: Cc.w, h, fill: { color: HEX.teal } });
    T(s, r[2], { x: Cc.x, y, w: Cc.w, h, fontSize: 16, bold: true, color: C.background1, align: 'center', valign: 'middle' });
    R(s, { x: B.x + B.w, y: cy - 0.01, w: Cc.x - B.x - B.w, h: 0.02, fill: { color: HEX.slate } });
  });
  groups.forEach(g => {
    const top = ry(g[1][0]), bot = ry(g[1][g[1].length - 1]) + h;
    R(s, { x: A.x, y: top, w: A.w, h: bot - top, fill: { color: HEX.navy } });
    T(s, g[0], { x: A.x, y: top, w: A.w, h: bot - top, fontSize: 14, bold: true, color: C.background1, align: 'center', valign: 'middle' });
    R(s, { x: D.x, y: top, w: D.w, h: bot - top, fill: { color: HEX.tealBg }, line: { color: HEX.teal, width: 1 } });
    T(s, g[2], { x: D.x, y: top, w: D.w, h: bot - top, fontSize: 17, bold: true, color: C.accent2, align: 'center', valign: 'middle' });
    g[1].forEach(i => {
      const cy = ry(i) + h / 2;
      R(s, { x: A.x + A.w, y: cy - 0.01, w: B.x - A.x - A.w, h: 0.02, fill: { color: HEX.slate } });
      R(s, { x: Cc.x + Cc.w, y: cy - 0.01, w: D.x - Cc.x - Cc.w, h: 0.02, fill: { color: HEX.slate } });
    });
  });
  RR(s, { x: M, y: 6.22, w: W - 2 * M, h: 0.36, fill: { color: HEX.navy } });
  T(s, [
    { text: '의료·복지·생산성 합계  893.6억 원', options: { bold: true } },
    { text: '     암수율 미반영. 암수율 반영 시 λ 10: 8,936.0억, λ 28.57: 2조 5,530.2억', options: { fontSize: 10.5, color: HEX.mist } },
  ], { x: M + 0.2, y: 6.22, w: W - 2 * M - 0.4, h: 0.36, fontSize: 12.5, color: C.background1, valign: 'middle' });
  source(s, '연구진 「마약류 사용의 사회적 비용」 제3장(2026) <표 3-2>~<표 3-22>');
  s.addNotes('2025년 의료·복지 78.6억, 생산성 815.0억 원(실측). 1명당 계수로 바꿔 N*를 곱함. 조기사망은 할인율 4%·임금상승 4% 적용.');
}

// ── 고통비용(PGS) 산출 ──
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 고통비용(PGS) 산출', '고통비용 2,426.4억 원 (λ 10: 2조 4,264.1억 원)');
{
  RR(s, { x: M, y: 1.55, w: W - 2 * M, h: 0.62, fill: { color: HEX.navy } });
  T(s, [
    { text: 'PGS  ', options: { bold: true, color: HEX.amber } },
    { text: '= 사망자 수 × 사망 PGS 원단위  +  중독자 수 × 중상 PGS 원단위', options: { bold: true } },
    { text: '     제안서 산식, 교통사고 고통비용 산정체계 준용', options: { fontSize: 11, color: HEX.mist } },
  ], { x: M + 0.25, y: 1.55, w: W - 2 * M - 0.5, h: 0.62, fontSize: 15, color: C.background1, valign: 'middle' });
  const hd = ['구분', '적용 인원', '원단위 (1인당)', '금액 (억 원)', '인원 근거', '원단위 근거'];
  const cw = [1.6, 1.35, 1.55, 1.45, 3.0, 3.18];
  let cx = M;
  R(s, { x: M, y: 2.35, w: W - 2 * M, h: 0.42, fill: { color: HEX.paper } });
  hd.forEach((h, j) => { T(s, h, { x: cx + (j >= 4 ? 0.35 : 0.1), y: 2.35, w: cw[j] - (j === 3 ? 0.35 : 0.1), h: 0.42, fontSize: 11.5, bold: true, valign: 'middle', align: j >= 1 && j <= 3 ? 'right' : 'left' }); cx += cw[j]; });
  const rows = [
    ['사망 PGS', '58명', '9.9억 원', '574.4', '2025년 사망 58명(20~64세, 연구진 추계 <표 3-16>)', '2024년 기준 9.7억 원 × 물가 1.021 (한국교통연구원, 2025)'],
    ['중독자 PGS', '1,649명', '1.12억 원', '1,852.0', '치료보호 인원 2025 실측 (대검찰청, 2026 표 3-82). 2024년 875명', '중상 2.2억 원의 50% × 물가 1.021 (한국교통연구원, 2025)'],
  ];
  rows.forEach((r, i) => {
    const y = 2.77 + i * 0.78;
    R(s, { x: M, y, w: W - 2 * M, h: 0.78, fill: { color: HEX.white } });
    R(s, { x: M, y: y + 0.77, w: W - 2 * M, h: 0.01, fill: { color: HEX.mist } });
    let cx = M;
    r.forEach((c, j) => { T(s, c, { x: cx + (j >= 4 ? 0.35 : 0.1), y, w: cw[j] - (j === 3 ? 0.35 : (j >= 4 ? 0.4 : 0.15)), h: 0.78, fontSize: j >= 4 ? 10.5 : 13, bold: j === 0 || j === 3, color: j === 3 ? HEX.teal : HEX.ink, align: j >= 1 && j <= 3 ? 'right' : 'left', valign: 'middle' }); cx += cw[j]; });
  });
  R(s, { x: M, y: 4.33, w: W - 2 * M, h: 0.48, fill: { color: HEX.tealBg } });
  T(s, '합계', { x: M + 0.1, y: 4.33, w: 1.5, h: 0.48, fontSize: 13, bold: true, valign: 'middle' });
  T(s, '2,426.4', { x: M + 4.5, y: 4.33, w: 1.1, h: 0.48, fontSize: 15, bold: true, color: C.accent2, align: 'right', valign: 'middle' });
  T(s, 'λ 10: 2조 4,264.1억 · λ 28.57: 6조 9,322.4억 (1명당 × N*)', { x: M + 6.0, y: 4.33, w: 6.0, h: 0.48, fontSize: 12, bold: true, valign: 'middle' });
  RR(s, { x: M, y: 4.98, w: 5.9, h: 1.55, fill: { color: HEX.navyBg } });
  T(s, [
    { text: '원단위 산정 방법 (한국교통연구원, 2025)', options: { bold: true, breakLine: true } },
    { text: '국민 1,000명 대상 조건부가치추정법(CVM)으로 사상 확률 감소에 대한 지불용의액(WTP) 조사', options: { bullet: true, breakLine: true } },
    { text: '사상자 본인과 가족의 고통을 합산(이번 조사부터 가족 포함)', options: { bullet: true, breakLine: true } },
    { text: '사망 PGS는 2013년 조사 약 2.8억 원에서 3배 이상 상승', options: { bullet: true } },
  ], { x: M + 0.15, y: 4.98, w: 5.6, h: 1.55, fontSize: 11, valign: 'middle', paraSpaceAfter: 2 });
  RR(s, { x: M + 6.1, y: 4.98, w: W - 2 * M - 6.1, h: 1.55, fill: { color: HEX.amberBg } });
  T(s, [
    { text: '해석상 유의점', options: { bold: true, breakLine: true } },
    { text: '교통사고 원단위를 마약류에 준용(제안서 방식). 마약류 고유 원단위는 없음', options: { bullet: true, breakLine: true } },
    { text: '치료보호 875 → 1,649명: 2024. 7. 건강보험 적용 이후 이용 증가(제도 변화 영향)', options: { bullet: true, breakLine: true } },
    { text: '가족 고통이 원단위에 포함 → 가족·주변인 케어(돌봄 비용)와 별개', options: { bullet: true } },
  ], { x: M + 6.25, y: 4.98, w: W - 2 * M - 6.4, h: 1.55, fontSize: 11, valign: 'middle', paraSpaceAfter: 2 });
  source(s, '한국교통연구원(2025. 7. 28.) 2024년 기준 원단위 × 물가 1.021; 대검찰청(2026) 「2025 마약류 범죄백서」 표 3-82(치료보호 2025); 사망자는 연구진 추계(2025년 58명)');
  s.addNotes('2025년 고통비용은 사망 58명 × 9.9억 = 574.4억, 치료보호 1,649명 × 1.12억 = 1,852.0억, 합계 2,426.4억 원. λ 10이면 2조 4,264.1억 원. 고통비용은 2024년 원단위에 물가를 곱함.');
}

s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 형사사법비용', '2025년 형사사법비용 3조 7,282.0억 원 (λ 10)');
s.addChart(pres.charts.BAR, [{ name: '마약류 비용', labels: ['교도소', '경찰', '검찰', '법원', '보호관찰소', '국립법무병원'], values: [1953.3, 1381.0, 199.3, 99.0, 90.5, 5.1] }], {
  x: M, y: 1.5, w: 7.6, h: 4.9, barDir: 'bar', chartColors: [HEX.teal], showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '#,##0.0', dataLabelFontSize: 12, dataLabelColor: HEX.ink, dataLabelFontFace: '+mn-lt',
  catAxisLabelColor: HEX.ink, catAxisLabelFontSize: 13, catAxisLabelFontFace: '+mn-lt', catAxisOrientation: 'maxMin', valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' },
  showLegend: false, showTitle: true, title: '기관별 마약류 비용 (억 원, 2025, 암수율 미반영)', titleFontSize: 13, titleColor: HEX.ink, titleFontFace: '+mn-lt', barGapWidthPct: 40,
});
RR(s, { x: 8.55, y: 1.55, w: 4.18, h: 2.35, fill: { color: HEX.navy } });
T(s, '형사사법비용 (암수율 10배)', { x: 8.8, y: 1.7, w: 3.8, h: 0.35, fontSize: 13, color: C.accent6 });
T(s, '3조 7,282.0억', { x: 8.8, y: 2.05, w: 3.8, h: 0.8, fontSize: 30, bold: true, color: C.background1 });
T(s, '미반영 3,728.2억 원. 6개 기관 2025 실측(검찰은 2024년 값)', { x: 8.8, y: 2.95, w: 3.75, h: 0.8, fontSize: 12, color: C.accent6 });
T(s, [
  { text: '교도소 52.4%, 경찰 37.0%로 두 기관이 89.4% 차지', options: { bullet: true, breakLine: true } },
  { text: '검거 사범 1명당 형사사법 계수 1,593.0만 원', options: { bullet: true, breakLine: true } },
  { text: '교도소 7,429명 = 기결 4,188 + 미결 3,241명(교정본부 확인). 기결분 1,101.2억 · 미결분 852.2억 원', options: { bullet: true } },
], { x: 8.55, y: 4.1, w: 4.18, h: 2.4, fontSize: 12, paraSpaceAfter: 6 });
source(s, '연구진 「마약류 범죄의 형사사법 비용」(2026) <표 2>~<표 18>, 마약류만(유해화학물질 제외)');
s.addNotes('2025년: 교도소 1,953.3억(결산 1조 6,992.2억 × 7,429 ÷ 64,626명), 경찰 1,381.0억, 검찰 199.3억(2024년 예산·인원), 법원 99.0억, 보호관찰소 90.5억, 국립법무병원 5.1억. 미반영 3,728.2억, 암수율 10배 3조 7,282.0억 원.');

// ── 형사사법비용 매칭도: 체계도 항목 ↔ 기관·산식 ↔ 금액 ↔ 항목 소계 ──
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 산출 매칭도', '체계도 항목별로 기관 산식과 금액을 맞춘 그림');
{
  const A = { x: M, w: 1.85 }, B = { x: M + 2.3, w: 4.85 }, Cc = { x: M + 7.6, w: 1.75 }, D = { x: M + 9.8, w: 2.33 };
  const y0 = 1.85, step = 0.72, h = 0.58;
  [['체계도 형사사법 항목', A], ['기관 · 산식 (결산 × 마약류 비율)', B], ['마약류 비용 (억 원)', Cc], ['항목 소계', D]].forEach(t =>
    T(s, t[0], { x: t[1].x, y: 1.45, w: t[1].w, h: 0.32, fontSize: 11, bold: true, color: C.accent5 }));
  const rows = [
    ['경찰', '결산 13조 3,558.3억 × 13,343 ÷ 1,290,412명', '1,381.0', '1인당 1,035.0만'],
    ['검찰', '2024 예산 1조 2,162.6억 × 23,022 ÷ 1,405,185명', '199.3', '1인당 86.6만'],
    ['법원', '형사소송 2,483.9억 × 13,849 ÷ 347,473명', '99.0', '1인당 71.5만'],
    ['교도소', '결산 1조 6,992.2억 × 7,429 ÷ 64,626명 (12. 31.)', '1,953.3', '1인당 2,629.3만'],
    ['국립법무병원', '결산 466.5억 × 9 ÷ 823명', '5.1', '1인당 5,668.8만'],
    ['보호관찰소', '결산 2,009.3억 × 1,853 ÷ 41,138명', '90.5', '1인당 488.4만'],
  ];
  const groups = [['단속·수사', [0, 1], '1,580.3억 원', ''], ['재판', [2], '99.0억 원', ''], ['형 집행·교정', [3, 4, 5], '2,048.9억 원', '보호관찰 제외 1,958.4억 원']];
  const ry = i => y0 + i * step;
  rows.forEach((r, i) => {
    const y = ry(i), cy = y + h / 2;
    R(s, { x: B.x, y, w: B.w, h, fill: { color: HEX.paper } });
    T(s, r[0], { x: B.x + 0.12, y, w: 1.35, h, fontSize: 12.5, bold: true, valign: 'middle' });
    T(s, r[1], { x: B.x + 1.45, y, w: B.w - 1.5, h, fontSize: 10, color: C.accent5, valign: 'middle' });
    R(s, { x: Cc.x, y, w: Cc.w, h, fill: { color: i === 5 ? HEX.slate : HEX.teal } });
    T(s, r[2], { x: Cc.x, y: y + 0.02, w: Cc.w, h: 0.36, fontSize: 15, bold: true, color: C.background1, align: 'center', valign: 'middle' });
    T(s, r[3], { x: Cc.x, y: y + 0.36, w: Cc.w, h: 0.22, fontSize: 8.5, color: C.background1, align: 'center' });
    R(s, { x: B.x + B.w, y: cy - 0.01, w: Cc.x - B.x - B.w, h: 0.02, fill: { color: HEX.slate } });
  });
  groups.forEach(g => {
    const top = ry(g[1][0]), bot = ry(g[1][g[1].length - 1]) + h;
    R(s, { x: A.x, y: top, w: A.w, h: bot - top, fill: { color: HEX.navy } });
    T(s, g[0], { x: A.x, y: top, w: A.w, h: bot - top, fontSize: 14, bold: true, color: C.background1, align: 'center', valign: 'middle' });
    R(s, { x: D.x, y: top, w: D.w, h: bot - top, fill: { color: HEX.tealBg }, line: { color: HEX.teal, width: 1 } });
    T(s, g[2], { x: D.x, y: top + (bot - top) / 2 - (g[3] ? 0.3 : 0.2), w: D.w, h: 0.4, fontSize: 16, bold: true, color: C.accent2, align: 'center', valign: 'middle' });
    if (g[3]) T(s, g[3], { x: D.x, y: top + (bot - top) / 2 + 0.1, w: D.w, h: 0.3, fontSize: 9.5, color: C.accent5, align: 'center' });
    g[1].forEach(i => {
      const cy = ry(i) + h / 2;
      R(s, { x: A.x + A.w, y: cy - 0.01, w: B.x - A.x - A.w, h: 0.02, fill: { color: HEX.slate } });
      R(s, { x: Cc.x + Cc.w, y: cy - 0.01, w: D.x - Cc.x - Cc.w, h: 0.02, fill: { color: HEX.slate } });
    });
  });
  RR(s, { x: M, y: 6.22, w: W - 2 * M, h: 0.36, fill: { color: HEX.navy } });
  T(s, [
    { text: '합계  3,728.2억 원 (λ 10: 3조 7,282.0억)  ·  1명당 1,593.0만 원', options: { bold: true } },
    { text: '     기관별 1인당은 분모가 달라 합산하지 않음', options: { fontSize: 10.5, color: HEX.mist } },
  ], { x: M + 0.2, y: 6.22, w: W - 2 * M - 0.4, h: 0.36, fontSize: 12.5, color: C.background1, valign: 'middle' });
  source(s, '연구진 「마약류 범죄의 형사사법 비용」(2026) <표 2>~<표 18>. 기관별 1인당 = 마약류 비용 ÷ 기관 마약류 인원(참고)');
  s.addNotes('2025년 매칭도. 6개 기관 실측, 검찰만 2024년 예산·인원.');
}

// ── 1명당 생애 사회적 비용: 모형 ──
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 1명당 생애 사회적 비용 (모형)', '중독자 1명 생애비용: 하한 3,194.7만~상한 16억 원');
{
  RR(s, { x: M, y: 1.5, w: W - 2 * M, h: 0.75, fill: { color: HEX.navy } });
  T(s, [
    { text: '생애비용 = 1년차 비용 + Σ ', options: { bold: true } },
    { text: '[활동 중독 × (반복 비용 + 재검거 × 형사사법) + 노동능력 상실 × 노동가치 + 초과 사망 × (사망 PGS + 잔여 소득)] ÷ 할인', options: {} },
  ], { x: M + 0.25, y: 1.5, w: W - 2 * M - 0.5, h: 0.75, fontSize: 13.5, color: C.background1, valign: 'middle' });
  const hd = ['시나리오', '잔여 중독기간', '노동능력 상실', '회복 후 잔존', '초과 사망(활동)', '초과 사망(회복)', '연 재검거'];
  const rows = [['A 조기회복', '5년', '12.5%', '0%', '0.79%', '0.1%', '5%'], ['B 기준', '16년', '15.6%', '50%', '0.97%', '0.2%', '10%'], ['C 만성화', '27년', '31.1%', '100%', '1.21%', '0.3%', '15%']];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.slate }, fontSize: 11.5, align: j ? 'right' : 'left' } }))].concat(
    rows.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: 12, bold: i === 1 || j === 0, fill: { color: i === 1 ? HEX.tealBg : HEX.white }, align: j ? 'right' : 'left' } }))));
  s.addTable(tr, { x: M, y: 2.4, w: W - 2 * M, colW: [2.0, 1.65, 1.65, 1.65, 1.75, 1.75, 1.68], rowH: 0.4, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.1, 0.03, 0.1] });
  const ev = [
    ['기대여명', '통계청 「2024년 생명표」 40세(남 41.9·여 47.4년)·60세(남 23.7·여 28.4년) 남녀 평균에 맞춘 Gompertz 곡선'],
    ['초과 사망', '암페타민류 사용자 조사망률 연 1.14%(0.92~1.42), SMR 6.83 (Stockings et al., 2019). 초과분 = 조사망률 × (1 − 1/6.83)'],
    ['중독기간', '첫 치료~단약 중앙값 9년, 첫 사용~단약 27년 (Dennis et al., 2005). B는 A(5년)·C(27년)의 중간값 16년'],
    ['노동능력 상실', '2025년 사범 무직 31.1%(대검찰청, 2026). B는 × 50%, A는 실직 25% × 50%(박성수, 2018)'],
    ['검증', '아편류 의존자 기대여명 일반인보다 남 14.7·여 15.8년 짧음(Lewer et al., 2020). 본 모형 단축 4.0~10.3년'],
  ];
  ev.forEach((r, i) => {
    const y = 4.15 + i * 0.44;
    R(s, { x: M, y, w: W - 2 * M, h: 0.4, fill: { color: i % 2 ? HEX.white : HEX.paper } });
    T(s, r[0], { x: M + 0.12, y, w: 1.6, h: 0.4, fontSize: 11.5, bold: true, valign: 'middle' });
    T(s, r[1], { x: M + 1.8, y, w: W - 2 * M - 1.9, h: 0.4, fontSize: 11, color: C.accent5, valign: 'middle' });
  });
  source(s, '2025년 검거 연령 분포 가중 평균. 2025년 불변가격, 실질 단가 증가 1.7%, 할인율 4.5%(3~5%), 총 누계는 물가 2.1% 반영·할인 없음. 한계: 생명표 보도 자료 인용(KOSIS 원표 확인 필요), 남녀 평균, 회복 후 초과 사망 가정, 국내 연구 없음');
  s.addNotes('1명당 생애비용 모형. 검거 해에 1년차 비용(하한 3,194.7만 원)을 내고, 이후 사망 시까지 활동 중독 기간의 반복 비용과 재검거, 노동능력 상실, 초과 사망 비용을 더한다. 기대여명은 통계청 생명표에 초과 사망률(Stockings et al., 2019)을 더해 계산했고 Lewer et al.(2020)과 비교해 검증했다. 국내 마약류 사용자 사망률 연구는 확인되지 않아 국내 자료가 생기면 가장 먼저 바꿀 모수.');
}

// ── 1명당 생애 사회적 비용: 결과 ──
s = content('Ⅴ. 집계 비용', 'Ⅴ. 집계 비용 — 1명당 생애 사회적 비용 (결과)', '기준(B) 현재가치 3.97억 · 명목 누계 12.28억 원');
{
  const hd = ['시나리오', 'PV 3%', 'PV 4%', 'PV 4.5%', 'PV 5%', '명목 누계', '기대여명 단축'];
  const rows = [
    ['A 조기회복', '2.12', '1.94', '1.86', '1.79', '4.39', '4.0년'],
    ['B 기준', '4.79', '4.21', '3.97', '3.75', '12.28', '7.5년'],
    ['C 만성화', '7.25', '6.30', '5.90', '5.55', '19.87 → 16.00', '10.3년'],
  ];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 12, align: j ? 'right' : 'left' } }))].concat(
    rows.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: 13, bold: i === 1 || j === 3, color: j === 3 ? HEX.teal : HEX.ink, fill: { color: i === 1 ? HEX.tealBg : HEX.white }, align: j ? 'right' : 'left' } }))));
  s.addTable(tr, { x: M, y: 1.5, w: 7.4, colW: [1.5, 0.9, 0.9, 1.0, 0.9, 1.25, 0.95], rowH: 0.48, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  T(s, '단위 억 원/명. 하한 0.32억 원·상한 16억 원 범위 적용. 현재가치는 모두 범위 안', { x: M, y: 3.5, w: 7.4, h: 0.3, fontSize: 10.5, color: C.accent5 });
  const comp = [["1년차", 0.32], ["반복(고통·의료·혼란)", 0.98], ["재검거 형사사법", 0.18], ["노동능력 상실", 0.7], ["초과사망(PGS)", 1.33], ["초과사망(소득)", 0.46]];
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
  const ag = [["17세", "674", "4.63", "22.65"], ["25세", "6,913", "4.62", "17.51"], ["35세", "6,986", "4.29", "12.54"], ["45세", "3,925", "3.66", "8.81"], ["55세", "2,428", "2.90", "6.05"], ["65세", "1,990", "2.26", "4.15"]];
  const tr2 = [['연령', '인원', 'PV', '누계'].map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.slate }, fontSize: 11, align: j ? 'right' : 'left' } }))].concat(
    ag.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: 11, fill: { color: i % 2 ? HEX.white : HEX.paper }, align: j ? 'right' : 'left' } }))));
  s.addTable(tr2, { x: X, y: 1.85, w: TW, colW: [0.9, 1.05, 1.0, 1.43], rowH: 0.34, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  RR(s, { x: X, y: 4.4, w: TW, h: 2.1, fill: { color: HEX.navyBg } });
  T(s, [
    { text: '초과 사망 고통(PGS)과 노동능력 상실이 가장 크게 움직임', options: { bullet: true, breakLine: true } },
    { text: '16억 원 상한은 C의 명목 누계에서만 닿음', options: { bullet: true, breakLine: true } },
    { text: '참고: 2025년 검거 전원 × B = 9.3조 원(λ 10 92.9조 원). 연간 사회적 비용과 더하지 않음', options: { bullet: true, breakLine: true } },
    { text: '주: 2016년 기준(별지 3)은 B 명목 누계 9.82억 원(2016년 가격). 2025년 가격으로 11.95억 원이라 본 연구와 비슷함. 차이는 가격 기준과 1년차 원단위(사망 고통 2.81억 원, 사회적 혼란 미산정)', options: { bullet: true, fontSize: 9.5, color: HEX.slate } },
  ], { x: X + 0.12, y: 4.4, w: TW - 0.24, h: 2.1, fontSize: 10, valign: 'middle', paraSpaceAfter: 3 });
  source(s, '통계청(2025), Stockings et al.(2019), Dennis et al.(2005), Lewer et al.(2020), 대검찰청(2026), 박성수(2018), 연구진 계산');
  s.addNotes('기준 시나리오 B의 1명당 생애 사회적 비용은 현재가치 4.5% 3.97억 원, 명목 총 누계 12.28억 원. A 1.86억, C 5.90억 원. C의 명목 누계 19.87억 원은 상한 16억 원으로 자름. 연간 총비용과는 기준이 달라 더하지 않음. 같은 모형을 2016년 기준에 적용한 부가연구(별지 3)는 9.82억 원(2016년 가격)으로, 2025년 가격으로 바꾸면 11.95억 원이라 본 연구와 비슷함.');
}

// ════════ Ⅵ. 교정 재활 비용편익 ════════
pres.addSection({ title: 'Ⅵ. 교정 재활 비용편익' });
s = pres.addSlide({ masterName: 'SECTION', sectionTitle: 'Ⅵ. 교정 재활 비용편익' });
s.addText('Ⅵ', { placeholder: 'num' }); s.addText('교정 재활 비용편익 (확정)', { placeholder: 'title' });
s.addText('재복역 실측(교정본부 자료)과 증분비용으로 B/C 산정', { placeholder: 'body' });

s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 교정 재활 비용편익 — 분석 구조', '증분비용과 재복역 감소 편익 비교');
chip(s, W - M - 1.4, 0.36, '확정', 'done', 1.4);
const box = (x, y, w, h, head, lines, col, bg) => {
  RR(s, { x, y, w, h, fill: { color: bg } });
  T(s, head, { x: x + 0.25, y: y + 0.15, w: w - 0.5, h: 0.42, fontSize: 17, bold: true, color: col });
  T(s, lines.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < lines.length - 1 } })), { x: x + 0.25, y: y + 0.65, w: w - 0.5, h: h - 0.8, fontSize: 12.5, paraSpaceAfter: 6 });
};
box(M, 1.55, 3.85, 2.75, '증분비용 ΔC (1인당)', ['프로그램 원가 UC-06 (과정 시간 비례)', '치료개입 UC-10', '사후관리 UC-12 ÷ (1+r)ᵗ', '수용기간 차이 ΔM × 변동원가', '수용비 전액은 이수·미이수 공통이라 제외'], HEX.navy, HEX.navyBg);
box(M + 4.1, 1.55, 3.85, 2.75, '편익 B (1인당 현재가치)', ['r0 기저재범률(미이수 재복역률)', 'Δr 재범감소율 = (r0 − r1) ÷ r0', 'SCᵣ 재복역 1건당 사회적 비용', 'D = Σ hₜ ÷ (1+r)ᵗ, 출소 후 3년(교정본부 자료)'], HEX.teal, HEX.tealBg);
box(M + 8.2, 1.55, 3.93, 2.75, '판정 지표', ['B/C = B ÷ ΔC', 'NPV = B − ΔC', '손익분기 Δr* = ΔC ÷ (r0 × SCᵣ × D)', '민감도: 문헌 효과, 신뢰구간 상한'], HEX.amber, HEX.amberBg);
T(s, '2025년 재활교육 개시 1,599명 · 이수 1,545명 · 중도탈락 54명 (과정별 이수)', { x: M, y: 4.6, w: 9, h: 0.35, fontSize: 13, bold: true });
[['기본 · 개시 1,283 · 탈락 46', '1,237명'], ['집중 · 개시 163 · 탈락 3', '160명'], ['심화 · 개시 44 · 탈락 4', '40명'], ['회복이음 · 개시 109 · 탈락 1', '108명']].forEach((c, i) => {
  const x = M + i * 3.07;
  R(s, { x, y: 5.0, w: 2.9, h: 1.1, fill: { color: HEX.paper } });
  T(s, c[1], { x: x + 0.2, y: 5.1, w: 2.6, h: 0.5, fontSize: 20, bold: true, color: C.accent1 });
  T(s, c[0], { x: x + 0.2, y: 5.62, w: 2.6, h: 0.35, fontSize: 11.5, color: C.accent5 });
});
source(s, '교정본부 자료(2026. 11.), 연구진 계산');
s.addNotes('제안서의 단약 편익(수용 중 마약 구입비 절감)은 불법시장 지출이 이전지출이라 제외. 의료절감·생산성회복은 SCᵣ에 포함해 별도 가산 안 함. 2025년 재활교육 개시 1,599명, 이수 1,545명, 중도탈락 54명(3.4%).');

// ── 비용편익 산출 구조(확정) ──
s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 교정 재활 비용편익 — 산출 구조', '증분비용(ΔC)과 재복역 1건당 비용(SCᵣ)의 산출 과정');
chip(s, W - M - 1.2, 0.36, '확정', 'done', 1.2);
const SC = { got: [HEX.teal, '실측'], est: [HEX.amber, '원단위·가정'], lit: [HEX.slate, '문헌'] };
Object.keys(SC).forEach((k, i) => {
  const x = W - M - 3 * 1.32 + i * 1.32;
  R(s, { x, y: 1.17, w: 0.16, h: 0.2, fill: { color: SC[k][0] } });
  T(s, SC[k][1], { x: x + 0.2, y: 1.12, w: 1.1, h: 0.3, fontSize: 10, color: C.accent5, valign: 'middle' });
});
function sb(x, y, w, h, op, title, val, note, st, fill) {
  R(s, { x, y, w, h, fill: { color: fill || HEX.paper } });
  R(s, { x, y, w: 0.09, h, fill: { color: SC[st][0] } });
  const dark = fill === HEX.navy || fill === HEX.teal;
  T(s, (op ? op + '  ' : '') + title, { x: x + 0.18, y: y + 0.05, w: w - 0.25, h: 0.28, fontSize: 10.5, bold: true, color: dark ? C.background1 : C.accent5 });
  T(s, val, { x: x + 0.18, y: y + 0.3, w: w - 0.25, h: 0.34, fontSize: 15, bold: true, color: dark ? C.background1 : C.accent1 });
  if (note) T(s, note, { x: x + 0.18, y: y + 0.62, w: w - 0.25, h: h - 0.64, fontSize: 9, color: dark ? C.accent6 : C.accent5 });
}
const LX = M, PW = 5.95, RX2 = M + 6.18;
T(s, '증분비용 ΔC (이수자 1인당, 2025년)', { x: LX, y: 1.45, w: PW, h: 0.35, fontSize: 14, bold: true, color: C.accent1 });
sb(LX, 1.88, 2.9, 0.98, '', '재활예산', '59.99억 원', '교정본부 자료 총액(집행액)', 'got');
sb(LX + 3.05, 1.88, 2.9, 0.98, '+', '전담인력 직접투입 인건비', '16.98억 원', '교정본부 자료 정원 × 2026 봉급표 × 1.6 × 투입비율', 'est');
sb(LX, 2.98, PW, 0.66, '÷', '2025 재활교육 이수 인원', '1,545명', '', 'got');
sb(LX, 3.76, PW, 0.66, '=', 'UC-06 이수자 1인당 프로그램 원가', '498.2만 원', '', 'got', HEX.teal);
sb(LX, 4.54, 1.9, 0.92, '+', 'UC-10 치료개입', '53.4만 원', '중독 외래 1인당 진료비', 'est');
sb(LX + 2.02, 4.54, 1.9, 0.92, '+', 'UC-12 사후관리', '83.6만 원', '치료보호 1인당 ÷ 1.045', 'est');
sb(LX + 4.04, 4.54, 1.91, 0.92, '+', 'ΔM × UC-02', '0', '수용기간 차이 없음(가정)', 'est');
sb(LX, 5.58, PW, 0.62, '=', 'ΔC 증분비용', '635.1만 원', '', 'est', HEX.navy);
T(s, '재복역 1건당 사회적 비용 SCᵣ (형사사법분)', { x: RX2, y: 1.45, w: PW, h: 0.35, fontSize: 14, bold: true, color: C.accent1 });
sb(RX2, 1.88, 1.85, 0.98, '', '평균 실형 기간', '2.45년', '백서 표 3-69(2025)', 'got');
sb(RX2 + 1.98, 1.88, 1.85, 0.98, '×', '실제 복역 비율', '85%', '가석방 반영 가정', 'est');
sb(RX2 + 3.96, 1.88, 1.99, 0.98, '×', 'UC-01 수용 1인·연', '2,378.4만 원', '교정본부 자료 8항목 1조 5,145.9억 ÷ 63,680명', 'got');
sb(RX2, 2.98, PW, 0.66, '=', '재수용비', '4,949.1만 원', '', 'est');
sb(RX2, 3.76, PW, 0.66, '+', '검찰 단계 1인당 (2024 결산 ÷ 처리인원)', '86.6만 원', '', 'got');
sb(RX2, 4.54, PW, 0.92, '=', 'SCᵣ 형사사법분 (하한)', '5,035.7만 원', '', 'est', HEX.navy);
R(s, { x: RX2, y: 5.58, w: PW, h: 0.62, fill: { color: HEX.white }, line: { color: HEX.amber, width: 1, dashType: 'dash' } });
T(s, '확장 SCᵣ = 하한 + 비형사사법 1명당 1,630.6만 = 6,666.3만 원 (의료·생산성 따로 더하지 않음)', { x: RX2 + 0.18, y: 5.58, w: PW - 0.3, h: 0.62, fontSize: 11, color: C.accent5, valign: 'middle' });
RR(s, { x: M, y: 6.27, w: W - 2 * M, h: 0.38, fill: { color: HEX.amberBg } });
T(s, '편익 B = (r0 34.5% − r1 31.6%) × SCᵣ × D 0.944 = 136.7만 원   →   B/C 0.22 (확장 SCᵣ 0.28)', { x: M + 0.2, y: 6.27, w: W - 2 * M - 0.4, h: 0.38, fontSize: 11.5, bold: true, color: C.accent3, valign: 'middle' });
s.addNotes('확정값. ΔC 635.1만 원 = 프로그램 498.2만 + 치료개입 53.4만 + 사후관리 83.6만. SCᵣ 하한 5,035.7만, 확장 6,666.3만 원. B/C 0.22~0.28.');


// ── 재복역 결과(교정본부 자료) ──
s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 교정 재활 비용편익 — 재복역 자료', '이수 31.6% vs 미이수·탈락 34.5%: 차이 2.9%p, 유의하지 않음');
{
  T(s, '마약류 출소자 3년 내 재복역 (교정본부 자료)', { x: M, y: 1.5, w: 4.0, h: 0.32, fontSize: 13, bold: true });
  const a8 = [['출소연도', '출소', '재복역', '재복역률'], ['2019', '1,605', '512', '31.9%'], ['2020', '1,602', '515', '32.1%'], ['2021', '1,386', '415', '29.9%'], ['2022', '1,384', '413', '29.8%'], ['합계', '5,977', '1,855', '31.0%']];
  s.addTable(a8.map((r, i) => r.map((v, j) => ({ text: v, options: { fontSize: 11.5, bold: i === 0 || i === 5, color: i === 0 ? HEX.white : HEX.ink, fill: { color: i === 0 ? HEX.navy : (i === 5 ? HEX.tealBg : (i % 2 ? HEX.white : HEX.paper)) }, align: j ? 'right' : 'left' } }))), { x: M, y: 1.85, w: 4.0, colW: [1.0, 1.0, 1.0, 1.0], rowH: 0.36, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  T(s, '재복역 시점: 1년 내 37.8% · 1~2년 43.1% · 2~3년 19.1% → D 0.944', { x: M, y: 4.1, w: 4.0, h: 0.6, fontSize: 10.5, color: C.accent5 });
  const X = M + 4.3, TW = W - M - X;
  T(s, '이수 여부별 3년 내 재복역 (교정본부 자료, 2019~2022 출소 합계)', { x: X, y: 1.5, w: TW, h: 0.32, fontSize: 13, bold: true });
  const a9 = [['구분', '출소', '재복역', '재복역률', '연령·형기·전과'], ['이수', '2,126', '672', '31.6%', '46~48세 · 26~31월 · 3~4범'], ['미이수', '101', '35', '34.7%', '45~49세 · 17~26월 · 3~6범'], ['중도탈락', '15', '5', '33.3%', '33~48세 · 20~31월 · 2~5범'], ['미이수+탈락 (r0)', '116', '40', '34.5%', '차 2.9%p (95% CI -6.0~11.7)'], ['참고: 교육 미지정', '3,735', '1,143', '30.6%', '전체 − 교육 지정, 모수 정의 다름']];
  s.addTable(a9.map((r, i) => r.map((v, j) => ({ text: v, options: { fontSize: 11, bold: i === 0 || i === 4, color: i === 0 ? HEX.white : HEX.ink, fill: { color: i === 0 ? HEX.navy : (i === 4 ? HEX.tealBg : (i % 2 ? HEX.white : HEX.paper)) }, align: j && j < 4 ? 'right' : 'left' } }))), { x: X, y: 1.85, w: TW, colW: [1.75, 0.8, 0.8, 0.95, TW - 4.3], rowH: 0.38, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  T(s, '과정별 이수자 재복역률: 기본 28.3% · 집중 41.2% · 심화 39.1%', { x: X, y: 4.2, w: TW, h: 0.35, fontSize: 12, bold: true });
  RR(s, { x: M, y: 4.85, w: W - 2 * M, h: 1.65, fill: { color: HEX.amberBg } });
  T(s, [
    { text: '이수자가 2.9%p 낮지만 비교 집단이 116명이라 차이는 유의하지 않다(z = 0.63).', options: { bullet: true, breakLine: true } },
    { text: '이수자는 형기가 길고, 고강도 과정(집중·심화)의 재복역률이 높다. 위험이 높은 사람이 고강도 과정에 배정된 것으로 보여 단순 비교는 효과를 과소 평가할 수 있다.', options: { bullet: true, breakLine: true } },
    { text: '비교 대상은 교육이 지정된 마약류사범. 기저 재복역률은 문헌 50.2%보다 낮은 실측 31.0~34.5%.', options: { bullet: true } },
  ], { x: M + 0.2, y: 4.85, w: W - 2 * M - 0.4, h: 1.65, fontSize: 12, valign: 'middle', paraSpaceAfter: 4 });
  source(s, '교정본부 자료(2026. 11.), 연구진 계산');
  s.addNotes('2019~2022년 마약류 출소자 5,977명 중 1,855명(31.0%)이 3년 안에 재복역. 교육 이수자 31.6%, 미이수·중도탈락 34.5%. 차이 2.9%p는 비교 집단이 116명으로 작아 유의하지 않음. 이수자 형기가 길고 고강도 과정의 재복역률이 높아 선택 편향 가능성.');
}

// ── 비용편익 확정 결과 ──
s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 교정 재활 비용편익 — 결과', '교정 재활 B/C 0.22~0.28: 관측 효과로는 편익이 비용에 못 미침');
{
  const hd = ['구분', '하한 (SCᵣ 형사사법분)', '확장 (SCᵣ 전 항목)'];
  const rows = [
    ['ΔC 증분비용 (프로그램 + 치료개입 + 사후관리)', '635.1만 원', '635.1만 원'],
    ['SCᵣ 재복역 1건당 사회적 비용', '5,035.7만 원', '6,666.3만 원'],
    ['B = (r0 − r1) × SCᵣ × D   [2.9%p × D 0.944]', '136.7만 원', '180.9만 원'],
    ['B/C (기본)', '0.22', '0.28'],
    ['NPV = B − ΔC', '-498.4만 원', '-454.2만 원'],
    ['손익분기 재복역률 차', '13.4%p', '10.1%p'],
    ['민감도: 문헌 효과(상대 19.2% → 6.6%p)', 'B/C 0.50', 'B/C 0.66'],
    ['민감도: 신뢰구간 상한 효과(11.7%p)', 'B/C 0.88', 'B/C 1.16'],
  ];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 12, align: j ? 'right' : 'left' } }))].concat(
    rows.map((r, i) => r.map((v, j) => ({ text: v, options: { fontSize: 12, bold: i === 3 || j === 0, color: i === 3 && j ? HEX.teal : HEX.ink, fill: { color: i === 3 ? HEX.tealBg : (i >= 6 ? HEX.amberBg : (i % 2 ? HEX.white : HEX.paper)) }, align: j ? 'right' : 'left' } }))));
  s.addTable(tr, { x: M, y: 1.5, w: 7.7, colW: [3.9, 1.8, 2.0], rowH: 0.47, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.04, 0.1, 0.04, 0.1] });
  RR(s, { x: 8.55, y: 1.5, w: 4.18, h: 4.95, fill: { color: HEX.navyBg } });
  T(s, [
    { text: '결론', options: { bold: true, fontSize: 14, breakLine: true } },
    { text: '관측된 재복역률 차(2.9%p)로는 B/C 0.22~0.28로 편익이 비용에 못 미친다.', options: { bullet: true, breakLine: true } },
    { text: '손익분기는 재복역률 차 10.1~13.4%p. 이수자 재복역률을 24.4% 이하로 낮추면 B/C ≥ 1이다.', options: { bullet: true, breakLine: true } },
    { text: '관측 차이는 유의하지 않고(95% CI −6.0~11.7%p), 이수자는 형기가 길어 효과가 과소 추정됐을 수 있다. 상한 효과에서는 B/C 1.16.', options: { bullet: true, breakLine: true } },
    { text: '정책 함의: 재활 확대와 함께 효과 측정(비교군·사후관리 연계)이 필요하다.', options: { bullet: true, bold: true } },
  ], { x: 8.75, y: 1.6, w: 3.8, h: 4.75, fontSize: 11.5, valign: 'top', paraSpaceAfter: 6 });
  source(s, '교정본부 자료(2026. 11.), 연구진 추계(치료보호·외래 진료비), 김도균·나종민(2025), 연구진 계산');
  s.addNotes('확정 B/C는 하한 0.22, 확장 0.28. 문헌 효과를 쓰면 0.50~0.66, 신뢰구간 상한 효과면 확장 1.16. 의료절감·생산성회복은 SCᵣ 안에 포함하고 따로 더하지 않음.');
}
// ════════ Ⅶ. 향후 계획 ════════
pres.addSection({ title: 'Ⅶ. 향후 계획' });
s = content('Ⅶ. 향후 계획', 'Ⅶ. 향후 계획', '최종보고서 작성과 정책 제언');
const plan = [
  ['1', '최종보고서 작성', '2025년 확정값(λ 10 7조 5,441.7억 원) 기준으로 본문·표 정리'],
  ['2', '산출 근거 정리', '항목별 산식·원단위·출처를 산출 근거 대장으로 정리'],
  ['3', '민감도 제시', 'λ 28.57, 할인율 3~5%, PGS 가구 구조, 교도소 기준'],
  ['4', '교정 재활 비용편익', 'B/C 0.22~0.28, 손익분기 10.1~13.4%p, 문헌·상한 효과 민감도'],
  ['5', '정책 제언', '재활 확대 규모, 효과 측정 체계, 사후관리 연계'],
];
plan.forEach((r, i) => {
  const y = 1.6 + i * 0.95;
  R(s, { x: M, y: y + 0.08, w: 0.6, h: 0.6, fill: { color: i === 0 ? HEX.teal : HEX.navy } }, pres.shapes.OVAL);
  T(s, r[0], { x: M, y: y + 0.08, w: 0.6, h: 0.6, fontSize: 18, bold: true, color: C.background1, align: 'center', valign: 'middle' });
  T(s, r[1], { x: M + 0.8, y: y + 0.02, w: 5.3, h: 0.38, fontSize: 15, bold: true });
  T(s, r[2], { x: M + 0.8, y: y + 0.4, w: 5.3, h: 0.4, fontSize: 12, color: C.accent5 });
});
RR(s, { x: 7.1, y: 1.6, w: 5.63, h: 4.6, fill: { color: HEX.amberBg } });
T(s, '주요 산정 가정', { x: 7.4, y: 1.8, w: 5.1, h: 0.42, fontSize: 16, bold: true, color: C.accent3 });
T(s, [
  { text: '고통비용 2,426.4억: 2024 원단위 × 물가', options: { bullet: true, breakLine: true } },
  { text: '검찰 199.3억: 2024 예산·인원', options: { bullet: true, breakLine: true } },
  { text: '사회적 혼란·기타 496.0억: 범죄 단가·2024 예산·문헌', options: { bullet: true, breakLine: true } },
  { text: '전담인력 인건비 16.98억: 투입비율 가정', options: { bullet: true, breakLine: true } },
  { text: '치료개입 53.4만 · 사후관리 83.6만: 외래 진료비·치료보호 예산', options: { bullet: true, breakLine: true } },
  { text: '재활예산 집행액 간주, 실제 복역 85%, ΔM 0', options: { bullet: true, breakLine: true } },
  { text: '생애비용: 회복 후 초과 사망, 재검거 확률', options: { bullet: true } },
], { x: 7.4, y: 2.3, w: 5.1, h: 3.8, fontSize: 12, paraSpaceAfter: 6 });
s.addNotes('2025년 기준 값으로 최종보고서를 작성하고 정책 제언을 정리한다.');

pres.addSection({ title: '맺음' });
s = pres.addSlide({ masterName: 'COVER', sectionTitle: '맺음' });
s.addText('감사합니다', { placeholder: 'title' });
s.addText([
  { text: '연구책임자  박성수 교수 (세명대학교 경찰학과)', options: { breakLine: true } },
  { text: '마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석 · 중간보고', options: {} },
], { placeholder: 'body' });

// ════════ 부록 ════════
pres.addSection({ title: '부록' });
s = pres.addSlide({ masterName: 'SECTION', sectionTitle: '부록' });
s.addText('A', { placeholder: 'num' }); s.addText('부록', { placeholder: 'title' });
s.addText('고통비용 시나리오, 1명당 비용 계수, 구성비, 교도소 인원 기준, 암수율별 항목표', { placeholder: 'body' });

// 부록 1. PGS 시나리오
s = content('부록', '부록 1 — 고통비용(PGS) 시나리오', '가구 구조별 4개 분야 λ 10: 7조 357.9억~7조 2,505.2억 원');
{
  const hd = ['시나리오', '1인가구 비중', 'PGS', '암수율 미반영', 'λ 10 (기본)', 'λ 28.57', '검거 사범 1명당'];
  const rows = [
    ['선행연구 시점 가구 구조 (2016)', '27.9%', '2,628.8', '7,250.5', '72,505.2', '207,147.4', '3,098.1만 원', 0],
    ['기본: 원단위 조사 시점 (2024)', '36.1%', '2,426.4', '7,048.1', '70,481.3', '201,365.1', '3,011.6만 원', 1],
    ['최근 가구 구조 (2025)', '36.6%', '2,414.1', '7,035.8', '70,357.9', '201,012.5', '3,006.4만 원', 0],
    ['참고: 본인 고통만 (가족 제외)', '—', '849.2', '5,471.0', '54,709.7', '156,305.5', '2,337.7만 원', 2],
    ['참고: PGS 미반영', '—', '0.0', '4,621.7', '46,217.3', '132,042.7', '1,974.8만 원', 2]
  ];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 11.5, align: j >= 1 ? 'right' : 'left' } }))].concat(
    rows.map(r => r.slice(0, 7).map((c, j) => ({ text: c, options: { fontSize: 12, bold: r[7] === 1 || j === 3, color: r[7] === 2 ? HEX.slate : (j === 3 ? HEX.teal : HEX.ink), fill: { color: r[7] === 1 ? HEX.tealBg : HEX.white }, align: j >= 1 ? 'right' : 'left' } }))));
  s.addTable(tr, { x: M, y: 1.55, w: W - 2 * M, colW: [3.2, 1.25, 1.2, 2.0, 1.4, 1.45, 1.63], rowH: 0.5, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.04, 0.1, 0.04, 0.1] });
  RR(s, { x: M, y: 4.75, w: 6.0, h: 1.75, fill: { color: HEX.navyBg } });
  T(s, [
    { text: '조정 방법', options: { bold: true, breakLine: true } },
    { text: 'PGS = 본인 고통 + 가족 고통. 가족 고통만 가구 구조에 비례해 조정', options: { bullet: true, breakLine: true } },
    { text: '가족 고통 조정 계수 = (1 − 1인가구 비중) ÷ (1 − 36.1%)', options: { bullet: true, breakLine: true } },
    { text: '본인 고통 비중 35% 가정: 2013년 본인 고통만 조사한 사망 PGS 약 2.8억 원(물가 반영 약 3.4억 원) ÷ 9.7억 원', options: { bullet: true } },
  ], { x: M + 0.15, y: 4.75, w: 5.7, h: 1.75, fontSize: 11, valign: 'middle', paraSpaceAfter: 2 });
  RR(s, { x: M + 6.2, y: 4.75, w: W - 2 * M - 6.2, h: 1.75, fill: { color: HEX.amberBg } });
  T(s, [
    { text: '해석', options: { bold: true, breakLine: true } },
    { text: '1인가구 증가(27.9% → 36.6%)로 가족 고통 몫이 줄어 PGS는 2016년 구조 대비 202.4억 원(λ 10 2,023.9억) 감소', options: { bullet: true, breakLine: true } },
    { text: '원단위 조사(2024)와 최근(2025)의 차이는 12.3억 원으로 작음', options: { bullet: true, breakLine: true } },
    { text: '원단위의 본인·가족 구성은 미공개. 원보고서 확인 후 확정', options: { bullet: true } },
  ], { x: M + 6.35, y: 4.75, w: W - 2 * M - 6.5, h: 1.75, fontSize: 11, valign: 'middle', paraSpaceAfter: 2 });
  source(s, '한국교통연구원(2025. 7. 28.) 보도자료; 통계청 인구주택총조사(2016: 1인가구 27.9%, 2024: 36.1%, 2025: 36.6%); 연구진 계산. 금액 억 원');
  s.addNotes('2025년 PGS 2,426.4억 원 기준의 가구 구조 시나리오. 4개 분야 λ 10은 2016년 구조 7조 2,505.2억, 기본 7조 481.3억, 2025년 구조 7조 357.9억 원. 본인 고통 비중 35%는 가정이며 원보고서 확인 필요.');
}

// 부록 2. 중독자 1명당 비용 계수
s = content('부록', '부록 2 — 중독자 1명당 비용 계수', '중독자(검거 사범) 1명이 늘 때 사회적 비용 3,223.6만 원');
{
  const L = [
    ['형사사법', '1,593.0', [['교도소', '834.6'], ['경찰', '590.1'], ['검찰', '85.1'], ['법원', '42.3'], ['보호관찰소', '38.7'], ['국립법무병원', '2.2']], HEX.navy],
    ['고통비용 (PGS)', '1,036.8', [['중독자 PGS', '791.3'], ['사망 PGS', '245.4']], HEX.red],
    ['생산성', '348.2', [['조기사망', '180.3'], ['노동력 상실·미취업', '158.3'], ['이환·입원', '9.6']], HEX.amber],
    ['사회적 혼란·기타', '212.0', [['예방·대응 예산', '153.8'], ['2차 범죄', '48.1'], ['약물 운전', '6.4'], ['가족 돌봄', '3.7']], HEX.slate],
    ['의료·복지', '33.6', [['직접 의료비', '19.0'], ['정신건강·복지', '7.3'], ['간접의료비', '7.3']], HEX.teal],
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
    { text: '합계 3,223.6만 원 / 1명', options: { bold: true, fontSize: 16, breakLine: true } },
    { text: '계수 = 2025년 항목별 비용 ÷ 검거 사범 23,403명. 암수율 반영 값 = 계수 × 실질 사용자 N*(λ 10: 234,030명, λ 28.57: 668,624명). 사회적 혼란·기타 포함 모든 항목에 적용. 기관별 계수는 평균비용 가정', options: { fontSize: 10.5, color: HEX.mist } },
  ], { x: M + 0.25, y: 5.55, w: W - 2 * M - 0.5, h: 0.95, color: C.background1, valign: 'middle' });
  source(s, '연구진 추계(2026), 한국교통연구원(2025), 대검찰청(2026), 연구진 계산. 단위 만 원/명');
  s.addNotes('2025년 1명당 비용 계수. 형사사법 1,593.0만, 고통비용 1,036.8만, 생산성 348.2만, 사회적 혼란·기타 212.0만, 의료·복지 33.6만, 합계 3,223.6만 원. 세부로는 교도소 834.6만, 중독자 PGS 791.3만, 경찰 590.1만 원 순.');
}

// 부록 3. 비용 비중
s = content('부록', '부록 3 — 사회적 비용 구성비', '형사사법 49.4% · 고통비용 32.2% · 생산성 10.8% (λ 10)');
{
  s.addChart(pres.charts.DOUGHNUT, [{ name: '구성비', labels: ['형사사법', '고통비용(PGS)', '생산성', '사회적 혼란·기타', '의료·복지'], values: [37282.0, 24264.1, 8149.7, 4960.4, 785.6] }], {
    x: M, y: 1.45, w: 6.4, h: 5.1, holeSize: 52, chartColors: [HEX.navy, HEX.red, HEX.amber, HEX.slate, HEX.teal],
    showPercent: true, showValue: false, showLegend: false, dataLabelColor: HEX.white, dataLabelFontSize: 13, dataLabelFontBold: true, dataLabelPosition: 'bestFit',
  });
  T(s, [{ text: '7조 5,441.7억', options: { bold: true, fontSize: 20, breakLine: true } }, { text: 'λ 10', options: { fontSize: 11, color: HEX.slate } }], { x: M + 1.95, y: 3.55, w: 2.5, h: 0.9, align: 'center', valign: 'middle' });
  const leg = [['형사사법', '3조 7,282.0억', '49.4%', HEX.navy], ['고통비용 (PGS)', '2조 4,264.1억', '32.2%', HEX.red], ['생산성', '8,149.7억', '10.8%', HEX.amber], ['사회적 혼란·기타', '4,960.4억', '6.6%', HEX.slate], ['의료·복지', '785.6억', '1.0%', HEX.teal]];
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
    { text: 'PGS 시나리오(부록 1)에 따라 고통비용 비중 32.1~33.9%', options: { bullet: true } },
  ], { x: 7.75, y: 5.0, w: 4.9, h: 1.4, fontSize: 11, valign: 'middle', paraSpaceAfter: 2 });
  source(s, '연구진 추계(2026), 한국교통연구원(2025), 연구진 계산');
  s.addNotes('2025년, 암수율 10배 기준 7조 5,441.7억 원의 구성비. 형사사법 49.4%, 고통비용 32.2%, 생산성 10.8%, 사회적 혼란·기타 6.6%, 의료·복지 1.0%.');
}

// 부록 4. 교도소 인원 기준
s = content('부록', '부록 4 — 교도소 인원 기준', '미결 포함 유지: 7,429명 = 기결 4,188 + 미결 3,241명');
{
  const hd = ['구분', '12. 31. 전체 수용자 (기본)', '연평균 (참고)', '차이'];
  const rows = [
    ['마약류 7,429명 구성 (교정본부 자료)', '기결 4,188 + 미결 3,241명', '—', ''],
    ['교도소 마약류 인원 ÷ 전체 수용', '7,429 ÷ 64,626명', '3,608 ÷ 63,680명', ''],
    ['마약류 비율', '11.50%', '5.67%', '−5.83%p'],
    ['교도소 비용 (결산 1조 6,992.2억 × 비율)', '1,953.3억', '962.7억', '-990.6억'],
    ['형사사법 6개 기관 (암수율 미반영)', '3,728.2억', '2,737.6억', '-990.6억'],
    ['형사사법 (λ 10)', '3조 7,282.0억', '2조 7,376.3억', '-9,905.7억'],
    ['사회적 비용 전체 (λ 10)', '7조 5,441.7억', '6조 5,536.0억', '-9,905.7억'],
    ['교도소 λ 10 금액 ÷ 교정 결산', '115.0%', '56.7%', ''],
  ];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 12, align: j ? 'right' : 'left' } }))].concat(
    rows.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: 12.5, bold: i === 5 || i === 6 || j === 1, color: j === 3 ? HEX.red : (j === 1 ? HEX.teal : HEX.ink), fill: { color: i === 6 ? HEX.tealBg : (i % 2 ? HEX.white : HEX.paper) }, align: j ? 'right' : 'left' } }))));
  s.addTable(tr, { x: M, y: 1.55, w: W - 2 * M, colW: [4.4, 2.6, 2.6, 2.53], rowH: 0.43, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.04, 0.12, 0.04, 0.12] });
  RR(s, { x: M, y: 5.6, w: W - 2 * M, h: 0.92, fill: { color: HEX.amberBg } });
  T(s, [
    { text: '기준  ', options: { bold: true } },
    { text: '교정본부 자료(2026. 11.): 3,477명(2024)·4,188명(2025)은 연말 기결수로 1일 평균이 아니다. 결산은 미결 수용비를 포함하므로 미결 포함 기준(7,429 ÷ 64,626명)을 유지한다. 1,953.3억 원 = 기결분 1,101.2억 + 미결분 852.2억 원. 연평균 열은 참고용', options: {} },
  ], { x: M + 0.2, y: 5.6, w: W - 2 * M - 0.4, h: 0.92, fontSize: 11.5, valign: 'middle' });
  source(s, '연구진 형사사법비용 추계(2026) <표 12>, 교정본부 자료(2025 결산, 1일 평균 63,680명), 교정본부 자료(2026. 11.), 연구진 계산');
  s.addNotes('교정본부 확인: 7,429명 = 기결 4,188 + 미결 3,241명. 미결 포함 기준 유지. 연평균 추정(962.7억 원)은 참고용.');
}

// 부록 5. 암수율별 항목표
s = content('부록', '부록 5 — 암수율별 항목 비용표', '암수율 10배(기본)와 28.57배(민감도)의 항목별 금액 (억 원)');
{
  const hd = ['부문', '세부 항목', '암수율 미반영', '1명당 계수 (만 원)', 'λ 10 (234,030명)', 'λ 28.57 (668,624명)', '비중'];
  const R5 = [
    ['형사사법', '소계', '3,728.2', '1,593.0', '37,282.0', '106,514.5', '49.4%', 1],
    ['', '교도소 · 경찰 · 검찰', '1,953.3 · 1,381.0 · 199.3', '834.6 · 590.1 · 85.1', '19,533.1 · 13,810.1 · 1,992.7', '55,806.2 · 39,455.4 · 5,693.1', '', 0],
    ['', '법원 · 보호관찰소 · 국립법무병원', '99.0 · 90.5 · 5.1', '42.3 · 38.7 · 2.2', '990.0 · 905.1 · 51.0', '2,828.4 · 2,585.8 · 145.8', '', 0],
    ['고통비용', '소계', '2,426.4', '1,036.8', '24,264.1', '69,322.4', '32.2%', 1],
    ['', '중독자(1,649명) · 사망(58명)', '1,852.0 · 574.4', '791.3 · 245.4', '18,519.9 · 5,744.1', '52,911.4 · 16,411.0', '', 0],
    ['생산성', '소계', '815.0', '348.2', '8,149.7', '23,283.6', '10.8%', 1],
    ['', '조기사망 · 미취업 · 이환·입원', '421.9 · 370.6 · 22.5', '180.3 · 158.3 · 9.6', '4,218.9 · 3,705.5 · 225.2', '12,053.4 · 10,586.7 · 643.5', '', 0],
    ['의료·복지', '소계', '78.6', '33.6', '785.6', '2,244.6', '1.0%', 1],
    ['', '직접 의료 · 간접 · 정신건강·복지', '44.6 · 17.0 · 17.0', '19.0 · 7.3 · 7.3', '445.8 · 169.8 · 170.0', '1,273.6 · 485.2 · 485.7', '', 0],
    ['사회혼란 등', '소계', '496.0', '212.0', '4,960.4', '14,171.8', '6.6%', 1],
    ['', '예방 · 2차 범죄', '360.0 · 112.5', '153.8 · 48.1', '3,600.0 · 1,125.2', '10,285.2 · 3,214.7', '', 0],
    ['', '운전 · 가족', '14.9 · 8.6', '6.4 · 3.7', '148.8 · 86.4', '425.2 · 246.7', '', 0],
    ['합계', '', '7,544.2', '3,223.6', '75,441.7', '215,537.0', '100%', 2],
  ];
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 10.5, align: j >= 2 ? 'right' : 'left' } }))].concat(
    R5.map(r => r.slice(0, 7).map((c, j) => ({ text: c, options: { fontSize: r[7] ? 10.5 : 9, bold: r[7] > 0, color: r[7] ? (j === 4 ? HEX.teal : HEX.ink) : HEX.slate, fill: { color: r[7] === 1 ? HEX.tealBg : (r[7] === 2 ? HEX.navyBg : HEX.white) }, align: j >= 2 ? 'right' : 'left' } }))));
  s.addTable(tr, { x: M, y: 1.5, w: W - 2 * M, colW: [1.05, 2.75, 1.6, 1.5, 2.05, 2.25, 0.75], rowH: 0.31, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  T(s, '1명당 계수 = 2025년 항목 비용 ÷ 검거 사범 23,403명. 암수율 반영 금액 = 1명당 계수 × 실질 사용자. 비중은 λ 10 기준. 모든 항목에 암수율 적용', { x: M, y: 6.38, w: W - 2 * M, h: 0.28, fontSize: 10.5, color: C.accent5 });
  source(s, '연구진 추계(2026), 한국교통연구원(2025), 대검찰청(2026), 박성수·백민석(2019), 연구진 계산');
  s.addNotes('2025년, 암수율 10배와 28.57배의 항목별 금액. 10배 합계 7조 5,441.7억 원, 28.57배 21조 5,537.0억 원. 사회적 혼란·기타 포함 모든 항목에 λ 적용.');
}

(async () => {
  const out = '/home/claude/deck25b/중간보고_마약류사회적비용_2025기준_보고용.pptx';
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  require('child_process').execSync(`python3 /home/claude/deck/fixppr.py "${out}"`, { stdio: 'inherit' });
  console.log('written', out);
})();
