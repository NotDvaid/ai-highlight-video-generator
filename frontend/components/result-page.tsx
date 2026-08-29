"use client";

import VideoGallery from "./video-gallery";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import { Download, RefreshCw, Sparkles } from "lucide-react";

interface ResultPageProps {
  videoUrl: string | null;
  onRegenerate: () => void;
  onStartOver: () => void;
}

export default function ResultPage({
  videoUrl,
  onRegenerate,
  onStartOver,
}: ResultPageProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4 flex justify-between">
          <span className="font-bold text-2xl md:text-5xl text-foreground">
            Impact Reels
          </span>
          <ThemeToggle />
        </div>
      </header>

      <main className="flex-1 container mx-auto px-4 py-10">
        <div className="space-y-6 text-center">
          <h1 className="text-3xl font-bold">Your Highlight Video</h1>

          <div className="bg-black rounded-xl overflow-hidden">
            {videoUrl ? (
              <video
                src={videoUrl}
                controls
                autoPlay
                className="w-full"
              />
            ) : (
              <div className="p-10 text-muted-foreground">
                No video available
              </div>
            )}
          </div>

          <div className="flex flex-col gap-3 max-w-md mx-auto">
            <Button asChild>
              <a href={videoUrl || "#"} download>
                <Download className="mr-2 w-4 h-4" />
                Download
              </a>
            </Button>

            <Button variant="outline" onClick={onRegenerate}>
              <RefreshCw className="mr-2 w-4 h-4" />
              Regenerate
            </Button>

            <Button onClick={onStartOver}>
              Create New Video
            </Button>
          </div>

          <VideoGallery />
        </div>
      </main>
    </div>
  );
}