"use client";

import * as React from "react";
import { api } from "@/lib/api";
import type { Crop } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, THead, TBody, TR, TH, TD } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { formatDate, formatNumber } from "@/lib/utils";

const stageVariant: Record<string, "default" | "warning" | "outline" | "secondary"> = {
  planned: "outline",
  seedling: "secondary",
  vegetative: "secondary",
  flowering: "warning",
  fruiting: "warning",
  maturity: "default",
  harvested: "default",
};

export default function CropsPage() {
  const [crops, setCrops] = React.useState<Crop[]>([]);

  React.useEffect(() => {
    api<Crop[]>("/crops").then(setCrops).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Crops</h1>
        <p className="text-sm text-muted-foreground">Plan and monitor crops across growth stages.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Active crops</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <THead>
              <TR>
                <TH>Crop</TH>
                <TH>Variety</TH>
                <TH>Sowing</TH>
                <TH>Expected harvest</TH>
                <TH>Stage</TH>
                <TH>Expected yield (kg)</TH>
              </TR>
            </THead>
            <TBody>
              {crops.map((c) => (
                <TR key={c.id}>
                  <TD className="font-medium">{c.crop_name}</TD>
                  <TD>{c.variety ?? "—"}</TD>
                  <TD>{formatDate(c.sowing_date)}</TD>
                  <TD>{formatDate(c.expected_harvest_date)}</TD>
                  <TD>
                    <Badge variant={stageVariant[c.growth_stage] ?? "outline"} className="capitalize">
                      {c.growth_stage}
                    </Badge>
                  </TD>
                  <TD>{c.expected_yield_kg ? formatNumber(c.expected_yield_kg) : "—"}</TD>
                </TR>
              ))}
              {crops.length === 0 && (
                <TR>
                  <TD colSpan={6} className="py-8 text-center text-sm text-muted-foreground">
                    No crops planned yet.
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
