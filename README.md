🎬 AI Highlight Video Generator

A full-stack application that generates short-form highlight videos (30–60 seconds) from user-uploaded images and videos.

---

##Overview

This system allows users to upload media and automatically generate highlight videos through a structured processing pipeline.

The architecture is designed to support future AI-based scoring and scene detection.

---

##Core Workflow

Upload → Processing → Clip Selection → Video Assembly → Export

---

##Features

- Upload up to 10 images or video files  
- Automatic highlight video generation (30–60 seconds)  
- Image-to-video clip conversion  
- Video normalization and concatenation using FFmpeg  
- Downloadable MP4 output  
- Object storage using MinIO (S3-compatible)  
- Processing progress tracking  
- Video gallery (view, download, delete)  
- Clean, responsive web interface  

---

##Tech Stack

**Frontend**
- Next.js (React, TypeScript)
- Tailwind CSS  

**Backend**
- FastAPI (Python)  

**Video Processing**
- FFmpeg  

**Storage**
- MinIO (S3-compatible object storage)  

---

##System Architecture

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

---

##Status

**Completed**
- Full-stack application setup  
- Media upload and storage pipeline  
- Video generation with FFmpeg  
- Backend and frontend integration  
- Video preview and management UI  

**In Progress**
- Scene detection improvements  
- Highlight ranking logic  
- UI progress enhancements  

**Planned**
- AI-based scoring system  
- Background job queue  
- User authentication  
- Metadata storage  

---

##Setup

👉 See full setup instructions here: [SETUP.md](./SETUP.md)

---

##Quick Start

```bash
git clone https://github.com/NotDvaid/ai-highlight-video-generator.git
cd ai-highlight-video-generator
npm install
npm run dev
