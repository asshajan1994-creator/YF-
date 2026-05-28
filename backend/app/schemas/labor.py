from datetime import date

from pydantic import BaseModel, Field

from app.models.labor import LaborType
from app.schemas.common import TimestampedRead


class LaborerBase(BaseModel):
    farm_id: int
    full_name: str = Field(min_length=1, max_length=255)
    phone: str | None = None
    labor_type: LaborType = LaborType.UNSKILLED
    daily_wage: float = Field(default=0.0, ge=0)
    is_active: bool = True


class LaborerCreate(LaborerBase):
    pass


class LaborerUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    labor_type: LaborType | None = None
    daily_wage: float | None = None
    is_active: bool | None = None


class LaborerRead(LaborerBase, TimestampedRead):
    pass


class AttendanceBase(BaseModel):
    laborer_id: int
    work_date: date
    hours_worked: float = Field(default=8.0, ge=0, le=24)
    task: str | None = None
    wage_paid: float = Field(default=0.0, ge=0)


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceRead(AttendanceBase, TimestampedRead):
    pass
