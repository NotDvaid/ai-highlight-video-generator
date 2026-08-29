"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import VideoGallery from "@/components/video-gallery";
import { ArrowLeft, Upload, Sparkles, Download, Zap, Heart } from "lucide-react";

export default function AboutPage() {
  const features = [
    {
      icon: Upload,
      title: "Upload Multiple Files",
      description:
        "Drag and drop any combination of photos and videos from your event. We support all major formats so you can upload everything in one go.",
    },
    {
      icon: Sparkles,
      title: "AI-Powered Selection",
      description:
        "Our AI analyzes every piece of media you upload, identifies the most compelling moments, and selects the best content for your highlight reel.",
    },
    {
      icon: Download,
      title: "Export and Share",
      description:
        "Once your highlight video is generated, download it instantly as a high-quality MP4 file ready to share anywhere.",
    },
    {
      icon: Zap,
      title: "No Editing Skills Required",
      description:
        "You don't need any video editing experience. Simply upload your media and let the AI handle the rest.",
    },
  ];

  return (
    <div className="min-h-screen flex flex-col">

      {/* HEADER */}
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

          {/* LEFT */}
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
            <span className="font-bold text-2xl md:text-4xl text-foreground truncate">
              Impact Reels
            </span>
          </div>

          {/* RIGHT */}
          <div className="flex items-center gap-2 w-full sm:w-auto justify-between sm:justify-end">

            <ThemeToggle />

            <div className="flex items-center gap-2">

              <Button asChild size="sm" variant="outline">
                <Link href="/">Home</Link>
              </Button>

              <Button asChild size="sm" variant="outline">
                <Link href="/history">History</Link>
              </Button>

            </div>
          </div>
        </div>
      </header>

      {/* PAGE CONTENT */}
      <div className="page-background flex-1 px-4 py-16">
        <div className="max-w-5xl mx-auto">

          {/* HEADER TEXT */}
          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
              About Impact Reels
            </h1>

            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              A free tool built to help nonprofits and community organizations
              turn event media into professional highlight videos powered by AI.
            </p>
          </div>

          {/* WHY SECTION */}
          <div className="mb-16">
            <div className="p-8 rounded-xl bg-card border border-border shadow-sm hover:shadow-md transition-all">

              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-lg bg-secondary/60 flex items-center justify-center">
                  <Heart className="w-5 h-5 text-foreground" />
                </div>

                <h2 className="text-xl font-semibold text-foreground">
                  Why We Built This
                </h2>
              </div>

              <p className="text-muted-foreground mb-4">
                Nonprofits and community organizations do incredible work every
                day, but they often lack the resources or technical expertise to
                create polished video content from their events.
              </p>

              <p className="text-muted-foreground">
                Impact Reels bridges that gap by providing an easy-to-use AI tool
                that transforms raw event media into shareable highlight reels —
                no editing experience required.
              </p>
            </div>
          </div>

          {/* HOW IT WORKS */}
          <div className="text-center mb-10">
            <h2 className="text-2xl font-semibold text-foreground">
              How It Works
            </h2>
          </div>

          {/* FEATURES */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            {features.map((feature) => (
              <div
                key={feature.title}
                className="p-6 rounded-xl bg-card border border-border shadow-sm hover:shadow-md hover:-translate-y-1 transition-all"
              >
                <div className="w-10 h-10 rounded-lg bg-secondary/60 flex items-center justify-center mb-4">
                  <feature.icon className="w-5 h-5 text-foreground" />
                </div>

                <h3 className="font-semibold text-foreground mb-2">
                  {feature.title}
                </h3>

                <p className="text-sm text-muted-foreground">
                  {feature.description}
                </p>
              </div>
            ))}

          </div>

        </div>
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