import re, sys
fn = sys.argv[1]; mode = sys.argv[2]  # final | report
s = open(fn).read()
def rep(a, b):
    global s
    assert a in s, a[:120]; s = s.replace(a, b)

# ── 목차 ──
s, k = re.subn(r"\['Ⅵ', '교정 재활 비용편익', '[^']*', 'done', '확정'\],",
               "['Ⅵ', '교정 재활 비용편익', '재복역 1건 기준과 생애가치 기준 B/C', 'done', '확정'],", s); assert k == 1
s, k = re.subn(r"\['Ⅶ', '[^']*', '[^']*', 'plan', '계획'\],",
               "['Ⅶ', '정책 제언과 향후 계획', '비용편익 근거의 제언, 최종보고서 작성', 'plan', '계획'],", s); assert k == 1

# ── 요약 ──
rep("교정 재활 B/C 0.22~0.28(문헌 효과 적용 시 0.50~0.66).",
    "교정 재활 B/C: 재복역 1건 기준 0.22~0.28, 생애가치 기준 3.44~8.28(현재가치 1.93~4.63).")

# ── Ⅵ 간지 ──
s, k = re.subn(r"s\.addText\('재복역 실측[^']*B/C [^']*', \{ placeholder: 'body' \}\);",
    "s.addText('재복역 1건 기준(하한)과 생애가치 기준으로 B/C 산정', { placeholder: 'body' });", s); assert k == 1

# ── 단기 결과 슬라이드 → 재복역 1건 기준 ──
rep("s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 교정 재활 비용편익 — 결과', '교정 재활 B/C 0.22~0.28: 관측 효과로는 편익이 비용에 못 미침');",
    "s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 교정 재활 비용편익 — 결과 ① 재복역 1건 기준', '재복역 1건 기준 B/C 0.22~0.28: 편익의 하한');")
rep("{ text: '정책 함의: 재활 확대와 함께 효과 측정(비교군·사후관리 연계)이 필요하다.', options: { bullet: true, bold: true } },",
    "{ text: '이 값은 출소 후 3년 안의 재복역 1건만 본 하한이다. 효과가 남은 생애의 중독 비용을 줄이는 몫은 생애가치 기준(결과 ②)으로 본다.', options: { bullet: true, bold: true } },")
rep("s.addNotes('확정 B/C는 하한 0.22, 확장 0.28.",
    "s.addNotes('재복역 1건 기준 B/C는 하한 0.22, 확장 0.28. 편익을 출소 후 3년 재복역 1건으로만 잡은 하한이다.")

