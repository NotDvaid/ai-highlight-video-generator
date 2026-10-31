
"use client";

import { useEffect, useState } from "react";
import { useTheme } from "next-themes";
import { ThemeToggle } from "@/components/theme-toggle";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ProcessingPageProps {
  jobId: string | null;
  onDone: (videoUrl: string) => void;
  onFailed: (error: string) => void;
}

export function ProcessingPage({
  jobId,
  onDone,
  onFailed,
}: ProcessingPageProps) {
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState("Preparing your media");
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  useEffect(() => {
    if (!jobId) return;

    let active = true;
    let timeout: ReturnType<typeof setTimeout>;

    const pollProgress = async () => {
      try {
        const response = await fetch(
          `${API_URL}/progress/${jobId}`
        );

        if (!response.ok) {
          throw new Error(
            `Progress request failed: ${response.status}`
          );
        }

        const data = await response.json();

        if (!active) return;

        if (data.status === "failed") {
          onFailed(data.error || "Video generation failed.");
          return;
        }

        if (data.status === "completed") {
          if (!data.video_url) {
            onFailed("The job completed, but no video URL was returned.");
            return;
          }

          setProgress(100);
          setStage("Your highlight is ready");

          timeout = setTimeout(() => {
            if (active) onDone(data.video_url);
          }, 700);

          return;
        }

        const value = Number(data.progress ?? 0);

        const nextProgress = Number.isFinite(value)
          ? Math.min(99, Math.max(0, value))
          : 0;

        setProgress(nextProgress);

        if (data.stage) {
          setStage(data.stage);
        }
      } catch (error) {
        if (active) {
          console.error("Could not fetch generation progress:", error);
        }
      }

      if (active) {
        timeout = setTimeout(pollProgress, 1000);
      }
    };

    void pollProgress();

    return () => {
      active = false;
      clearTimeout(timeout);
    };
  }, [jobId, onDone, onFailed]);


  return (
    <div
      className={`min-h-screen flex flex-col overflow-hidden ${
        isDark
          ? "bg-[#172016] text-[#F1EFE8]"
          : "bg-[#F1EFE8] text-[#3B6D11]"
      }`}
    >
      <header className="relative z-10 border-b border-[#3B6D11]/15">
        <div className="container mx-auto flex items-center justify-between px-6 py-5">
          <span
            className={`text-2xl font-extrabold tracking-tight ${
              isDark ? "text-[#C0DD97]" : "text-[#3B6D11]"
            }`}
          >
            Impact Reel
          </span>
          <ThemeToggle />
        </div>
      </header>

      <main
        className={`relative flex flex-1 items-center justify-center overflow-hidden px-5 py-12 ${
          isDark ? "bg-[#172016]" : "bg-[#F1EFE8]"
        }`}
      >
        {/* Soft brand-colored background atmosphere */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute left-1/2 top-1/2 h-[440px] w-[440px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#97C459]/15 blur-[90px]"
        />

        <div className="relative z-10 w-full max-w-lg space-y-10 text-center">

          {/* Logo and integrated progress animation */}
          <div className="relative mx-auto flex h-[270px] w-[270px] items-center justify-center">

            {/* Soft amber glow */}
            <div
              aria-hidden="true"
              className={`pointer-events-none absolute left-1/2 top-1/2 h-[440px] w-[440px] -translate-x-1/2 -translate-y-1/2 rounded-full blur-[90px] ${
                isDark ? "bg-[#639922]/15" : "bg-[#97C459]/15"
              }`}
            />

            {/* Cinematic camera lens rings */}
            <div aria-hidden="true" className="lens-ring lens-ring-outer" />
            <div aria-hidden="true" className="lens-ring lens-ring-inner" />

            {/* Moving amber spotlight */}
            <div aria-hidden="true" className="lens-spotlight" />

            <img
              src={isDark ? "/ImpactLight.png" : "/ImpactDark.png"}
              alt="Impact Reel logo"
              className="relative z-10 h-[205px] w-[205px] object-contain drop-shadow-[0_8px_16px_rgba(59,109,17,0.18)]"
            />

            {/* Progress ring surrounding the logo */}
            <svg
              className="absolute inset-0 h-full w-full -rotate-90"
              viewBox="0 0 100 100"
              role="progressbar"
              aria-label="Video generation progress"
              aria-valuemin={0}
              aria-valuemax={100}
              aria-valuenow={Math.round(progress)}
            >
              <circle
                cx="50"
                cy="50"
                r="47"
                fill="none"
                stroke={isDark ? "#C0DD97" : "#3B6D11"}
                strokeOpacity={isDark ? "0.18" : "0.12"}
                strokeWidth="1.8"
              />

              <circle
                cx="50"
                cy="50"
                r="47"
                fill="none"
                stroke={isDark ? "#97C459" : "#639922"}
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeDasharray="295.31"
                strokeDashoffset={295.31 * (1 - progress / 100)}
                className="transition-[stroke-dashoffset] duration-700 ease-out"
              />


            </svg>
          </div>

          {/* Status */}
          <div className="space-y-3">
            <p className={`text-xs font-bold uppercase tracking-[0.28em] ${
                  isDark ? "text-[#EF9F27]" : "text-[#639922]"
                }`}>
              Your story. Your impact.
            </p>

            <h2 className={`text-3xl font-extrabold tracking-tight ${
                  isDark ? "text-[#F1EFE8]" : "text-[#3B6D11]"
                }`}>
              Creating your highlight
            </h2>

            <p
              className={`min-h-6 text-base transition-all duration-300 ${
                isDark ? "text-[#F1EFE8]/70" : "text-[#3B6D11]/70"
              }`}
            >
              {stage}
            </p>
          </div>

          {/* Progress details */}
          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span className={`font-medium ${
                      isDark ? "text-[#F1EFE8]/70" : "text-[#3B6D11]/70"
                    }`}>
                Creating your reel
              </span>

              <span className={`font-bold tabular-nums ${
                      isDark ? "text-[#C0DD97]" : "text-[#639922]"
                    }`}>
                {Math.round(progress)}%
              </span>
            </div>

            <div className={`h-2.5 overflow-hidden rounded-full ${
                    isDark ? "bg-white/10" : "bg-[#3B6D11]/10"
                  }`}>
              <div
                className={`text-sm ${
                isDark ? "text-[#F1EFE8]/75" : "text-[#3B6D11]/75"
              }`}
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Footer */}
          <div className="space-y-2 pt-2">
            <p className={`text-sm ${
                  isDark ? "text-[#F1EFE8]/75" : "text-[#3B6D11]/75"
                }`}>
              We're turning your moments into something memorable.
            </p>

            <p className={`text-xs ${
                  isDark ? "text-[#F1EFE8]/50" : "text-[#3B6D11]/50"
                }`}>
              Keep this page open while your highlight is being created.
            </p>
          </div>
        </div>

  <style jsx>{`
    .lens-ring {
      position: absolute;
      border-radius: 50%;
      pointer-events: none;
      will-change: transform;
    }

    .lens-ring-outer {
      inset: 5px;
      border: 1px solid rgba(151, 196, 89, 0.35);
      border-top-color: rgba(239, 159, 39, 0.65);
      animation: lens-rotate 16s linear infinite;
    }

    .lens-ring-inner {
      inset: 17px;
      border: 1px solid rgba(151, 196, 89, 0.25);
      border-bottom-color: rgba(239, 159, 39, 0.5);
      animation: lens-counter-rotate 11s linear infinite;
    }

    .lens-spotlight {
      position: absolute;
      inset: 5px;
      border-radius: 50%;
      pointer-events: none;
      background: conic-gradient(
        from 0deg,
        transparent 0deg,
        transparent 275deg,
        rgba(239, 159, 39, 0.05) 300deg,
        rgba(239, 159, 39, 0.8) 325deg,
        rgba(239, 159, 39, 0.12) 340deg,
        transparent 360deg
      );
      -webkit-mask: radial-gradient(
        farthest-side,
        transparent calc(100% - 3px),
        #000 calc(100% - 2px)
      );
      mask: radial-gradient(
        farthest-side,
        transparent calc(100% - 3px),
        #000 calc(100% - 2px)
      );
      animation: spotlight-sweep 5s linear infinite;
    }

    @keyframes lens-rotate {
      to {
        transform: rotate(360deg);
      }
    }

    @keyframes lens-counter-rotate {
      to {
        transform: rotate(-360deg);
      }
    }

    @keyframes spotlight-sweep {
      to {
        transform: rotate(360deg);
      }
    }

    @media (prefers-reduced-motion: reduce) {
      .lens-ring,
      .lens-spotlight {
        animation: none;
      }
    }
  `}</style>

      </main>
    </div>
  );
}
