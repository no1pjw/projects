# BallPark Security Lab Starter

야구 팬 커뮤니티 + 직관 기록 + 포인트/예매 시뮬레이션을 주제로 만든 **로컬 모의해킹/취약점 진단 실습용 Web/API 서비스**입니다.

이 저장소의 첫 버전은 의도적으로 취약한 `vulnerable` MVP입니다. 목표는 취약점을 악용하는 것이 아니라, 본인 로컬 랩에서 다음 흐름을 완성하는 것입니다.

```text
서비스 구현 -> 취약점 진단 -> 원인 분석 -> 조치 가이드 작성 -> 보안 수정 -> 재검증 -> 보고서 작성
```

## 1. 빠른 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/init_db.py
uvicorn app.main:app --reload
```

Windows PowerShell에서는 가상환경 활성화 명령이 다릅니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/init_db.py
uvicorn app.main:app --reload
```

실행 후 접속:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/games/1/page
```

## 2. Seed 계정

| username | password | role |
|---|---|---|
| alice | alice1234 | user |
| bob | bob1234 | user |
| admin | admin1234 | admin |

## 3. 현재 구현된 기능

- 회원가입
- 로그인 및 데모 토큰 발급
- 팀 목록 조회
- 경기 목록/상세 조회
- 경기 댓글 작성/조회
- HTML 경기 상세 페이지
- 직관 기록 작성/조회
- 포인트 충전 시뮬레이션
- 티켓 예매 시뮬레이션
- 관리자 경기 수정 API
- 프로필 파일 업로드

## 4. 의도적으로 포함된 취약점 후보

| 취약점 후보 | 관련 기능 | 보고서 키워드 |
|---|---|---|
| 하드코딩된 토큰 Secret | 인증 | Secret Management |
| 약한 비밀번호 해시 | 인증 | Password Storage |
| 타 사용자 직관 기록 조회 | `/api/users/{user_id}/attendance` | IDOR, Broken Access Control |
| 관리자 API 권한검증 누락 | `/api/admin/games/{game_id}` | Broken Function Level Authorization |
| 댓글 HTML 이스케이프 미흡 | `/games/{game_id}/page` | Stored XSS |
| 포인트 금액 검증 미흡 | `/api/points/charge` | Business Logic Flaw |
| 티켓 가격 클라이언트 신뢰 | `/api/tickets/reserve` | Price Tampering |
| 중복 좌석 예매 검증 미흡 | `/api/tickets/reserve` | Race/Business Logic |
| 파일 업로드 검증 미흡 | `/api/profile/upload` | File Upload Security |

## 5. 추천 작업 순서

1. 이 MVP를 로컬에서 실행한다.
2. `/docs`에서 API를 눌러보며 기능을 이해한다.
3. `docs/START_HERE.md` 순서대로 기능 명세와 자산 목록을 작성한다.
4. Burp Suite 또는 OWASP ZAP을 프록시로 연결해 요청/응답을 기록한다.
5. 취약점 후보를 하나씩 검증하고 `docs/FINDING_TEMPLATE.md` 형식으로 보고서를 작성한다.
6. `secure` 브랜치 또는 별도 폴더에서 취약점을 수정한다.
7. 수정 전/후 차이를 `docs/RETEST_REPORT.md`로 정리한다.

## 6. 주의사항

이 코드는 본인 로컬 환경의 학습용 랩입니다. 실제 타인 서비스, 외부 시스템, 허가받지 않은 자산을 대상으로 테스트하지 마세요.
