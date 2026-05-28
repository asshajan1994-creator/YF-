"use client";

import * as React from "react";
import { api } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, THead, TBody, TR, TH, TD } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { formatCurrency, formatDate } from "@/lib/utils";

interface Operation {
  id: number;
  field_id: number;
  operation_type: string;
  status: string;
  scheduled_date: string | null;
  completed_date: string | null;
  assigned_to: string | null;
  cost: number;
}

const statusVariant: Record<string, "default" | "warning" | "destructive" | "outline"> = {
  pending: "outline",
  in_progress: "warning",
  completed: "default",
  cancelled: "destructive",
};

export default function OperationsPage() {
  const [ops, setOps] = React.useState<Operation[]>([]);

  React.useEffect(() => {
    api<Operation[]>("/operations").then(setOps).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Operations</h1>
        <p className="text-sm text-muted-foreground">Plowing, sowing, irrigation, harvesting and more.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All operations</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <THead>
              <TR>
                <TH>Type</TH>
                <TH>Scheduled</TH>
                <TH>Completed</TH>
                <TH>Assigned to</TH>
                <TH>Status</TH>
                <TH>Cost</TH>
              </TR>
            </THead>
            <TBody>
              {ops.map((o) => (
                <TR key={o.id}>
                  <TD className="font-medium capitalize">{o.operation_type.replace(/_/g, " ")}</TD>
                  <TD>{formatDate(o.scheduled_date)}</TD>
                  <TD>{formatDate(o.completed_date)}</TD>
                  <TD>{o.assigned_to ?? "—"}</TD>
                  <TD>
                    <Badge variant={statusVariant[o.status] ?? "outline"} className="capitalize">
                      {o.status.replace(/_/g, " ")}
                    </Badge>
                  </TD>
                  <TD>{formatCurrency(o.cost)}</TD>
                </TR>
              ))}
              {ops.length === 0 && (
                <TR>
                  <TD colSpan={6} className="py-8 text-center text-sm text-muted-foreground">
                    No operations logged yet.
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
