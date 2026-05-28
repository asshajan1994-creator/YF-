"use client";

import * as React from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { Map, Wheat, Users, ClipboardList, Wallet, AlertCircle, Sprout, TrendingUp } from "lucide-react";
import { api } from "@/lib/api";
import type { DashboardData } from "@/lib/types";
import { formatCurrency, formatNumber } from "@/lib/utils";
import { StatCard } from "@/components/dashboard/stat-card";
import { AlertsCard } from "@/components/dashboard/alerts-card";
import { UpcomingOps } from "@/components/dashboard/upcoming-ops";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function DashboardPage() {
  const [data, setData] = React.useState<DashboardData | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    api<DashboardData>("/dashboard")
      .then(setData)
      .catch((e) => setError(e.message ?? "Failed to load dashboard"));
  }, []);

  if (error) {
    return (
      <div className="rounded-md border border-destructive/40 bg-destructive/10 p-4 text-sm text-destructive">
        {error}
      </div>
    );
  }
  if (!data) {
    return <div className="text-sm text-muted-foreground">Loading dashboard…</div>;
  }

  const s = data.stats;
  const chartData = [
    { name: "Revenue", value: s.monthly_revenue },
    { name: "Expense", value: s.monthly_expense },
    { name: "Profit", value: s.monthly_profit },
  ];

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">Operations dashboard</h1>
        <p className="text-sm text-muted-foreground">
          Live overview of your farms, crops, labor and finances.
        </p>
      </header>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Total area"
          value={`${formatNumber(s.total_area_acres, { maximumFractionDigits: 1 })} acres`}
          icon={Map}
        />
        <StatCard label="Active crops" value={String(s.active_crops)} icon={Wheat} />
        <StatCard label="Active labor" value={String(s.active_laborers)} icon={Users} />
        <StatCard label="Pending operations" value={String(s.pending_operations)} icon={ClipboardList} />
        <StatCard
          label="Monthly revenue"
          value={formatCurrency(s.monthly_revenue)}
          icon={TrendingUp}
        />
        <StatCard
          label="Monthly expense"
          value={formatCurrency(s.monthly_expense)}
          icon={Wallet}
        />
        <StatCard
          label="Monthly profit"
          value={formatCurrency(s.monthly_profit)}
          trend={s.monthly_profit >= 0 ? "up" : "down"}
          delta={s.monthly_profit >= 0 ? "Above breakeven" : "Below breakeven"}
          icon={Sprout}
        />
        <StatCard label="Low stock items" value={String(s.low_stock_items)} icon={AlertCircle} />
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Monthly financial snapshot</CardTitle>
          </CardHeader>
          <CardContent className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    background: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: 8,
                  }}
                  formatter={(v: number) => formatCurrency(v)}
                />
                <Legend />
                <Bar dataKey="value" name="₹" fill="hsl(var(--primary))" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
        <AlertsCard alerts={data.alerts} />
      </div>

      <UpcomingOps items={data.upcoming_operations} />
    </div>
  );
}
