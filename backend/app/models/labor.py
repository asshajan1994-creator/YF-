import enum
from datetime import date

from sqlalchemy import Boolean, Date, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LaborType(str, enum.Enum):
    SKILLED = "skilled"
    UNSKILLED = "unskilled"
    CONTRACTOR = "contractor"


class Laborer(Base):
    __tablename__ = "laborers"

    farm_id: Mapped[int] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    labor_type: Mapped[LaborType] = mapped_column(
        Enum(LaborType, name="labor_type"), default=LaborType.UNSKILLED, nullable=False
    )
    daily_wage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Attendance(Base):
    __tablename__ = "attendance"

    laborer_id: Mapped[int] = mapped_column(
        ForeignKey("laborers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    work_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    hours_worked: Mapped[float] = mapped_column(Float, default=8.0, nullable=False)
    task: Mapped[str | None] = mapped_column(String(255), nullable=True)
    wage_paid: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
