# GARD Journal & Ledger · 공개 전시장 / 구매자·구독자 검토 앱

**공개 GitHub 업로드 전용 ZIP.** 오너 HTML, 전체 Excel, 145개 원본기록, 영수증, 공동창업자 개별 지급원장은 이 ZIP에 포함되어 있지 않습니다.

## GitHub → Netlify 처음 배포 (빌드 없음)

1. GitHub에서 새 **공개 전용 저장소** (예: `GARD-Journal-Trust-Ledger-v2`)를 만듭니다. 기존 `GARD-Trust-Asset-Market-OS-` 앱은 v1 공개 JSON 형식이므로, 단순히 v2 JSON만 교체하지 마세요.
2. 이 ZIP을 압축 해제해 **최상위**의 `netlify.toml`, `site/`, `tools/`, `README_DEPLOY_KO.md`를 GitHub의 **main 브랜치**에 업로드하고 `Commit changes` 합니다. ZIP 파일 그 자체만 업로드하면 정적 사이트로 동작하지 않습니다.
3. Netlify에서 **Add new project → Import an existing project → GitHub** → 새 저장소를 연결합니다.
4. 배포 설정에서 **Build command = 비움**, **Publish directory = `site`**를 확인합니다 (`netlify.toml`에 이미 설정되어 있음).
5. Netlify 주소 `/`는 공개 전시장, `/buyer.html`은 수신자 JSON 수동 열기·독립평가 화면입니다. 첫 화면에 미팅/분개 0개가 나오는 것은 **공개 승인본이 아직 없기 때문**입니다.

## 매주 새 공개본 업데이트 — Python 불필요

1. 오너의 `OWNER_GARD_JOURNAL_V2.html` → **④ 공개범위 승인** → 전체 공개 선택 → 연도와 주체 선택 → 미리보기 → **공개본 생성·다운로드**.
2. 브라우저에 `public.json`이 다운로드됩니다. 이 파일에 실제로 공개해도 되는 숫자·문장이 들어있는지 텍스트 편집기로 **직접 확인**합니다.
3. GitHub 저장소에서 `main` 브랜치의 `site/data/` 폴더를 엽니다. 브랜치에 `91f1186` 같은 커밋 해시가 표시되면 **main으로 이동**해야 업로드 메뉴가 나타납니다.
4. `Add file → Upload files`에서 **`public.json` 하나만** 업로드하여 기존 파일을 교체하고 커밋합니다. GitHub UI가 파일 교체 업로드를 허용하지 않으면 `site/data/public.json` 파일의 편집(연필 아이콘) 화면에 새 JSON 전체 텍스트를 붙여 넣고 커밋할 수도 있습니다.
5. Netlify가 연결되어 있다면 새 커밋 후 재배포됩니다. `/`에서 공개일지·분개·재무표가 보이고, 화면에 **해시 검증** 상태가 표시되는지 확인합니다.

**선택사항:** 이력도 GitHub에 남기려면 `tools/publish_update_v2.py`를 Python 3으로 실행하여 `site/data/public.json`, `site/data/history.json`, `site/data/versions/<id>.json`을 동시 갱신한 후 GitHub에 커밋합니다. 버전 저장은 비공개로 되돌릴 수 없는 공개 이력입니다.

## 수신자 제한 공유

`buyer`, `subscriber`, `approved` 대상 암호화 파일은 **공개 저장소에 올리지 않습니다.** 오너가 수신자에게 별도로 보내며, 암호는 다른 채널로 전달합니다. 같은 공개 웹앱에서 파일을 선택해 복호화합니다. 로그인 기능이나 철회 권한은 없습니다. 서버 인증과 계약·결제 연동이 필요하면 다음 단계의 백엔드 구축이 필요합니다.

## 보안·한계

- `site/data/public.json`만 누구나 읽을 수 있습니다. **오너 HTML 또는 XLSX, 암호화 파일도 공개 저장소에 업로드하지 마세요.** GitHub에 업로드한 자료는 삭제 후에도 Git 이력에서 남을 수 있습니다.
- SHA-256은 공개본의 변경 여부만 검사하며 작성자 확인이나 법적 전자서명이 아닙니다.
- 재무제표는 선택공개 분개만으로 만든 부분원장 관리표입니다. 감사보고서, 완성된 법정 결산, 신주등기 증명이 아닙니다.
- 공개 대상이 0건인 경우 0원으로 표시되어도 **미공개 실체의 가치 0원**이라는 뜻은 아닙니다.
