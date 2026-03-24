# YOLO-Talk (Visual Q&A)

Progetto per l'analisi di immagini tramite YOLOv8 e Google Gemini.

### Setup iniziale (Windows)

1.  Assicurarsi che **uv** sia installato sul sistema.
2.  Aprire il terminale nella cartella del progetto ed eseguire:

    ```cmd
    set UV_LINK_MODE=copy
    uv sync
    ```

### Avvio dell'applicazione

Per avviare l'interfaccia utente (Frontend), aprire il terminale ed eseguire:

```cmd
uv run streamlit run app/client.py

Per avviare il server (Backend), aprire il terminale ed eseguire:

```cmd
uv run uvicorn app.server:app --reload
```