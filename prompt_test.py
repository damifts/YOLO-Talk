import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

yoloV8 = """"""
domanda_utente = " "

prompt = f"""Sei un assistente AI specializzato nell'analisi visiva avanzata.
Rispondi alla domanda dell'utente usando sia:
1) i dati strutturati del modello YOLO;
2) la tua conoscenza generale.

Dati YOLOv8:
{yoloV8}

Domanda utente:
{domanda_utente}

Istruzioni di risposta:
- Fornisci una risposta chiara e diretta in italiano.
- Non mostrare ragionamenti interni.
- Se i dati YOLO sono insufficienti, dichiaralo brevemente e rispondi con la migliore stima possibile.
"""

response = client.models.generate_content(
  model="gemma-4-26b-a4b-it",
  contents=prompt,
)

risposta = response.text

if __name__ == "__main__":
    print(risposta)
