from datetime import date

from pydantic import BaseModel, Field

from app.models.financial import TxnCategory, TxnType
from app.schemas.common import TimestampedRead


class TransactionBase(BaseModel):
    farm_id: int
    crop_id: int | None = None
    txn_type: TxnType
    category: TxnCategory = TxnCategory.OTHER
    txn_date: date
    amount: float = Field(ge=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    counterparty: str | None = None
    invoice_number: str | None = None
    hsn_code: str | None = None
    gst_pct: float | None = Field(default=None, ge=0, le=100)
    description: str | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    txn_type: TxnType | None = None
    category: TxnCategory | None = None
    txn_date: date | None = None
    amount: float | None = None
    currency: str | None = None
    counterparty: str | None = None
    invoice_number: str | None = None
    hsn_code: str | None = None
    gst_pct: float | None = None
    description: str | None = None


class TransactionRead(TransactionBase, TimestampedRead):
    pass
