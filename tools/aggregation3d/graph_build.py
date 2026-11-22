"""Build the cost-flow graph (raw data -> stages -> final indicators) from the
2025 aggregate workbook, and run omission / gap / duplicate / reconciliation checks.
Usage: python3 -I graph_build.py <xlsx> <out.json>"""
import sys, json, re
import openpyxl

xlsx, out = sys.argv[1], sys.argv[2]
wf = openpyxl.load_workbook(xlsx, data_only=False)
wv = openpyxl.load_workbook(xlsx, data_only=True)
S0, S1, S2, S3, S4, S6, S7 = ('0.총괄_2025', '1.입력값', '2.사회적 혼란·기타', '3.암수율 적용',
                               '4.1인당 생애비용(별지 2)', '6.교정 재활 비용편익', '7.생애가치 비용편익')
def v(sh, c): return wv[sh][c].value
def f(sh, c): return wf[sh][c].value

N = v(S1, 'C2')
nodes, edges = [], []
def node(id, label, stage, cl, value, unit, src, cell=None, note='', flags=None):
    nodes.append(dict(id=id, label=label, stage=stage, cl=cl, value=value, unit=unit, src=src,
                      cell=cell, note=note, flags=flags or []))
def edge(a, b, kind='link', note=''):
    edges.append(dict(s=a, t=b, kind=kind, note=note))

# ---------------- 공통
node('n_arrest', '검거 사범 2025', 0, '공통', N, '명', '실측', f"{S1}!C2", '대검찰청(2026)')
node('n_l10', '암수율 기본', 0, '공통', v(S1, 'C3'), '배', '가정', f"{S1}!C3", '박성수(2018)과 같은 10배')
node('n_l28', '암수율 민감도', 0, '공통', v(S1, 'C4'), '배', '가정', f"{S1}!C4", '박성수·백민석(2019)')
node('n_cpi', '물가 계수 2025/2024', 0, '공통', v(S1, 'C5'), '배', '실측', f"{S1}!C5", '통계청 소비자물가')

# ---------------- 형사사법
cj = [('police', '경찰', 6, 2, '세출결산', '전체 검거', '마약류 검거', '실측'),
      ('pros', '검찰', 9, 3, '총예산(2024)', '전체 처리(2024)', '마약류(2024)', '2024 대용'),
      ('court', '법원', 12, 4, '형사소송 예산', '형사공판 처리', '마약류 인원', '실측'),
      ('prison', '교도소', 15, 5, '세출결산', '전체 수용(12. 31.)', '마약류 수용(12. 31.)', '실측'),
      ('hosp', '국립법무병원', 18, 6, '세출결산', '전체 인원', '마약류 인원', '실측'),
      ('prob', '보호관찰소', 21, 7, '세출결산', '총 접수', '마약류 접수', '실측')]
for key, name, r, r0, l1, l2, l3, src in cj:
    node(f'{key}_b', f'{name} {l1}', 0, '형사사법', v(S1, f'C{r}'), '원', src, f"{S1}!C{r}")
    node(f'{key}_t', f'{name} {l2}', 0, '형사사법', v(S1, f'C{r+1}'), '명', src, f"{S1}!C{r+1}")
    node(f'{key}_d', f'{name} {l3}', 0, '형사사법', v(S1, f'C{r+2}'), '명', src, f"{S1}!C{r+2}")
    node(f'{key}_ratio', f'{name} 마약류 배분비율', 1, '형사사법', v(S1, f'C{r+2}') / v(S1, f'C{r+1}'), '비율', '계산',
         note=f'{l3} ÷ {l2}')
    edge(f'{key}_t', f'{key}_ratio'); edge(f'{key}_d', f'{key}_ratio')
    node(f'{key}', name, 2, '형사사법', v(S0, f'E{r0}'), '원', '계산', f"{S0}!E{r0}", f(S0, f'E{r0}'))
    edge(f'{key}_b', key); edge(f'{key}_ratio', key)
node('pros_b25', '검찰 2025 결산(미사용)', 0, '형사사법', 1287948927480, '원', '실측', f"{S1}!F9 주석",
     '2025 처리 인원이 없어 2024 예산·인원을 대신 사용', ['ref'])
node('f_cj', '형사사법 소계', 3, '형사사법', v(S0, 'E20'), '원', '계산', f"{S0}!E20")
for key, *_ in cj: edge(key, 'f_cj')

