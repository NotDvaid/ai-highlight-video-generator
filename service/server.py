
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from datetime import datetime
from dotenv import load_dotenv
from service.video_orchestrator import VideoOrchestrator

import os
import shutil
import uuid
import subprocess
import time

from service.models.requests import AssetUpload
from service.jobs.job_manager import (
    create_job,
    get_job,
    update_job,
)

load_dotenv()

MAX_FILES = 10

app = FastAPI()



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
STORAGE_FOLDER = os.path.join(BASE_DIR, "storage")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STORAGE_FOLDER, exist_ok=True)

app.mount(
    "/videos",
    StaticFiles(directory=STORAGE_FOLDER),
    name="videos",
)

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_FOLDER),
    name="uploads",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/progress/{job_id}")
def get_progress(job_id: str):
    job = get_job(job_id)

    if job is None:
        return {"status": "not_found", "progress": 0}

    return job

def report_job_progress(job_id: str,progress: int,stage: str,):
    update_job(job_id,progress=progress,stage=stage,)

def process_video_job(job_id, assets, prompt, chronological):
    update_job(
        job_id,
        status="processing",
        progress=5,
        stage="Starting video generation",
    )

    try:
        orchestrator = VideoOrchestrator()

        output_path = orchestrator.orchestrate(
            assets=assets,
            prompt=prompt,
            chronological=chronological,
            progress_callback=lambda progress, stage: report_job_progress(
                job_id,
                progress,
                stage,
            ),
        )

        if not output_path or not os.path.isfile(output_path):
            raise FileNotFoundError(
                "Video rendering finished, but the output file was not found."
            )

        video_filename = os.path.basename(output_path)
        video_url = f"/videos/{video_filename}"

        update_job(
            job_id,
            status="completed",
            progress=100,
            stage="Video ready",
            video_url=video_url,
            error=None,
        )

    except Exception as error:
        print(f"[JOB ERROR] {job_id}: {error}")

        update_job(
            job_id,
            status="failed",
            error=str(error),
            stage="Video generation failed",
        )

@app.post("/test-job")
def test_job():
    job_id = create_job()

    update_job(
        job_id,
        status="processing",
        progress=30,
        stage="Analyzing media",
    )

    return {"job_id": job_id}

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
        output_path,
    ]

    subprocess.run(cmd, check=True)


def get_capture_time(file_path: str) -> datetime | None:
    """
    Read image timestamps from EXIF first, then fall back to FFprobe
    metadata for videos and other supported media containers.
    """

    # 1. Read image EXIF metadata.
    try:
        from PIL import Image
        import piexif

        with Image.open(file_path) as image:
            exif_bytes = image.info.get("exif")

        if exif_bytes:
            exif = piexif.load(exif_bytes)

            value = (
                exif.get("Exif", {}).get(
                    piexif.ExifIFD.DateTimeOriginal
                )
                or exif.get("0th", {}).get(
                    piexif.ImageIFD.DateTime
                )
            )

            if value:
                if isinstance(value, bytes):
                    value = value.decode("utf-8")

                return datetime.strptime(
                    value,
                    "%Y:%m:%d %H:%M:%S",
                )

    except (ImportError, OSError, ValueError, KeyError, TypeError):
        pass


       # 2. Read video metadata using FFprobe.
    try:
        import json
        import subprocess
        from zoneinfo import ZoneInfo

        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-show_entries", "format_tags=creation_time",
                "-of", "json",
                file_path,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        metadata = json.loads(result.stdout)

        creation_time = (
            metadata.get("format", {})
            .get("tags", {})
            .get("creation_time")
        )

        if not creation_time:
            for stream in metadata.get("streams", []):
                creation_time = (
                    stream.get("tags", {}).get("creation_time")
                )

                if creation_time:
                    break

        if creation_time:
            parsed = datetime.fromisoformat(
                creation_time.replace("Z", "+00:00")
            )

            if parsed.tzinfo is not None:
                parsed = parsed.astimezone(
                    ZoneInfo("America/New_York")
                ).replace(tzinfo=None)

            return parsed

    except (
        subprocess.SubprocessError,
        json.JSONDecodeError,
        ValueError,
        OSError,
    ):
        pass

    return None


@app.post("/create-highlight")
def create_highlight(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    prompt: str = Form(""),
):
    request_started = time.perf_counter()
    stage_started = request_started

    if not files:
        return {"error": "Please upload at least one file."}

    if len(files) > MAX_FILES:
        return {"error": f"Max {MAX_FILES} files allowed"}

    assets = []

    # Save uploads and extract their timestamps.
    for file in files:
        asset_id = uuid.uuid4()

        extension = os.path.splitext(file.filename or "")[1]

        file_path = os.path.join(
            UPLOAD_FOLDER,
            f"{asset_id}{extension}",
        )

        with open(file_path, "wb") as destination:
            shutil.copyfileobj(file.file, destination)

        media_type = (
            "video"
            if file.content_type
            and file.content_type.startswith("video/")
            else "image"
        )

        capture_time = get_capture_time(file_path)

        asset = AssetUpload(
            asset_id=asset_id,
            path=file_path,
            media_type=media_type,
            capture_time=capture_time,
        )

        print(
            f"CAPTURE TIME: {file.filename} -> {capture_time}"
        )

        assets.append(asset)


    print(
        f"[TIMING] Save files + timestamps: "
        f"{time.perf_counter() - stage_started:.2f}s"
    )
    stage_started = time.perf_counter()

    # Detect an explicit request for chronological ordering.
    prompt_lower = prompt.lower()

    chronological_phrases = [
        "chronologically",
        "chronological order",
        "oldest to newest",
        "newest to oldest",
        "earliest to latest",
        "latest to earliest",
        "date and time recorded",
        "recording timestamp",
        "in the order they were taken",
        "in the order they were recorded",
        "in the order they were captured",
    ]

    chronological = any(
        phrase in prompt_lower
        for phrase in chronological_phrases
    )

    if chronological:
        missing_timestamps = [
            os.path.basename(asset.path)
            for asset in assets
            if asset.capture_time is None
        ]

        if missing_timestamps:
            return {
                "error": (
                    "Chronological ordering was requested, but "
                    "some files have no readable capture timestamp."
                ),
                "files_missing_timestamps": missing_timestamps,
            }
    # Create a job to track video generation.
    job_id = create_job()

    # Run video generation in the background.
    background_tasks.add_task(
        process_video_job,
        job_id,
        assets,
        prompt,
        chronological,
    )

    return {
        "job_id": job_id,
        "status": "queued",
    }
