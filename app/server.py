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
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
yoloV8 = """"""

domanda_utente = " "




# Carica il modello una sola volta all'avvio
model = YOLO("yolov8n.pt")

# CORS per permettere chiamate dal frontend Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def ricevi_img(image: UploadFile = File(...), domanda: str = "Cosa vedi nell'immagine?") -> dict:
    if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Formato file non supportato.")

    try:
        contenuto = await image.read()
        img_pil = Image.open(io.BytesIO(contenuto)).convert("RGB")

        # 1. YOLO detection
        results = model(img_pil)
        detections = []
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
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

        # 2. Prompt costruito CON le detection reali
        prompt = f"""Sei un assistente AI specializzato nell'analisi visiva avanzata.
Rispondi alla domanda dell'utente usando sia:
1) i dati strutturati del modello YOLO;
2) la tua conoscenza generale.

Dati YOLOv8:
{detections}

Domanda utente:
{domanda}

Istruzioni:
- Rispondi in italiano, in modo chiaro e diretto.
- Se i dati YOLO sono insufficienti, dichiaralo brevemente.
"""

        # 3. Chiamata Gemini DENTRO il try, con i dati reali
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return {
            "status": "ok",
            "file": image.filename,
            "n_oggetti": len(detections),
            "detections": detections,
            "risposta_gemini": response.text,  # ← inclusa nel return!
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore: {str(e)}")