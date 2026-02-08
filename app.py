import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIGURAZIONE E TESTI ---
st.set_page_config(page_title="Autovalutazione Merito", layout="centered") # [cite: 26]

# Costanti e Dimensioni
LIVELLI = {
    "Livello 1: Operatore Reattivo": "Riconosci il merito in modo discontinuo. Tendi a focalizzarti sulla correzione degli errori senza inquadrarli in una visione strategica.",
    "Livello 2: Gestore Consapevole": "Distitngui tra necessità e opportunità, ma la comunicazione del 'perché' ai collaboratori può essere potenziata.",
    "Livello 3: Leader Motivatore": "Applichi correttamente la sequenza 'Dove-Perché-Come'. Riconosci la condotta opportuna prima di correggere l'errore.",
    "Livello 4: Maestro del Merito": "Crei una cultura dell'eccellenza. Il tuo riconoscimento del merito è il pilastro della motivazione del team."
}

# --- 2. INTERFACCIA UTENTE (UI) ---

# Logo e Titolo
col_logo, col_mid, col_right = st.columns([1, 2, 1])
with col_mid:
    try:
        st.image("GENERA Logo Colore.png", use_container_width=True) # 
    except:
        st.warning("Caricare il file 'GENERA Logo Colore.png' su GitHub per visualizzare il logo.")

st.markdown("<h1 style='text-align: center;'>L'Arte del Riconoscimento del Merito</h1>", unsafe_allow_html=True)

# Introduzione
st.info("""
**L'importanza del Merito:** Riconoscere correttamente il merito non è solo un atto di giustizia, ma la leva principale per sostenere la motivazione intrinseca dei collaboratori. 
**Obiettivo:** Questa autovalutazione ti aiuterà a capire come gestisci il flusso strategico del comando e come distingui tra ciò che è dovuto e ciò che è valore aggiunto.
""")

# Parte Socio-Anagrafica
st.subheader("Informazioni Socio-Anagrafiche")
with st.container():
    nome = st.text_input("Nome o Nickname")
    genere = st.selectbox("Genere", ["maschile", "femminile", "non binario", "non risponde"])
    eta = st.selectbox("Età", ["fino a 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", "51-60 anni", "61-70 anni", "più di 70 anni"])
    titolo = st.selectbox("Titolo di studio", ["licenza media", "qualifica professionale", "diploma di maturità", "laurea triennale", "laurea magistrale (o ciclo unico)", "titolo post lauream"])
    ruolo = st.selectbox("Ruolo professionale", ["imprenditore", "top manager", "middle manager", "impiegato", "operaio", "tirocinante", "libero professionista"])

# Questionario (12 Items)
st.subheader("Questionario di Autovalutazione")
items = [
    ("Quando delego un compito, spiego sempre il 'Dove' (visione) e il 'Perché' prima del 'Come'?", "Strategia"),
    ("Mi assicuro che il collaboratore abbia interiorizzato il 'Perché' di un'azione prima di procedere?", "Strategia"),
    ("Verifico se il 'Come' proposto dal collaboratore sia coerente con il 'Perché' iniziale?", "Strategia"),
    ("Distingo chiaramente tra un compito svolto per puro adempimento (necessità) e uno svolto con iniziativa (opportunità)?", "Discernimento"),
    ("Premio con enfasi diversa chi esegue il necessario rispetto a chi coglie un'opportunità di miglioramento?", "Discernimento"),
    ("Sono consapevole di quando un'azione non fatta è una violazione di una necessità?", "Discernimento"),
    ("Riconosco pubblicamente la 'condotta opportuna' prima di segnalare eventuali inopportunità?", "Riconoscimento"),
    ("Il mio primo feedback a un collaboratore riguarda ciò che è stato fatto correttamente?", "Riconoscimento"),
    ("Valuto positivamente chi propone 'come fare meglio' partendo da un obiettivo chiaro?", "Riconoscimento"),
    ("Intervengo ASAP (al più presto) per correggere una non conformità tecnica?", "Tempismo"),
    ("Segnalo prontamente una condotta inopportuna, spiegandone il motivo strategico?", "Tempismo"),
    ("Dedico tempo a spiegare 'come posso fare così' per trasformare un errore in apprendimento?", "Tempismo")
]

risposte = []
with st.form("quiz_form"): # [cite: 29-30]
    for i, (testo, dim) in enumerate(items):
        r = st.radio(f"{i+1}. {testo}", ["Mai", "Raramente", "Spesso", "Sempre"], horizontal=True, key=f"q_{i}")
        mappa_punti = {"Mai": 1, "Raramente": 2, "Spesso": 3, "Sempre": 4}
        risposte.append(mappa_punti[r])
    
    submit = st.form_submit_button("Calcola Risultato")

# --- 3. LOGICA DI CALCOLO E FEEDBACK ---
if submit:
    punteggio_totale = sum(risposte)
    media = punteggio_totale / 12
    
    # Definizione Livello
    if media <= 1.5: livello_key = "Livello 1: Operatore Reattivo"
    elif media <= 2.5: livello_key = "Livello 2: Gestore Consapevole"
    elif media <= 3.5: livello_key = "Livello 3: Leader Motivatore"
    else: livello_key = "Livello 4: Maestro del Merito"

    st.divider()
    st.header(f"Risultato: {livello_key}")
    
    # Grafico Radar semplificato
    fig, ax = plt.subplots()
    ax.barh(["Punteggio Totale"], [punteggio_totale], color='skyblue')
    ax.set_xlim(12, 48)
    st.pyplot(fig) # [cite: 17]

    st.write(f"**Descrizione:** {LIVELLI[livello_key]}")
    
    # Placeholder per salvataggio dati (Necessità di sicurezza)
    st.success("Test completato. I dati sono pronti per il salvataggio sicuro.") # [cite: 20-21]

if __name__ == "__main__": # [cite: 34-35]
    pass # main() gestito da Streamlit
