from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Field(Base):
    __tablename__ = "fields"

    farm_id: Mapped[int] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    area_acres: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    soil_ph: Mapped[float | None] = mapped_column(Float, nullable=True)
    soil_n: Mapped[float | None] = mapped_column(Float, nullable=True)
    soil_p: Mapped[float | None] = mapped_column(Float, nullable=True)
    soil_k: Mapped[float | None] = mapped_column(Float, nullable=True)
    organic_matter_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    moisture_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    irrigation_type: Mapped[str | None] = mapped_column(String(60), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
