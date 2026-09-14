import io

import pytest
from fastapi import HTTPException, UploadFile

from app.documents.service import validate_upload


@pytest.mark.asyncio
async def test_supported_pdf_upload():
    upload = UploadFile(
        filename="test.pdf",
        file=io.BytesIO(b"%PDF-1.4 fake test"),
        headers={"content-type": "application/pdf"},
    )

    content, stored_filename, sha256 = await validate_upload(upload)

    assert content.startswith(b"%PDF")
    assert stored_filename.endswith(".pdf")
    assert len(sha256) == 64


@pytest.mark.asyncio
async def test_unsupported_extension_rejected():
    upload = UploadFile(
        filename="malicious.exe",
        file=io.BytesIO(b"bad"),
        headers={"content-type": "application/octet-stream"},
    )

    with pytest.raises(HTTPException) as exc:
        await validate_upload(upload)

    assert exc.value.status_code == 415