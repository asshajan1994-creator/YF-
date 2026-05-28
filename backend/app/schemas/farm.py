from pydantic import BaseModel, Field

from app.schemas.common import TimestampedRead


class FarmBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    location: str | None = None
    district: str | None = None
    state: str = "Tamil Nadu"
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    total_area_acres: float = Field(default=0.0, ge=0)
    soil_type: str | None = None
    climate_zone: str | None = None
    notes: str | None = None


class FarmCreate(FarmBase):
    pass


class FarmUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    district: str | None = None
    state: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    total_area_acres: float | None = None
    soil_type: str | None = None
    climate_zone: str | None = None
    notes: str | None = None


class FarmRead(FarmBase, TimestampedRead):
    owner_id: int
