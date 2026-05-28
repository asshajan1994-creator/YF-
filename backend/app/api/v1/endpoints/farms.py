from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import DB, CurrentUser
from app.models.farm import Farm
from app.models.user import UserRole
from app.schemas.farm import FarmCreate, FarmRead, FarmUpdate

router = APIRouter()


def _can_modify(user, farm: Farm) -> bool:
    return user.role in {UserRole.ADMIN, UserRole.MANAGER} or farm.owner_id == user.id


@router.get("", response_model=list[FarmRead])
async def list_farms(db: DB, current_user: CurrentUser) -> list[Farm]:
    stmt = select(Farm).order_by(Farm.created_at.desc())
    if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
        stmt = stmt.where(Farm.owner_id == current_user.id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("", response_model=FarmRead, status_code=status.HTTP_201_CREATED)
async def create_farm(payload: FarmCreate, db: DB, current_user: CurrentUser) -> Farm:
    farm = Farm(**payload.model_dump(), owner_id=current_user.id)
    db.add(farm)
    await db.flush()
    await db.refresh(farm)
    return farm


@router.get("/{farm_id}", response_model=FarmRead)
async def get_farm(farm_id: int, db: DB, current_user: CurrentUser) -> Farm:
    result = await db.execute(select(Farm).where(Farm.id == farm_id))
    farm = result.scalar_one_or_none()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    if not _can_modify(current_user, farm) and farm.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not permitted")
    return farm


@router.patch("/{farm_id}", response_model=FarmRead)
async def update_farm(farm_id: int, payload: FarmUpdate, db: DB, current_user: CurrentUser) -> Farm:
    result = await db.execute(select(Farm).where(Farm.id == farm_id))
    farm = result.scalar_one_or_none()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    if not _can_modify(current_user, farm):
        raise HTTPException(status_code=403, detail="Not permitted")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(farm, key, value)
    await db.flush()
    await db.refresh(farm)
    return farm


@router.delete("/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_farm(farm_id: int, db: DB, current_user: CurrentUser) -> None:
    result = await db.execute(select(Farm).where(Farm.id == farm_id))
    farm = result.scalar_one_or_none()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    if not _can_modify(current_user, farm):
        raise HTTPException(status_code=403, detail="Not permitted")
    await db.delete(farm)
