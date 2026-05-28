from datetime import date

from pydantic import BaseModel, Field, model_validator

from app.models.crop import GrowthStage
from app.schemas.common import TimestampedRead


class CropBase(BaseModel):
    field_id: int
    crop_name: str = Field(min_length=1, max_length=120)
    variety: str | None = None
    sowing_date: date | None = None
    expected_harvest_date: date | None = None
    growth_stage: GrowthStage = GrowthStage.PLANNED
    expected_yield_kg: float | None = Field(default=None, ge=0)
    actual_yield_kg: float | None = Field(default=None, ge=0)
    estimated_cost: float | None = Field(default=None, ge=0)
    notes: str | None = None

    @model_validator(mode="after")
    def _validate_harvest_after_sowing(self):
        if self.sowing_date and self.expected_harvest_date:
            if self.expected_harvest_date < self.sowing_date:
                raise ValueError("expected_harvest_date must be on or after sowing_date")
        return self


class CropCreate(CropBase):
    pass


class CropUpdate(BaseModel):
    crop_name: str | None = None
    variety: str | None = None
    sowing_date: date | None = None
    expected_harvest_date: date | None = None
    growth_stage: GrowthStage | None = None
    expected_yield_kg: float | None = None
    actual_yield_kg: float | None = None
    estimated_cost: float | None = None
    notes: str | None = None


class CropRead(CropBase, TimestampedRead):
    pass
