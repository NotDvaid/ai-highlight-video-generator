# AI VIDEO GENERATOR — SETUP GUIDE

## Project Overview

This project generates AI-powered highlight videos from uploaded images and videos.

### Technologies
- Next.js — Frontend
- FastAPI — Backend
- FFmpeg — Video processing and rendering
- Python — Backend processing
- Node.js — Frontend tooling

---

## Prerequisites

Install the following:

- Node.js 18 or newer
- Python 3.13
- FFmpeg, available in PATH
- Git

Verify installations:

```bash
node -v
npm -v
python --version
ffmpeg -version
```

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/GGC-SD/AIvideoGenerator.git
cd AIvideoGenerator
```

---

## Step 2 — Install Node Dependencies

From the project root:

```bash
npm install
```

Install frontend dependencies:

```bash
cd frontend
npm install
cd ..
```

---

## Step 3 — Set Up Python

Create a virtual environment from the project root:

```bash
python -m venv .venv
```

Activate the environment.

Windows:

```bash
.venv\Scripts\activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Step 4 — Project Structure

```text
AIvideoGenerator/
│
├── frontend/
│
├── service/
│   ├── ai/
│   ├── jobs/
│   ├── media/
│   ├── models/
│   ├── renderer/
│   ├── storage/
│   ├── uploads/
│   ├── server.py
│   └── video_orchestrator.py
│
├── .venv/
├── package.json
└── requirements.txt
```

---

## Step 5 — Storage

MinIO is present in the project from an earlier storage implementation.

It does not need to be downloaded, installed, or configured to run the current application.

The project currently uses local filesystem storage for uploaded media and generated videos.

Cloudflare R2 is planned as the future storage solution. MinIO will be removed as part of that transition.

---

## Step 6 — Start the Application

From the project root:

```bash
npm run dev
```

This starts:

- Next.js frontend
- FastAPI backend

---

## Step 7 — Access the Application

Frontend:

http://localhost:3000

Backend:

http://localhost:8000

FastAPI documentation:

http://localhost:8000/docs

---

## How the System Works

1. User uploads images and videos through the frontend.
2. Files are sent to the FastAPI backend.
3. Backend saves uploaded files locally.
4. Capture timestamps are extracted when available.
5. A background job is created.
6. VideoOrchestrator coordinates video generation.
7. MediaAnalyzer analyzes uploaded assets.
8. Prompt Engine interprets editing instructions.
9. Planner creates the video timeline.
10. Composer creates the rendering plan.
11. FFmpegRenderer renders the video.
12. Generated MP4 is stored locally.
13. Frontend retrieves job progress and the generated video.

---

## Running the Application

From the project root:

```bash
npm run dev
```

Open:

http://localhost:3000

---

## Common Issues

### Python Dependencies Failing

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### FFmpeg Errors

Ensure FFmpeg is installed and available in PATH.

Verify:

```bash
ffmpeg -version
```

### Frontend or Backend Not Starting

Install root dependencies:

```bash
npm install
```

Install frontend dependencies:

```bash
cd frontend
npm install
cd ..
```

Verify that the Python virtual environment exists and that backend dependencies are installed.

---

## Development Philosophy

Inspect → Understand → Improve → Test → Repeat.

Preserve existing functionality and avoid introducing unnecessary dependencies or architectural changes.