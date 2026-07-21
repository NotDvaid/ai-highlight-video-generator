"use client";

import AppHeader from "@/components/app-header";
import VideoGallery from "@/components/video-gallery";

export default function ResultPage({
  videoUrl,
  onRegenerate,
  onStartOver,
}: {
  videoUrl: string | null;
  onRegenerate: () => void;
  onStartOver: () => void;
}) {
  return (
    <div className="min-h-screen flex flex-col">
      <AppHeader />

      <main className="flex-1 text-center p-6 space-y-6">
        <h1 className="text-2xl font-bold">Your Highlight Video</h1>

        {videoUrl ? (
          <video
            src={videoUrl}
            controls
            className="w-full max-w-2xl mx-auto"
          />
        ) : (
          <p>No video found</p>
        )}

        <div className="flex gap-3 justify-center">
          <button onClick={onRegenerate}>Regenerate</button>
          <button onClick={onStartOver}>Start Over</button>
        </div>

        <VideoGallery />
      </main>
    </div>
  );
}