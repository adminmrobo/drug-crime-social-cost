# 마약류범죄와 교정기관 중독재활 체계의 사회적 비용 비교분석

**Social Costs of Drug Crime and Correctional Addiction Rehabilitation: A Comparative Analysis**

법무부 연구용역의 자료 취합·계산·진행판 저장소입니다. 회신값을 엑셀에 넣고 push하면 계산과 진행판이 자동으로 갱신됩니다. **서식·구조와 진행판의 틀은 잠겨 있어 자료를 넣는 과정에서 바뀌지 않습니다.**

## 페이지 (GitHub Pages)

| 주소 | 내용 | 만드는 방식 |
|---|---|---|
| `/` (index.html) | 첫 화면. 아래 페이지로 가는 목록 | 손으로 관리 |
| `/cost-map.html` | 사회적 비용 구조도: 당초 모델 → 구현 모델 → 회신 반영, 비용 39칸과 자료 연결, 칸별 계산 상태 | 손으로 관리 |
| `/dist/index.html` | 교정 재활 비용편익 진행판 | 자동 생성 |
| `/dist/guide.html` | 입력 가이드 | 자동 생성 |
| `/dist/report.md` | 최근 갱신 보고 | 자동 생성 |
| `/dist/workbook.xlsx` | 최신 계산 엑셀 | 자동 생성 |

설정: **Settings → Pages → Source: Deploy from a branch → Branch: `main`, `/ (root)`**. 1~2분 뒤 `https://<계정>.github.io/<저장소>/`에서 열립니다.

> **공개 범위 주의.** 무료 계정의 Pages는 공개 저장소에서만 동작하고, 주소를 아는 누구나 볼 수 있습니다. 이 저장소에는 교정본부·대검찰청 회신 수치(행정내부자료)가 들어 있습니다. 공개 전에 발주처와 확인하십시오. 페이지에 `noindex`를 넣어 검색 노출은 막았지만 접근 제한 수단은 아닙니다.

## 사람이 하는 일

### 회신값을 받았을 때 (비용편익 쪽, 서식 1~12·별도요청)

1. `data/workbook.xlsx`의 해당 서식 칸에 회신값을 넣습니다.
   - 넣을 수 있는 칸: 서식 시트의 **빈칸**, **파란 글씨 칸**, 「원단위계산」 시트의 **노란 칸**(가정값)
   - 넣을 수 없는 칸: 제목, 항목명, 단위, KEY, 산식, 「취합현황」 시트, 「1.요청표」의 진행 상태
2. `data/dashboard.json`에서 해당 요청의 `status`·`pill`·`got`·`received`·`missing`·`doing`을 고치고, `meta.asof`·`meta.version`을 올리고 `meta.history`에 한 줄을 더합니다.
3. 커밋해서 `main`에 push합니다. (검토를 받으려면 pull request — 점검만 돌고 결과는 저장하지 않습니다.)

### 제3장 사회적 비용 자료를 받았을 때 (구조 시트)

`data/workbook.xlsx`의 「구조_」 시트 6개가 제3장 사회적 비용의 칸과 입력 변수 자리입니다. **산식은 아직 없고 자리만 고정되어 있습니다.**

| 시트 | 내용 |
|---|---|
| 구조_안내 | 칸 색의 뜻, 입력 순서, 예시 |
| 구조_칸 | 39칸의 성격(비용 종류·단위·적용 인원·λ 적용·연간/생애·SCᵣ 포함·합산되는 곳·현재 분류). 변수 수·미입력 수 자동 |
| 구조_변수 | 칸별 입력 변수 110개. 값을 넣으면 상태(입력됨·대체 입력·가정·연결·미입력)가 자동으로 바뀜 |
| 구조_집계 | 절별·상태별 변수 개수와 입력 비율, 칸 분류 개수 |
| 구조_스위치 | 구조에 걸린 미결정 7가지. 선택을 바꾸면 「구조_칸」 관련 열이 따라감 |
| 구조_중복규칙 | 한쪽에만 넣어야 하는 6쌍 |

1. 「구조_변수」의 출처 상세 열에서 서식 번호·자료명으로 행을 찾습니다.
2. 노란 칸(출처 종류·기준연도·값·메모)만 고칩니다. 값은 원 단위로 환산하고, 비율은 소수로 넣습니다(4.5% → 0.045).
3. 팀 결정이 나면 「구조_스위치」의 현재 선택을 바꿉니다.
4. 커밋해서 push합니다. 구조 시트도 잠금 점검을 받습니다.

## 자동으로 되는 일 (GitHub Actions: `.github/workflows/pipeline.yml`)

