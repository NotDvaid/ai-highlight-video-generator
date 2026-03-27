🎬 AI Highlight Video Generator

A full-stack application that generates short-form highlight videos (30–60 seconds) from user-uploaded images and videos.

Overview

This project enables users to upload media and automatically generate highlight videos through a structured processing pipeline. The system focuses on efficiently preparing, selecting, and assembling media into a polished final output.

The architecture is designed to support future integration of AI-based scoring and scene detection.

Core Workflow

Upload → Processing → Clip Selection → Video Assembly → Export

Features
-Upload up to 10 images or video files
-Automatic highlight video generation (30–60 seconds)
-Image-to-video clip conversion
-Video normalization and concatenation using FFmpeg
-Downloadable MP4 output
-Object storage using MinIO (S3-compatible)
-Processing progress tracking
-Video gallery (view, download, delete)
-Clean, responsive web interface
 
Tech Stack

Frontend
-Next.js (React, TypeScript)
-Tailwind CSS

Backend
-FastAPI (Python)

Video Processing
-FFmpeg

Storage
-MinIO (S3-compatible object storage)

Pipeline Design (In Progress)
-Feature extraction
-Segment scoring
-Clip selection

System Architecture
Frontend (Next.js)
        ↓
Backend API (FastAPI)
        ↓
Object Storage (MinIO)
        ↓
Processing Pipeline
        ↓
FFmpeg Video Assembly
        ↓
Output Storage + Delivery

Current Status

Completed
-Full-stack application setup
-Media upload and storage pipeline
-Video generation with FFmpeg
-Backend API and frontend integration
-Video preview, download, and management UI

In Progress
-Scene detection improvements
-Highlight ranking and scoring logic
-UI progress tracking enhancements

Planned
-Background job queue for processing
-AI-based highlight scoring
-User authentication
-Metadata storage

Scope (MVP)
-No audio processing or music syncing
-No subtitles or overlays
-No advanced AI scene understanding (planned for future iterations)

Local Development
git clone <repo-url>
cd ai-highlight-video-generator
npm run dev

Local Services

Frontend: http://localhost:3000
Backend API: http://127.0.0.1:8000
API Docs: http://127.0.0.1:8000/docs
MinIO Console: http://127.0.0.1:9001
