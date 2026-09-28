from datetime import datetime

from sqlalchemy import DateTime, Float, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Location(Base):
    """사용자가 GPS 버튼으로 조회한 위치 기록"""

    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    # 위치 정확도 (미터 단위)
    accuracy: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