| 단계 | 내용 | 실패하면 |
|---|---|---|
| ① 잠금 점검 | `locked/manifest.json`의 해시와 `locked/form_lock.json`의 고정 칸을 비교 | 바뀐 파일·칸을 알려 주고 멈춤 |
| ② 생성 | `dashboard.json`으로 1.요청표 진행 상태와 「취합현황」 시트를 다시 만듦 | — |
| ③ 재계산 | LibreOffice로 재계산, 「원단위계산」 오류값(#REF! 등) 검사 | 오류 칸을 알려 주고 멈춤 |
| ④ 점검 | 산식 관계·상태값·문구 자리표시 31건 점검 | 불일치 목록을 보여 주고 멈춤 |
| ⑤ 저장 | `dist/`에 index.html·data.json·guide.html·workbook.xlsx·report.md를 쓰고 커밋 | — |

실패하면 `dist/`는 이전 결과 그대로 남습니다. 실행 요약(Actions 화면)에 바뀐 값과 확인할 일이 나옵니다.

### 회신이 오면 자동으로 바뀌는 연결

- 서식9 「2025 전체 이수·미이수」 두 줄의 출소인원·재복역이 모두 채워지면 → r0·r1·Δr이 논문값에서 회신값으로
- 서식7 6번(정신과 진료·약품비)과 12번(치료개입 대상 인원)이 채워지면 → UC-10
- 별도요청 2번(치료보호 집행액)과 3번(지원 인원)의 2025년 값이 채워지면 → UC-12
- 나머지 원단위는 연결된 서식 칸을 그대로 따라감

값이 바뀌어 진행판 문구(예: "미산출", "문헌 대체")를 고쳐야 할 때는 report.md의 「확인할 일」에 나옵니다. **구조도(`cost-map.html`)는 자동 갱신 대상이 아닙니다.** 분류나 값이 바뀌면 손으로 고칩니다(아래 「앞으로 할 일」).

## 폴더

```
index.html       첫 화면(페이지 목록)
cost-map.html    사회적 비용 구조도(단독 페이지)
.nojekyll        GitHub Pages가 파일을 그대로 내보내게 함
data/            입력 — workbook.xlsx(서식·계산·구조 시트), dashboard.json(상태·문구·수기값)
locked/          잠금 — index.template.html(진행판 틀), guide.html, form_lock.json, manifest.json, CHANGELOG.md
config/          잠금 — values_map.json(진행판 숫자 ↔ 엑셀 셀)
pipeline/        잠금 — run.py(전체 실행), lock.py, checks.py, render.py, relock.py, common.py
dist/            결과 — 자동 생성, 손으로 고치지 않음
tools/           서식·구조 생성 기록. 파이프라인은 쓰지 않음
  form_builder/    최초 서식 생성(build.py·calc.py·status.py)
  structure/       구조 시트 생성(build_structure.py)
```

## 내 컴퓨터에서 돌려 보기

LibreOffice와 Python 3.10 이상이 필요합니다.

```bash
pip install -r requirements.txt
python pipeline/run.py --check   # 점검만
python pipeline/run.py           # dist/까지 갱신
```

## 서식·구조·진행판 틀을 바꿔야 할 때 (판 올림)

자료를 넣는 중에는 하지 않습니다. 산식 경로를 새로 잇거나, 칸·변수를 더하거나, 화면 구역을 바꿀 때만 합니다.

```bash
# 구조 칸·변수를 바꿀 때: tools/structure/build_structure.py를 고친 뒤
python tools/structure/build_structure.py data/workbook.xlsx
# 엑셀 서식이나 locked/ · pipeline/ 파일을 고친 뒤(구조 변경 포함)
python pipeline/relock.py --version 구조-v2 --reason "바꾼 이유"
python pipeline/run.py
```

`build_structure.py`를 다시 돌리면 구조 시트를 새로 만들므로 **이미 넣은 값이 지워집니다.** 값을 넣기 시작한 뒤에는 엑셀에서 직접 행을 더하고 relock하십시오. `locked/CHANGELOG.md`에 판 이름과 이유가 남습니다.

## 저장소 설정 권장

- Settings → Branches → `main` 보호 규칙: pull request 필수, 「자동 계산·대시보드 갱신」 검사 통과 필수, Code owners 검토 필수
- Settings → Actions → General → Workflow permissions: **Read and write**(dist 자동 커밋용)
- `.github/CODEOWNERS`의 `@OWNER`를 실제 GitHub 아이디로 바꾸기

## 앞으로 할 일

1. 팀 결정 7건(「구조_스위치」)과 공개통계 수집 뒤, 제3장 계산 시트를 「원단위계산」처럼 만들어 「구조_변수」 값을 잇는다.
2. 구조도가 `dist/data.json`을 읽게 바꿔, 숫자와 분류를 손으로 적는 부분을 없앤다.
3. 진행판(Claude Artifact) 링크 https://claude.ai/artifact/BgZ4KRaZP8LqdFtFDncmWm 와 구조도 링크 https://claude.ai/artifact/54Gi8pYbXpjHheJb7tkY6b 는 Claude에게 "dist 기준으로 갱신"을 요청해 다시 올린다.

## 판 기록

`locked/CHANGELOG.md` 참조. 현재 판: **구조-v1.1** (2026-10-21, 제3장 구조 시트 6개 추가 후 여백 조정).
