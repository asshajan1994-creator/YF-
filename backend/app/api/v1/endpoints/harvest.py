from datetime import date

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import DB, CurrentUser
from app.models.crop import Crop, GrowthStage
from app.models.harvest import HarvestRecord
from app.schemas.harvest import HarvestCreate, HarvestRead, HarvestUpdate

router = APIRouter()


@router.get("", response_model=list[HarvestRead])
async def list_harvests(
    db: DB,
    current_user: CurrentUser,
    crop_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
) -> list[HarvestRecord]:
    stmt = select(HarvestRecord).order_by(HarvestRecord.harvest_date.desc())
    if crop_id is not None:
        stmt = stmt.where(HarvestRecord.crop_id == crop_id)
    if from_date is not None:
        stmt = stmt.where(HarvestRecord.harvest_date >= from_date)
    if to_date is not None:
        stmt = stmt.where(HarvestRecord.harvest_date <= to_date)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("", response_model=HarvestRead, status_code=status.HTTP_201_CREATED)
async def create_harvest(
    payload: HarvestCreate, db: DB, current_user: CurrentUser
) -> HarvestRecord:
    crop = (await db.execute(select(Crop).where(Crop.id == payload.crop_id))).scalar_one_or_none()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    if crop.expected_harvest_date and payload.harvest_date < crop.expected_harvest_date:
        # warn but allow — early harvest possible
        pass

    record = HarvestRecord(**payload.model_dump())
    db.add(record)

    # Update crop state with cumulative yield and stage.
    crop.actual_yield_kg = (crop.actual_yield_kg or 0.0) + record.quantity_kg
    crop.growth_stage = GrowthStage.HARVESTED

    await db.flush()
    await db.refresh(record)
    return record


@router.patch("/{harvest_id}", response_model=HarvestRead)
async def update_harvest(
    harvest_id: int, payload: HarvestUpdate, db: DB, current_user: CurrentUser
) -> HarvestRecord:
    result = await db.execute(select(HarvestRecord).where(HarvestRecord.id == harvest_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Harvest record not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    await db.flush()
    await db.refresh(record)
    return record


@router.delete("/{harvest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_harvest(harvest_id: int, db: DB, current_user: CurrentUser) -> None:
    result = await db.execute(select(HarvestRecord).where(HarvestRecord.id == harvest_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Harvest record not found")
    await db.delete(record)
