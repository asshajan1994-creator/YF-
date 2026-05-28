from datetime import date, timedelta

from fastapi import APIRouter
from sqlalchemy import func, select

from app.api.deps import DB, CurrentUser
from app.models.crop import Crop, GrowthStage
from app.models.farm import Farm
from app.models.field import Field
from app.models.financial import FinancialTransaction, TxnType
from app.models.inventory import InventoryItem
from app.models.labor import Laborer
from app.models.operation import Operation, OperationStatus
from app.models.user import UserRole
from app.schemas.dashboard import (
    AlertItem,
    DashboardResponse,
    DashboardStats,
    UpcomingOperation,
)

router = APIRouter()


@router.get("", response_model=DashboardResponse)
async def get_dashboard(db: DB, current_user: CurrentUser) -> DashboardResponse:
    today = date.today()
    month_start = today.replace(day=1)
    horizon = today + timedelta(days=30)

    farm_stmt = select(Farm)
    if current_user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
        farm_stmt = farm_stmt.where(Farm.owner_id == current_user.id)
    farms = (await db.execute(farm_stmt)).scalars().all()
    farm_ids = [f.id for f in farms] or [0]
    total_area = sum(f.total_area_acres for f in farms)

    active_crops = (
        await db.execute(
            select(func.count(Crop.id))
            .join(Field, Field.id == Crop.field_id)
            .where(Field.farm_id.in_(farm_ids))
            .where(Crop.growth_stage != GrowthStage.HARVESTED)
        )
    ).scalar_one()

    active_laborers = (
        await db.execute(
            select(func.count(Laborer.id))
            .where(Laborer.farm_id.in_(farm_ids))
            .where(Laborer.is_active.is_(True))
        )
    ).scalar_one()

    pending_ops = (
        await db.execute(
            select(func.count(Operation.id))
            .join(Field, Field.id == Operation.field_id)
            .where(Field.farm_id.in_(farm_ids))
            .where(Operation.status.in_([OperationStatus.PENDING, OperationStatus.IN_PROGRESS]))
        )
    ).scalar_one()

    monthly_expense = (
        await db.execute(
            select(func.coalesce(func.sum(FinancialTransaction.amount), 0))
            .where(FinancialTransaction.farm_id.in_(farm_ids))
            .where(FinancialTransaction.txn_type == TxnType.EXPENSE)
            .where(FinancialTransaction.txn_date >= month_start)
        )
    ).scalar_one()

    monthly_revenue = (
        await db.execute(
            select(func.coalesce(func.sum(FinancialTransaction.amount), 0))
            .where(FinancialTransaction.farm_id.in_(farm_ids))
            .where(FinancialTransaction.txn_type == TxnType.REVENUE)
            .where(FinancialTransaction.txn_date >= month_start)
        )
    ).scalar_one()

    low_stock = (
        await db.execute(
            select(func.count(InventoryItem.id))
            .where(InventoryItem.farm_id.in_(farm_ids))
            .where(InventoryItem.quantity <= InventoryItem.reorder_level)
            .where(InventoryItem.reorder_level > 0)
        )
    ).scalar_one()

    stats = DashboardStats(
        total_area_acres=total_area,
        active_crops=active_crops,
        active_laborers=active_laborers,
        pending_operations=pending_ops,
        monthly_expense=float(monthly_expense),
        monthly_revenue=float(monthly_revenue),
        monthly_profit=float(monthly_revenue) - float(monthly_expense),
        low_stock_items=low_stock,
    )

    upcoming_rows = (
        await db.execute(
            select(Operation, Field.name)
            .join(Field, Field.id == Operation.field_id)
            .where(Field.farm_id.in_(farm_ids))
            .where(Operation.status != OperationStatus.COMPLETED)
            .where(Operation.scheduled_date.is_not(None))
            .where(Operation.scheduled_date <= horizon)
            .order_by(Operation.scheduled_date.asc())
            .limit(10)
        )
    ).all()

    upcoming = [
        UpcomingOperation(
            id=op.id,
            operation_type=op.operation_type.value,
            scheduled_date=op.scheduled_date,
            field_name=field_name,
            status=op.status.value,
        )
        for op, field_name in upcoming_rows
    ]

    alerts: list[AlertItem] = []
    if low_stock:
        alerts.append(
            AlertItem(
                level="warning",
                title="Low inventory",
                detail=f"{low_stock} item(s) at or below reorder level",
            )
        )
    overdue = [op for op, _ in upcoming_rows if op.scheduled_date and op.scheduled_date < today]
    if overdue:
        alerts.append(
            AlertItem(
                level="critical",
                title="Overdue operations",
                detail=f"{len(overdue)} operation(s) past their scheduled date",
            )
        )
    if stats.monthly_profit < 0:
        alerts.append(
            AlertItem(
                level="warning",
                title="Monthly loss",
                detail=f"Expenses exceed revenue by ₹{abs(stats.monthly_profit):,.0f} this month",
            )
        )

    return DashboardResponse(stats=stats, upcoming_operations=upcoming, alerts=alerts)
