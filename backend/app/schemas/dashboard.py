from datetime import date

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_area_acres: float
    active_crops: int
    active_laborers: int
    pending_operations: int
    monthly_expense: float
    monthly_revenue: float
    monthly_profit: float
    low_stock_items: int


class UpcomingOperation(BaseModel):
    id: int
    operation_type: str
    scheduled_date: date | None
    field_name: str
    status: str


class AlertItem(BaseModel):
    level: str
    title: str
    detail: str


class DashboardResponse(BaseModel):
    stats: DashboardStats
    upcoming_operations: list[UpcomingOperation]
    alerts: list[AlertItem]
