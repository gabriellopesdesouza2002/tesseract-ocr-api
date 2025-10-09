from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Header
from typing import Optional
from ocr import ocr_pdf
import tempfile
import os

app = FastAPI(title='Tesseract OCR API (PDF)')

API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise RuntimeError("Environment variable API_TOKEN is not set.")


def verify_bearer_token(authorization: Optional[str] = Header(None)):
    """Validates the Authorization: Bearer <token> header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split()
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    if scheme.lower() != "bearer" or token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return True


@app.post('/ocr-pdf')
async def ocr_pdf_endpoint(
    file: UploadFile = File(...),
    lang: str = Form('por', description="OCR language code, e.g. 'por', 'eng' or 'por+eng'"),
    dpi: int = Form(300),
    limit_pages: int|None = Form(None),
    authorized: bool = Depends(verify_bearer_token)
):
    """Receives a PDF and returns extracted text via Tesseract."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
        tmp_pdf.write(await file.read())
        tmp_pdf_path = tmp_pdf.name

    text = ocr_pdf(tmp_pdf_path, lang=lang, dpi=dpi, limit_pages=limit_pages)
    return { 
        'text': text,
        'parameters': {'language': lang, 'dpi': dpi, 'limit_pages': limit_pages}
        }
