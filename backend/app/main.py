from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .cache import get_latest_location, redis_client, set_latest_location
from .database import Base, engine, get_session
from .models import Location
from .schemas import LocationIn, LocationOut


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 테이블이 없으면 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await redis_client.aclose()
    await engine.dispose()


app = FastAPI(title="GPS API", lifespan=lifespan)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/locations", response_model=LocationOut, status_code=201)
async def create_location(
    payload: LocationIn, session: AsyncSession = Depends(get_session)
) -> LocationOut:
    # PostgreSQL에 기록을 저장하고, 최신 위치는 Redis에 캐시
    location = Location(**payload.model_dump())
    session.add(location)
    await session.commit()
    await session.refresh(location)

    result = LocationOut.model_validate(location)
    await set_latest_location(result)
    return result


@app.get("/api/locations/latest", response_model=LocationOut)
async def read_latest_location(
    session: AsyncSession = Depends(get_session),
) -> LocationOut:
    cached = await get_latest_location()
    if cached:
        return cached

    # 캐시에 없으면 DB에서 가장 최근 기록을 찾아 캐시를 채움
    location = await session.scalar(
        select(Location).order_by(Location.created_at.desc(), Location.id.desc()).limit(1)
    )
    if location is None:
        raise HTTPException(status_code=404, detail="저장된 위치가 없습니다")

    result = LocationOut.model_validate(location)
    await set_latest_location(result)
    return result
