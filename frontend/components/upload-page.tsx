"use client";

import React from "react";
import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ThemeToggle } from "@/components/theme-toggle";
import { ArrowLeft, Upload, X, FileImage, FileVideo, Sparkles, Trash2, Plus, Music, AlertCircle } from "lucide-react";


type CaptionEntry = { text: string; start_time: number; end_time: number };

interface UploadPageProps {
  onBack: () => void;
  onGenerate: (files: File[], description: string, musicFile: File | null, captions: CaptionEntry[]) => void;
}

// Supported file types for validation
const SUPPORTED_VIDEO_EXTENSIONS = [".mp4", ".mov", ".mkv", ".avi", ".webm"];
const SUPPORTED_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp", ".gif"];
const SUPPORTED_VIDEO_MIMES = ["video/mp4", "video/quicktime", "video/x-matroska", "video/x-msvideo", "video/webm"];
const SUPPORTED_IMAGE_MIMES = ["image/png", "image/jpeg", "image/webp", "image/gif"];

function isFileSupported(file: File): boolean {
  const ext = file.name.toLowerCase().slice(file.name.lastIndexOf("."));
  const mime = file.type.toLowerCase();

  // Check MIME type first
  if (SUPPORTED_VIDEO_MIMES.includes(mime) || SUPPORTED_IMAGE_MIMES.includes(mime)) {
    return true;
  }

  // Fallback to extension check
  if (SUPPORTED_VIDEO_EXTENSIONS.includes(ext) || SUPPORTED_IMAGE_EXTENSIONS.includes(ext)) {
    return true;
  }

  return false;
}

function getUnsupportedFileMessage(files: File[]): string | null {
  const unsupported = files.filter((f) => !isFileSupported(f));
  if (unsupported.length === 0) return null;

  const names = unsupported.map((f) => f.name).join(", ");
  return `Unsupported file(s): ${names}. Please use .mp4, .mov, or .mkv for videos, or .png, .jpg, .jpeg for images.`;
}