NEW = r"""
// ── 생애가치 기반 편익 모형 ──
s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 교정 재활 비용편익 — 생애가치 모형', '재활 효과가 남은 생애의 중독 비용을 줄이는 몫을 편익으로 본다');
{
  RR(s, { x: M, y: 1.5, w: 5.55, h: 1.25, fill: { color: HEX.navyBg } });
  T(s, '편익 B = e × Σ w(t) × C(t)        (t = 1년차 이후, 남은 생애)', { x: M + 0.2, y: 1.6, w: 5.2, h: 0.4, fontSize: 14, bold: true, color: C.accent1 });
  T(s, [
    { text: 'C(t): 1인당 생애비용(B 시나리오)의 t년차 비용. 누적 11.96억 원(현재가치 3.65억 원)', options: { bullet: true, breakLine: true } },
    { text: '비용 ΔC 635.1만 원은 재복역 1건 기준과 같다', options: { bullet: true } },
  ], { x: M + 0.2, y: 2.02, w: 5.2, h: 0.7, fontSize: 11, color: C.text1, paraSpaceAfter: 2 });
  const ef = [['e 재활 효과(상대 감소)', ''], ['관측(교정본부 자료)', '8.3%  (2.87%p ÷ 34.5%, 유의하지 않음)'], ['국내 문헌', '19.2%  (김도균·나종민, 2025)'], ['국외 메타분석', '20%  (OR 1.37, 재범 35%→28%)']];
  const pe = [['w(t) 효과 지속', ''], ['3년 한정', '재복역 추적 기간까지만'], ['5년 반감 (기준)', '5년마다 효과가 절반'], ['평생 유지', '상한 참고']];
  [[ef, 2.95], [pe, 4.65]].forEach(([tb, y]) => {
    s.addTable(tb.map((r, i) => r.map((v, j) => ({ text: v, options: { fontSize: 11, bold: i === 0 || j === 0, color: i === 0 ? HEX.white : HEX.ink, fill: { color: i === 0 ? HEX.navy : (i % 2 ? HEX.white : HEX.paper) }, colspan: i === 0 && j === 0 ? 2 : undefined } }))).map((r, i) => i === 0 ? [r[0]] : r),
      { x: M, y, w: 5.55, colW: [1.85, 3.7], rowH: 0.34, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  });
  const X = M + 5.85, TW = W - M - X;
  T(s, '선행연구와 참고 기준', { x: X, y: 1.5, w: TW, h: 0.32, fontSize: 13, bold: true });
  const lit = [
    ['연구', '내용', '활용'],
    ['Cohen & Piquero(2009)', '중증 약물사용자 1명의 생애 외부비용 84만~110만 달러(현재가치)', '생애가치 편익 개념'],
    ['Mitchell 외(2006)', '교정시설 약물치료 66개 연구 메타분석, 재범 OR 1.37', '국외 효과 20%'],
    ['김도균·나종민(2025)', '국내 마약류사범 재범 감소 효과', '국내 효과 19.2%'],
    ['Inciardi 외(2004)', '교정 치료공동체 + 출소 후 사후관리 5년 추적, 재체포·약물사용 감소', '효과 지속 근거'],
    ['WSIPP(2023)', '교정시설 치료공동체 B/C 9.56', '결과 비교'],
    ['Ettner 외(2006)', '치료비 1달러당 편익 약 7달러', '결과 비교'],
    ['NIDA(2006)', '치료 1달러당 범죄 관련 비용 4~7달러 절감', '결과 비교'],
    ['기획재정부(2017)', '사회적 할인율 4.5%', '현재가치 할인'],
  ];
  s.addTable(lit.map((r, i) => r.map((v, j) => ({ text: v, options: { fontSize: 10, bold: i === 0 || j === 0, color: i === 0 ? HEX.white : HEX.ink, fill: { color: i === 0 ? HEX.navy : (i % 2 ? HEX.white : HEX.paper) } } }))),
    { x: X, y: 1.85, w: TW, colW: [1.7, TW - 3.0, 1.3], rowH: 0.47, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  source(s, 'Cohen & Piquero(2009), Mitchell·Wilson·MacKenzie(2006), Inciardi·Martin·Butzin(2004), WSIPP(2023), Ettner 외(2006), NIDA(2006), 김도균·나종민(2025), 기획재정부(2017), 연구진 계산');
  s.addNotes('재복역 1건 기준은 출소 후 3년 재복역만 편익으로 본다. 생애가치 기준은 재활 효과 e가 1년차 이후 남은 생애의 중독 관련 비용을 같은 비율로 줄인다고 보고, 효과는 w(t)만큼 남는다고 둔다. 미래 비용은 B 시나리오 생애비용에서 1년차를 뺀 값으로 누적 11.96억 원, 현재가치 3.65억 원이다. Cohen과 Piquero(2009)는 고위험 청소년 1명의 생애 외부비용을 추정하였고, 중증 약물사용자는 84만~110만 달러였다.');
}

// ── 생애가치 B/C 결과 ──
s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 교정 재활 비용편익 — 결과 ② 생애가치 기준', '생애가치 기준 B/C 3.44~8.28(현재가치 1.93~4.63)');
{
  const hd = ['효과 지속', '관측 8.3%', '국내 19.2%', '국외 20%', '손익분기 e*'];
  const rows = [
    ['3년 한정', '1.52 (1.04)', '3.51 (2.39)', '3.66 (2.49)', '5.5% (8.0%)'],
    ['5년 반감 (기준)', '3.44 (1.93)', '7.94 (4.44)', '8.28 (4.63)', '2.4% (4.3%)'],
    ['평생 유지', '15.68 (4.78)', '36.17 (11.03)', '37.67 (11.49)', '0.5% (1.7%)'],
  ];
  T(s, 'B/C: 누적 기준 (현재가치 4.5%), B 시나리오', { x: M, y: 1.5, w: 7.7, h: 0.32, fontSize: 13, bold: true });
  const tr = [hd.map((h, j) => ({ text: h, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 11.5, align: j ? 'right' : 'left' } }))].concat(
    rows.map((r, i) => r.map((v, j) => ({ text: v, options: { fontSize: 12, bold: i === 1 || j === 0, color: i === 1 && j ? HEX.teal : HEX.ink, fill: { color: i === 1 ? HEX.tealBg : (i % 2 ? HEX.white : HEX.paper) }, align: j ? 'right' : 'left' } }))));
  s.addTable(tr, { x: M, y: 1.85, w: 7.7, colW: [1.7, 1.45, 1.5, 1.5, 1.55], rowH: 0.44, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  T(s, '민감도 (5년 반감, 현재가치 B/C, 관측 · 국외 효과)', { x: M, y: 3.75, w: 7.7, h: 0.32, fontSize: 13, bold: true });
  const sv = [['구분', '관측', '국외', '구분', '관측', '국외'], ['A 조기회복', '1.12', '2.70', '할인율 3%', '2.14', '5.15'], ['C 만성화', '2.67', '6.41', '할인율 5%', '1.86', '4.48']];
  s.addTable(sv.map((r, i) => r.map((v, j) => ({ text: v, options: { fontSize: 11.5, bold: i === 0 || j === 0 || j === 3, color: i === 0 ? HEX.white : HEX.ink, fill: { color: i === 0 ? HEX.navy : (i % 2 ? HEX.white : HEX.paper) }, align: j % 3 ? 'right' : 'left' } }))),
    { x: M, y: 4.1, w: 7.7, colW: [1.6, 1.1, 1.15, 1.6, 1.1, 1.15], rowH: 0.36, border: { type: 'solid', color: HEX.mist, pt: 0.5 }, fontFace: '맑은 고딕', valign: 'middle', margin: [0.03, 0.08, 0.03, 0.08] });
  RR(s, { x: M, y: 5.35, w: 7.7, h: 1.2, fill: { color: HEX.amberBg } });
  T(s, [
    { text: '2025년 이수 1,545명 기준 순편익(5년 반감): 관측 효과 239.8억 원(현재가치 90.8억 원), 국외 효과 713.9억 원(현재가치 355.9억 원)', options: { bullet: true, breakLine: true } },
    { text: '국외 결과와 비교: WSIPP 9.56, Ettner 외 약 7, NIDA 4~7. 현재가치 B/C 1.93~4.63은 이보다 낮은 보수적 범위이다.', options: { bullet: true } },
  ], { x: M + 0.2, y: 5.35, w: 7.3, h: 1.2, fontSize: 11.5, valign: 'middle', paraSpaceAfter: 4 });
  RR(s, { x: 8.55, y: 1.5, w: 4.18, h: 5.05, fill: { color: HEX.navyBg } });
  T(s, [
    { text: '해석', options: { bold: true, fontSize: 14, breakLine: true } },
    { text: '재활 효과가 5년마다 절반으로 줄어도 관측 효과로 B/C 3.44(현재가치 1.93)이다.', options: { bullet: true, breakLine: true } },
    { text: '손익분기 효과는 2.4%(현재가치 4.3%)로, 이수자 100명 중 미이수 대비 재범자가 1~2명만 줄어도 비용을 회수한다.', options: { bullet: true, breakLine: true } },
    { text: '효과가 3년에 그치면 관측 효과의 현재가치 B/C는 1.04로 손익분기에 가깝다. 효과를 오래 유지하는 것이 편익의 크기를 정한다.', options: { bullet: true, breakLine: true } },
    { text: '전제와 한계: 관측 효과는 유의하지 않고, 효과가 모든 중독 관련 비용에 같은 비율로 미친다고 가정하였다. 판정은 현재가치 기준으로 한다.', options: { bullet: true, bold: true } },
  ], { x: 8.75, y: 1.6, w: 3.8, h: 4.85, fontSize: 11.5, valign: 'top', paraSpaceAfter: 6 });
  source(s, '교정본부 자료(2026. 11.), 통계청 생명표(2024), Mitchell 외(2006), 김도균·나종민(2025), WSIPP(2023), Ettner 외(2006), NIDA(2006), 연구진 계산');
  s.addNotes('생애가치 기준 B/C는 누적 기준으로 관측 효과 3.44, 국내 문헌 7.94, 국외 메타분석 8.28이고, 현재가치로는 1.93, 4.44, 4.63이다(효과 5년 반감). 손익분기 효과는 누적 2.4%, 현재가치 4.3%. 효과가 3년에 그치면 현재가치 1.04~2.49, 평생 유지되면 4.78~11.49. 고위험(C 시나리오)일수록 B/C가 높다(관측 2.67). 관측 효과는 통계적으로 유의하지 않으므로 결과는 효과 가정에 따른 범위로 읽는다.');
}
"""