# ---------------- 고통비용
node('tx_n', '치료보호 인원 2025', 0, '고통비용', v(S1, 'C24'), '명', '실측', f"{S1}!C24")
node('pgs_add_u', '중독자 PGS 원단위(2024)', 0, '고통비용', v(S1, 'C25'), '원', '추정·문헌', f"{S1}!C25",
     '중상 PGS 2.2억 원 × 50%(연구진 가정)')
node('death_n', '약물중독 사망자(20~64세)', 0, '고통비용', v(S1, 'C26'), '명', '실측', f"{S1}!C26")
node('pgs_d_u', '사망 PGS 원단위(2024)', 0, '고통비용', v(S1, 'C27'), '원', '추정·문헌', f"{S1}!C27",
     '한국교통연구원(2025) 교통사고 원단위 준용')
node('pgs_add_u25', '중독자 PGS 원단위 × 물가', 1, '고통비용', v(S1, 'C25') * v(S1, 'C5'), '원', '계산')
node('pgs_d_u25', '사망 PGS 원단위 × 물가', 1, '고통비용', v(S1, 'C27') * v(S1, 'C5'), '원', '계산')
edge('pgs_add_u', 'pgs_add_u25'); edge('n_cpi', 'pgs_add_u25'); edge('pgs_d_u', 'pgs_d_u25'); edge('n_cpi', 'pgs_d_u25')
node('pgs_add', '중독자 PGS', 2, '고통비용', v(S0, 'E8'), '원', '계산', f"{S0}!E8")
node('pgs_d', '사망 PGS', 2, '고통비용', v(S0, 'E9'), '원', '계산', f"{S0}!E9")
edge('tx_n', 'pgs_add'); edge('pgs_add_u25', 'pgs_add'); edge('death_n', 'pgs_d'); edge('pgs_d_u25', 'pgs_d')
node('f_pgs', '고통비용 소계', 3, '고통비용', v(S0, 'E21'), '원', '계산', f"{S0}!E21")
edge('pgs_add', 'f_pgs'); edge('pgs_d', 'f_pgs')

# ---------------- 생산성 (입력 자체가 연구진 추계 총액)
for key, name, r, r0 in [('early', '조기사망', 28, 10), ('morb', '이환·입원', 29, 11), ('unemp', '노동력 상실·미취업', 30, 12)]:
    node(f'{key}_in', f'{name} 손실(연구진 추계)', 0, '생산성', v(S1, f'C{r}'), '원', '엑셀 밖 근거', f"{S1}!C{r}",
         '세부 산식(임금·취업률·손실일수)은 별도 추계 파일에 있음', ['nobase'])
    node(key, name, 2, '생산성', v(S0, f'E{r0}'), '원', '계산', f"{S0}!E{r0}")
    edge(f'{key}_in', key)
node('f_prod', '생산성 소계', 3, '생산성', v(S0, 'E22'), '원', '계산', f"{S0}!E22")
for k in ['early', 'morb', 'unemp']: edge(k, 'f_prod')

# ---------------- 의료·복지
node('claim', '청구 진료비', 0, '의료·복지', v(S1, 'C31'), '원', '실측', f"{S1}!C31")
node('tx_budget', '치료보호 지원 예산', 0, '의료·복지', v(S1, 'C32'), '원', '실측', f"{S1}!C32")
node('ind_rate', '간접의료비 비율', 0, '의료·복지', v(S1, 'C33'), '비율', '추정·문헌', f"{S1}!C33", '박성수(2018) 38.1%')
node('mh_in', '정신건강·복지 지원(연구진 추계)', 0, '의료·복지', v(S1, 'C34'), '원', '엑셀 밖 근거', f"{S1}!C34",
     '세부 내역은 별도 추계 파일', ['nobase'])
node('dmed', '직접 의료비', 2, '의료·복지', v(S0, 'E13'), '원', '계산', f"{S0}!E13")
node('imed', '간접의료비', 2, '의료·복지', v(S0, 'E14'), '원', '계산', f"{S0}!E14")
node('mh', '정신건강·복지', 2, '의료·복지', v(S0, 'E15'), '원', '계산', f"{S0}!E15")
edge('claim', 'dmed'); edge('tx_budget', 'dmed'); edge('dmed', 'imed'); edge('ind_rate', 'imed'); edge('mh_in', 'mh')
node('f_med', '의료·복지 소계', 3, '의료·복지', v(S0, 'E23'), '원', '계산', f"{S0}!E23")
for k in ['dmed', 'imed', 'mh']: edge(k, 'f_med')

