# AIvideoGenerator

## Description
This project is an AI-powered Highlight Video Generator designed to help nonprofits and community organizations quickly create short-form promotional videos. The MVP allows users to upload photos and videos, provide a short text prompt describing the desired style, and receive a polished 30–60 second highlight video.

The system works similarly to CapCut’s auto-cut feature. It is not a chatbot. Users simply upload media and provide a description, and the system generates a silent highlight video that can be downloaded in common formats such as MP4.

The primary MVP workflow is:

Upload → Analysis → Simple Cut → Export

---

## Links
(To be added later)

---

## Technologies

Frontend:
- React / Next.js
- TypeScript
- HTML
- CSS

Backend:
- FastAPI

Video Processing
- FFmpeg
- MoviePy

Automation / Workflow:
- n8n

Storage:
- MinIO

Optional / Supporting:
- Supabase (authentication and metadata)

---

## Working Features (MVP Scope)

- Upload up to 10 media files (photos and/or videos)
- Enforced maximum file size per upload
- Text prompt input for AI-guided editing
- Automatic generation of 30–60 second highlight video
- Silent video output (audio not included in MVP)
- Download/export generated video
- Media stored using MinIO object storage
- Lightweight, simple, and visually clean web UI
- Basic processing status (processing / completed / failed)

---

## MVP Non-Goals
- No audio processing or music syncing
- No captions or text overlays
- No advanced AI scene understanding
- No user customization beyond a simple text prompt
- No videos longer than the 30-60 second output range

---

## Architecture Overview (MVP)

```text
[React / Next.js Web App]
      |
      | 1) Upload media + prompt
      v
[FastAPI Backend Service]
      |
      | 2) Store uploaded media
      v
[MinIO Object Storage]  <--- input files (photos/videos)
      |
      | 3) Create processing job
      v
[Ai Processing Service]
      |
      | 4) - Scene detection
      |    - Highlight selection
      |    - Clip extraction
      v
[FFmpeg / MoviePy]
      |
      | 5) Video assembly
      v
[MinIO Output Storage]  <--- output MP4
      |
      | 6) Provide download link
      v
[React / Next.js Web App]
```

---
## Current Sprint Status
Sprint Goal

Implement the core upload → AI processing → video export pipeline.
---

Completed

Next.js frontend interface

File upload UI

FastAPI backend service

Basic highlight generation pipeline

FFmpeg video processing integration
---

In Progress

Scene detection integration

Highlight ranking improvements

Output video generation pipeline
---

Next Steps

Improve scene ranking logic

Add job queue for video processing

Improve frontend progress feedback

Integrate storage fully with MinIO


## Installation (Development)

Clone the repository:

git clone <repo-url>
cd AIvideoGenerator
---
Start Backend
cd ai-service
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python -m uvicorn server:app --reload
---
Start Frontend
cd frontend
npm install
npm run dev
---

Frontend runs on:

http://localhost:3000

Backend runs on:

http://127.0.0.1:8000
---
# Team Name 

Hydro 

Spring 2026 

AI Highlight Video Generator


# Team roles 

Dino Maksumic, 20% Programmer, 20% Documentation Lead, 60% Testing Lead 

Mohammed Islam, 20% Programmer, 50% Lead Programmer, 30% Client Liaison 

David Jones, 40% Programmer, 60% UI designer 

Rahsun Mclaurin, 20% Programmer, 60% Data Modeler, 20% Project Manager

