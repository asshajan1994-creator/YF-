"use client";

import * as React from "react";
import { api } from "@/lib/api";
import type { InventoryItem } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, THead, TBody, TR, TH, TD } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { formatCurrency, formatDate, formatNumber } from "@/lib/utils";

export default function InventoryPage() {
  const [items, setItems] = React.useState<InventoryItem[]>([]);

  React.useEffect(() => {
    api<InventoryItem[]>("/inventory").then(setItems).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Inventory</h1>
        <p className="text-sm text-muted-foreground">Seeds, fertilizers, pesticides and tools.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Stock</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <THead>
              <TR>
                <TH>Item</TH>
                <TH>Category</TH>
                <TH>Quantity</TH>
                <TH>Reorder level</TH>
                <TH>Unit cost</TH>
                <TH>Expiry</TH>
                <TH>Stock status</TH>
              </TR>
            </THead>
            <TBody>
              {items.map((i) => {
                const low = i.reorder_level > 0 && i.quantity <= i.reorder_level;
                return (
                  <TR key={i.id}>
                    <TD className="font-medium">{i.name}</TD>
                    <TD className="capitalize">{i.category.replace(/_/g, " ")}</TD>
                    <TD>{formatNumber(i.quantity)} {i.unit}</TD>
                    <TD>{formatNumber(i.reorder_level)} {i.unit}</TD>
                    <TD>{formatCurrency(i.unit_cost)}</TD>
                    <TD>{formatDate(i.expiry_date)}</TD>
                    <TD>
                      <Badge variant={low ? "destructive" : "default"}>{low ? "Low" : "OK"}</Badge>
                    </TD>
                  </TR>
                );
              })}
              {items.length === 0 && (
                <TR>
                  <TD colSpan={7} className="py-8 text-center text-sm text-muted-foreground">
                    No inventory items yet.
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