# ---------------- 사회적 혼란·기타 (시트 2: 수식 안 숫자)
H = 'hard'  # 수식 안에 직접 적힌 숫자
node('as_n', '상해 연평균 인원(2021~2024)', 0, '사회적 혼란·기타', 323, '명', '2024 대용', f"{S2}!F2 수식 안",
     '(40,679 − 39,387) ÷ 4. 입력값 시트에 없음', [H])
node('sx_n', '성폭력 연평균 인원(2021~2024)', 0, '사회적 혼란·기타', 477.25, '명', '2024 대용', f"{S2}!F3 수식 안",
     '(23,613 − 21,704) ÷ 4. 입력값 시트에 없음', [H])
node('attr', '마약 상태 귀속 비율', 0, '사회적 혼란·기타', 0.25, '비율', '가정', f"{S2}!F2·F3 수식 안", '연구진 가정', [H])
node('as_u', '상해 1건당 단가(2008)', 0, '사회적 혼란·기타', 22066382, '원', '추정·문헌', f"{S2}!F2 수식 안", '박경래 외(2010)', [H])
node('sx_u', '성폭력 1건당 단가(2008)', 0, '사회적 혼란·기타', 0.2 * 217208694 + 0.8 * 9429124, '원', '추정·문헌',
     f"{S2}!F3 수식 안", '강간 20% × 2.17억 + 추행 80% × 943만 원', [H])
node('cpi08', '물가 환산 2008→2025', 0, '사회적 혼란·기타', 114.2 * 1.021 / 81.5, '배', '실측', f"{S2} 수식 안",
     '114.2 × 1.021 ÷ 81.5. 물가 계수 1.021이 입력값 시트와 연결되지 않음', [H])
node('as', '2차 범죄: 상해', 1, '사회적 혼란·기타', v(S2, 'F2'), '원', '계산', f"{S2}!F2")
node('sx', '2차 범죄: 성폭력', 1, '사회적 혼란·기타', v(S2, 'F3'), '원', '계산', f"{S2}!F3")
for a in ['as_n', 'attr', 'as_u', 'cpi08']: edge(a, 'as', 'copy' if a != 'as' else 'link')
for a in ['sx_n', 'attr', 'sx_u', 'cpi08']: edge(a, 'sx', 'copy')
node('crime2', '2차 범죄 피해', 2, '사회적 혼란·기타', v(S0, 'E16'), '원', '계산', f"{S0}!E16")
edge('as', 'crime2'); edge('sx', 'crime2')
node('murder', '마약 상태 살인(합계 제외)', 1, '사회적 혼란·기타', v(S2, 'F9'), '원', '추정·문헌', f"{S2}!F9",
     '연 65명 × 25% × 173.2억 원. 합계에서 제외', ['ref'])
node('mfds', '식약처 마약류 예산(2024)', 0, '사회적 혼란·기타', 37700000000, '원', '2024 대용', f"{S2}!F4 수식 안",
     '2025 예산 미확인', [H])
node('prev', '예방·홍보·재활 예산', 2, '사회적 혼란·기타', v(S0, 'E17'), '원', '계산', f"{S0}!E17",
     '377억 − 17억. 17억이 입력값 C34와 연결되지 않음')
edge('mfds', 'prev', 'copy'); edge('mh_in', 'prev', 'copy', '중복 제거를 위해 차감(−17억 원)')
node('fam_k', '동거 가족 수(0.64명)', 0, '사회적 혼란·기타', 140593 / 220043, '명', '추정·문헌', f"{S2}!F5 수식 안",
     '140,593 ÷ 220,043', [H])
node('fam_u', '가족 1인당 의료비 £450(2008)', 0, '사회적 혼란·기타', 450, '파운드', '추정·문헌', f"{S2}!F5 수식 안",
     'Copello, Templeton & Powell(2010). 환율·물가 환산 × 1.27 × 847.5 ÷ 0.689 × 1.166', [H])
node('family', '가족 돌봄', 2, '사회적 혼란·기타', v(S0, 'E18'), '원', '계산', f"{S0}!E18",
     '치료보호 1,649명을 수식에 직접 적음(입력값 C24와 연결 없음)')
edge('tx_n', 'family', 'copy'); edge('fam_k', 'family', 'copy'); edge('fam_u', 'family', 'copy')
node('dui_n', '마약류 운전 사고 2025', 0, '사회적 혼란·기타', 33, '건', '실측', f"{S2}!F6 수식 안", '경찰청(2026)', [H])
node('dui_u', '교통사고 1건당 평균 비용(2023)', 0, '사회적 혼란·기타', 54059500000000 / 1252433, '원', '추정·문헌',
     f"{S2}!F6 수식 안", '한국교통연구원(2025): 54조 595억 원 ÷ 1,252,433건', [H])
