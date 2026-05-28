from datetime import date

from pydantic import BaseModel, Field

from app.models.inventory import InputCategory
from app.schemas.common import TimestampedRead


class InventoryBase(BaseModel):
    farm_id: int
    name: str = Field(min_length=1, max_length=255)
    category: InputCategory
    quantity: float = Field(default=0.0, ge=0)
    unit: str = Field(default="kg", max_length=20)
    unit_cost: float = Field(default=0.0, ge=0)
    reorder_level: float = Field(default=0.0, ge=0)
    expiry_date: date | None = None
    storage_location: str | None = None
    supplier: str | None = None
    npk_ratio: str | None = None
    notes: str | None = None


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    name: str | None = None
    category: InputCategory | None = None
    quantity: float | None = None
    unit: str | None = None
    unit_cost: float | None = None
    reorder_level: float | None = None
    expiry_date: date | None = None
    storage_location: str | None = None
    supplier: str | None = None
    npk_ratio: str | None = None
    notes: str | None = None


class InventoryRead(InventoryBase, TimestampedRead):
    pass
