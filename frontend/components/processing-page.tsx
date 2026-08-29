"use client";

import { useEffect, useState } from "react";
import { ThemeToggle } from "@/components/theme-toggle";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function ProcessingPage({
  jobId,
  videoReady,
  onDone,
}: {
  jobId: string | null;
  videoReady?: boolean;
  onDone: () => void;
}) {
  const [progress, setProgress] = useState(0);

  // Auto-transition when video is ready (even if polling didn't catch it)
  useEffect(() => {
    if (videoReady) {
      setProgress(100);
      setTimeout(() => {
        onDone();
      }, 500);
    }
  }, [videoReady, onDone]);

  useEffect(() => {
    if (!jobId || videoReady) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_URL}/progress/${jobId}`);
        const data = await res.json();

        const value = data.progress ?? 0;
        setProgress(value);

        if (value >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            onDone();
          }, 500);
        }
      } catch (err) {
        console.error(err);
      }
    }, 500);

    return () => clearInterval(interval);
  }, [jobId, videoReady, onDone]);

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4 flex justify-between">
          <span className="font-bold text-2xl md:text-5xl text-foreground truncate">
            Impact Reels
          </span>
          <ThemeToggle />
        </div>
      </header>

      <main className="flex-1 flex items-center justify-center">
        <div className="text-center space-y-6">
          <h2 className="text-xl font-semibold">
            Generating Highlight...
          </h2>

          <div className="relative w-28 h-28 mx-auto">
            <svg
              className="w-28 h-28 transform -rotate-90"
              viewBox="0 0 100 100"
            >
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="currentColor"
                strokeWidth="8"
                className="text-gray-300"
              />

              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="currentColor"
                strokeWidth="8"
                strokeLinecap="round"
                className="text-yellow-400 transition-all duration-500"
                strokeDasharray={`${progress * 2.83} 283`}
              />
            </svg>

            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-lg font-bold">
                {Math.round(progress)}%
              </span>
            </div>
          </div>

          <p className="text-muted-foreground">
            {progress < 30 && "Analyzing clips..."}
            {progress >= 30 && progress < 60 && "Selecting best moments..."}
            {progress >= 60 && progress < 90 && "Editing video..."}
            {progress >= 90 && "Finalizing..."}
          </p>
        </div>
      </main>
    </div>
  );
}