"""파이프라인 공통 설정. 잠금 대상 파일입니다(locked/manifest.json에 해시가 기록됨)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
LOCKED = ROOT / 'locked'
CONFIG = ROOT / 'config'
DIST = ROOT / 'dist'
BUILD = ROOT / 'build'

WORKBOOK = DATA / 'workbook.xlsx'          # 입력: 서식 엑셀
DASHBOARD = DATA / 'dashboard.json'        # 입력: 상태·문구
TEMPLATE = LOCKED / 'index.template.html'  # 잠금: 대시보드 틀
GUIDE = LOCKED / 'guide.html'              # 잠금: 입력 가이드
FORM_LOCK = LOCKED / 'form_lock.json'      # 잠금: 서식의 고정 칸 목록
MANIFEST = LOCKED / 'manifest.json'        # 잠금 파일 해시
VALUES_MAP = CONFIG / 'values_map.json'    # 잠금: 값 키 → 셀

CALC_SHEET = '원단위계산'
# 파이프라인이 dashboard.json에서 만들어 덮어쓰는 칸(사람이 엑셀에서 고치지 않음)
GENERATED_SHEETS = {'취합현황'}
GENERATED_CELLS = {'1.요청표': ['A2'] + [f'E{r}' for r in range(5, 18)] + [f'G{r}' for r in range(5, 18)]}
# 통째로 잠그는 시트(안내·설명·검토 기록)
FULL_LOCK_SHEETS = {'0.읽어주세요', 'KEY 설명', '장문자료 검토', '1.요청표'}

INPUT_FONT = {'FF0000FF', 'FFC00000'}  # 파란 글씨(입력값), 빨간 글씨(회신 메모)
INPUT_FILL = {'FFFFFF00'}              # 노란 칸(가정값)

REQUEST_STATUS = ['완료', '부분', '미회신', '문헌대체', '추가']
COUNT_STATUS = ['완료', '부분', '미회신', '문헌대체']
UNIT_STATUS = ['반영', '가정', '미반영', '문헌대체', '부분']
TREE_STATUS = ['반영', '부분', '미반영', '가정', '문헌대체']

LOCKED_FILES = [
    'locked/index.template.html', 'locked/guide.html', 'locked/form_lock.json', 'config/values_map.json',
    'pipeline/common.py', 'pipeline/lock.py', 'pipeline/checks.py', 'pipeline/render.py', 'pipeline/run.py', 'pipeline/relock.py',
    '.github/workflows/pipeline.yml',
]


def load_json(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def save_json(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
