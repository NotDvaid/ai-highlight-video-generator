"use client";

import { Button } from "@/components/ui/button";

interface AboutPageProps {
  onBack: () => void;
}

export function AboutPage({ onBack }: AboutPageProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <span className="font-semibold text-lg text-foreground">About Impact Reels</span>
          <Button onClick={onBack} variant="outline" size="sm">
            Back
          </Button>
        </div>
      </header>

      <main className="flex-1 container mx-auto px-4 py-12 max-w-3xl">
        <h1 className="text-3xl font-bold mb-6">What it is</h1>
        <p className="text-muted-foreground mb-6">
          Impact-Reel is a highlight video generator for nonprofits and community organizations.
          It turns your event photos and videos into a short 30–60 second highlight reel—no editing skills required.
        </p>

        <h2 className="text-2xl font-semibold mb-4">How it’s used</h2>
        <ol className="list-decimal ml-6 space-y-2 text-muted-foreground">
          <li>Upload up to 10 photos and/or videos.</li>
          <li>Enter a short description of the style you want.</li>
          <li>The system processes the media and generates a silent highlight video.</li>
          <li>Download the MP4 and share it.</li>
        </ol>
      </main>

      <footer className="border-t border-border py-6">
        <div className="container mx-auto px-4 text-center text-muted-foreground text-sm">
          Built for nonprofits and community organizations
        </div>
      </footer>
    </div>
  );
}