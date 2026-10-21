"""산식 일관성 점검(대시보드 하단 자동 점검과 같은 규칙)과 갱신 누락 경고."""
import math, re
from common import REQUEST_STATUS, COUNT_STATUS, UNIT_STATUS, TREE_STATUS

PH = re.compile(r'\{(\w+)\|(\w+)\}')


def _close(a, b):
    return all(isinstance(x, (int, float)) and math.isfinite(x) for x in (a, b)) and abs(a - b) <= max(1.0, abs(b) * 1e-3)


def run(data):
    V = {k: o.get('value') for k, o in data['values'].items()}
    g = lambda k: V.get(k, float('nan')) if V.get(k) is not None else float('nan')
    errs, warns, passed = [], [], 0

    def eq(name, got, exp):
        nonlocal passed
        if _close(got, exp):
            passed += 1
        else:
            errs.append(f'{name}: 입력 {got} / 재계산 {exp}')

    def ok(name, cond, detail=''):
        nonlocal passed
        if cond:
            passed += 1
        else:
            errs.append(f'{name}: {detail}')

    R = data['requests']
    counted = [r for r in R if r.get('counted')]
    bad = [f"{r['id']}:{r['status']}" for r in R if r['status'] not in REQUEST_STATUS]
    ok('요청 상태값이 허용 목록 안에 있음', not bad, ', '.join(bad))
    ok('집계 대상 건수 = 상태별 합계', sum(1 for r in counted if r['status'] in COUNT_STATUS) == len(counted))
    ok('회신 항목 수 ≤ 요청 항목 수', all(r.get('got', 0) <= r.get('asked', 0) for r in counted))
    ids = {u['id'] for u in data['units']}; rids = {r['id'] for r in R}
    brk = [x for f in data['flow'] for x in f['reqs'] if x not in rids] + [x for f in data['flow'] for x in f['units'] if x not in ids]
    ok('흐름도가 가리키는 요청·원단위가 모두 있음', not brk, ', '.join(brk))
    badu = [f"{u['id']}:{u['status']}" for u in data['units'] if u['status'] not in UNIT_STATUS]
    ok('원단위 상태값이 허용 목록 안에 있음', not badu, ', '.join(badu))

    eq('r0 = 미이수 재복역 ÷ 미이수 인원', g('r0'), g('e0') / g('n0'))
    eq('r1 = 이수 재복역 ÷ 이수 인원', g('r1'), g('e1') / g('n1'))
    eq('Δr = (r0 − r1) ÷ r0', g('dr'), (g('r0') - g('r1')) / g('r0'))
    eq('r0×Δr = r0 − r1', g('avoid'), g('r0') - g('r1'))
    eq('UC-07 = PG 비용풀 ÷ 이수 인시', g('uc07'), g('pgpool') / g('hours'))
    eq('UC-06 평균 = PG 비용풀 ÷ 이수 인원', g('uc06avg'), g('pgpool') / g('comp'))
    eq('ΔC = UC-06 + UC-10 + UC-12 + ΔM×UC-02', g('dc'), g('uc06avg') + g('uc10') + g('uc12') + g('dm') * g('uc02'))
    r, s3 = g('rate'), g('s3')
    eq('D = Σ hₜ/(1+r)^t', g('D'), sum(s3 / 3 / (1 + r) ** t for t in (1, 2, 3)) + sum((1 - s3) / 2 / (1 + r) ** t for t in (4, 5)))
    eq('SCᵣ = 재수용비 + 검찰 단계 비용', g('scr'), g('reinc') + g('prospc'))
    eq('재수용비 = 실형기간 × 복역비율 × UC-01', g('reinc'), g('sent') * g('served') * g('uc01y'))
    eq('B = r0×Δr × SCᵣ × D', g('B'), g('avoid') * g('scr') * g('D'))
    eq('B/C = B ÷ ΔC', g('bc'), g('B') / g('dc'))
    eq('NPV = B − ΔC', g('npv'), g('B') - g('dc'))
    eq('ROI = (B − ΔC) ÷ ΔC', g('roi'), (g('B') - g('dc')) / g('dc'))
    eq('Δr* = ΔC ÷ (r0 × SCᵣ × D)', g('drstar'), g('dc') / (g('r0') * g('scr') * g('D')))
    eq('SCᵣ* = ΔC ÷ (r0×Δr × D)', g('scrstar'), g('dc') / (g('avoid') * g('D')))
    eq('전체 증분비용 = ΔC × 이수 인원', g('totc'), g('dc') * g('comp'))
    for i in (1, 2, 3, 4):
        eq(f'민감도 {i}: B/C', g(f'sens{i}_bc'), g('r0') * g(f'sens{i}_dr') * g('scr') * g('D') / g('dc'))
    eq('민감도 기본값의 Δr = 현재 Δr', g('sens2_dr'), g('dr'))
    eq('N* = 검거 인원 × 암수율 λ', g('nstar'), g('arrest_drug') * g('lambda'))

    if 'sc_tree' in data:
        badt = []
        def walk(n):
            if not n.get('children'):
                if n.get('status') not in TREE_STATUS:
                    badt.append(f"{n['label']}:{n.get('status')}")
            for c in n.get('children', []):
                walk(c)
        walk(data['sc_tree']['root'])
        ok('사회적 비용 나무의 말단 상태값이 허용 목록 안에 있음', not badt, ', '.join(badt))

    # 문구 속 자리표시가 모두 values에 있는지
    missing = set()
    def scan(o):
        if isinstance(o, str):
            missing.update(k for k, _ in PH.findall(o) if k not in V)
        elif isinstance(o, dict):
            [scan(v) for k, v in o.items() if k != 'values']
        elif isinstance(o, list):
            [scan(v) for v in o]
    scan(data)
    ok('문구 속 {값} 자리표시가 모두 values에 있음', not missing, ', '.join(sorted(missing)))
    nulls = [k for k, v in V.items() if v is None or (isinstance(v, float) and not math.isfinite(v))]
    ok('모든 값이 계산됨(빈칸·오류 없음)', not nulls, ', '.join(nulls))

    # ── 경고: 계산은 맞지만 문구·상태를 고쳐야 할 수 있는 경우 ──
    U = {u['id']: u for u in data['units']}
    if (V.get('uc10') or 0) > 0 and U.get('UC-10', {}).get('status') == '미반영':
        warns.append('UC-10에 값이 생겼습니다. dashboard.json units의 UC-10 상태·문구(미산출)를 고치십시오.')
    if (V.get('uc12') or 0) > 0 and U.get('UC-12', {}).get('status') == '미반영':
        warns.append('UC-12에 값이 생겼습니다. dashboard.json units의 UC-12 상태·문구(미산출)를 고치십시오.')
    if V.get('oc9') == 1 and U.get('r0 · Δr', {}).get('status') == '문헌대체':
        warns.append('r0·Δr이 서식9 회신값으로 바뀌었습니다. units "r0 · Δr"와 요청 9번의 상태(문헌대체)·문구를 고치십시오.')
    for r in counted:
        if r['status'] == '미회신' and r.get('got', 0) > 0:
            warns.append(f"요청 {r['id']}: 상태는 미회신인데 회신 항목 수가 {r['got']}입니다.")
        if r['status'] == '완료' and r.get('got', 0) < r.get('asked', 0):
            warns.append(f"요청 {r['id']}: 상태는 완료인데 회신 항목이 {r['got']}/{r['asked']}입니다.")
    return passed, errs, warns
