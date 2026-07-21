"use client";

import { useEffect, useState } from "react";
import { Download, Trash2, Play } from "lucide-react";

type Video = {
  name: string;
  url: string;
};

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function VideoGallery() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);
  const [enabled, setEnabled] = useState(false);

  // 🗑 DELETE VIDEO
  const deleteVideo = async (name: string) => {
    const confirmDelete = confirm("Delete this video?");
    if (!confirmDelete) return;

    try {
      const res = await fetch(
        `${API_URL}/video?object_name=${name}`,
        { method: "DELETE" }
      );

      if (!res.ok) throw new Error("Delete failed");

      const updated = videos.filter((v) => v.name !== name);
      setVideos(updated);

      localStorage.setItem("video_history", JSON.stringify(updated));
    } catch (err) {
      console.error("Delete error:", err);
      alert("Delete not available yet");
    }
  };

  // 📦 LOAD FROM LOCAL STORAGE
  useEffect(() => {
    try {
      const local = localStorage.getItem("video_history");

      if (local) {
        const parsed = JSON.parse(local);

        if (Array.isArray(parsed) && parsed.length > 0) {
          setVideos(parsed);
          setEnabled(true);
          return;
        }
      }

      setEnabled(false);
    } catch (err) {
      console.warn("Gallery error:", err);
      setEnabled(false);
    }
  }, []);

  // 🚫 NOTHING TO SHOW
  if (!enabled) {
    return (
      <div className="text-center text-muted-foreground py-12">
        No videos yet
      </div>
    );
  }

  return (
    <div className="space-y-10">
      {/* HEADER */}
      <div>
        <h2 className="text-2xl font-bold text-foreground">
          Your Highlights
        </h2>
        <p className="text-muted-foreground text-sm">
          Hover to preview • Click to watch
        </p>
      </div>

      {/* GRID */}
      {videos.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {videos.map((video) => (
            <div
              key={video.name}
              onClick={() => setSelectedVideo(video)}
              className="group rounded-2xl overflow-hidden bg-card border border-border
              shadow-sm hover:shadow-2xl hover:-translate-y-1 hover:scale-[1.03]
              transition-all duration-300 cursor-pointer"
            >
              {/* VIDEO */}
              <div
                className="relative aspect-video bg-black overflow-hidden"
                onMouseEnter={(e) => {
                  const vid = e.currentTarget.querySelector("video");
                  if (vid) {
                    vid.currentTime = 0;
                    vid.play().catch(() => {});
                  }
                }}
                onMouseLeave={(e) => {
                  const vid = e.currentTarget.querySelector("video");
                  if (vid) {
                    vid.pause();
                    vid.currentTime = 0;
                  }
                }}
              >
                <video
                  src={video.url}
                  muted
                  playsInline
                  preload="metadata"
                  className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                />

                {/* PLAY ICON */}
                <div className="absolute inset-0 flex items-center justify-center opacity-100 group-hover:opacity-0 transition pointer-events-none">
                  <div className="bg-black/50 rounded-full p-3">
                    <Play className="w-6 h-6 text-white" />
                  </div>
                </div>

                {/* OVERLAY */}
                <div className="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition pointer-events-none" />
              </div>

              {/* INFO */}
              <div className="p-4 space-y-2">
                <p className="text-sm font-semibold text-foreground truncate">
                  Highlight Video
                </p>

                <div className="flex justify-between items-center mt-2">
                  <div className="flex gap-2">
                    {/* DOWNLOAD */}
                    <a
                      href={video.url}
                      download
                      onClick={(e) => e.stopPropagation()}
                      className="flex items-center gap-1 px-3 py-1.5 rounded-md text-sm font-medium
                      text-yellow-600 bg-yellow-500/10
                      hover:bg-yellow-500/20 hover:text-yellow-700
                      transition-all duration-200"
                    >
                      <Download className="w-4 h-4" />
                      Download
                    </a>

                    {/* DELETE */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteVideo(video.name);
                      }}
                      className="flex items-center gap-1 px-3 py-1.5 rounded-md text-sm font-medium
                      text-red-600 bg-red-500/10
                      hover:bg-red-500/20 hover:text-red-700
                      transition-all duration-200"
                    >
                      <Trash2 className="w-4 h-4" />
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center text-muted-foreground py-12">
          No videos yet
        </div>
      )}

      {/* 🎬 MODAL */}
      {selectedVideo && (
        <div
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50"
          onClick={() => setSelectedVideo(null)}
        >
          <div
            className="relative w-[90%] max-w-4xl"
            onClick={(e) => e.stopPropagation()}
          >
            <video
              src={selectedVideo.url}
              controls
              autoPlay
              className="w-full rounded-xl"
            />

            <button
              onClick={() => setSelectedVideo(null)}
              className="absolute top-2 right-2 bg-black/60 text-white px-3 py-1 rounded-lg"
            >
              ✕
            </button>
          </div>
        </div>
      )}
    </div>
  );
}