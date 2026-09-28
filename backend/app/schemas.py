from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LocationIn(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    accuracy: float | None = Field(default=None, ge=0)


class LocationOut(LocationIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
