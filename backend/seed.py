"""Seed demo data so dashboards have something to show.

Usage:
    python seed.py
"""
import asyncio
from datetime import date, timedelta

from sqlalchemy import select

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import AsyncSessionLocal, engine
from app.models.crop import Crop, GrowthStage
from app.models.farm import Farm
from app.models.field import Field
from app.models.financial import FinancialTransaction, TxnCategory, TxnType
from app.models.inventory import InputCategory, InventoryItem
from app.models.labor import Laborer, LaborType
from app.models.operation import Operation, OperationStatus, OperationType
from app.models.user import User, UserRole


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        existing = (await db.execute(select(User).where(User.email == "demo@farmbrain.in"))).scalar_one_or_none()
        if existing:
            print("Demo data already exists — skipping seed.")
            return

        admin = User(
            email="demo@farmbrain.in",
            full_name="Karthik Murugan",
            phone="+91 98765 43210",
            hashed_password=hash_password("demo1234"),
            role=UserRole.ADMIN,
        )
        db.add(admin)
        await db.flush()

        farm = Farm(
            name="Velliangiri Estate",
            owner_id=admin.id,
            location="Pollachi",
            district="Coimbatore",
            state="Tamil Nadu",
            latitude=10.6597,
            longitude=77.0083,
            total_area_acres=42.5,
            soil_type="Red loam",
            climate_zone="Tropical semi-arid",
        )
        db.add(farm)
        await db.flush()

        north_field = Field(farm_id=farm.id, name="North Block", area_acres=18.0, soil_ph=6.8,
                            moisture_pct=58, irrigation_type="Drip")
        south_field = Field(farm_id=farm.id, name="South Block", area_acres=12.5, soil_ph=7.1,
                            moisture_pct=42, irrigation_type="Flood")
        west_field = Field(farm_id=farm.id, name="West Plot", area_acres=12.0, soil_ph=6.5,
                           moisture_pct=63, irrigation_type="Drip")
        db.add_all([north_field, south_field, west_field])
        await db.flush()

        today = date.today()
        crops = [
            Crop(field_id=north_field.id, crop_name="Paddy", variety="ADT 43",
                 sowing_date=today - timedelta(days=70),
                 expected_harvest_date=today + timedelta(days=45),
                 growth_stage=GrowthStage.FLOWERING,
                 expected_yield_kg=14000, estimated_cost=85000),
            Crop(field_id=south_field.id, crop_name="Sugarcane", variety="Co 86032",
                 sowing_date=today - timedelta(days=210),
                 expected_harvest_date=today + timedelta(days=120),
                 growth_stage=GrowthStage.VEGETATIVE,
                 expected_yield_kg=42000, estimated_cost=140000),
            Crop(field_id=west_field.id, crop_name="Turmeric", variety="Erode Local",
                 sowing_date=today - timedelta(days=180),
                 expected_harvest_date=today + timedelta(days=30),
                 growth_stage=GrowthStage.MATURITY,
                 expected_yield_kg=9500, estimated_cost=62000),
        ]
        db.add_all(crops)
        await db.flush()

        ops = [
            Operation(field_id=north_field.id, crop_id=crops[0].id,
                      operation_type=OperationType.IRRIGATION,
                      status=OperationStatus.PENDING,
                      scheduled_date=today + timedelta(days=1),
                      assigned_to="Murugan team", cost=2500),
            Operation(field_id=south_field.id, crop_id=crops[1].id,
                      operation_type=OperationType.FERTILIZATION,
                      status=OperationStatus.IN_PROGRESS,
                      scheduled_date=today,
                      assigned_to="Velu", cost=8500),
            Operation(field_id=west_field.id, crop_id=crops[2].id,
                      operation_type=OperationType.HARVESTING,
                      status=OperationStatus.PENDING,
                      scheduled_date=today + timedelta(days=20),
                      assigned_to="Harvest crew", cost=22000),
            Operation(field_id=north_field.id, crop_id=crops[0].id,
                      operation_type=OperationType.PESTICIDE,
                      status=OperationStatus.PENDING,
                      scheduled_date=today - timedelta(days=2),
                      assigned_to="Krishnan", cost=4200),
        ]
        db.add_all(ops)

        laborers = [
            Laborer(farm_id=farm.id, full_name="Velu Subramanian",
                    phone="+91 99425 11122", labor_type=LaborType.SKILLED, daily_wage=650),
            Laborer(farm_id=farm.id, full_name="Lakshmi Devi",
                    phone="+91 99425 22233", labor_type=LaborType.UNSKILLED, daily_wage=400),
            Laborer(farm_id=farm.id, full_name="Krishnan Pandian",
                    phone="+91 99425 33344", labor_type=LaborType.SKILLED, daily_wage=600),
            Laborer(farm_id=farm.id, full_name="Selvi Ramamurthy",
                    phone="+91 99425 44455", labor_type=LaborType.UNSKILLED, daily_wage=400),
            Laborer(farm_id=farm.id, full_name="Arun Kumar",
                    phone="+91 99425 55566", labor_type=LaborType.CONTRACTOR, daily_wage=900),
        ]
        db.add_all(laborers)

        inventory = [
            InventoryItem(farm_id=farm.id, name="ADT 43 Paddy Seed",
                          category=InputCategory.SEED, quantity=120, unit="kg",
                          unit_cost=85, reorder_level=50, storage_location="Bin A"),
            InventoryItem(farm_id=farm.id, name="Urea",
                          category=InputCategory.FERTILIZER, quantity=80, unit="kg",
                          unit_cost=12, reorder_level=100, npk_ratio="46-0-0",
                          storage_location="Bin B"),
            InventoryItem(farm_id=farm.id, name="DAP",
                          category=InputCategory.FERTILIZER, quantity=250, unit="kg",
                          unit_cost=27, reorder_level=150, npk_ratio="18-46-0",
                          storage_location="Bin B"),
            InventoryItem(farm_id=farm.id, name="Chlorpyrifos",
                          category=InputCategory.PESTICIDE, quantity=12, unit="L",
                          unit_cost=480, reorder_level=15,
                          expiry_date=today + timedelta(days=180),
                          storage_location="Locked cabinet"),
            InventoryItem(farm_id=farm.id, name="Diesel",
                          category=InputCategory.OTHER, quantity=180, unit="L",
                          unit_cost=92, reorder_level=100, storage_location="Tank 2"),
        ]
        db.add_all(inventory)

        # Spread transactions across the current month.
        txns = [
            FinancialTransaction(farm_id=farm.id, txn_type=TxnType.EXPENSE,
                                 category=TxnCategory.INPUTS, txn_date=today - timedelta(days=20),
                                 amount=24500, counterparty="AgriMart Pollachi",
                                 description="Urea + DAP purchase", hsn_code="3102", gst_pct=5),
            FinancialTransaction(farm_id=farm.id, txn_type=TxnType.EXPENSE,
                                 category=TxnCategory.LABOR, txn_date=today - timedelta(days=14),
                                 amount=18200, description="Weekly wages"),
            FinancialTransaction(farm_id=farm.id, txn_type=TxnType.EXPENSE,
                                 category=TxnCategory.WATER, txn_date=today - timedelta(days=10),
                                 amount=3200, description="Borewell electricity"),
            FinancialTransaction(farm_id=farm.id, txn_type=TxnType.REVENUE,
                                 category=TxnCategory.CROP_SALE, txn_date=today - timedelta(days=7),
                                 amount=185000, counterparty="Coimbatore Mandi",
                                 description="Turmeric advance sale", hsn_code="0910", gst_pct=5),
            FinancialTransaction(farm_id=farm.id, txn_type=TxnType.EXPENSE,
                                 category=TxnCategory.EQUIPMENT, txn_date=today - timedelta(days=3),
                                 amount=6800, description="Tractor service"),
            FinancialTransaction(farm_id=farm.id, txn_type=TxnType.REVENUE,
                                 category=TxnCategory.SUBSIDY, txn_date=today - timedelta(days=2),
                                 amount=22000, description="PM-KISAN installment"),
        ]
        db.add_all(txns)

        await db.commit()
        print("Seeded demo data: 1 admin, 1 farm, 3 fields, 3 crops, 4 operations,")
        print("                  5 laborers, 5 inventory items, 6 transactions.")


if __name__ == "__main__":
    asyncio.run(seed())
