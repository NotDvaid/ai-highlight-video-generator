
import uuid

jobs = {}


def create_job():
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "progress": 0,
        "stage": "Waiting to start",
        "video_url": None,
        "error": None,
    }

    return job_id


def update_job(job_id: str, **updates):
    if job_id in jobs:
        jobs[job_id].update(updates)


def get_job(job_id: str):
    return jobs.get(job_id)
