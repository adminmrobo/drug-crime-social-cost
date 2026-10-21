"""전체 갱신을 한 번에 실행한다.

  python pipeline/run.py            잠금 점검 → 재계산 → 대시보드 생성 → 산식 점검 → dist/에 저장
  python pipeline/run.py --check    dist/를 바꾸지 않고 점검만

순서: ① 잠금 파일·서식 고정 칸 점검 ② dashboard.json으로 요청표·취합현황 칸 생성 ③ LibreOffice로 재계산
④ 값 수집과 산식 점검 ⑤ 이전 결과와 비교한 보고서 ⑥ dist/ 저장. 하나라도 실패하면 dist/는 그대로 둔다.
"""
import argparse, shutil, subprocess, sys, json, datetime
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.workbook.properties import CalcProperties

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (WORKBOOK, DASHBOARD, DIST, BUILD, CALC_SHEET, COUNT_STATUS, load_json)
import lock, checks, render

FILL = {'완료': 'FFE2EFDA', '부분': 'FFFFF2CC', '미회신': 'FFF8CBAD', '문헌대체': 'FFDDEBF7', '추가': 'FFEDEDED'}
LABEL = {'문헌대체': '문헌 대체', '추가': '추가 반영'}


def fail(title, items):
    print(f'\n✕ {title}')
    for i in items:
        print('  - ' + i)
    print('\n갱신을 멈췄습니다. dist/는 바뀌지 않았습니다.')
    sys.exit(1)


def write_generated(wb, dash):
    """dashboard.json의 요청 상태를 엑셀 1.요청표(E·G열)와 취합현황 시트에 옮긴다."""
    R = dash['requests']
    counted = [r for r in R if r.get('counted')]
    cnt = {s: sum(1 for r in counted if r['status'] == s) for s in COUNT_STATUS}
    ws = wb['1.요청표']
    ws['A2'].value = (f"총 {len(counted)}건. {dash['meta']['asof']} 기준: 완료 {cnt['완료']}, 부분 {cnt['부분']}, 미회신 {cnt['미회신']}, "
                      f"문헌 대체 {cnt['문헌대체']}. 상세는 「취합현황」 시트(자동 생성), 계산은 「원단위계산」 시트.")
    rowmap = {str(ws.cell(r, 1).value): r for r in range(5, 18)}
    for r in counted:
        rr = rowmap.get(str(r['id']))
        if not rr:
            continue
        ws.cell(rr, 5).value = r['owner']
        c = ws.cell(rr, 7); c.value = f"{LABEL.get(r['status'], r['status'])} ({r.get('pill', '')})"
        c.font = Font(name='맑은 고딕', size=9, bold=True)
        c.fill = PatternFill('solid', fgColor=FILL.get(r['status'], 'FFFFFFFF'))
    # 취합현황 시트 다시 만들기
    idx = wb.sheetnames.index('취합현황')
    del wb['취합현황']
    ws = wb.create_sheet('취합현황', idx)
    ws.sheet_view.showGridLines = False
    F = '맑은 고딕'; thin = Side(style='thin', color='FFBFBFBF'); box = Border(left=thin, right=thin, top=thin, bottom=thin)
    ws['A1'] = f"자료 요청 {len(counted)}건 취합 현황 ({dash['meta']['asof']}, {dash['meta']['version']})"; ws['A1'].font = Font(name=F, size=13, bold=True)
    ws['A2'] = ('이 시트는 data/dashboard.json에서 자동으로 만들어집니다. 여기서 고치지 말고 dashboard.json을 고치십시오. '
                f"상태: 완료 {cnt['완료']} · 부분 {cnt['부분']} · 미회신 {cnt['미회신']} · 문헌 대체 {cnt['문헌대체']}")
    ws['A2'].font = Font(name=F, size=9, color='FF595959')
    heads = ['번호', '요청 자료', '상태', '회신 항목', '회신일', '받은 내용', '빠진 내용', '모델 반영', '비고', '진행 중', '소관']
    widths = [6, 22, 10, 9, 11, 44, 36, 20, 30, 34, 20]
    for j, (h, w) in enumerate(zip(heads, widths), 1):
        c = ws.cell(4, j, h); c.font = Font(name=F, size=9, bold=True, color='FFFFFFFF'); c.fill = PatternFill('solid', fgColor='FF1F3864')
        c.border = box; c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.column_dimensions[c.column_letter].width = w
    for i, r in enumerate(R, 5):
        vals = [r['id'], r['name'] + (' ◆' if r.get('core') else ''), LABEL.get(r['status'], r['status']),
                f"{r.get('got', 0)}/{r.get('asked', 0)}" if r.get('asked') else '-', r.get('replied') or '미회신',
                r.get('received') or '-', r.get('missing') or '-', r.get('model', ''), r.get('note', ''), r.get('doing', ''), r.get('owner', '')]
        for j, v in enumerate(vals, 1):
            c = ws.cell(i, j, v); c.font = Font(name=F, size=9); c.border = box; c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.cell(i, 3).fill = PatternFill('solid', fgColor=FILL.get(r['status'], 'FFFFFFFF'))
    ws.freeze_panes = 'C5'


