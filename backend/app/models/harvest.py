import enum
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class QualityGrade(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    REJECT = "reject"


class HarvestRecord(Base):
    __tablename__ = "harvest_records"

    crop_id: Mapped[int] = mapped_column(ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True)
    harvest_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    quantity_kg: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    quality_grade: Mapped[QualityGrade] = mapped_column(
        Enum(QualityGrade, name="quality_grade"), default=QualityGrade.A, nullable=False
    )
    storage_location: Mapped[str | None] = mapped_column(String(120), nullable=True)
    moisture_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    market_price_per_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    sold_to: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
