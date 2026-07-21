"use client";

import { useState } from "react";
import { LandingPage } from "@/components/landing-page";
import { UploadPage } from "@/components/upload-page";
import { ProcessingPage } from "@/components/processing-page";
import ResultPage from "@/components/result-page";

type AppState = "landing" | "upload" | "processing" | "preview";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function Home() {
  const [state, setState] = useState<AppState>("landing");
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  const handleGenerate = async (files: File[], prompt: string) => {
  setState("processing");

  try {
    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    formData.append("prompt", prompt);

    const res = await fetch(`${API_URL}/create-highlight`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    setVideoUrl(data.video_url);

    // ONLY switch AFTER backend finishes
    setState("preview");

  } catch (err) {
    console.error(err);
    alert("Failed to generate video");
    setState("upload");
  }
};

  return (
    <>
      {state === "landing" && (
        <LandingPage onGetStarted={() => setState("upload")} />
      )}

      {state === "upload" && (
        <UploadPage
          onGenerate={handleGenerate}
          onBack={() => setState("landing")}
        />
      )}

      {state === "processing" && <ProcessingPage />}

      {state === "preview" && (
        <ResultPage
          videoUrl={videoUrl}
          onRegenerate={() => setState("upload")}
          onStartOver={() => setState("landing")}
        />
      )}
    </>
  );
}