"""재계산된 엑셀과 dashboard.json으로 대시보드 데이터(data.json)와 화면(index.html)을 만든다."""
import json, re, shutil
from openpyxl import load_workbook
from common import TEMPLATE, GUIDE, VALUES_MAP, load_json


def collect_values(calculated_xlsx, dash):
    vm = load_json(VALUES_MAP)['values']
    wb = load_workbook(calculated_xlsx, data_only=True)
    values = {}
    for k, o in vm.items():
        sheet, cell = o['cell'].split('!')
        v = wb[sheet][cell].value
        if isinstance(v, float):
            v = round(v, 6)
        if isinstance(v, str):  # 엑셀 오류값(#DIV/0! 등)
            v = None
        values[k] = {'label': o['label'], 'unit': o['unit'], 'src': o['cell'], 'value': v}
    for k, o in dash.get('manual_values', {}).items():
        values[k] = {'label': o['label'], 'unit': o['unit'], 'src': '수기(dashboard.json manual_values)', 'value': o['value'], 'note': o.get('note', '')}
    a, l = values.get('arrest_drug', {}).get('value'), values.get('lambda', {}).get('value')
    values['nstar'] = {'label': 'N* 암수 보정 실제 사용자 수', 'unit': '명', 'src': '자동(arrest_drug × lambda)',
                       'value': round(a * l, 2) if a is not None and l is not None else None}
    return values


def build_data(values, dash):
    data = {k: v for k, v in dash.items() if k != 'manual_values'}
    data['values'] = values
    return data


def write_page(data, out_dir):
    tpl = TEMPLATE.read_text(encoding='utf-8')
    blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    pat = re.compile(r'/\*DATA-BEGIN\*/.*?/\*DATA-END\*/', re.S)
    if len(pat.findall(tpl)) != 1:
        raise SystemExit('템플릿의 DATA 자리를 찾지 못했습니다')
    (out_dir / 'index.html').write_text(pat.sub(lambda m: '/*DATA-BEGIN*/' + blob + '/*DATA-END*/', tpl), encoding='utf-8')
    (out_dir / 'data.json').write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    shutil.copy(GUIDE, out_dir / 'guide.html')
