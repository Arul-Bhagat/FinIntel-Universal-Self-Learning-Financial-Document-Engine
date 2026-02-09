import time
from app.jobs import update_job_status, set_job_result, get_job
from app.client import call_ocr_service, call_validation_service 


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

    # OCR
    ocr_result = call_ocr_service(job["path"])

    # Knowledge object
    knowledge_object = {
        "doc_type": doc_type,
        "entities": ocr_result.get("entities", {}),
        "tables": ocr_result.get("tables", []),
        "metadata": {
            "filename": filename,
            "job_id": job_id
        }
    }

    # Validation
    validation_result = call_validation_service(knowledge_object)

    result = {
        "doc_type": doc_type,
        "entities": knowledge_object["entities"],
        "tables": knowledge_object["tables"],
        "validation": validation_result
    }

    set_job_result(job_id, result)
    update_job_status(job_id, "DONE")
