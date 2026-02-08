import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Autovalutazione Merito - GENERA", layout="centered")

# --- 2. LOGO E TITOLO ---
# Centratura del logo tramite colonne
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("GENERA Logo Colore.png", use_container_width=True)
    except:
        st.info("Nota: Carica 'GENERA Logo Colore.png' nella cartella GitHub per visualizzare il logo.")

st.markdown("<h1 style='text-align: center;'>Autovalutazione: La Gestione del Merito</h1>", unsafe_allow_html=True)

# --- 3. INTRODUZIONE ---
st.markdown("""
### Perché questa autovalutazione?
Il riconoscimento del merito non è un semplice premio, ma una **competenza strategica**. Saper distinguere tra ciò che è dovuto (necessità) e ciò che è valore aggiunto (opportunità) permette di alimentare la motivazione reale. 

**Obiettivo:** Misurare la tua capacità di guidare i collaboratori attraverso la logica del 'Dove e Perché' e la tua prontezza nel validare la condotta opportuna.
""")

# --- 4. INFORMAZIONI SOCIO-ANAGRAFICHE ---
st.subheader("Profilo Compilatore")
with st.container():
    nome = st.text_input("Nome o Nickname")
    genere = st.selectbox("Genere", ["maschile", "femminile", "non binario", "non risponde"])
    eta = st.selectbox("Età", ["fino a 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", "51-60 anni", "61-70 anni", "più di 70 anni"])
    titolo_studio = st.selectbox("Titolo di studio", ["licenza media", "qualifica professionale", "diploma di maturità", "laurea triennale", "laurea magistrale (o ciclo unico)", "titolo post lauream"])
    ruolo = st.selectbox("Ruolo professionale", ["imprenditore", "top manager", "middle manager", "impiegato", "operaio", "tirocinante", "libero professionista"])

# --- 5. QUESTIONARIO (12 ITEMS) ---
st.divider()
st.subheader("Questionario")

items = [
    # Pilastro 1: Dove-Perché-Come
    ("Prima di spiegare 'come' fare, chiarisco sempre il 'dove' (obiettivo strategico)?", "Strategia"),
    ("Mi assicuro che il collaboratore comprenda il 'perché' di un compito prima di assegnarlo?", "Strategia"),
    ("Dopo il 'come', dedico tempo a spiegare 'come posso fare così' (metodo e crescita)?", "Strategia"),
    ("Verifico se la visione d'insieme è chiara prima di scendere nei dettagli operativi?", "Strategia"),
    # Pilastro 2: Necessità vs Opportunità
    ("Riesco a distinguere chiaramente tra un compito eseguito per dovere e uno di valore aggiunto?", "Discernimento"),
    ("Valuto in modo differente l'adempimento necessario dalla condotta opportuna?", "Discernimento"),
    ("Sono consapevole di quali compiti siano 'necessità' (non negoziabili) per il mio team?", "Discernimento"),
    ("Saper cogliere un'opportunità di miglioramento è un criterio chiave della mia valutazione?", "Discernimento"),
    # Pilastro 3: ASAP e Riconoscimento
    ("Riconosco la condotta opportuna e il corretto adempimento prima di segnalare l'errore?", "Riconoscimento"),
    ("Intervengo ASAP (immediatamente) quando rilevo una non conformità tecnica?", "Riconoscimento"),
    ("Segnalo ASAP una condotta inopportuna per evitare che diventi una prassi?", "Riconoscimento"),
    ("Il mio feedback inizia sempre validando ciò che è stato fatto bene e opportunamente?", "Riconoscimento")
]

mappa_punti = {"Mai": 1, "Quasi mai": 2, "Spesso": 3, "Sempre": 4}

with st.form("valutazione_merito"):
    risposte = []
    for testo, cat in items:
        scelta = st.select_slider(testo, options=["Mai", "Quasi mai", "Spesso", "Sempre"], key=testo)
        risposte.append((cat, mappa_punti[scelta]))
    
    submitted = st.form_submit_button("Invia e Visualizza Risultati")

# --- 6. ELABORAZIONE RISULTATI E FEEDBACK ---
if submitted:
    df_risposte = pd.DataFrame(risposte, columns=["Categoria", "Punteggio"])
    score_totale = df_risposte["Punteggio"].sum()
    medie = df_risposte.groupby("Categoria")["Punteggio"].mean()
    
    # Definizione Livelli
    if score_totale <= 18:
        livello = "Manager Reattivo"
        desc = "Tendi a intervenire solo sull'errore. È opportuno lavorare sulla comunicazione del 'Perché' strategico."
    elif score_totale <= 30:
        livello = "Coordinatore Consapevole"
        desc = "Distingui necessità e opportunità, ma il riconoscimento della condotta corretta deve diventare più tempestivo (ASAP)."
    elif score_totale <= 42:
        livello = "Leader Motivatore"
        desc = "Ottima gestione del flusso 'Dove-Perché-Come'. Sei propenso a valorizzare il merito prima di correggere."
    else:
        livello = "Maestro del Merito"
        desc = "Eccellenza assoluta. Il tuo approccio crea una cultura dove il merito è il motore della motivazione."

    # Feedback Visivo
    st.divider()
    st.header(f"Profilo: {livello}")
    st.write(f"**Analisi:** {desc}")

    # Grafico a barre per categorie
    fig, ax = plt.subplots(figsize=(8, 4))
    medie.plot(kind='barh', color=['#4e79a7', '#f28e2b', '#e15759'], ax=ax)
    ax.set_xlim(1, 4)
    ax.set_title("Performance per Area Strategica")
    st.pyplot(fig)

    # Logica di salvataggio (Necessità tecnica per Drive)
    # [Qui andrà la funzione salva_su_google_sheet(dati)]
    st.success(f"Grazie {nome}, i tuoi risultati sono stati elaborati.")
