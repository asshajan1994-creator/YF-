import enum
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OperationType(str, enum.Enum):
    PLOWING = "plowing"
    SOWING = "sowing"
    IRRIGATION = "irrigation"
    FERTILIZATION = "fertilization"
    PESTICIDE = "pesticide"
    WEEDING = "weeding"
    HARVESTING = "harvesting"
    OTHER = "other"


class OperationStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Operation(Base):
    __tablename__ = "operations"

    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_id: Mapped[int | None] = mapped_column(ForeignKey("crops.id", ondelete="SET NULL"), nullable=True)
    operation_type: Mapped[OperationType] = mapped_column(
        Enum(OperationType, name="operation_type"), nullable=False
    )
    status: Mapped[OperationStatus] = mapped_column(
        Enum(OperationStatus, name="operation_status"), default=OperationStatus.PENDING, nullable=False
    )
    scheduled_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    completed_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    assigned_to: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