node('dui', '약물 운전 교통사고', 2, '사회적 혼란·기타', v(S0, 'E19'), '원', '계산', f"{S0}!E19")
edge('dui_n', 'dui', 'copy'); edge('dui_u', 'dui', 'copy')
node('fear', '범죄 공포·방어 행동', 2, '사회적 혼란·기타', 0, '원', '가정', f"{S2}!F7",
     '범죄 1건당 단가에 포함되어 0원(박경래 외, 2010; Cohen et al., 2004)')
node('f_soc', '사회적 혼란·기타 소계', 3, '사회적 혼란·기타', v(S0, 'E24'), '원', '계산', f"{S0}!E24")
for k in ['crime2', 'prev', 'family', 'dui', 'fear']: edge(k, 'f_soc')

# ---------------- 총액·1명당·암수율
node('total', '사회적 비용(암수율 미반영)', 4, '총괄', v(S0, 'E25'), '원', '계산', f"{S0}!E25")
for k in ['f_cj', 'f_pgs', 'f_prod', 'f_med', 'f_soc']: edge(k, 'total')
node('per', '검거 사범 1명당 비용', 4, '총괄', v(S0, 'G25') * 1e4, '원', '계산', f"{S0}!G25")
edge('total', 'per'); edge('n_arrest', 'per')
node('lam10', '사회적 비용(암수율 10배)', 5, '총괄', v(S0, 'H25') * 1e8, '원', '계산', f"{S0}!H25")
node('lam28', '사회적 비용(암수율 28.57배)', 5, '총괄', v(S0, 'I25') * 1e8, '원', '계산', f"{S0}!I25")
edge('per', 'lam10'); edge('n_arrest', 'lam10'); edge('n_l10', 'lam10')
edge('per', 'lam28'); edge('n_arrest', 'lam28'); edge('n_l28', 'lam28')

# ---------------- 생애비용 (시트 4: 값만 있고 수식 없음)
for key, label, row, unit in [('lp_dur', '잔여 중독기간 중앙값(B)', 2, '년'), ('lp_lab', '노동능력 상실 비율(B)', 3, '비율'),
                              ('lp_mort', '초과 사망률(활동, B)', 5, '비율'), ('lp_rearr', '연 재검거 확률(B)', 7, '비율')]:
    node(key, label, 0, '생애비용', v(S4, f'D{row}'), unit, '가정' if 'rearr' in key else '추정·문헌', f"{S4}!D{row}",
         v(S4, f'F{row}') or '')
node('lp_life', '생명표 기대여명(Gompertz)', 0, '생애비용', v(S4, 'C24'), '년', '실측', f"{S4}!C24",
     '통계청(2025. 12. 3.) 2024년 생명표. 보도 자료에서 옮김', [])
node('l_first', '1년차 비용', 1, '생애비용', v(S4, 'D8'), '원', '계산', f"{S4}!D8", '값만 적힘(수식 없음). 2차 범죄 하한 45.0억 원 기준')
node('l_rep', '반복 비용(활동 중독 1년)', 1, '생애비용', v(S4, 'D9'), '원', '계산', f"{S4}!D9", '값만 적힘. 2차 범죄 전체 112.5억 원 기준')
node('l_rearr', '재검거 1회 형사사법', 1, '생애비용', v(S4, 'D10'), '원', '계산', f"{S4}!D10", '값만 적힘. 형사사법 1명당과 같음')
node('l_dpgs', '사망 PGS(2025)', 1, '생애비용', v(S4, 'D11'), '원', '계산', f"{S4}!D11", '값만 적힘')
edge('per', 'l_first', 'copy'); edge('crime2', 'l_first', 'copy', '하한 45.0억 원으로 바꿔 적용')
for k in ['pgs_add', 'dmed', 'imed', 'mh', 'morb', 'crime2', 'family', 'dui']: edge(k, 'l_rep', 'copy')
edge('f_cj', 'l_rearr', 'copy'); edge('pgs_d_u25', 'l_dpgs', 'copy')
node('life_pv', '생애비용 B(현재가치 4.5%)', 4, '생애비용', v(S4, 'D15'), '원', '엑셀 밖 근거', f"{S4}!D15",
     '연령별·연도별 모형 계산은 엑셀 밖에서 하고 결과만 적음', ['nobase'])
node('life_cum', '생애비용 B(누적 기준)', 5, '생애비용', v(S4, 'D17'), '원', '엑셀 밖 근거', f"{S4}!D17",
     '대표값. 연간 사회적 비용과 더하지 않음', ['nobase'])
