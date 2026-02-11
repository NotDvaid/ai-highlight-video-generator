"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export default function SettingsTab() {
  const { theme, setTheme, systemTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);
  if (!mounted) return null;

  const current = theme === "system" ? systemTheme : theme;

  const buttonClass =
    "px-4 py-2 rounded-md border border-border cursor-pointer transition-colors hover:border-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent";

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-lg font-semibold text-foreground">
        Appearance
      </h2>

      <div className="flex gap-3">
        <button onClick={() => setTheme("light")} className={buttonClass}>
          Light
        </button>
        <button onClick={() => setTheme("dark")} className={buttonClass}>
          Dark
        </button>
        <button onClick={() => setTheme("system")} className={buttonClass}>
          System
        </button>
      </div>

      <p className="text-sm text-muted-foreground">
        Current theme: {current}
      </p>
    </div>
  );
}
