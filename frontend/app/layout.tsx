import React from "react"
import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import "./interfaceSettings.css";
import { ThemeProvider } from "../components/theme-provider";
import SettingsButton from "../components/SettingsButton";


const _geist = Geist({ subsets: ["latin"] });
const _geistMono = Geist_Mono({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: 'Highlight AI - Instant Video Highlights',
  description: 'Upload your media and let AI generate beautiful highlight videos in seconds. Perfect for nonprofits and community organizations.',
  generator: 'v0.app',
  icons: {
    icon: [
      {
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    apple: '/apple-icon.png',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
  <html lang="en" suppressHydrationWarning>
    <body className="font-sans antialiased relative">
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
        {/* Animated Grid Background */}
        <div className="grid-background" aria-hidden="true" />
        <div className="grid-accent-glow" aria-hidden="true" />

        {/* Main Content */}
        <div className="relative z-0">
          {children}
        </div>

        {/* Floating settings button */}
        <SettingsButton />

        <Analytics />
      </ThemeProvider>
    </body>
  </html>
)
}