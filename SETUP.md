#Setup Guide

This project is a full-stack highlight video generation system that processes user-uploaded media and produces a combined video output.

---

##Prerequisites

Make sure you have the following installed:

- Node.js (v18+ recommended)
- Python (3.10+)
- FFmpeg (installed and added to PATH)
- Git

Verify installations:

```bash
node -v
python --version
ffmpeg -version
```

Getting Started
1. Clone the Repository
git clone https://github.com/NotDvaid/ai-highlight-video-generator.git
cd ai-highlight-video-generator
2. Install Node Dependencies

From the root folder:

npm install

Then install frontend dependencies:

cd frontend
npm install
cd ..
3. Set Up Python Environment

Navigate to the AI service:

cd ai_service

Create a virtual environment:

python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Return to root:

cd ..
4. Install MinIO (Storage)

MinIO is used for storing generated videos.

Download MinIO:
https://dl.min.io/server/minio/release/windows-amd64/minio.exe

Place minio.exe inside:

storage/

Expected structure:

ai-highlight-video-generator/
├── frontend/
├── ai_service/
├── storage/
│   ├── minio.exe
│   └── minio-data/
├── package.json
5. Run the Application

From the root directory:

npm run dev

This starts:

Frontend (Next.js)
Backend (FastAPI)
MinIO storage server

Local Access
Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
MinIO Dashboard: http://localhost:9001

MinIO Login
Username: minioadmin
Password: minioadmin
