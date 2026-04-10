import io
import json
import os
import base64
from typing import List
from openai import OpenAI

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from google import genai
from PIL import Image
from pydantic import BaseModel, Field
from ultralytics import YOLO

# Carica le variabili dal file .env
load_dotenv()

app = FastAPI(title="YOLO-Talk")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class Detection(BaseModel):
    classe: str
    confidenza: float = Field(ge=0.0, le=1.0)
    bounding_box: BoundingBox


class AnalyzeResponse(BaseModel):
    n_oggetti: int
    detections: List[Detection]
    risposta_gemini: str
    image_b64: str


# Carica il modello una sola volta all'avvio
model = YOLO("yolov8n.pt")


@app.post("/analyze")
async def analizza_immagine(
    immagine: UploadFile = File(...),
    domanda: str = "Cosa vedi nell'immagine?",
) -> AnalyzeResponse:
    if immagine.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Formato file non supportato.")

    try:
        contenuto = await immagine.read()
        img_pil = Image.open(io.BytesIO(contenuto)).convert("RGB")

        # 1. YOLO detection
        results = model(img_pil)
        detections = []
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
                detections.append(
                    {
                        "classe": model.names[cls_id],
                        "confidenza": round(conf, 4),
                        "bounding_box": {
                            "x1": round(xyxy[0], 1),
                            "y1": round(xyxy[1], 1),
                            "x2": round(xyxy[2], 1),
                            "y2": round(xyxy[3], 1),
                        },
                    }
                )

        # 1.b Immagine annotata direttamente da YOLO (box + label)
        img_array = results[0].plot()
        img_annotata = Image.fromarray(img_array[:, :, ::-1])

        buffer = io.BytesIO()
        img_annotata.save(buffer, format="PNG")
        image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # 2. Prompt costruito con detection formattate
        detections_json = json.dumps(detections, ensure_ascii=False, indent=2)
        prompt = (
            "Sei un assistente AI specializzato nell'analisi visiva avanzata.\n"
            "Usa sia i dati strutturati di YOLO sia la tua conoscenza generale.\n\n"
            "Dati YOLOv8 (JSON):\n"
            f"{detections_json}\n\n"
            "Domanda utente:\n"
            f"{domanda}\n\n"
            "Istruzioni:\n"
            "- Rispondi in italiano, in modo chiaro e diretto.\n"
            "- Non includere il ragionamento interno.\n"
            "- Se i dati YOLO sono insufficienti, dichiaralo brevemente.\n"
        )

        # 3. Chiamata Gemini DENTRO il try, con i dati reali
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            contents=prompt,
        )

        return AnalyzeResponse(
            n_oggetti=len(detections),
            detections=detections,
            risposta_gemini=response.text,
            image_b64=image_b64,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore: {str(e)}")
