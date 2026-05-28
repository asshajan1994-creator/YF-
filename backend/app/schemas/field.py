from pydantic import BaseModel, Field

from app.schemas.common import TimestampedRead


class FieldBase(BaseModel):
    farm_id: int
    name: str = Field(min_length=1, max_length=120)
    area_acres: float = Field(default=0.0, ge=0)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    soil_ph: float | None = Field(default=None, ge=0, le=14)
    soil_n: float | None = None
    soil_p: float | None = None
    soil_k: float | None = None
    organic_matter_pct: float | None = Field(default=None, ge=0, le=100)
    moisture_pct: float | None = Field(default=None, ge=0, le=100)
    irrigation_type: str | None = None
    notes: str | None = None


class FieldCreate(FieldBase):
    pass


class FieldUpdate(BaseModel):
    name: str | None = None
    area_acres: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    soil_ph: float | None = None
    soil_n: float | None = None
    soil_p: float | None = None
    soil_k: float | None = None
    organic_matter_pct: float | None = None
    moisture_pct: float | None = None
    irrigation_type: str | None = None
    notes: str | None = None


class FieldRead(FieldBase, TimestampedRead):
    pass
