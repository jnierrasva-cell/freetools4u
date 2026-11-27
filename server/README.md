# FreeTools4U API

Backend for FreeTools4U.xyz — converts PDFs to Word (.docx) using `pdf2docx`.

## Endpoints
- `GET /` — health check
- `POST /convert/pdf-to-word` — form field `file` (PDF) → returns `.docx` binary

## Run locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
