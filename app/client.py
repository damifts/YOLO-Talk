import streamlit as st
import requests

# URL predefinito del backend locale
URL_BACKEND = "http://127.0.0.1:8000"

def main():
    st.title("YOLO-Talk - Interfaccia di Analisi")
    st.write("Seleziona un file immagine per testare il rilevamento oggetti del server.")

    # Caricamento file immagine
    file_immagine = st.file_uploader("Immagine", type=["jpg", "jpeg", "png"])
    
    if st.button("Invia Analisi"):
        if file_immagine:
            with st.spinner("Comunicazione con il server in corso..."):
                # Preparazione payload per FastAPI
                file_payload = {"image": (file_immagine.name, file_immagine.getvalue(), file_immagine.type)}
                
                try:
                    # Chiamata POST al backend (senza campo question)
                    risposta = requests.post(f"{URL_BACKEND}/analyze", files=file_payload)
                    
                    if risposta.status_code == 200:
                        st.success("Analisi completata con successo.")
                        st.json(risposta.json())
                    else:
                        st.error(f"Errore del server: codice {risposta.status_code}")
                
                except Exception as e:
                    st.error(f"Impossibile raggiungere il backend: {e}")
        else:
            st.warning("Caricare un file prima di procedere.")

if __name__ == "__main__":
    main()
