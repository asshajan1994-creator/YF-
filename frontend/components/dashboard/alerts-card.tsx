import { AlertTriangle, AlertCircle, Info } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface Alert {
  level: string;
  title: string;
  detail: string;
}

const iconMap: Record<string, { icon: typeof AlertTriangle; tone: string }> = {
  critical: { icon: AlertCircle, tone: "text-destructive" },
  warning: { icon: AlertTriangle, tone: "text-accent" },
  info: { icon: Info, tone: "text-primary" },
};

export function AlertsCard({ alerts }: { alerts: Alert[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Alerts</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {alerts.length === 0 && (
          <div className="text-sm text-muted-foreground">No active alerts. Everything looks good.</div>
        )}
        {alerts.map((a, i) => {
          const cfg = iconMap[a.level] ?? iconMap.info;
          const Icon = cfg.icon;
          return (
            <div key={i} className="flex items-start gap-3 rounded-md border p-3">
              <Icon className={cn("mt-0.5 h-4 w-4 shrink-0", cfg.tone)} />
              <div className="min-w-0">
                <div className="text-sm font-medium">{a.title}</div>
                <div className="text-xs text-muted-foreground">{a.detail}</div>
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
