import streamlit as st
import requests

# URL predefinito del backend locale
URL_BACKEND = "http://127.0.0.1:8000"

def main():
    st.title("YOLO-Talk - Interfaccia di Analisi")
    st.write("Seleziona un file immagine ed inserisci una domanda per ottenere informazioni sul contenuto dell'immagine.")

    # Caricamento file immagine
    file_immagine = st.file_uploader("Immagine", type=["jpg", "jpeg", "png"])
    # Input per la domanda da inviare al backend
    domanda = st.text_input("Domanda", placeholder="Chiedi cosa vuoi rilevare dall'immagine (es. 'Quante persone ci sono?', 'C'è qualcosa di pericoloso?')")
    bottone_disabilitato = not (file_immagine and domanda.strip())
    if not file_immagine:
        testo_help = "Carica un'immagine per abilitare l'invio."
    elif not domanda.strip():
        testo_help = "Inserisci una domanda per abilitare l'invio."
    elif not (domanda.strip() and file_immagine):
        testo_help = "Carica un'immagine e inserisci una domanda per abilitare l'invio."
    else:
        testo_help = ""
    bottone_analisi = st.button("Invia Analisi", disabled=bottone_disabilitato, help=testo_help)
    
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
