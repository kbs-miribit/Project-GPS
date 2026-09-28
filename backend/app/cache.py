import logging

from redis.asyncio import Redis

from .config import REDIS_URL
from .schemas import LocationOut

logger = logging.getLogger(__name__)

redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

LATEST_LOCATION_KEY = "location:latest"


async def get_latest_location() -> LocationOut | None:
    # 캐시 장애가 나도 서비스는 DB로 계속 동작하도록 예외를 삼킴
    try:
        cached = await redis_client.get(LATEST_LOCATION_KEY)
    except Exception:
        logger.warning("Redis 조회 실패", exc_info=True)
        return None
    return LocationOut.model_validate_json(cached) if cached else None


async def set_latest_location(location: LocationOut) -> None:
    try:
        await redis_client.set(LATEST_LOCATION_KEY, location.model_dump_json())
    except Exception:
        logger.warning("Redis 저장 실패", exc_info=True)
