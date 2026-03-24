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

@app.get("/analyze")
async def ricevi_img(file_immagine:UploadFile)-> dict[str, str | list[str]]:

#apertura e conversione immagine in RGB
    try:
        contenuto_file_immagine = await file_immagine.read()
        contenuto = Image.open(file_immagine).convert("RGB")
    except Exception as errore_img:
        raise HTTPException(status_code=400, detail="Immagine non valida") from errore_img
    
    risultati_yolo=model.predict(file_immagine)
