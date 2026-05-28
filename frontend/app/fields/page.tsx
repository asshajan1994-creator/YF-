"use client";

import * as React from "react";
import { api } from "@/lib/api";
import type { Field, Farm } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, THead, TBody, TR, TH, TD } from "@/components/ui/table";
import { formatNumber } from "@/lib/utils";

export default function FieldsPage() {
  const [fields, setFields] = React.useState<Field[]>([]);
  const [farms, setFarms] = React.useState<Farm[]>([]);

  React.useEffect(() => {
    api<Field[]>("/fields").then(setFields).catch(() => {});
    api<Farm[]>("/farms").then(setFarms).catch(() => {});
  }, []);

  const farmName = (id: number) => farms.find((f) => f.id === id)?.name ?? `Farm #${id}`;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Fields</h1>
        <p className="text-sm text-muted-foreground">Plot-level mapping, soil health and irrigation.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All fields</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <THead>
              <TR>
                <TH>Field</TH>
                <TH>Farm</TH>
                <TH>Area (acres)</TH>
                <TH>Soil pH</TH>
                <TH>Moisture %</TH>
                <TH>Irrigation</TH>
              </TR>
            </THead>
            <TBody>
              {fields.map((f) => (
                <TR key={f.id}>
                  <TD className="font-medium">{f.name}</TD>
                  <TD>{farmName(f.farm_id)}</TD>
                  <TD>{formatNumber(f.area_acres, { maximumFractionDigits: 1 })}</TD>
                  <TD>{f.soil_ph ?? "—"}</TD>
                  <TD>{f.moisture_pct ?? "—"}</TD>
                  <TD>{f.irrigation_type ?? "—"}</TD>
                </TR>
              ))}
              {fields.length === 0 && (
                <TR>
                  <TD colSpan={6} className="py-8 text-center text-sm text-muted-foreground">
                    No fields recorded yet.
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
