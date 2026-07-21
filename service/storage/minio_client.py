from dotenv import load_dotenv
load_dotenv()

from minio import Minio
import os, json, mimetypes

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_PUBLIC_URL = os.getenv("MINIO_PUBLIC_URL", "http://localhost:9000").rstrip("/")

MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")

BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "videos")

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

_bucket_initialized = False

def _ensure_bucket():
    global _bucket_initialized

    if _bucket_initialized:
        return

    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)

    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"],
        }]
    }

    client.set_bucket_policy(BUCKET_NAME, json.dumps(policy))
    _bucket_initialized = True


def upload_file(file_path, object_name):
    try:
        _ensure_bucket()

        content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

        client.fput_object(
            BUCKET_NAME,
            object_name,
            file_path,
            content_type=content_type,
        )

        return f"{MINIO_PUBLIC_URL}/{BUCKET_NAME}/{object_name}"

    except Exception as err:
        print("[minio] upload error:", err)
        return None