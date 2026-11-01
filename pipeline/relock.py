"""서식·대시보드 틀을 의도적으로 바꿀 때만 쓰는 판 올림 도구.

  python pipeline/relock.py --version 서식-v2 --reason "서식9 행 구성 변경"

data/workbook.xlsx의 현재 모양을 새 잠금 기준으로 저장하고, 잠금 파일 해시를 다시 적고,
locked/CHANGELOG.md에 이유를 남긴다. 회신값을 넣을 때는 쓰지 않는다.
"""
import argparse, datetime, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORKBOOK, FORM_LOCK, MANIFEST, LOCKED, save_json, load_json
import lock


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', required=True)
    ap.add_argument('--reason', required=True)
    a = ap.parse_args()
    old = load_json(MANIFEST).get('form_version') if MANIFEST.exists() else None
    if old == a.version:
        sys.exit(f'판 이름이 지금과 같습니다({old}). 새 이름을 쓰십시오.')
    save_json(FORM_LOCK, lock.build_form_lock(WORKBOOK))
    save_json(MANIFEST, {'form_version': a.version, 'updated': datetime.date.today().isoformat(), 'files': lock.file_hashes()})
    log = LOCKED / 'CHANGELOG.md'
    head = '' if log.exists() else '# 서식·대시보드 판 기록\n\n잠금 기준을 바꿀 때마다 한 줄씩 남습니다.\n\n'
    with log.open('a', encoding='utf-8') as f:
        f.write(head + f'- {datetime.date.today().isoformat()} · {a.version} (이전 {old or "없음"}): {a.reason}\n')
    print(f'잠금 기준을 {a.version}(으)로 바꿨습니다. CHANGELOG에 기록했습니다.')


if __name__ == '__main__':
    main()
