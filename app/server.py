import base64
import io
import os
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from ultralytics import YOLO

load_dotenv()

app = FastAPI(title="YOLO-Talk")
model = YOLO('yolov8n')

# Qui abilitiamo CORS per permettere al client Streamlit di chiamare il backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def ricevi_img(file_immagine: UploadFile = File(...)) -> dict[str, str | list[str]]:

    try:
        contenuto_file_immagine = await file_immagine.read()
        # immagine_utente = Image.open(io.BytesIO(contenuto_file_immagine)).convert("RGB")
        # from PIL
        immagine_utente = Image.open(file_immagine)

    except Exception as errore_img:
        raise HTTPException(status_code=400, detail="Immagine non valida") from errore_img

    # risultati_yolo = model.predict(immagine_utente)
    risultati_yolo = model.predict(source=immagine_utente, save=True)  # save plotted images

    for risultato in risultati_yolo:
        for box in risultato.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            print(f"Classe: {model.names[cls]}, Confidenza: {conf:.2f}")