def recalc(src, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = ['soffice', '--headless', '--calc', '--convert-to', 'xlsx', '--outdir', str(outdir), str(src)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    out = outdir / src.name
    if not out.exists():
        fail('재계산 실패(LibreOffice)', [p.stdout[-400:], p.stderr[-400:]])
    wb = load_workbook(out, data_only=True)
    errs = [f'{c.coordinate}: {c.value}' for row in wb[CALC_SHEET].iter_rows() for c in row
            if isinstance(c.value, str) and c.value.startswith('#') and c.value.rstrip('!?0/').upper() in ('#REF', '#NAME', '#DIV', '#VALUE', '#N/A', '#NUM', '#NULL')]
    if errs:
        fail('계산 시트에 오류값이 있습니다', errs[:20])
    return out


def fmtv(v):
    if isinstance(v, float):
        return f'{v:,.4f}' if abs(v) < 10 else f'{v:,.0f}'
    return f'{v:,}' if isinstance(v, int) else str(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='dist/를 바꾸지 않고 점검만')
    a = ap.parse_args()
    print('① 잠금 점검')
    m_errs, form_ver = lock.check_manifest()
    if m_errs:
        fail('잠금 파일이 바뀌었습니다. 대시보드·서식을 바꾸려면 pipeline/relock.py로 판을 올리십시오.', m_errs)
    f_errs = lock.check_form(WORKBOOK)
    if f_errs:
        fail('서식의 고정 칸(제목·항목명·산식)이 바뀌었습니다. 회신값은 빈칸·파란 글씨·노란 칸에만 넣으십시오.', f_errs)
    print(f'   잠금 파일·서식 이상 없음 (서식 판 {form_ver})')
    dash = load_json(DASHBOARD)

    print('② 요청표·취합현황 생성')
    shutil.rmtree(BUILD, ignore_errors=True); BUILD.mkdir()
    wb = load_workbook(WORKBOOK)
    write_generated(wb, dash)
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
    formulas = BUILD / 'workbook.xlsx'
    wb.save(formulas)

    print('③ 재계산')
    calculated = recalc(formulas, BUILD / 'calc')

    print('④ 값 수집·산식 점검')
    values = render.collect_values(calculated, dash)
    data = render.build_data(values, dash)
    passed, errs, warns = checks.run(data)
    if errs:
        fail(f'점검 {len(errs)}건 불일치(산식·상태값·문구)', errs)
    print(f'   점검 {passed}건 통과, 경고 {len(warns)}건')

    print('⑤ 이전 결과와 비교')
    prev = {}
    if (DIST / 'data.json').exists():
        prev = {k: o.get('value') for k, o in load_json(DIST / 'data.json').get('values', {}).items()}
    changes = [(k, prev.get(k), o['value'], o['label']) for k, o in values.items() if prev and prev.get(k) != o['value']]
    lines = [f"# 갱신 보고 ({datetime.datetime.now():%Y-%m-%d %H:%M}, 대시보드 {dash['meta']['version']}, 서식 판 {form_ver})", '',
             f'- 산식 점검: {passed}건 통과', f'- 바뀐 값: {len(changes) if prev else "첫 실행"}', f'- 경고: {len(warns)}건', '']
    if warns:
        lines += ['## 확인할 일', *[f'- {w}' for w in warns], '']
    if changes:
        lines += ['## 바뀐 값', '| 키 | 항목 | 이전 | 현재 |', '|---|---|---:|---:|',
                  *[f'| {k} | {lab} | {fmtv(p)} | {fmtv(n)} |' for k, p, n, lab in changes], '']
    key = ['dc', 'B', 'bc', 'drstar', 'scrstar', 'r0', 'dr', 'uc10', 'uc12']
    lines += ['## 핵심 값', '| 키 | 항목 | 값 |', '|---|---|---:|', *[f"| {k} | {values[k]['label']} | {fmtv(values[k]['value'])} |" for k in key]]
    report = '\n'.join(lines) + '\n'
    print(report)
    if a.check:
        print('점검만 실행했습니다(--check). dist/는 그대로입니다.')
        return
    print('⑥ dist/ 저장')
    DIST.mkdir(exist_ok=True)
    render.write_page(data, DIST)
    shutil.copy(formulas, DIST / 'workbook.xlsx')
    (DIST / 'report.md').write_text(report, encoding='utf-8')
    print('   dist/index.html · data.json · guide.html · workbook.xlsx · report.md')


if __name__ == '__main__':
    main()
