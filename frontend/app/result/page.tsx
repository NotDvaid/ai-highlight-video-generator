"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ResultPage from "@/components/result-page";

export default function Page() {
  const router = useRouter();
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  useEffect(() => {
    const storedVideoUrl = sessionStorage.getItem("videoUrl");

    if (!storedVideoUrl) {
      router.push("/upload");
      return;
    }

    setVideoUrl(storedVideoUrl);
  }, [router]);

  return (
    <ResultPage
      videoUrl={videoUrl}
      onRegenerate={() => router.push("/upload")}
      onStartOver={() => {
        sessionStorage.removeItem("videoUrl");
        router.push("/");
      }}
    />
  );
}