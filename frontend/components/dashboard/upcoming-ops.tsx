import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";

interface Op {
  id: number;
  operation_type: string;
  scheduled_date: string | null;
  field_name: string;
  status: string;
}

const statusVariant: Record<string, "default" | "warning" | "destructive" | "outline"> = {
  pending: "outline",
  in_progress: "warning",
  completed: "default",
  cancelled: "destructive",
};

export function UpcomingOps({ items }: { items: Op[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Upcoming operations (next 30 days)</CardTitle>
      </CardHeader>
      <CardContent>
        {items.length === 0 ? (
          <div className="text-sm text-muted-foreground">No upcoming operations scheduled.</div>
        ) : (
          <ul className="divide-y">
            {items.map((op) => (
              <li key={op.id} className="flex items-center justify-between py-3">
                <div>
                  <div className="text-sm font-medium capitalize">{op.operation_type.replace(/_/g, " ")}</div>
                  <div className="text-xs text-muted-foreground">{op.field_name} · {formatDate(op.scheduled_date)}</div>
                </div>
                <Badge variant={statusVariant[op.status] ?? "outline"} className="capitalize">
                  {op.status.replace(/_/g, " ")}
                </Badge>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
