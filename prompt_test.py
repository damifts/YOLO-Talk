import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

yoloV8=""""""


domanda_utente=" "

prompt=f"""Sei un'Assistente AI specializzata nell'analisi visiva avanzata.
Il tuo compito è rispondere alle domande dell'utente integrando la tua vasta
base di conoscenza con i dati strutturati provenienti da un modello di YOLO.

Dati YOLOV8:{yoloV8}




dopo aver analizzato tutti questi dati rispondi in modo chiaro alla seguente domanda del utente,non mettere il ragionamento ma solo la risposta:
{domanda_utente}

"""

response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
        
      )
    
risposta=response.text

   
if __name__ == "__main__":

    print(risposta)

