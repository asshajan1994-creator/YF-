from datetime import date

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import DB, CurrentUser
from app.models.operation import Operation, OperationStatus
from app.schemas.operation import OperationCreate, OperationRead, OperationUpdate

router = APIRouter()


@router.get("", response_model=list[OperationRead])
async def list_operations(
    db: DB,
    current_user: CurrentUser,
    field_id: int | None = None,
    status_filter: OperationStatus | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
) -> list[Operation]:
    stmt = select(Operation).order_by(Operation.scheduled_date.asc().nullslast())
    if field_id is not None:
        stmt = stmt.where(Operation.field_id == field_id)
    if status_filter is not None:
        stmt = stmt.where(Operation.status == status_filter)
    if from_date is not None:
        stmt = stmt.where(Operation.scheduled_date >= from_date)
    if to_date is not None:
        stmt = stmt.where(Operation.scheduled_date <= to_date)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("", response_model=OperationRead, status_code=status.HTTP_201_CREATED)
async def create_operation(payload: OperationCreate, db: DB, current_user: CurrentUser) -> Operation:
    op = Operation(**payload.model_dump())
    db.add(op)
    await db.flush()
    await db.refresh(op)
    return op


@router.get("/{operation_id}", response_model=OperationRead)
async def get_operation(operation_id: int, db: DB, current_user: CurrentUser) -> Operation:
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    op = result.scalar_one_or_none()
    if not op:
        raise HTTPException(status_code=404, detail="Operation not found")
    return op


@router.patch("/{operation_id}", response_model=OperationRead)
async def update_operation(
    operation_id: int, payload: OperationUpdate, db: DB, current_user: CurrentUser
) -> Operation:
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    op = result.scalar_one_or_none()
    if not op:
        raise HTTPException(status_code=404, detail="Operation not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(op, key, value)
    await db.flush()
    await db.refresh(op)
    return op


@router.delete("/{operation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_operation(operation_id: int, db: DB, current_user: CurrentUser) -> None:
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    op = result.scalar_one_or_none()
    if not op:
        raise HTTPException(status_code=404, detail="Operation not found")
    await db.delete(op)
