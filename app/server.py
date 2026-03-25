# backend.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from ultralytics import YOLO
from PIL import Image
import io
import uuid
import os
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

app = FastAPI(title="YOLO-Talk")


# Carica il modello una sola volta all'avvio
model = YOLO("yolov8n.pt")
gemini = genai.GenerativeModel("gemini-2.5-flash")

# CORS per permettere chiamate dal frontend Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def ricevi_img(image: UploadFile = File(...)) -> dict:
    # Validazione tipo file
    if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Formato file non supportato. Usa JPG o PNG.")

    try:
        # Leggi i bytes e converti in immagine PIL
        contenuto = await image.read()
        img_pil = Image.open(io.BytesIO(contenuto)).convert("RGB")

        # Esegui la detection
        results = model(img_pil)

        # Estrai le detection
        detections = []
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()  # [x1, y1, x2, y2]

                detections.append({
                    "classe": model.names[cls_id],
                    "confidenza": round(conf, 4),
                    "bounding_box": {
                        "x1": round(xyxy[0], 1),
                        "y1": round(xyxy[1], 1),
                        "x2": round(xyxy[2], 1),
                        "y2": round(xyxy[3], 1),
                    }
                })
    

        return {
            "status": "ok",
            "file": image.filename,
            "n_oggetti": len(detections),
            "detections": detections,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'analisi: {str(e)}")