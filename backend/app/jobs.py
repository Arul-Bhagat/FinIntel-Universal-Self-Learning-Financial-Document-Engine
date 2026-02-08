# In-memory job store
JOBS = {}

def create_job(job_id: str, filename: str, path: str):
    JOBS[job_id] = {
        "job_id": job_id,
        "filename": filename,
        "path": path,
        "status": "QUEUED"
    }

def get_job(job_id: str):
    return JOBS.get(job_id)

def update_job_status(job_id: str, status: str):
    if job_id in JOBS:
        JOBS[job_id]["status"] = status
