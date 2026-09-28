# Project-GPS

'GPS' 버튼을 누르면 브라우저 Geolocation API로 현재 위치를 가져와 버튼 위에 표시하고, 서버에 저장하는 웹 서비스입니다.

## 구조

```
브라우저 ──> Next.js (3000) ──/api 프록시──> FastAPI (8000) ──> PostgreSQL (위치 기록 저장)
                                                        └──> Redis (최신 위치 캐시)
```

- `frontend/` : Next.js + React. `app/page.tsx`에 GPS 버튼과 위치 표시
- `backend/` : FastAPI. 시작 시 `locations` 테이블 자동 생성

## 실행

```bash
docker compose up -d --build
```

https://geolocationapi.miribit.cloud (또는 서버에서 http://localhost) 접속 후 'GPS' 버튼 클릭 → 브라우저의 위치 권한 허용

> Geolocation API는 보안 컨텍스트(HTTPS 또는 localhost)에서만 동작합니다.

## API

| 메서드 | 경로 | 설명 |
| --- | --- | --- |
| GET | `/api/health` | 상태 확인 |
| POST | `/api/locations` | 위치 저장 (`latitude`, `longitude`, `accuracy`) → PostgreSQL 저장 + Redis 캐시 갱신 |
| GET | `/api/locations/latest` | 최신 위치 조회 (Redis 우선, 없으면 DB) |

API 문서: http://localhost:8000/docs

## 설정

DB 계정은 기본값 `gps/gps/gps`를 사용합니다. 바꾸려면 `.env.example`을 참고해 `.env`를 만드세요.