export function UploadPage({ onBack, onGenerate }: UploadPageProps) {

  const [files, setFiles] = useState<File[]>([]);
  const [description, setDescription] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [musicFile, setMusicFile] = useState<File | null>(null);
  const [musicEnabled, setMusicEnabled] = useState(false);
  const [captionsEnabled, setCaptionsEnabled] = useState(false);
  const [captions, setCaptions] = useState<Array<{text: string, start_time: number, end_time: number}>>([]);
  const [fileError, setFileError] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    setFileError(null);

    const droppedFiles = Array.from(e.dataTransfer.files);

    // Check for unsupported files
    const errorMsg = getUnsupportedFileMessage(droppedFiles);
    if (errorMsg) {
      setFileError(errorMsg);
    }

    // Only add supported files
    const supportedFiles = droppedFiles.filter(isFileSupported);
    if (supportedFiles.length > 0) {
      setFiles((prev) => [...prev, ...supportedFiles]);
    }
  }, []);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFileError(null);

      const selectedFiles = Array.from(e.target.files);

      // Check for unsupported files
      const errorMsg = getUnsupportedFileMessage(selectedFiles);
      if (errorMsg) {
        setFileError(errorMsg);
      }

      // Only add supported files
      const supportedFiles = selectedFiles.filter(isFileSupported);
      if (supportedFiles.length > 0) {
        setFiles((prev) => [...prev, ...supportedFiles]);
      }
    }
  }, []);

  const removeFile = useCallback((index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const getFileIcon = (file: File) => {
    if (file.type.startsWith("video/")) {
      return <FileVideo className="w-5 h-5 text-accent" />;
    }
    return <FileImage className="w-5 h-5 text-accent" />;
  };

  return (
    <div className="min-h-screen flex flex-col">

      {/* HEADER */}
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">

          <div className="flex items-center gap-2">
            {/* Light Mode Logo */}
<img
  src="/ImpactLight.png"
  alt="Impact Reels logo"
  className="w-40 h-auto rounded-lg block dark:hidden"
/>

{/* Dark Mode Logo */}
<img
  src="/ImpactDark.png"
  alt="Impact Reels logo"
  className="w-40 h-auto rounded-lg hidden dark:block"
/>

            <span className="font-bold text-2xl md:text-5xl text-foreground truncate">
              Impact Reels
            </span>
          </div>

          <ThemeToggle />
        </div>
      </header>

      {/* BACKGROUND */}
      <div className="page-background flex-1">

        <main className="container mx-auto px-4 py-8 max-w-2xl">

          {/* BACK BUTTON */}
          <Button
            variant="ghost"
            size="icon"
            className="cursor-pointer mb-4"
            onClick={onBack}
          >
            <ArrowLeft className="w-8 h-8" />
          </Button>

          <div className="space-y-8">

            {/* TITLE */}
            <div className="text-center space-y-2">
              <h1 className="text-2xl md:text-3xl font-bold text-foreground">
                Upload Your Media
              </h1>

              <p className="text-muted-foreground">
                Add photos and videos from your event
              </p>
            </div>

            {/* FILE ERROR ALERT */}
            {fileError && (
              <div className="flex items-start gap-3 p-4 rounded-lg bg-destructive/10 border border-destructive/30 text-destructive">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-sm font-medium">Unsupported File Type</p>
                  <p className="text-sm mt-1">{fileError}</p>
                </div>
                <button
                  onClick={() => setFileError(null)}
                  className="text-destructive/70 hover:text-destructive"
                  aria-label="Dismiss error"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            )}

            {/* DROP ZONE */}
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={`
                border-2 border-dashed rounded-xl p-12 text-center transition-all cursor-pointer
                bg-card shadow-sm hover:shadow-md hover:scale-[1.01]
                ${isDragging ? "border-accent bg-accent/10" : "border-border hover:border-accent"}
              `}
              onClick={() => document.getElementById("file-input")?.click()}
            >
              <input
                id="file-input"
                type="file"
                multiple
                accept=".mp4,.mov,.mkv,.avi,.webm,.png,.jpg,.jpeg,.webp,.gif,video/mp4,video/quicktime,video/x-matroska,image/png,image/jpeg,image/webp"
                onChange={handleFileSelect}
                className="hidden"
              />

              <div className="flex flex-col items-center gap-4">

                <div className="w-16 h-16 rounded-full bg-secondary flex items-center justify-center">
                  <Upload className="w-8 h-8 text-muted-foreground" />
                </div>

                <div>
                  <p className="font-medium text-foreground">
                    Drag and drop files here
                  </p>

                  <p className="text-sm text-muted-foreground mt-1">
                    or click to browse
                  </p>
                </div>

                <p className="text-xs text-muted-foreground">
                  Supports images & videos
                </p>

              </div>
            </div>

            {/* FILE LIST */}
            {files.length > 0 && (
              <div className="space-y-3">

                <p className="text-sm font-medium text-foreground">
                  {files.length} file{files.length !== 1 && "s"} selected
                </p>

                <div className="space-y-2 max-h-48 overflow-y-auto">

                  {files.map((file, index) => (
                    <div
                      key={`${file.name}-${index}`}
                      className="flex items-center gap-3 p-3 rounded-lg bg-card border border-border"
                    >

                      {getFileIcon(file)}

                      <span className="flex-1 text-sm text-foreground truncate">
                        {file.name}
                      </span>

                      <span className="text-xs text-muted-foreground">
                        {(file.size / 1024 / 1024).toFixed(1)} MB
                      </span>

                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 cursor-pointer"
                        onClick={() => removeFile(index)}
                      >
                        <X className="w-4 h-4" />
                      </Button>

                    </div>
                  ))}

                </div>

                {/* RESET FILES */}
                <Button
                  variant="outline"
                  className="w-full cursor-pointer"
                  onClick={() => setFiles([])}
                >
                  Upload Different Files
                </Button>

              </div>
            )}

            {/* DESCRIPTION CARD */}
            <div className="space-y-3 bg-card border border-border rounded-xl p-4 shadow-sm">

              <label className="text-sm font-medium text-foreground">
                Describe your event (optional)
              </label>

              <Textarea
                placeholder="e.g., Annual charity fundraiser, community picnic..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="min-h-24 bg-card border border-border rounded-lg p-3 text-foreground placeholder:text-muted-foreground"
              />

            </div>

            {/* BACKGROUND MUSIC — optional */}
            <div className="space-y-3 bg-card border border-border rounded-xl p-4 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-foreground">Background Music</label>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    Optional. Mixes a music track under your video's original audio.
                  </p>
                </div>
                <button
                  onClick={() => {
                    setMusicEnabled(!musicEnabled);
                    if (musicEnabled) setMusicFile(null);
                  }}
                  className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors focus:outline-none ${
                    musicEnabled ? "bg-accent" : "bg-muted"
                  }`}
                  role="switch"
                  aria-checked={musicEnabled}
                >
                  <span className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${
                    musicEnabled ? "translate-x-5" : "translate-x-1"
                  }`} />
                </button>
              </div>

              {musicEnabled && (
                musicFile ? (
                  <div className="flex items-center justify-between bg-secondary rounded-lg px-3 py-2">
                    <div className="flex items-center gap-2">
                      <Music className="w-4 h-4 text-accent" />
                      <span className="text-sm text-foreground truncate">{musicFile.name}</span>
                    </div>
                    <button
                      onClick={() => setMusicFile(null)}
                      className="ml-2 text-muted-foreground hover:text-destructive transition-colors"
                      aria-label="Remove music file"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                ) : (
                  <label className="flex items-center justify-center gap-2 border border-dashed border-border rounded-lg p-4 cursor-pointer hover:bg-secondary transition-colors">
                    <Music className="w-4 h-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Click to upload audio file</span>
                    <input
                      type="file"
                      accept="audio/mp3,audio/mpeg,audio/wav,audio/aac,audio/ogg,audio/flac,audio/*"
                      className="hidden"
                      onChange={(e) => setMusicFile(e.target.files?.[0] ?? null)}
                    />
                  </label>
                )
              )}
            </div>

            {/* CAPTIONS — optional toggle */}
            <div className="space-y-3 bg-card border border-border rounded-xl p-4 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-foreground">Captions</label>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    Add timed text overlays to your highlight video
                  </p>
                </div>
                <button
                  onClick={() => {
                    setCaptionsEnabled(!captionsEnabled);
                    if (captionsEnabled) setCaptions([]);
                  }}
                  className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors focus:outline-none ${
                    captionsEnabled ? "bg-accent" : "bg-muted"
                  }`}
                  role="switch"
                  aria-checked={captionsEnabled}
                >
                  <span
                    className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${
                      captionsEnabled ? "translate-x-5" : "translate-x-1"
                    }`}
                  />
                </button>
              </div>

              {captionsEnabled && (
                <div className="space-y-2">
                  {captions.length === 0 && (
                    <p className="text-xs text-muted-foreground italic">
                      No captions yet. Click "Add Caption" to start.
                    </p>
                  )}

                  {captions.map((caption, i) => (
                    <div key={i} className="flex gap-2 items-center">
                      <input
                        type="text"
                        placeholder="Caption text..."
                        value={caption.text}
                        onChange={(e) => {
                          const updated = [...captions];
                          updated[i] = { ...updated[i], text: e.target.value };
                          setCaptions(updated);
                        }}
                        className="flex-1 bg-card border border-border rounded-lg px-3 py-1.5 text-sm text-foreground placeholder:text-muted-foreground"
                      />
                      <input
                        type="number"
                        step="0.1"
                        min="0"
                        placeholder="Start (s)"
                        value={caption.start_time}
                        onChange={(e) => {
                          const updated = [...captions];
                          updated[i] = { ...updated[i], start_time: parseFloat(e.target.value) || 0 };
                          setCaptions(updated);
                        }}
                        className="w-24 bg-card border border-border rounded-lg px-3 py-1.5 text-sm text-foreground"
                      />
                      <input
                        type="number"
                        step="0.1"
                        min="0"
                        placeholder="End (s)"
                        value={caption.end_time}
                        onChange={(e) => {
                          const updated = [...captions];
                          updated[i] = { ...updated[i], end_time: parseFloat(e.target.value) || 0 };
                          setCaptions(updated);
                        }}
                        className="w-24 bg-card border border-border rounded-lg px-3 py-1.5 text-sm text-foreground"
                      />
                      <button
                        onClick={() => setCaptions(captions.filter((_, idx) => idx !== i))}
                        className="text-muted-foreground hover:text-destructive transition-colors"
                        aria-label="Remove caption"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  ))}

                  {captions.length < 20 && (
                    <button
                      onClick={() => setCaptions([...captions, { text: "", start_time: 0, end_time: 3 }])}
                      className="text-sm text-accent hover:underline flex items-center gap-1 mt-1"
                    >
                      <Plus className="w-3 h-3" /> Add Caption
                    </button>
                  )}
                </div>
              )}
            </div>

            {/* GENERATE BUTTON */}
            <Button
              size="lg"
              className="w-full text-lg py-6 cursor-pointer transition-all hover:scale-[1.02] hover:bg-accent hover:text-accent-foreground"
              disabled={files.length === 0}
              onClick={() => onGenerate(files, description, musicFile, captions)}
            >
              <Sparkles className="w-5 h-5 mr-2" />
              Generate Highlight Video
            </Button>

          </div>
        </main>

      </div>
    </div>
  );
}
