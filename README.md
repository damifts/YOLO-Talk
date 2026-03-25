# YOLO-Talk (Visual Q&A)

Analisi immagini con YOLOv8 + Gemini.

## Requisiti

- Python 3.12+
- uv installato
- Variabile ambiente GOOGLE_API_KEY configurata (es. file .env)
- Progetto in una cartella locale (non sotto OneDrive)

## Setup (Windows)

```cmd
set UV_LINK_MODE=copy
uv cache clean
uv sync
```

## Avvio

Backend:

```cmd
uv run uvicorn app.server:app --reload
```

Frontend:

```cmd
uv run streamlit run app/client.py
```