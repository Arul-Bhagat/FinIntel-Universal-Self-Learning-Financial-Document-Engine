# backend/app/client.py
import os
import requests

OCR_URL = os.getenv("OCR_URL", "http://127.0.0.1:9001/ocr")
VAL_URL = os.getenv("VAL_URL", "http://127.0.0.1:9002/validate")

def call_ocr_service(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            r = requests.post(OCR_URL, files=files, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        # fallback
        return {"error": str(e), "entities": {}, "tables": []}

def call_validation_service(knowledge_object: dict) -> dict:
    try:
        r = requests.post(VAL_URL, json=knowledge_object, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        # fallback
        return {
            "error": str(e),
            "totalChecks": 0,
            "passed": 0,
            "warnings": 0,
            "errors": 1,
            "findings": [{
                "type": "error",
                "title": "Validation service not reachable",
                "details": str(e),
                "documents": [knowledge_object.get("metadata", {}).get("filename", "unknown")]
            }]
        }
