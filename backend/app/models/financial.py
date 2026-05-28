import enum
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TxnType(str, enum.Enum):
    EXPENSE = "expense"
    REVENUE = "revenue"


class TxnCategory(str, enum.Enum):
    INPUTS = "inputs"
    LABOR = "labor"
    EQUIPMENT = "equipment"
    WATER = "water"
    ELECTRICITY = "electricity"
    CROP_SALE = "crop_sale"
    BYPRODUCT = "byproduct"
    SUBSIDY = "subsidy"
    OTHER = "other"


class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    farm_id: Mapped[int] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_id: Mapped[int | None] = mapped_column(ForeignKey("crops.id", ondelete="SET NULL"), nullable=True)
    txn_type: Mapped[TxnType] = mapped_column(Enum(TxnType, name="txn_type"), nullable=False)
    category: Mapped[TxnCategory] = mapped_column(
        Enum(TxnCategory, name="txn_category"), default=TxnCategory.OTHER, nullable=False
    )
    txn_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    counterparty: Mapped[str | None] = mapped_column(String(255), nullable=True)
    invoice_number: Mapped[str | None] = mapped_column(String(80), nullable=True)
    hsn_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    gst_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
