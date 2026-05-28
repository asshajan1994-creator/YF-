from datetime import date

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import DB, CurrentUser
from app.models.labor import Attendance, Laborer
from app.schemas.labor import (
    AttendanceCreate,
    AttendanceRead,
    LaborerCreate,
    LaborerRead,
    LaborerUpdate,
)

router = APIRouter()


@router.get("", response_model=list[LaborerRead])
async def list_laborers(
    db: DB, current_user: CurrentUser, farm_id: int | None = None
) -> list[Laborer]:
    stmt = select(Laborer).order_by(Laborer.created_at.desc())
    if farm_id is not None:
        stmt = stmt.where(Laborer.farm_id == farm_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("", response_model=LaborerRead, status_code=status.HTTP_201_CREATED)
async def create_laborer(payload: LaborerCreate, db: DB, current_user: CurrentUser) -> Laborer:
    laborer = Laborer(**payload.model_dump())
    db.add(laborer)
    await db.flush()
    await db.refresh(laborer)
    return laborer


@router.patch("/{laborer_id}", response_model=LaborerRead)
async def update_laborer(
    laborer_id: int, payload: LaborerUpdate, db: DB, current_user: CurrentUser
) -> Laborer:
    result = await db.execute(select(Laborer).where(Laborer.id == laborer_id))
    laborer = result.scalar_one_or_none()
    if not laborer:
        raise HTTPException(status_code=404, detail="Laborer not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(laborer, key, value)
    await db.flush()
    await db.refresh(laborer)
    return laborer


@router.delete("/{laborer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_laborer(laborer_id: int, db: DB, current_user: CurrentUser) -> None:
    result = await db.execute(select(Laborer).where(Laborer.id == laborer_id))
    laborer = result.scalar_one_or_none()
    if not laborer:
        raise HTTPException(status_code=404, detail="Laborer not found")
    await db.delete(laborer)


@router.post("/attendance", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    payload: AttendanceCreate, db: DB, current_user: CurrentUser
) -> Attendance:
    laborer = (await db.execute(select(Laborer).where(Laborer.id == payload.laborer_id))).scalar_one_or_none()
    if not laborer:
        raise HTTPException(status_code=404, detail="Laborer not found")

    record = Attendance(**payload.model_dump())
    if not record.wage_paid:
        record.wage_paid = round(laborer.daily_wage * (record.hours_worked / 8.0), 2)
    db.add(record)
    await db.flush()
    await db.refresh(record)
    return record


@router.get("/attendance", response_model=list[AttendanceRead])
async def list_attendance(
    db: DB,
    current_user: CurrentUser,
    laborer_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
) -> list[Attendance]:
    stmt = select(Attendance).order_by(Attendance.work_date.desc())
    if laborer_id is not None:
        stmt = stmt.where(Attendance.laborer_id == laborer_id)
    if from_date is not None:
        stmt = stmt.where(Attendance.work_date >= from_date)
    if to_date is not None:
        stmt = stmt.where(Attendance.work_date <= to_date)
    result = await db.execute(stmt)
    return list(result.scalars().all())
