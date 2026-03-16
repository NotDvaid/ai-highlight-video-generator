from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, Form, File
from typing import List
import shutil
import os
import joblib
import uuid
import cv2
import numpy as np

from ffmpeg_editor import FFmpegEditor

from feature_extractor import VideoFeatureExtractor

from feature_extraction import extract_features_from_clip

from minio_client import upload_file

app = FastAPI()

# GLOBAL PROGRESS
progress_status = {"progress": 0}

# Serve output videos
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model = joblib.load("highlight_model.pkl")


@app.post("/create-highlight")
async def create_highlight(
    files: List[UploadFile] = File(...),
    prompt: str = Form("")
):

    print("FILES RECEIVED:", len(files))
    print("PROMPT:", prompt)

    progress_status["progress"] = 0

    scored_segments = []
    image_clips = []

    total_files = len(files)

    for file_idx, file in enumerate(files):

        unique_name = str(uuid.uuid4()) + "_" + file.filename
        input_path = os.path.join(UPLOAD_FOLDER, unique_name)

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        filename = file.filename.lower()

        # IMAGE
        if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            img_clip_path = os.path.join(OUTPUT_FOLDER, f"img_{uuid.uuid4()}.mp4")
            FFmpegEditor.create_image_clip(input_path, img_clip_path, duration=3, fps=24)
            image_clips.append(img_clip_path)

        # VIDEO
        else:
            metadata = FFmpegEditor.get_video_metadata(input_path)
            duration = int(metadata.get("duration", 0))
            segment_length = 3

            # STEP 1: Score all segments (fast — no ffmpeg trimming yet)
            segment_scores = []
            segments = list(range(0, duration, segment_length))
            total_segments = len(segments)

            for seg_idx, t in enumerate(segments):
                start = t
                end = min(t + segment_length, duration)

                features = extract_features_from_clip(input_path, start, end)
                score = model.predict_proba([features])[0][1]

                segment_scores.append((score, input_path, start, end))

                # Update progress: scoring is 0-50%
                file_progress = (seg_idx + 1) / total_segments
                overall = ((file_idx + file_progress) / total_files) * 50
                progress_status["progress"] = int(overall)

            # STEP 2: Sort by score, keep top segments (enough for ~60s)
            segment_scores.sort(reverse=True, key=lambda x: x[0])
            max_segments = 60 // segment_length
            top_segments = segment_scores[:max_segments]

            # STEP 3: Only trim the top segments
            for trim_idx, (score, src_path, start, end) in enumerate(top_segments):
                seg_path = os.path.join(OUTPUT_FOLDER, f"seg_{uuid.uuid4()}.mp4")
                FFmpegEditor.trim_clip(src_path, seg_path, start, end)
                scored_segments.append((score, seg_path))

                # Update progress: trimming is 50-70%
                trim_progress = (trim_idx + 1) / len(top_segments)
                progress_status["progress"] = 50 + int(trim_progress * 20)

    scored_segments.sort(reverse=True, key=lambda x: x[0])
    selected_paths = [seg for _, seg in scored_segments] + image_clips

    if not selected_paths:
        return {"error": "No valid media"}

    progress_status["progress"] = 70

    # Normalize all clips to consistent resolution/FPS
    normalized_paths = []
    for norm_idx, clip_path in enumerate(selected_paths):
        norm_path = clip_path.replace(".mp4", "_norm.mp4")
        FFmpegEditor.normalize_clip(clip_path, norm_path)
        normalized_paths.append(norm_path)

        # Update progress: normalizing is 70-85%
        progress_status["progress"] = 70 + int(((norm_idx + 1) / len(selected_paths)) * 15)

    progress_status["progress"] = 85

    # Concatenate
    concat_path = os.path.join(OUTPUT_FOLDER, f"concat_{uuid.uuid4()}.mp4")
    FFmpegEditor.concatenate_clips(normalized_paths, concat_path)

    progress_status["progress"] = 90

    total_meta = FFmpegEditor.get_video_metadata(concat_path)
    total_duration = total_meta.get("duration", 0)

    if total_duration < 60 and normalized_paths:
        loops = int(60 // total_duration) + 1 if total_duration > 0 else 1
        looped_paths = normalized_paths * loops
        FFmpegEditor.concatenate_clips(looped_paths, concat_path)

    progress_status["progress"] = 93

    # Trim to 60 seconds
    output_name = f"highlight_{uuid.uuid4()}.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    FFmpegEditor.trim_clip(concat_path, output_path, 0, 60)
    
    # Upload highlight video to MinIO
    video_url = upload_file(output_path, f"videos/{output_name}")
    print("Uploaded highlight video to MinIO:", video_url)

    progress_status["progress"] = 96

    # Upload highlight video to MinIO
    video_url = upload_file(output_path, f"videos/{output_name}")
    print("Uploaded highlight video to MinIO:", video_url)

    progress_status["progress"] = 98

    # Clean up temporary files
    for seg_path in selected_paths + normalized_paths + [concat_path]:
        try:
            os.remove(seg_path)
        except OSError:
            pass

    progress_status["progress"] = 100

    return {
        "message": "Highlight created",
        "prompt": prompt,
        "video_url": video_url
    }


@app.post("/edit")
async def edit_video(
    file: UploadFile = File(...),
    prompt: str = Form("")
):
    """Apply a filter/edit to a video based on a text prompt."""
    unique_name = str(uuid.uuid4()) + "_" + file.filename
    input_path = os.path.join(UPLOAD_FOLDER, unique_name)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_name = f"edited_{uuid.uuid4()}.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    prompt_lower = prompt.lower()
    known_filters = [
        "brightness", "contrast", "saturation", "blur", "sharpen",
        "speed", "fade_in", "fade_out", "grayscale", "sepia",
    ]

    applied = None
    for filter_name in known_filters:
        if filter_name.replace("_", " ") in prompt_lower or filter_name in prompt_lower:
            FFmpegEditor.apply_filter(input_path, output_path, filter_name)
            applied = filter_name
            break

    if applied is None:
        shutil.copy(input_path, output_path)

    return {
        "message": "Edit applied" if applied else "No matching filter found; returned original",
        "filter": applied,
        "output": f"outputs/{output_name}",
    }


@app.get("/metadata")
async def get_metadata(filepath: str):
    """Return video metadata for a file in the uploads or outputs directory."""
    from fastapi import HTTPException
    abs_path = os.path.realpath(filepath)
    allowed_dirs = [
        os.path.realpath(UPLOAD_FOLDER),
        os.path.realpath(OUTPUT_FOLDER),
    ]
    if not any(abs_path.startswith(d + os.sep) or abs_path == d for d in allowed_dirs):
        raise HTTPException(status_code=400, detail="filepath must be within uploads or outputs directory")
    metadata = FFmpegEditor.get_video_metadata(abs_path)
    return metadata


@app.get("/progress")
def get_progress():
    return progress_status