from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    crops,
    dashboard,
    farms,
    fields,
    financial,
    harvest,
    inventory,
    labor,
    operations,
    users,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(farms.router, prefix="/farms", tags=["farms"])
api_router.include_router(fields.router, prefix="/fields", tags=["fields"])
api_router.include_router(crops.router, prefix="/crops", tags=["crops"])
api_router.include_router(operations.router, prefix="/operations", tags=["operations"])
api_router.include_router(labor.router, prefix="/labor", tags=["labor"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(financial.router, prefix="/financial", tags=["financial"])
api_router.include_router(harvest.router, prefix="/harvest", tags=["harvest"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
