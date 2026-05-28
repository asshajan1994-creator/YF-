"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Sprout,
  Tractor,
  Users,
  Package,
  Wallet,
  Wheat,
  Map,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/farms", label: "Farms", icon: Map },
  { href: "/fields", label: "Fields", icon: Sprout },
  { href: "/crops", label: "Crops", icon: Wheat },
  { href: "/operations", label: "Operations", icon: Tractor },
  { href: "/labor", label: "Labor", icon: Users },
  { href: "/inventory", label: "Inventory", icon: Package },
  { href: "/finance", label: "Finance", icon: Wallet },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-60 shrink-0 flex-col border-r bg-card md:flex">
      <div className="flex h-14 items-center gap-2 border-b px-4">
        <div className="grid h-8 w-8 place-items-center rounded-md bg-primary text-primary-foreground">
          <Sprout className="h-4 w-4" />
        </div>
        <div>
          <div className="text-sm font-semibold leading-tight">FarmBrain</div>
          <div className="text-[10px] uppercase tracking-wider text-muted-foreground">ERP</div>
        </div>
      </div>
      <nav className="flex flex-1 flex-col gap-1 p-2">
        {navItems.map(({ href, label, icon: Icon }) => {
          const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors",
                active
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground",
              )}
            >
              <Icon className="h-4 w-4" />
              {label}
            </Link>
          );
        })}
      </nav>
      <div className="border-t p-3 text-xs text-muted-foreground">
        v0.1.0 · Tamil Nadu edition
      </div>
    </aside>
  );
}
