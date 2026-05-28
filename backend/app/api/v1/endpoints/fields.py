from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import DB, CurrentUser
from app.models.field import Field
from app.schemas.field import FieldCreate, FieldRead, FieldUpdate

router = APIRouter()


@router.get("", response_model=list[FieldRead])
async def list_fields(db: DB, current_user: CurrentUser, farm_id: int | None = None) -> list[Field]:
    stmt = select(Field).order_by(Field.created_at.desc())
    if farm_id is not None:
        stmt = stmt.where(Field.farm_id == farm_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("", response_model=FieldRead, status_code=status.HTTP_201_CREATED)
async def create_field(payload: FieldCreate, db: DB, current_user: CurrentUser) -> Field:
    field = Field(**payload.model_dump())
    db.add(field)
    await db.flush()
    await db.refresh(field)
    return field


@router.get("/{field_id}", response_model=FieldRead)
async def get_field(field_id: int, db: DB, current_user: CurrentUser) -> Field:
    result = await db.execute(select(Field).where(Field.id == field_id))
    field = result.scalar_one_or_none()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    return field


@router.patch("/{field_id}", response_model=FieldRead)
async def update_field(field_id: int, payload: FieldUpdate, db: DB, current_user: CurrentUser) -> Field:
    result = await db.execute(select(Field).where(Field.id == field_id))
    field = result.scalar_one_or_none()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(field, key, value)
    await db.flush()
    await db.refresh(field)
    return field


@router.delete("/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_field(field_id: int, db: DB, current_user: CurrentUser) -> None:
    result = await db.execute(select(Field).where(Field.id == field_id))
    field = result.scalar_one_or_none()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    await db.delete(field)
