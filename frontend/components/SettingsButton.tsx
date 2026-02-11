"use client";

import { useState } from "react";
import SettingsTab from "./SettingsTab";

export default function SettingsButton() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-50 rounded-full border border-border bg-background px-4 py-2 text-sm shadow-md
                   cursor-pointer transition-colors hover:border-accent
                   focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      >
        ⚙ Settings
      </button>

      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
          <div className="relative w-full max-w-sm rounded-lg bg-background border border-border p-4">
            <button
              onClick={() => setOpen(false)}
              className="absolute right-3 top-2 rounded-md px-2 py-1 cursor-pointer
                         transition-colors hover:border hover:border-accent
                         focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
            >
              ✕
            </button>

            <SettingsTab />
          </div>
        </div>
      )}
    </>
  );
}
