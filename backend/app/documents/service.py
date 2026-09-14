import hashlib
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".docx"}

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


async def validate_upload(file: UploadFile) -> tuple[bytes, str, str]:
    original_name = Path(file.filename or "upload").name
    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(415, "Unsupported file type.")

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(415, "Unsupported MIME type.")

    content = await file.read()

    max_bytes = settings.max_upload_mb * 1024 * 1024

    if len(content) > max_bytes:
        raise HTTPException(
            413,
            f"File exceeds {settings.max_upload_mb} MB limit.",
        )

    if not content:
        raise HTTPException(400, "Uploaded file is empty.")

    sha256 = hashlib.sha256(content).hexdigest()

    stored_filename = f"{uuid.uuid4()}{extension}"

    return content, stored_filename, sha256