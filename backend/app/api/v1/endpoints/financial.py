from datetime import date

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from app.api.deps import DB, CurrentUser
from app.models.financial import FinancialTransaction, TxnCategory, TxnType
from app.schemas.financial import TransactionCreate, TransactionRead, TransactionUpdate

router = APIRouter()


@router.get("", response_model=list[TransactionRead])
async def list_transactions(
    db: DB,
    current_user: CurrentUser,
    farm_id: int | None = None,
    txn_type: TxnType | None = None,
    category: TxnCategory | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
) -> list[FinancialTransaction]:
    stmt = select(FinancialTransaction).order_by(FinancialTransaction.txn_date.desc())
    if farm_id is not None:
        stmt = stmt.where(FinancialTransaction.farm_id == farm_id)
    if txn_type is not None:
        stmt = stmt.where(FinancialTransaction.txn_type == txn_type)
    if category is not None:
        stmt = stmt.where(FinancialTransaction.category == category)
    if from_date is not None:
        stmt = stmt.where(FinancialTransaction.txn_date >= from_date)
    if to_date is not None:
        stmt = stmt.where(FinancialTransaction.txn_date <= to_date)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: TransactionCreate, db: DB, current_user: CurrentUser
) -> FinancialTransaction:
    txn = FinancialTransaction(**payload.model_dump())
    db.add(txn)
    await db.flush()
    await db.refresh(txn)
    return txn


@router.patch("/{txn_id}", response_model=TransactionRead)
async def update_transaction(
    txn_id: int, payload: TransactionUpdate, db: DB, current_user: CurrentUser
) -> FinancialTransaction:
    result = await db.execute(select(FinancialTransaction).where(FinancialTransaction.id == txn_id))
    txn = result.scalar_one_or_none()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(txn, key, value)
    await db.flush()
    await db.refresh(txn)
    return txn


@router.delete("/{txn_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(txn_id: int, db: DB, current_user: CurrentUser) -> None:
    result = await db.execute(select(FinancialTransaction).where(FinancialTransaction.id == txn_id))
    txn = result.scalar_one_or_none()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    await db.delete(txn)


@router.get("/summary")
async def financial_summary(
    db: DB,
    current_user: CurrentUser,
    farm_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
) -> dict:
    stmt = select(
        FinancialTransaction.txn_type,
        FinancialTransaction.category,
        func.sum(FinancialTransaction.amount).label("total"),
    ).group_by(FinancialTransaction.txn_type, FinancialTransaction.category)

    if farm_id is not None:
        stmt = stmt.where(FinancialTransaction.farm_id == farm_id)
    if from_date is not None:
        stmt = stmt.where(FinancialTransaction.txn_date >= from_date)
    if to_date is not None:
        stmt = stmt.where(FinancialTransaction.txn_date <= to_date)

    rows = (await db.execute(stmt)).all()
    expense_total = 0.0
    revenue_total = 0.0
    breakdown: dict[str, float] = {}
    for txn_type, category, total in rows:
        amount = float(total or 0)
        breakdown[f"{txn_type.value}:{category.value}"] = amount
        if txn_type == TxnType.EXPENSE:
            expense_total += amount
        elif txn_type == TxnType.REVENUE:
            revenue_total += amount
    return {
        "expense_total": expense_total,
        "revenue_total": revenue_total,
        "profit": revenue_total - expense_total,
        "breakdown": breakdown,
    }
