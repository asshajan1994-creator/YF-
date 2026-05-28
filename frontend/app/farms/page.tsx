"use client";

import * as React from "react";
import { Plus } from "lucide-react";
import { api } from "@/lib/api";
import type { Farm } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, THead, TBody, TR, TH, TD } from "@/components/ui/table";
import { formatNumber, formatDate } from "@/lib/utils";

export default function FarmsPage() {
  const [farms, setFarms] = React.useState<Farm[]>([]);
  const [error, setError] = React.useState<string | null>(null);
  const [showForm, setShowForm] = React.useState(false);
  const [form, setForm] = React.useState({
    name: "",
    location: "",
    district: "",
    total_area_acres: 0,
    soil_type: "",
  });

  const load = React.useCallback(() => {
    api<Farm[]>("/farms")
      .then(setFarms)
      .catch((e) => setError(e.message));
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  async function onCreate(e: React.FormEvent) {
    e.preventDefault();
    try {
      await api("/farms", { method: "POST", body: { ...form, total_area_acres: Number(form.total_area_acres) } });
      setShowForm(false);
      setForm({ name: "", location: "", district: "", total_area_acres: 0, soil_type: "" });
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create farm");
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Farms</h1>
          <p className="text-sm text-muted-foreground">Manage farm registrations and land details.</p>
        </div>
        <Button onClick={() => setShowForm((v) => !v)}>
          <Plus className="h-4 w-4" />
          {showForm ? "Close" : "Add farm"}
        </Button>
      </div>

      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>New farm</CardTitle>
          </CardHeader>
          <CardContent>
            <form className="grid gap-4 md:grid-cols-2" onSubmit={onCreate}>
              <div className="space-y-1.5">
                <label className="text-sm font-medium">Name</label>
                <Input
                  value={form.name}
                  onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                  required
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium">Location</label>
                <Input
                  value={form.location}
                  onChange={(e) => setForm((f) => ({ ...f, location: e.target.value }))}
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium">District</label>
                <Input
                  value={form.district}
                  onChange={(e) => setForm((f) => ({ ...f, district: e.target.value }))}
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium">Total area (acres)</label>
                <Input
                  type="number"
                  step="0.1"
                  min={0}
                  value={form.total_area_acres}
                  onChange={(e) => setForm((f) => ({ ...f, total_area_acres: Number(e.target.value) }))}
                />
              </div>
              <div className="space-y-1.5 md:col-span-2">
                <label className="text-sm font-medium">Soil type</label>
                <Input
                  value={form.soil_type}
                  onChange={(e) => setForm((f) => ({ ...f, soil_type: e.target.value }))}
                  placeholder="e.g. Red loam, Black cotton, Alluvial"
                />
              </div>
              <div className="md:col-span-2">
                <Button type="submit">Create farm</Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {error && (
        <div className="rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </div>
      )}

      <Card>
        <CardContent className="p-0">
          <Table>
            <THead>
              <TR>
                <TH>Name</TH>
                <TH>Location</TH>
                <TH>District</TH>
                <TH>Area (acres)</TH>
                <TH>Soil</TH>
                <TH>Added</TH>
              </TR>
            </THead>
            <TBody>
              {farms.map((f) => (
                <TR key={f.id}>
                  <TD className="font-medium">{f.name}</TD>
                  <TD>{f.location ?? "—"}</TD>
                  <TD>{f.district ?? "—"}</TD>
                  <TD>{formatNumber(f.total_area_acres, { maximumFractionDigits: 1 })}</TD>
                  <TD>{f.soil_type ?? "—"}</TD>
                  <TD>{formatDate(f.created_at)}</TD>
                </TR>
              ))}
              {farms.length === 0 && (
                <TR>
                  <TD colSpan={6} className="py-8 text-center text-sm text-muted-foreground">
                    No farms yet. Click &ldquo;Add farm&rdquo; to register your first farm.
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
