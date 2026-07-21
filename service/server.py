from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import shutil, os, uuid, subprocess
from dotenv import load_dotenv
from ai_service.storage.minio_client import upload_file

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

# ---------------- ROUTE ----------------
@app.post("/create-highlight")
def create_highlight(
    files: List[UploadFile] = File(...),
    prompt: str = Form("")
):

    if len(files) > MAX_FILES:
        return {"error": f"Max {MAX_FILES} files allowed"}

    processed_files = []

    # -------- STEP 1: NORMALIZE (FIX AUDIO HERE) --------
    for file in files:
        raw_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_raw.mp4")
        clean_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_clean.mp4")

        with open(raw_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        try:
            subprocess.run([
                "ffmpeg",
                "-y",
                "-fflags", "+genpts",
                "-i", raw_path,

                # video normalize
                "-vf", "scale=720:1280,setsar=1",
                "-r", "30",

                # KEY FIXES
                "-map", "0:v:0",
                "-map", "0:a?",             # allow missing audio
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",

                "-c:a", "aac",
                "-b:a", "128k",
                "-ar", "48000",

                "-af", "aresample=async=1",  # fix audio sync

                "-movflags", "+faststart",

                clean_path
            ], check=True)

            processed_files.append(clean_path)

        except subprocess.CalledProcessError:
            print(f"Failed processing: {file.filename}")
            continue

        finally:
            os.remove(raw_path)

    if not processed_files:
        return {"error": "No valid videos processed"}

    # -------- STEP 2: CONCAT (FIX AUDIO TIMING) --------
    concat_file = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_concat.txt")

    with open(concat_file, "w") as f:
        for path in processed_files:
            f.write(f"file '{path}'\n")

    final_output = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_final.mp4")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-fflags", "+genpts",
        "-i", concat_file,

        "-vsync", "vfr",

        "-c:v", "libx264",
        "-c:a", "aac",

        "-movflags", "+faststart",

        final_output
    ], check=True)

    # -------- STEP 3: EDIT --------
    edited_output = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_edited.mp4")
    apply_prompt_edit(final_output, edited_output, prompt)

    # -------- STEP 4: UPLOAD --------
    video_name = os.path.basename(edited_output)
    video_url = upload_file(edited_output, video_name)

    # -------- CLEANUP --------
    for fpath in processed_files:
        os.remove(fpath)

    os.remove(concat_file)
    os.remove(final_output)
    os.remove(edited_output)

    return {
        "video_url": video_url
    }