import time
from app.jobs import update_job_status, set_job_result, get_job

def guess_doc_type(filename: str) -> str:
    name = filename.lower()

    if "bank" in name or "statement" in name:
        return "bank_statement"
    if "payslip" in name or "salary" in name:
        return "payslip"
    if "invoice" in name or "bill" in name:
        return "invoice"

    return "unknown"


def process_document(job_id: str):
    update_job_status(job_id, "RUNNING")
    time.sleep(2)

    job = get_job(job_id)
    filename = job["filename"] if job else ""

    doc_type = guess_doc_type(filename)

    result = {
        "doc_type": doc_type,
        "entities": {},
        "tables": [],
        "validation_status": "NEEDS_REVIEW",
        "debug": {
            "filename_used_for_classification": filename
        }
    }

    set_job_result(job_id, result)
    update_job_status(job_id, "DONE")
