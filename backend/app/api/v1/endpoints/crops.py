from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import DB, CurrentUser
from app.models.crop import Crop, GrowthStage
from app.schemas.crop import CropCreate, CropRead, CropUpdate

router = APIRouter()


@router.get("", response_model=list[CropRead])
async def list_crops(
    db: DB,
    current_user: CurrentUser,
    field_id: int | None = None,
    growth_stage: GrowthStage | None = None,
) -> list[Crop]:
    stmt = select(Crop).order_by(Crop.created_at.desc())
    if field_id is not None:
        stmt = stmt.where(Crop.field_id == field_id)
    if growth_stage is not None:
        stmt = stmt.where(Crop.growth_stage == growth_stage)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("", response_model=CropRead, status_code=status.HTTP_201_CREATED)
async def create_crop(payload: CropCreate, db: DB, current_user: CurrentUser) -> Crop:
    crop = Crop(**payload.model_dump())
    db.add(crop)
    await db.flush()
    await db.refresh(crop)
    return crop


@router.get("/{crop_id}", response_model=CropRead)
async def get_crop(crop_id: int, db: DB, current_user: CurrentUser) -> Crop:
    result = await db.execute(select(Crop).where(Crop.id == crop_id))
    crop = result.scalar_one_or_none()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop


@router.patch("/{crop_id}", response_model=CropRead)
async def update_crop(crop_id: int, payload: CropUpdate, db: DB, current_user: CurrentUser) -> Crop:
    result = await db.execute(select(Crop).where(Crop.id == crop_id))
    crop = result.scalar_one_or_none()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")

    if (
        payload.growth_stage == GrowthStage.HARVESTED
        and crop.expected_harvest_date is None
        and payload.expected_harvest_date is None
    ):
        # No-op guard: allow but no business rule failure.
        pass

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(crop, key, value)
    await db.flush()
    await db.refresh(crop)
    return crop


@router.delete("/{crop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crop(crop_id: int, db: DB, current_user: CurrentUser) -> None:
    result = await db.execute(select(Crop).where(Crop.id == crop_id))
    crop = result.scalar_one_or_none()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    await db.delete(crop)
