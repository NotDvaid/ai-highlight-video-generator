"use client";

import { useEffect, useState } from "react";
import AppHeader from "@/components/app-header";

export function ProcessingPage() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 95) return prev;
        return prev + (prev < 60 ? 8 : 2);
      });
    }, 300);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      <AppHeader />

      <main className="flex-1 flex items-center justify-center">
        <div className="text-center space-y-6">
          <h2 className="text-xl font-semibold">
            Generating Highlight...
          </h2>

          <div className="relative w-28 h-28 mx-auto">
            <svg className="w-28 h-28 transform -rotate-90" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="45" fill="none" stroke="gray" strokeWidth="8"/>
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="gold"
                strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray={`${progress * 2.83} 283`}
              />
            </svg>

            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-lg font-bold">
                {Math.round(progress)}%
              </span>
            </div>
          </div>

          <p>
            {progress < 30 && "Analyzing clips..."}
            {progress >= 30 && progress < 60 && "Finding highlights..."}
            {progress >= 60 && progress < 90 && "Editing video..."}
            {progress >= 90 && "Finalizing..."}
          </p>
        </div>
      </main>
    </div>
  );
}