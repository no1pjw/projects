# API 테스트 예시

## 로그인

```bash
curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","password":"alice1234"}'
```

응답의 `access_token` 값을 복사해서 아래처럼 사용합니다.

```bash
TOKEN='여기에_토큰_붙여넣기'
```

## 내 정보 확인

```bash
curl -s http://127.0.0.1:8000/api/me \
  -H "Authorization: Bearer $TOKEN"
```

## 경기 목록 조회

```bash
curl -s http://127.0.0.1:8000/api/games
```

## 댓글 작성

```bash
curl -s -X POST http://127.0.0.1:8000/api/games/1/comments \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"content":"오늘 경기 기대됩니다!"}'
```

## 직관 기록 작성

```bash
curl -s -X POST http://127.0.0.1:8000/api/attendance \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"game_id":1,"seat_section":"1B-101","memo":"첫 직관"}'
```

## 직관 기록 조회

```bash
curl -s http://127.0.0.1:8000/api/users/1/attendance \
  -H "Authorization: Bearer $TOKEN"
```

## 포인트 충전

```bash
curl -s -X POST http://127.0.0.1:8000/api/points/charge \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"amount":1000,"reason":"event"}'
```

## 티켓 예매 시뮬레이션

```bash
curl -s -X POST http://127.0.0.1:8000/api/tickets/reserve \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"game_id":1,"seat_no":"A-01","client_price":3000}'
```

## 관리자 경기 수정 API

```bash
curl -s -X PUT http://127.0.0.1:8000/api/admin/games/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"home_score":7,"away_score":2,"status":"final"}'
```
