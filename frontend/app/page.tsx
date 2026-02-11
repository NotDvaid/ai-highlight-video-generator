"use client";

import { useState } from "react";
import { LandingPage } from "@/components/landing-page";
import { UploadPage } from "@/components/upload-page";
import { ProcessingPage } from "@/components/processing-page";
import { ResultPage } from "@/components/result-page";
import { AboutPage } from "@/components/about-page";

type AppState = "landing" | "about" | "upload" | "processing" | "result";

export default function Home() {
  const [state, setState] = useState<AppState>("landing");
  const [, setUploadedFiles] = useState<File[]>([]);
  const [, setEventDescription] = useState("");


  const handleBack = () => {
    setState("landing");
  };

  const handleAbout = () => setState("about");

  const handleBackFromAbout = () => setState("landing");

  const handleGenerate = (files: File[], description: string) => {
    setUploadedFiles(files);
    setEventDescription(description);
    setState("processing");
  };

  const handleProcessingComplete = () => {
    setState("result");
  };

  const handleRegenerate = () => {
    setState("processing");
  };

  const handleBackToUpload = () => {
    setState("upload");
  };

  return (
    <>
      {state === "landing" && (<LandingPage onAbout={handleAbout} />
      )}
      {state === "upload" && (
        <UploadPage onBack={handleBack} onGenerate={handleGenerate} />
      )}
      {state === "processing" && (
        <ProcessingPage onComplete={handleProcessingComplete} />
      )}
      {state === "result" && (
        <ResultPage onBack={handleBackToUpload} onRegenerate={handleRegenerate} />
      )}
      {state === "about" && (
        <AboutPage onBack={handleBackFromAbout} />
      )}
    </>
  );
}
