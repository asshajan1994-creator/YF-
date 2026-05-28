from datetime import date

from pydantic import BaseModel, Field

from app.models.operation import OperationStatus, OperationType
from app.schemas.common import TimestampedRead


class OperationBase(BaseModel):
    field_id: int
    crop_id: int | None = None
    operation_type: OperationType
    status: OperationStatus = OperationStatus.PENDING
    scheduled_date: date | None = None
    completed_date: date | None = None
    assigned_to: str | None = None
    cost: float = Field(default=0.0, ge=0)
    notes: str | None = None


class OperationCreate(OperationBase):
    pass


class OperationUpdate(BaseModel):
    operation_type: OperationType | None = None
    status: OperationStatus | None = None
    scheduled_date: date | None = None
    completed_date: date | None = None
    assigned_to: str | None = None
    cost: float | None = None
    notes: str | None = None


class OperationRead(OperationBase, TimestampedRead):
    pass
