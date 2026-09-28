import os

# 로컬 실행 시 기본값, Docker에서는 docker-compose.yml의 환경변수로 덮어씀
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://gps:gps@localhost:5432/gps")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