for k in ['l_first', 'l_rep', 'l_rearr', 'l_dpgs', 'lp_dur', 'lp_lab', 'lp_mort', 'lp_rearr', 'lp_life']:
    edge(k, 'life_pv', 'model')
edge('life_pv', 'life_cum', 'model')

# ---------------- 교정 재활 비용편익 (시트 6)
node('r_budget', '재활 예산 + 전담인력 인건비', 0, '재활 비용편익', v(S6, 'C23'), '원', '엑셀 밖 근거', f"{S6}!C23",
     '59.99억(집행액 간주) + 16.98억(정원 × 봉급표 × 1.6 × 투입비율 추정). 합계만 값으로 적음', ['nobase'])
node('r_comp', '2025 이수 인원', 0, '재활 비용편익', 1545, '명', '실측', f"{S6}!C24 수식 안", '교정본부 자료(2026. 11.)', [H])
node('r_out_cost', '중독 외래 진료비·인원', 0, '재활 비용편익', 979000000, '원', '추계치', f"{S6}!C33 수식 안",
     '9.79억 원 ÷ 1,835명. 의료·복지 추계값을 옮겨 적음', [H])
node('uc06', 'UC-06 프로그램 원가', 1, '재활 비용편익', v(S6, 'C23') / 1545, '원', '계산', f"{S6}!C24 일부")
node('uc10', 'UC-10 치료개입', 1, '재활 비용편익', v(S6, 'C33'), '원', '계산', f"{S6}!C33")
node('uc12', 'UC-12 사후관리', 1, '재활 비용편익', v(S6, 'C34'), '원', '계산', f"{S6}!C34",
     '14.4억 원 ÷ 1,649명 ÷ 1.045. 입력값 C24·C32와 연결 없음')
edge('r_budget', 'uc06'); edge('r_comp', 'uc06', 'copy'); edge('r_out_cost', 'uc10', 'copy')
edge('tx_budget', 'uc12', 'copy'); edge('tx_n', 'uc12', 'copy')
node('dC', 'ΔC 증분비용(이수자 1인)', 2, '재활 비용편익', v(S6, 'C24'), '원', '계산', f"{S6}!C24")
for k in ['uc06', 'uc10', 'uc12']: edge(k, 'dC')
node('c_n1', '이수 출소·재복역(2019~2022)', 0, '재활 비용편익', v(S6, 'C14'), '명', '실측', f"{S6}!C14·C15", '2,126명 중 672명')
node('c_n0', '미이수·탈락 출소·재복역', 0, '재활 비용편익', v(S6, 'C16'), '명', '실측', f"{S6}!C16·C17", '116명 중 40명')
node('c_all', '전체 출소·재복역(2019~2022)', 0, '재활 비용편익', v(S6, 'C10'), '명', '실측', f"{S6}!C10·C11",
     '5,977명 중 1,855명(31.0%). 현황 서술용, 계산에 쓰이지 않음', ['ref'])
node('c_stock', '연말 기결·미결(2024·2025)', 0, '재활 비용편익', v(S6, 'C3'), '명', '실측', f"{S6}!C2·C3·C4",
     '기결 3,477·4,188명, 미결 3,241명. 교도소 기결·미결 배분과 현황 서술용', ['ref'])
node('r1', 'r1 이수 재복역률', 1, '재활 비용편익', v(S6, 'C18'), '비율', '계산', f"{S6}!C18")
node('r0', 'r0 미이수·탈락 재복역률', 1, '재활 비용편익', v(S6, 'C19'), '비율', '계산', f"{S6}!C19")
edge('c_n1', 'r1'); edge('c_n0', 'r0')
node('dr', '재복역률 차 r0 − r1', 2, '재활 비용편익', v(S6, 'C20'), '비율', '계산', f"{S6}!C20", '95% CI −6.0~+11.7%p, 유의하지 않음')
edge('r1', 'dr'); edge('r0', 'dr')
node('D', '할인계수 D(3년 시점 분포)', 1, '재활 비용편익', v(S6, 'C13'), '계수', '엑셀 밖 근거', f"{S6}!C13",
     '1년 내 37.8%, 1~2년 43.1%, 2~3년 19.1%로 계산한 값만 적음', ['nobase'])
node('scr_in', '평균 실형·복역 비율·UC-01·검찰 단계', 0, '재활 비용편익', 50357000, '원', '엑셀 밖 근거', f"{S6}!C25",
     '2.45년 × 85% × 2,378.4만 원 + 86.6만 원. 근거 셀 없이 결과만 적음(곱하면 5,039.6만 원)', ['nobase'])
