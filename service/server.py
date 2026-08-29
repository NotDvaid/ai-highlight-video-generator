from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from typing import List
import os
import shutil
import uuid
import subprocess

from dotenv import load_dotenv



from service.models.asset import Asset
from service.ai.prompt_engine import accept_request
from service.ai.planner import Planner
from service.renderer.composer import Composer
from service.renderer.ffmpeg_render import FFmpegRenderer
from service.storage.minio_client import upload_file

load_dotenv()

# ---------------- SETUP ----------------
MAX_FILES = 10

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- STATIC ----------------
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

# ---------------- EDITING ----------------
def apply_prompt_edit(input_path, output_path, prompt):
    filters = []
    prompt = prompt.lower()

    if "black and white" in prompt:
        filters.append("hue=s=0")
    if "bright" in prompt:
        filters.append("eq=brightness=0.05")
    if "blur" in prompt:
        filters.append("boxblur=2")

    cmd = ["ffmpeg", "-y", "-i", input_path]

    if filters:
        cmd += ["-vf", ",".join(filters)]

    cmd += [
        "-c:v", "libx264",
        "-c:a", "aac",
        "-movflags", "+faststart",
        output_path
    ]

    subprocess.run(cmd, check=True)

@app.post("/create-highlight")
def create_highlight(
    files: List[UploadFile] = File(...),
    prompt: str = Form("")
):

    if len(files) > MAX_FILES:
        return {"error": f"Max {MAX_FILES} files allowed"}

    assets = []

    for file in files:

        asset_id = uuid.uuid4()

        extension = os.path.splitext(file.filename)[1]
        file_path = os.path.join(
            UPLOAD_FOLDER,
            f"{asset_id}{extension}"
        )

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        media_type = (
            "video"
            if file.content_type and file.content_type.startswith("video/")
            else "image"
        )

        asset = Asset(
            asset_id=asset_id,
            path=file_path,
            media_type=media_type,
            duration=5.0,
            width=1920,
            height=1080,
            has_audio=media_type == "video",
            fps=30.0 if media_type == "video" else 0.0,
        )

        assets.append(asset)

    planner = Planner()
    composer = Composer()
    renderer = FFmpegRenderer()

    ai_plan = accept_request(prompt, assets)

    timeline = planner.create_timeline(
        assets,
        ai_plan
    )

    render_plan = composer.compose(timeline)

    output_path = renderer.render(render_plan)

    video_name = os.path.basename(output_path)

    video_url = upload_file(
        output_path,
        video_name
    )

    return {
        "video_url": video_url
    }