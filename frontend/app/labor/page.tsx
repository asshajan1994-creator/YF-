"use client";

import * as React from "react";
import { api } from "@/lib/api";
import type { Laborer } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, THead, TBody, TR, TH, TD } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { formatCurrency } from "@/lib/utils";

export default function LaborPage() {
  const [laborers, setLaborers] = React.useState<Laborer[]>([]);

  React.useEffect(() => {
    api<Laborer[]>("/labor").then(setLaborers).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Labor</h1>
        <p className="text-sm text-muted-foreground">Workers, attendance and wage tracking.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Workers</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <THead>
              <TR>
                <TH>Name</TH>
                <TH>Phone</TH>
                <TH>Type</TH>
                <TH>Daily wage</TH>
                <TH>Status</TH>
              </TR>
            </THead>
            <TBody>
              {laborers.map((l) => (
                <TR key={l.id}>
                  <TD className="font-medium">{l.full_name}</TD>
                  <TD>{l.phone ?? "—"}</TD>
                  <TD className="capitalize">{l.labor_type}</TD>
                  <TD>{formatCurrency(l.daily_wage)}</TD>
                  <TD>
                    <Badge variant={l.is_active ? "default" : "outline"}>
                      {l.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </TD>
                </TR>
              ))}
              {laborers.length === 0 && (
                <TR>
                  <TD colSpan={5} className="py-8 text-center text-sm text-muted-foreground">
                    No labor records yet.
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
