"use client";

import * as React from "react";
import { api } from "@/lib/api";
import type { FinancialTransaction } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, THead, TBody, TR, TH, TD } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { formatCurrency, formatDate } from "@/lib/utils";

export default function FinancePage() {
  const [rows, setRows] = React.useState<FinancialTransaction[]>([]);
  const [summary, setSummary] = React.useState<{ expense_total: number; revenue_total: number; profit: number } | null>(null);

  React.useEffect(() => {
    api<FinancialTransaction[]>("/financial").then(setRows).catch(() => {});
    api<{ expense_total: number; revenue_total: number; profit: number; breakdown: Record<string, number> }>(
      "/financial/summary",
    )
      .then((s) => setSummary({ expense_total: s.expense_total, revenue_total: s.revenue_total, profit: s.profit }))
      .catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Finance</h1>
        <p className="text-sm text-muted-foreground">Costs, revenue and profitability.</p>
      </div>

      {summary && (
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardContent className="p-5">
              <div className="text-xs uppercase tracking-wide text-muted-foreground">Total revenue</div>
              <div className="mt-1 text-2xl font-semibold">{formatCurrency(summary.revenue_total)}</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-5">
              <div className="text-xs uppercase tracking-wide text-muted-foreground">Total expense</div>
              <div className="mt-1 text-2xl font-semibold">{formatCurrency(summary.expense_total)}</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-5">
              <div className="text-xs uppercase tracking-wide text-muted-foreground">Profit</div>
              <div className={`mt-1 text-2xl font-semibold ${summary.profit < 0 ? "text-destructive" : "text-primary"}`}>
                {formatCurrency(summary.profit)}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Transactions</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <THead>
              <TR>
                <TH>Date</TH>
                <TH>Type</TH>
                <TH>Category</TH>
                <TH>Counterparty</TH>
                <TH>Description</TH>
                <TH>Amount</TH>
              </TR>
            </THead>
            <TBody>
              {rows.map((r) => (
                <TR key={r.id}>
                  <TD>{formatDate(r.txn_date)}</TD>
                  <TD>
                    <Badge variant={r.txn_type === "revenue" ? "default" : "destructive"} className="capitalize">
                      {r.txn_type}
                    </Badge>
                  </TD>
                  <TD className="capitalize">{r.category.replace(/_/g, " ")}</TD>
                  <TD>{r.counterparty ?? "—"}</TD>
                  <TD className="max-w-xs truncate">{r.description ?? "—"}</TD>
                  <TD className="font-medium">{formatCurrency(r.amount, r.currency)}</TD>
                </TR>
              ))}
              {rows.length === 0 && (
                <TR>
                  <TD colSpan={6} className="py-8 text-center text-sm text-muted-foreground">
                    No transactions recorded yet.
                  </TD>
                </TR>
              )}
            </TBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