if mode == 'final':
    anchor = "s = content('Ⅵ. 교정 재활 비용편익', 'Ⅵ. 자료 구분'"
else:
    anchor = "// ════════ Ⅶ"
i = s.index(anchor); s = s[:i] + NEW.lstrip('\n') + s[i:]

POL = r"""// ════════ Ⅶ. 정책 제언 ════════
pres.addSection({ title: 'Ⅶ. 정책 제언' });
s = pres.addSlide({ masterName: 'SECTION', sectionTitle: 'Ⅶ. 정책 제언' });
s.addText('Ⅶ', { placeholder: 'num' }); s.addText('정책 제언과 향후 계획', { placeholder: 'title' });
s.addText('효과의 지속, 효과 측정, 지역사회 수용 기반', { placeholder: 'body' });

const pcard = (x, y, w, h, no, head, ev, lines, col, bg) => {
  RR(s, { x, y, w, h, fill: { color: bg } });
  R(s, { x: x + 0.2, y: y + 0.18, w: 0.46, h: 0.46, fill: { color: col } }, pres.shapes.OVAL);
  T(s, no, { x: x + 0.2, y: y + 0.18, w: 0.46, h: 0.46, fontSize: 14, bold: true, color: C.background1, align: 'center', valign: 'middle' });
  T(s, head, { x: x + 0.8, y: y + 0.15, w: w - 0.95, h: 0.52, fontSize: 15, bold: true, color: col, valign: 'middle' });
  T(s, ev, { x: x + 0.2, y: y + 0.78, w: w - 0.4, h: 0.7, fontSize: 12, bold: true, color: C.accent5 });
  T(s, lines.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < lines.length - 1 } })), { x: x + 0.2, y: y + 1.6, w: w - 0.4, h: h - 1.75, fontSize: 13.5, paraSpaceAfter: 8 });
};

s = content('Ⅶ. 정책 제언', 'Ⅶ. 정책 제언 ① 비용편익 근거', '재활 효과를 오래 유지하고, 측정하고, 필요한 사람에게 집중한다');
{
  const cw = (W - 2 * M - 3 * 0.15) / 4;
  pcard(M, 1.5, cw, 4.2, '1', '출소 전후 연속 처우', '효과 3년 한정 B/C 1.52(현재가치 1.04) → 5년 반감 3.44(1.93)',
    ['교정 재활–출소–지역사회 치료를 한 사례 경로로 잇는다', '출소 전후 일정 기간을 전환 구간으로 정해 지역 치료기관에 직접 인계한다', '인계에 필요한 최소 정보만 본인 동의를 받아 공유한다'], HEX.teal, HEX.tealBg);
  pcard(M + (cw + 0.15), 1.5, cw, 4.2, '2', '효과 측정과 성과관리', '관측 효과 2.9%p, 95% CI −6.0~11.7%p (비교군 116명)',
    ['교육 지정자 가운데 비교군을 두는 평가 설계를 도입한다', '재복역 외에 재검거, 치료 유지, 취업을 공동 성과지표로 둔다', '교정·보호관찰·치료기관 자료를 개인 단위로 연계해 추적한다'], HEX.navy, HEX.navyBg);
  pcard(M + 2 * (cw + 0.15), 1.5, cw, 4.2, '3', '고위험군 우선 배정', 'B/C(현재가치, 관측) A 1.12 · B 1.93 · C 2.67',
    ['중독이 만성화될 위험이 높을수록 줄일 수 있는 생애비용이 크다', '위험·욕구 평가로 과정 강도를 정하고 고위험군을 우선 배정한다', '집중·심화 과정 이수자의 사후관리를 강화한다'], HEX.amber, HEX.amberBg);
  pcard(M + 3 * (cw + 0.15), 1.5, cw, 4.2, '4', '재활 규모 확대', '손익분기 효과 2.4%(현재가치 4.3%), 이수 1,545명 순편익 239.8억(90.8억)',
    ['낮은 손익분기 효과를 고려해 이수 인원을 단계적으로 늘린다', '확대와 평가를 함께 설계해 효과가 확인되는 과정부터 넓힌다', '중도탈락(3.4%) 사유를 관리한다'], HEX.red, HEX.redBg);
  RR(s, { x: M, y: 5.85, w: W - 2 * M, h: 0.62, fill: { color: HEX.navy } });
  T(s, '생애가치 B/C는 효과의 지속 기간에 가장 민감하다: 관측 효과 현재가치 B/C 3년 한정 1.04 → 5년 반감 1.93 → 평생 유지 4.78', { x: M + 0.25, y: 5.85, w: W - 2 * M - 0.5, h: 0.62, fontSize: 13.5, bold: true, color: C.background1, valign: 'middle' });
  source(s, '연구진 계산, Mitchell 외(2006), Inciardi·Martin·Butzin(2004), NIDA(2006)');
  s.addNotes('제언 1~4는 비용편익 결과에서 나온다. 효과가 오래 남을수록 B/C가 커지므로 출소 전후의 연속 처우가 편익의 크기를 정한다. 교정시설 치료에 출소 후 사후관리가 더해질 때 재범 감소가 크다는 국외 연구(Inciardi 외, 2004; Mitchell 외, 2006)와 같은 방향이다. 관측 효과가 유의하지 않은 것은 비교군이 작기 때문이므로 평가 설계가 필요하다.');
}

s = content('Ⅶ. 정책 제언', 'Ⅶ. 정책 제언 ② 지역사회 기반과 제도', '교정 이후를 받칠 지역사회 수용 능력과 법·협력 체계를 갖춘다');
{
  const cw = (W - 2 * M - 2 * 0.15) / 3;
  pcard(M, 1.5, cw, 4.2, '5', '치료 지향 보호관찰', '출소 후 감독이 치료 유지로 이어져야 효과가 남는다',
    ['출소 후 위험·욕구를 다시 평가해 감독 강도와 치료 수준을 맞춘다', '약물검사 양성은 제재에 앞서 치료 연계의 계기로 쓴다', '마약류 전담 보호관찰 인력과 교육을 늘린다'], HEX.navy, HEX.navyBg);
  pcard(M + (cw + 0.15), 1.5, cw, 4.2, '6', '지역사회 수용 능력', '연속 처우의 받침: 주거, 치료, 동료 지원',
    ['출소자가 머물며 치료를 이어 갈 중간 단계의 회복 주거를 확충한다', '치료보호 기관의 인력·병상과 진료 보상을 현실화한다', '회복 경험자의 동료 지원과 민간 단체 연계를 제도화한다'], HEX.teal, HEX.tealBg);
  pcard(M + 2 * (cw + 0.15), 1.5, cw, 4.2, '7', '법적 근거와 부처 협력', '교정·보호관찰·보건복지·지자체가 한 경로를 공유',
    ['기관 간 인계와 정보 공유의 법적 근거를 둔다', '부처 간 조정 협의체와 공동 예산·성과관리를 운영한다', '수사·재판 초기에 치료 필요를 선별해 치료 연계를 넓힌다'], HEX.amber, HEX.amberBg);
  RR(s, { x: M, y: 5.85, w: W - 2 * M, h: 0.62, fill: { color: HEX.navy } });
  T(s, '제언 1~4가 교정시설 안의 과제라면, 제언 5~7은 그 효과가 출소 뒤에도 남도록 하는 지역사회의 조건이다', { x: M + 0.25, y: 5.85, w: W - 2 * M - 0.5, h: 0.62, fontSize: 13.5, bold: true, color: C.background1, valign: 'middle' });
  source(s, '연구진 정리, NIDA(2006)');
  s.addNotes('제언 5~7은 연속 처우가 작동하기 위한 기반이다. 교정 재활의 효과가 출소 뒤에도 남으려면 보호관찰과 지역사회 치료·주거가 이를 받쳐야 한다. 치료의 연속성이 회복의 핵심이라는 점은 NIDA(2006)에서도 확인된다.');
}

// ── 향후 계획 ──
"""
i = s.index("// ════════ Ⅶ"); j = s.index("pres.addSection({ title: 'Ⅶ. 향후 계획' });")
s = s[:i] + POL + s[j + len("pres.addSection({ title: 'Ⅶ. 향후 계획' });"):]
s, k = re.subn(r"s = content\('Ⅶ\. 향후 계획', 'Ⅶ\. [^']*', '[^']*'\);",
               "s = content('Ⅶ. 정책 제언', 'Ⅶ. 향후 계획', '최종보고서 작성');", s); assert k == 1
rep("['4', '교정 재활 비용편익', 'B/C 0.22~0.28, 손익분기 10.1~13.4%p, 문헌·상한 효과 민감도'],",
    "['4', '교정 재활 비용편익', '재복역 1건 기준 B/C 0.22~0.28, 생애가치 기준 3.44~8.28(현재가치 1.93~4.63)'],")
rep("['5', '정책 제언', '재활 확대 규모, 효과 측정 체계, 사후관리 연계'],",
    "['5', '정책 제언', '제언 1~7의 실행 과제·소관·단계 구체화'],")
open(fn, 'w').write(s)
print('ok', fn)
