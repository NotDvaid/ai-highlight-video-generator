from minio import Minio
from minio.error import S3Error
import json

MINIO_ENDPOINT = "127.0.0.1:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "impact-reels"

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)


def ensure_bucket_public():

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"]
            }
        ]
    }

    client.set_bucket_policy(BUCKET_NAME, json.dumps(policy))


def upload_file(file_path, object_name):

    try:
        if not client.bucket_exists(BUCKET_NAME):
            client.make_bucket(BUCKET_NAME)

        # ensure bucket is public
        ensure_bucket_public()

        client.fput_object(
            BUCKET_NAME,
            object_name,
            file_path
        )

        return f"http://{MINIO_ENDPOINT}/{BUCKET_NAME}/{object_name}"

    except S3Error as err:
        print("MinIO error:", err)
        return None