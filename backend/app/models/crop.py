import enum
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class GrowthStage(str, enum.Enum):
    PLANNED = "planned"
    SEEDLING = "seedling"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    FRUITING = "fruiting"
    MATURITY = "maturity"
    HARVESTED = "harvested"


class Crop(Base):
    __tablename__ = "crops"

    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    variety: Mapped[str | None] = mapped_column(String(120), nullable=True)
    sowing_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expected_harvest_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    growth_stage: Mapped[GrowthStage] = mapped_column(
        Enum(GrowthStage, name="growth_stage"), default=GrowthStage.PLANNED, nullable=False
    )
    expected_yield_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    actual_yield_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    estimated_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
