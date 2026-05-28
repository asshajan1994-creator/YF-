from datetime import date

from pydantic import BaseModel, Field

from app.models.harvest import QualityGrade
from app.schemas.common import TimestampedRead


class HarvestBase(BaseModel):
    crop_id: int
    harvest_date: date
    quantity_kg: float = Field(default=0.0, ge=0)
    quality_grade: QualityGrade = QualityGrade.A
    storage_location: str | None = None
    moisture_pct: float | None = Field(default=None, ge=0, le=100)
    market_price_per_kg: float | None = Field(default=None, ge=0)
    sold_to: str | None = None
    notes: str | None = None


class HarvestCreate(HarvestBase):
    pass


class HarvestUpdate(BaseModel):
    harvest_date: date | None = None
    quantity_kg: float | None = None
    quality_grade: QualityGrade | None = None
    storage_location: str | None = None
    moisture_pct: float | None = None
    market_price_per_kg: float | None = None
    sold_to: str | None = None
    notes: str | None = None


class HarvestRead(HarvestBase, TimestampedRead):
    pass
