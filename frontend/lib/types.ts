export type UserRole = "admin" | "manager" | "supervisor" | "farmer" | "accountant";

export interface User {
  id: number;
  email: string;
  full_name: string;
  phone: string | null;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Farm {
  id: number;
  name: string;
  owner_id: number;
  location: string | null;
  district: string | null;
  state: string;
  latitude: number | null;
  longitude: number | null;
  total_area_acres: number;
  soil_type: string | null;
  climate_zone: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface Field {
  id: number;
  farm_id: number;
  name: string;
  area_acres: number;
  soil_ph: number | null;
  moisture_pct: number | null;
  irrigation_type: string | null;
  created_at: string;
  updated_at: string;
}

export type GrowthStage =
  | "planned"
  | "seedling"
  | "vegetative"
  | "flowering"
  | "fruiting"
  | "maturity"
  | "harvested";

export interface Crop {
  id: number;
  field_id: number;
  crop_name: string;
  variety: string | null;
  sowing_date: string | null;
  expected_harvest_date: string | null;
  growth_stage: GrowthStage;
  expected_yield_kg: number | null;
  actual_yield_kg: number | null;
  estimated_cost: number | null;
  created_at: string;
  updated_at: string;
}

export interface Laborer {
  id: number;
  farm_id: number;
  full_name: string;
  phone: string | null;
  labor_type: "skilled" | "unskilled" | "contractor";
  daily_wage: number;
  is_active: boolean;
}

export interface InventoryItem {
  id: number;
  farm_id: number;
  name: string;
  category: "seed" | "fertilizer" | "pesticide" | "fungicide" | "tool" | "spare_part" | "other";
  quantity: number;
  unit: string;
  unit_cost: number;
  reorder_level: number;
  expiry_date: string | null;
  storage_location: string | null;
}

export interface FinancialTransaction {
  id: number;
  farm_id: number;
  txn_type: "expense" | "revenue";
  category: string;
  txn_date: string;
  amount: number;
  currency: string;
  counterparty: string | null;
  description: string | null;
}

export interface DashboardData {
  stats: {
    total_area_acres: number;
    active_crops: number;
    active_laborers: number;
    pending_operations: number;
    monthly_expense: number;
    monthly_revenue: number;
    monthly_profit: number;
    low_stock_items: number;
  };
  upcoming_operations: Array<{
    id: number;
    operation_type: string;
    scheduled_date: string | null;
    field_name: string;
    status: string;
  }>;
  alerts: Array<{
    level: string;
    title: string;
    detail: string;
  }>;
}