node('scr_lo', 'SCᵣ 하한(형사사법분)', 2, '재활 비용편익', v(S6, 'C25'), '원', '계산', f"{S6}!C25")
edge('scr_in', 'scr_lo', 'copy')
node('scr_hi', 'SCᵣ 확장', 2, '재활 비용편익', v(S6, 'C26'), '원', '계산', f"{S6}!C26",
     '(3,223.6 − 1,593.0)만 원을 수식에 직접 적음. 총괄 시트와 연결 없음')
edge('scr_lo', 'scr_hi'); edge('per', 'scr_hi', 'copy'); edge('f_cj', 'scr_hi', 'copy', '형사사법 1명당을 빼서 중복 방지')
node('B_lo', '편익 B 하한(재복역)', 3, '재활 비용편익', v(S6, 'C27'), '원', '계산', f"{S6}!C27")
node('B_hi', '편익 B 확장(재복역)', 3, '재활 비용편익', v(S6, 'C28'), '원', '계산', f"{S6}!C28")
for t, s in [('B_lo', 'scr_lo'), ('B_hi', 'scr_hi')]:
    edge('dr', t); edge(s, t); edge('D', t)
node('bc_lo', 'B/C 재복역 하한', 4, '재활 비용편익', v(S6, 'C29'), '배', '계산', f"{S6}!C29")
node('bc_hi', 'B/C 재복역 확장', 4, '재활 비용편익', v(S6, 'C30'), '배', '계산', f"{S6}!C30")
edge('B_lo', 'bc_lo'); edge('dC', 'bc_lo'); edge('B_hi', 'bc_hi'); edge('dC', 'bc_hi')

# ---------------- 생애가치 비용편익 (시트 7)
node('e_obs', '재활 효과 e(관측)', 1, '재활 비용편익', v(S7, 'C3'), '비율', '계산', f"{S7}!C3",
     '값만 적음(2.87%p ÷ 34.5%). 시트 6 재복역률 차와 연결 없음')
node('e_lit', '재활 효과 e(국내·국외 문헌)', 0, '재활 비용편익', v(S7, 'D3'), '비율', '추정·문헌', f"{S7}!D3·E3",
     '김도균·나종민(2025) 19.2%, Mitchell 외(2006) 20%')
edge('dr', 'e_obs', 'copy'); edge('r0', 'e_obs', 'copy')
node('dC7', 'ΔC(시트 7)', 2, '재활 비용편익', v(S7, 'C2'), '원', '계산', f"{S7}!C2", '6,351,000원을 값으로 적음(시트 6은 6,351,044원)')
edge('dC', 'dC7', 'copy')
node('sigma', 'Σ w(t)·C(t)(현재가치, 5년 반감)', 3, '생애비용', v(S7, 'C24'), '원', '엑셀 밖 근거', f"{S7}!C24",
     'B 시나리오 1년차 이후 생애비용 × 효과 지속. 결과만 적음', ['nobase'])
edge('life_pv', 'sigma', 'model')
node('bl', '생애가치 편익 B(관측)', 4, '재활 비용편익', v(S7, 'C25'), '원', '계산', f"{S7}!C25")
edge('e_obs', 'bl'); edge('sigma', 'bl')
node('bc_life', 'B/C 생애가치(대표값)', 5, '재활 비용편익', v(S7, 'C26'), '배', '계산', f"{S7}!C26", '관측 효과, 현재가치 4.5%, 5년 반감')
edge('bl', 'bc_life'); edge('dC7', 'bc_life')
node('bc_life_lit', 'B/C 생애가치(문헌 효과)', 5, '재활 비용편익', v(S7, 'D26'), '배', '계산', f"{S7}!D26·E26", '국내 4.44, 국외 4.63')
edge('e_lit', 'bc_life_lit'); edge('sigma', 'bc_life_lit'); edge('dC7', 'bc_life_lit')
node('cohort', '2025 이수 1,545명 순편익(현재가치)', 5, '재활 비용편익', v(S7, 'C69') * 1e8, '원', '계산', f"{S7}!C69")
edge('bl', 'cohort'); edge('dC7', 'cohort'); edge('r_comp', 'cohort', 'copy')

# ================= checks
ids = {n['id']: n for n in nodes}
out_deg = {n['id']: 0 for n in nodes}; in_deg = {n['id']: 0 for n in nodes}
for e in edges:
    assert e['s'] in ids and e['t'] in ids, e
    out_deg[e['s']] += 1; in_deg[e['t']] += 1
