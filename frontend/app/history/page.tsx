"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import VideoGallery from "@/components/video-gallery";
import { ArrowLeft } from "lucide-react";

export default function HistoryPage() {
  return (
    <div className="min-h-screen flex flex-col">

      {/* HEADER */}
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">

          {/* LEFT SIDE */}
          <div className="flex items-center gap-2 min-w-0">
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

          {/* RIGHT SIDE */}
          <div className="flex items-center gap-2">

            <ThemeToggle />

            <div className="flex items-center gap-2">

              {/* HOME */}
              <Button asChild size="sm" variant="outline" className="cursor-pointer">
                <Link href="/">Home</Link>
              </Button>

              {/* ABOUT */}
              <Button asChild size="sm" variant="outline" className="cursor-pointer">
                <Link href="/about">About</Link>
              </Button>

            </div>

          </div>

        </div>
      </header>

      {/* BACK BUTTON */}
      <div className="container mx-auto px-4 pt-4">
        <Button asChild variant="ghost" size="icon" className="cursor-pointer">
          <Link href="/">
            <ArrowLeft />
          </Link>
        </Button>
      </div>

      {/* MAIN */}
      <div className="page-background flex-1">

        <main className="container mx-auto px-4 py-12 max-w-6xl">

          <div className="space-y-12">

            {/* HERO */}
            <div className="text-center space-y-2">
              <h1 className="text-3xl md:text-5xl font-bold text-foreground">
                Video History
              </h1>

              <p className="text-muted-foreground">
                View and manage your generated highlight videos
              </p>
            </div>

            {/* VIDEO GALLERY */}
            <VideoGallery />

          </div>

        </main>

      </div>

      {/* FOOTER */}
      <footer className="border-t border-border py-6">
        <div className="container mx-auto px-4 text-center text-muted-foreground text-sm">
          Built for nonprofits and community organizations
        </div>
      </footer>

    </div>
  );
}