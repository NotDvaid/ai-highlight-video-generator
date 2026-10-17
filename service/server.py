
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

import os
import shutil
import uuid
import subprocess
import json

from service.models.asset import Asset
from service.ai.prompt_engine import accept_request
from service.ai.media_analyzer import MediaAnalyzer
from service.ai.planner import Planner
from service.renderer.composer import Composer
from service.renderer.ffmpeg_render import FFmpegRenderer
from service.storage.minio_client import upload_file


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

    # 2. Fall back to FFprobe metadata.
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-show_entries",
                "format_tags=creation_time:stream_tags=creation_time",
                "-of", "json",
                file_path,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        metadata = json.loads(result.stdout)

        tags = metadata.get("format", {}).get("tags", {})
        capture_time = tags.get("creation_time")

        if not capture_time:
            for stream in metadata.get("streams", []):
                capture_time = stream.get(
                    "tags", {}
                ).get("creation_time")

                if capture_time:
                    break

        if capture_time:
            parsed = datetime.fromisoformat(
                capture_time.replace("Z", "+00:00")
            )

            # Keep timestamps consistently comparable when some media
            # includes timezone information and other media does not.
            if parsed.tzinfo is not None:
                parsed = parsed.replace(tzinfo=None)

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
    files: List[UploadFile] = File(...),
    prompt: str = Form(""),
):
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

        asset = Asset(
            asset_id=asset_id,
            path=file_path,
            media_type=media_type,
            duration=5.0,
            width=1920,
            height=1080,
            has_audio=media_type == "video",
            fps=30.0 if media_type == "video" else 0.0,
            capture_time=capture_time,
        )

        print(
            f"CAPTURE TIME: {file.filename} -> {capture_time}"
        )

        assets.append(asset)

    # Analyze each uploaded asset.
    analyzer = MediaAnalyzer()
    analysis_results = []

    for asset in assets:
        analysis = analyzer.analyze(asset)
        analysis_results.append(analysis)

    # Generate the AI editing plan.
    ai_plan = accept_request(
        prompt,
        assets,
        analysis_results,
    )

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

    # Build timeline and render the video.
    planner = Planner()

    timeline = planner.create_timeline(
        assets,
        ai_plan,
        chronological=chronological,
    )

    composer = Composer()
    renderer = FFmpegRenderer()

    render_plan = composer.compose(timeline)
    output_path = renderer.render(render_plan)

    video_name = os.path.basename(output_path)

    return {
        "video_url": f"http://localhost:8000/videos/{video_name}"
    }
