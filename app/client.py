import streamlit as st
import requests

# URL predefinito del backend locale
URL_BACKEND = "http://127.0.0.1:8000"

def main():
    st.title("YOLO-Talk - Interfaccia di Analisi")
    st.write("Seleziona un file immagine per testare il rilevamento oggetti del server.")

    # Caricamento file immagine
    file_immagine = st.file_uploader("Immagine", type=["jpg", "jpeg", "png"])
    domanda = st.text_input("Domanda", placeholder="Chiedi cosa vuoi rilevare dall'immagine (es. 'Quante persone ci sono?', 'C'è qualcosa di pericoloso?')")
    bottone_disabilitato = not (file_immagine and domanda.strip())
    bottone_analisi = st.button("Invia Analisi", disabled=bottone_disabilitato, help="Carica un'immagine e inserisci una domanda per attivare l'invio.")
    
    if bottone_analisi:
        with st.spinner("Comunicazione con il server in corso..."):
            # Preparazione payload con immagine per FastAPI
            file_payload = {"image": (file_immagine.name, file_immagine.getvalue(), file_immagine.type)}
            # Preparazione payload con domanda per FastAPI
            data_payload = {"question": domanda}
            
            try:
                # Chiamata POST al backend (con immagine e campo domanda)
                risposta = requests.post(f"{URL_BACKEND}/analyze", files=file_payload, data=data_payload)
                
                if risposta.status_code == 200:
                    st.success("Analisi completata con successo.")
                    st.json(risposta.json())
                else:
                    st.error(f"Errore del server: codice {risposta.status_code}")
            
            except Exception as e:
                st.error(f"Impossibile raggiungere il backend: {e}")

if __name__ == "__main__":
    main()