checks = []
def chk(kind, level, node_ids, title, detail):
    checks.append(dict(kind=kind, level=level, nodes=node_ids, title=title, detail=detail))
    for i in node_ids:
        tag = {'누락': 'orphan', '공백': 'nobase', '중복': 'shared', '대사': 'mismatch', '연결': 'hard'}[kind]
        if tag not in ids[i]['flags']: ids[i]['flags'].append(tag)

# 1) 누락: 아래 단계 노드인데 위로 이어지지 않음
final = {'lam10', 'lam28', 'life_cum', 'bc_life', 'bc_life_lit', 'cohort', 'bc_lo', 'bc_hi'}
for n in nodes:
    if out_deg[n['id']] == 0 and n['id'] not in final:
        ref = 'ref' in n['flags']
        chk('누락', '참고' if ref else '확인', [n['id']], f"{n['label']}: 위 단계로 이어지지 않음",
            n['note'] or '계산에 쓰이지 않는 원자료')
# 2) 공백: 엑셀 안에 근거 셀 없이 결과값만 적힌 항목
for n in nodes:
    if n['src'] == '엑셀 밖 근거':
        chk('공백', '확인', [n['id']], f"{n['label']}: 엑셀에 근거 셀 없음", n['note'])
# 3) 중복: 같은 원자료가 연간 사회적 비용 합계 안에서 두 항목 이상으로 들어감
succ = {}
for e in edges: succ.setdefault(e['s'], []).append(e['t'])
sc_items = {'police', 'pros', 'court', 'prison', 'hosp', 'prob', 'pgs_add', 'pgs_d', 'early', 'morb', 'unemp',
            'dmed', 'imed', 'mh', 'crime2', 'prev', 'family', 'dui', 'fear'}
def reach(n, seen=None):
    seen = seen or set()
    for t in succ.get(n, []):
        if t not in seen:
            seen.add(t); reach(t, seen)
    return seen
dup_notes = {
    'tx_n': '중독자 PGS(본인·가족의 고통)와 가족 돌봄(가족 의료비)에 같은 인원을 씀. 비용 성격이 달라 중복은 아니나, 가족 고통과 가족 의료비의 경계를 보고서에 명시',
    'mh_in': '의료·복지에 +17억 원, 예방 예산에서 −17억 원. 중복을 없애기 위한 처리(합계에는 한 번만 들어감)',
    'claim': '직접 의료비와 그 38.1%인 간접의료비로 이어짐. 비율 방식이라 중복 아님',
    'tx_budget': '직접 의료비와 그 38.1%인 간접의료비로 이어짐. 비율 방식이라 중복 아님',
    'dmed': '간접의료비가 직접 의료비의 38.1%로 산정됨. 비율 방식이라 중복 아님',
    'n_cpi': '여러 항목의 물가 환산에 쓰이는 공통 계수',
    'attr': '상해·성폭력에 같은 귀속 비율을 적용', 'cpi08': '상해·성폭력에 같은 물가 환산을 적용',
}
for n in nodes:
    if n['stage'] >= 2: continue
    hit = reach(n['id']) & sc_items
    if len(hit) >= 2:
        lv = '확인' if n['id'] == 'tx_n' else '참고'
        chk('중복', lv, [n['id']], f"{n['label']}: 연간 합계 안 {len(hit)}개 항목으로 들어감({', '.join(sorted(ids[h]['label'] for h in hit))})",
            dup_notes.get(n['id'], '같은 합계 안에서 두 번 더해지는지 확인'))
shared = [n['label'] for n in nodes if n['id'] in ('per', 'f_cj', 'crime2', 'tx_budget', 'tx_n')]
chk_note = ('연간 사회적 비용의 값이 생애비용·재활 비용편익의 원단위로도 쓰임(' + ', '.join(shared) +
            '). 세 결과는 기준이 달라 서로 더하지 않으므로 중복 계상이 아님')
checks.append(dict(kind='중복', level='참고', nodes=[], title='분석 간 공유 원단위', detail=chk_note))
# 4) 대사: 합계와 값 옮김 검산
item_sum = sum(ids[k]['value'] for k in ['police', 'pros', 'court', 'prison', 'hosp', 'prob', 'pgs_add', 'pgs_d', 'early',
                                          'morb', 'unemp', 'dmed', 'imed', 'mh', 'crime2', 'prev', 'family', 'dui', 'fear'])
