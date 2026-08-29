"use client";

import { useState } from "react";
import { LandingPage } from "@/components/landing-page";
import { UploadPage } from "@/components/upload-page";
import { ProcessingPage } from "@/components/processing-page";
import ResultPage from "@/components/result-page";

type AppState = "landing" | "upload" | "processing" | "result";
type CaptionEntry = { text: string; start_time: number; end_time: number };

const API_URL = "http://localhost:8000";

export default function Home() {
  const [state, setState] = useState<AppState>("landing");
  const [resultVideo, setResultVideo] = useState<string | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);

  const handleGetStarted = () => setState("upload");

  const handleGenerate = async (
    files: File[],
    description: string,
    musicFile: File | null,
    captions: CaptionEntry[]
  ) => {
    // Reset state and navigate to processing page immediately for visual feedback
    setResultVideo(null);
    setJobId(null);
    setState("processing");

    try {
      const formData = new FormData();

      files.forEach((file) => {
        formData.append("files", file);
      });

      formData.append("prompt", description);

      if (musicFile) {
        formData.append("music_file", musicFile);
      }

      if (captions.length > 0) {
        formData.append("captions_json", JSON.stringify(captions));
      }

      const res = await fetch(`${API_URL}/create-highlight`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const error = await res.json().catch(() => ({ detail: "Upload failed" }));
        throw new Error(error.detail || "Upload failed");
      }

      const data = await res.json();

      if (!data.video_url) {
        throw new Error("No video URL returned from server");
      }

      setResultVideo(data.video_url);
      setJobId(data.job_id);
    } catch (err) {
      console.error(err);
      alert(err instanceof Error ? err.message : "Failed to generate video");
      setState("upload");
    }
  };

  return (
    <>
      {state === "landing" && (
        <LandingPage onGetStarted={handleGetStarted} />
      )}

      {state === "upload" && (
        <UploadPage
          onGenerate={handleGenerate}
          onBack={() => setState("landing")}
        />
      )}

      {state === "processing" && (
        <ProcessingPage
          jobId={jobId}
          videoReady={!!resultVideo}
          onDone={() => setState("result")}
        />
      )}

      {state === "result" && (
        <ResultPage
          videoUrl={resultVideo}
          onRegenerate={() => setState("processing")}
          onStartOver={() => setState("upload")}
        />
      )}
    </>
  );
}