# server/main.py
import io
import os
import tempfile
import logging
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pdf2docx import Converter

# ---------- config ----------
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
ALLOWED_ORIGINS = [
    "https://freetools4u.xyz",
    "https://www.freetools4u.xyz",
    "https://jnierrasva-cell.github.io",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pdf2word")

app = FastAPI(title="FreeTools4U API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok", "service": "freetools4u-api"}


@app.post("/convert/pdf-to-word")
async def convert_pdf_to_word(file: UploadFile = File(...)):
    # --- validate ---
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)} MB.",
        )
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file.")

    # --- convert in temp dir ---
    tmp_dir = tempfile.mkdtemp()
    pdf_path = Path(tmp_dir) / "input.pdf"
    docx_path = Path(tmp_dir) / "output.docx"
    pdf_path.write_bytes(contents)

    try:
        logger.info(f"Converting {file.filename} ({len(contents)} bytes)")
        cv = Converter(str(pdf_path))
        try:
            cv.convert(str(docx_path))   # full-document conversion
        finally:
            cv.close()

        if not docx_path.exists() or docx_path.stat().st_size == 0:
            raise HTTPException(status_code=500, detail="Conversion produced empty file.")

        docx_bytes = docx_path.read_bytes()
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Conversion failed")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {e}")
    finally:
        # cleanup
        try:
            if pdf_path.exists(): pdf_path.unlink()
            if docx_path.exists(): docx_path.unlink()
            os.rmdir(tmp_dir)
        except Exception:
            pass

    out_name = Path(file.filename).stem + ".docx"
    return StreamingResponse(
        io.BytesIO(docx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{out_name}"'},
    )