sub_sum = sum(ids[k]['value'] for k in ['f_cj', 'f_pgs', 'f_prod', 'f_med', 'f_soc'])
recon = [
    ('18개 항목 합 = 총액', item_sum, ids['total']['value']),
    ('5개 분야 소계 합 = 총액', sub_sum, ids['total']['value']),
    ('시트 2 합계 = 사회적 혼란·기타 소계', v(S2, 'F8'), ids['f_soc']['value']),
    ('1명당 × 234,030명 = 암수율 10배 총액', ids['per']['value'] * N * 10, ids['lam10']['value']),
    ('시트 3 합계 = 총괄 합계(억 원)', v(S3, 'C20') * 1e8 if v(S3, 'C20') else None, ids['total']['value']),
]
first_calc = (ids['total']['value'] - ids['crime2']['value'] + 4.5e9) / N
rep_calc = sum(ids[k]['value'] for k in ['pgs_add', 'dmed', 'imed', 'mh', 'morb', 'crime2', 'family', 'dui']) / N
copies = [
    ('dC7', 'ΔC: 시트 7 값 vs 시트 6 수식', ids['dC7']['value'], ids['dC']['value']),
    ('e_obs', '관측 효과 e: 값 vs 재복역률 차 ÷ r0', ids['e_obs']['value'], ids['dr']['value'] / ids['r0']['value']),
    ('scr_hi', 'SCᵣ 확장: 수식 안 3,223.6 − 1,593.0 vs 총괄 시트 값', ids['scr_hi']['value'],
     ids['scr_lo']['value'] + ids['per']['value'] - ids['f_cj']['value'] / N),
    ('scr_lo', 'SCᵣ 하한: 적힌 값 vs 2.45 × 0.85 × 2,378.4만 + 86.6만', ids['scr_lo']['value'], 2.45 * 0.85 * 23784000 + 866000),
    ('l_first', '생애 1년차: 적힌 값 vs 1명당(2차 범죄 45.0억 원)', ids['l_first']['value'], first_calc),
    ('l_rep', '생애 반복 비용: 적힌 값 vs 항목 1명당 합', ids['l_rep']['value'], rep_calc),
    ('l_rearr', '재검거 1회: 적힌 값 vs 형사사법 1명당', ids['l_rearr']['value'], ids['f_cj']['value'] / N),
]
recon_rows = []
for t, a, b in recon:
    if a is None: continue
    recon_rows.append(dict(title=t, a=a, b=b, diff=a - b, ok=abs(a - b) <= max(1, abs(b) * 1e-9)))
for nid, t, a, b in copies:
    d = a - b; rel = abs(d) / abs(b) if b else 0
    ok = rel < 1e-9
    recon_rows.append(dict(title=t, a=a, b=b, diff=d, ok=ok, rel=rel))
    if not ok:
        chk('대사', '확인' if rel > 1e-4 else '참고', [nid], t, f"차이 {d:,.4g} ({rel*100:.3f}%)")
# 기준 불일치(별도)
chk('대사', '확인', ['l_first', 'l_rep'], '생애 1년차와 반복 비용의 2차 범죄 기준이 다름',
    f"1년차는 하한 45.0억 원, 반복 비용은 전체 112.5억 원 기준. 하한으로 맞추면 반복 비용 {rep_calc - (ids['crime2']['value'] - 4.5e9) / N:,.0f}원(−3.2%)")
# 5) 연결 끊김: 수식 안에 직접 적은 숫자(입력값 시트에 있는 값과 같은 것 포함)
hard_dup = [('family', '치료보호 1,649명', '입력값 C24'), ('uc12', '치료보호 1,649명·예산 14.4억 원', '입력값 C24·C32'),
            ('prev', '정신건강·복지 17억 원', '입력값 C34'), ('cpi08', '물가 계수 1.021', '입력값 C5')]
for nid, what, where in hard_dup:
    chk('연결', '확인', [nid], f"{ids[nid]['label']}: {what}을 수식에 직접 적음",
        f"{where}을 바꿔도 이 값은 바뀌지 않음. 셀 참조로 바꾸면 누락·불일치를 막을 수 있음")
n_hard = sum(1 for n in nodes if 'hard' in n['flags'])

summary = dict(nodes=len(nodes), edges=len(edges), raw=sum(1 for n in nodes if n['stage'] == 0),
               kinds={k: sum(1 for c in checks if c['kind'] == k) for k in ['누락', '공백', '중복', '대사', '연결']},
               hard_nodes=n_hard, recon=recon_rows)
json.dump(dict(nodes=nodes, edges=edges, checks=checks, summary=summary), open(out, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1, default=str))
for c in checks: print(c['kind'], c['level'], c['title'])
