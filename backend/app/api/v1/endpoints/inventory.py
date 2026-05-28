from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import DB, CurrentUser
from app.models.inventory import InputCategory, InventoryItem
from app.schemas.inventory import InventoryCreate, InventoryRead, InventoryUpdate

router = APIRouter()


@router.get("", response_model=list[InventoryRead])
async def list_inventory(
    db: DB,
    current_user: CurrentUser,
    farm_id: int | None = None,
    category: InputCategory | None = None,
    low_stock: bool = False,
) -> list[InventoryItem]:
    stmt = select(InventoryItem).order_by(InventoryItem.name.asc())
    if farm_id is not None:
        stmt = stmt.where(InventoryItem.farm_id == farm_id)
    if category is not None:
        stmt = stmt.where(InventoryItem.category == category)
    if low_stock:
        stmt = stmt.where(InventoryItem.quantity <= InventoryItem.reorder_level)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("", response_model=InventoryRead, status_code=status.HTTP_201_CREATED)
async def create_inventory_item(
    payload: InventoryCreate, db: DB, current_user: CurrentUser
) -> InventoryItem:
    item = InventoryItem(**payload.model_dump())
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.patch("/{item_id}", response_model=InventoryRead)
async def update_inventory_item(
    item_id: int, payload: InventoryUpdate, db: DB, current_user: CurrentUser
) -> InventoryItem:
    result = await db.execute(select(InventoryItem).where(InventoryItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory_item(item_id: int, db: DB, current_user: CurrentUser) -> None:
    result = await db.execute(select(InventoryItem).where(InventoryItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    await db.delete(item)
