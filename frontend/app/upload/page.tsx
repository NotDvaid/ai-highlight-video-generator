"use client";

import { UploadPage } from "@/components/upload-page";
import { useRouter } from "next/navigation";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  type CaptionEntry = {
    text: string;
    start_time: number;
    end_time: number;
  };

export default function Page() {
  const router = useRouter();


  const handleGenerate = async (
    files: File[],
    description: string,
    musicFile: File | null,
    captions: CaptionEntry[],
  ) => {
    try {
      // Show processing screen immediately
      router.push("/processing");

      const formData = new FormData();

      files.forEach((file) => {
        formData.append("files", file);
      });

      // Your backend calls this field "prompt"
      formData.append("prompt", description);

      const response = await fetch(
        `${API_URL}/create-highlight`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error(
          `Backend returned ${response.status}`
        );
      }

      const data = await response.json();

      if (!data.video_url) {
        throw new Error("Backend did not return a video URL");
      }

      // Save the generated video URL so the result page can access it
      sessionStorage.setItem(
        "videoUrl",
        data.video_url
      );

      // Move to result page
      router.push("/result");

    } catch (error) {
      console.error("Generation failed:", error);

      alert("Failed to generate video.");

      router.push("/upload");
    }
  };

  return (
    <UploadPage
      onBack={() => router.push("/")}
      onGenerate={handleGenerate}
    />
  );
}