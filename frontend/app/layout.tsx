import React from "react"
import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import { ThemeProvider } from '@/components/theme-provider'
import './interfaceSettings.css';

const _geist = Geist({ subsets: ["latin"] });
const _geistMono = Geist_Mono({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: 'Impact Reels - AI-Powered Highlight Videos',
  description:
    'Upload your media and let AI generate beautiful highlight videos in seconds. Perfect for nonprofits and community organizations.',
  generator: 'v0.app',

  icons: {
    icon: [
      {
        url: '/ImpactLight.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/ImpactDark.png',
        media: '(prefers-color-scheme: dark)',
      },
    ],
    apple: '/apple-icon.png',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="font-sans antialiased">
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
        
        <Analytics />
      </body>
    </html>
  )
}