# AI Video Generator – Setup Guide

This project generates AI-powered highlight videos from uploaded media using:

* Next.js (Frontend)
* FastAPI + Python (Backend)
* FFmpeg (Video Processing)
* MinIO (Object Storage)

Follow the steps below to run the project locally.

---

# Prerequisites

Before starting, make sure you have the following installed:

• Node.js (v18+ recommended)
• Python (3.10+)
• FFmpeg installed and available in PATH
• Git

You can verify installations with:

```
node -v
python --version
ffmpeg -version
```

---

# 1. Repository

```
cd AIvideoGenerator
```

---

# 2. Install Node Dependencies

From the project root:

```
npm install
```

---

# 3. Install Python Dependencies

Navigate to the AI service folder:

```
cd ai-service
```

Create a virtual environment (recommended):

```
python -m venv venv
```

Activate it:

Windows:

```
venv\Scripts\activate
```

Mac/Linux:

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Return to the root directory:

```
cd ..
```

---

# 4. Install MinIO

MinIO is used for storing generated highlight videos.

Download it here:

https://min.io/download

After downloading **minio.exe**, place it in this folder:

```
AIvideoGenerator/storage/
```

Your folder structure should look like:

```
AIvideoGenerator
 ├ frontend
 ├ ai-service
 ├ storage
 │   ├ minio.exe
 │   └ minio-data
 ├ package.json
 └ SETUP.md
```

---

# 5. Start the Project

From the project root run:

```
npm run dev
```

This command will start:

• MinIO Storage Server
• FastAPI Backend
• Next.js Frontend

---

# 6. Access the Application

Frontend:

```
http://localhost:3000
```

Backend API:

```
http://localhost:8000
```

MinIO Dashboard:

```
http://localhost:9001
```

Login credentials:

```
Username: minioadmin
Password: minioadmin
```

---

# How the System Works

1. User uploads images/videos in the frontend.
2. Files are sent to the FastAPI backend.
3. FFmpeg processes the media.
4. The AI model selects highlight segments.
5. A final 60-second highlight video is generated.
6. The video is uploaded to MinIO storage.
7. The frontend displays the video preview.

---

# Running the System

Every time you want to run the project:

```
npm run dev
```

This launches everything automatically.

---

# Common Issues

## MinIO not found

Make sure:

```
storage/minio.exe
```

exists in the storage folder.

---

## FFmpeg errors

Ensure FFmpeg is installed and available in PATH.

Test with:


ffmpeg -version


# Notes

Large binaries like `minio.exe` are not stored in the Git repository because GitHub limits files to 100MB.

 must download MinIO manually.

