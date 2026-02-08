import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials

# 1. CONFIGURAZIONE E TESTI [cite: 12, 13]
DIMENSIONI = ["Strategia", "Discernimento", "Tempismo", "Riconoscimento"]

DOMANDE = [
    {
        "testo": "Prima di spiegare 'come' svolgere un compito, quanto ti assicuri che il collaboratore ne conosca il 'dove' (obiettivo) e il 'perché'?",
        "dimensione": "Strategia"
    },
    {
        "testo": "Nel valutare un risultato, quanto riesci a distinguere tra ciò che era un atto dovuto (necessità) e ciò che è stato un valore aggiunto (opportunità)?",
        "dimensione": "Discernimento"
    },
    {
        "testo": "Quando rilevi una non conformità tecnica, con quale rapidità intervieni per correggerla (ASAP)?",
        "dimensione": "Tempismo"
    },
    {
        "testo": "Quanto ti impegni a riconoscere la 'condotta opportuna' PRIMA di segnalare eventuali inopportunità o errori?",
        "dimensione": "Riconoscimento"
    }
]

OPZIONI = ["Mai", "Raramente", "Spesso", "Sempre"]
VALORI = [1, 2, 3, 4]

# 2. FUNZIONI LOGICHE [cite: 17, 19]
def get_livello(punteggio_medio):
    if punteggio_medio <= 1.5: return "Operatore Reattivo"
    if punteggio_medio <= 2.5: return "Gestore Consapevole"
    if punteggio_medio <= 3.5: return "Leader Motivatore"
    return "Maestro del Merito"

def plot_radar(punteggi):
    categories = DIMENSIONI
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    values = punteggi + punteggi[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    plt.xticks(angles[:-1], categories)
    ax.plot(angles, values)
    ax.fill(angles, values, 'b', alpha=0.1)
    return fig

# 3. INTERFACCIA UTENTE [cite: 24, 25]
def main():
    st.set_page_config(page_title="Self-Assessment Merito") # [cite: 26]
    st.title("Autovalutazione: Gestione del Merito")
    
    # [cite: 42] Assicurati di avere il file logo nella cartella
    # st.image("GENERA Logo Colore.png", width=200)

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    with st.form("assessment_form"): # [cite: 29]
        risposte = []
        for q in DOMANDE:
            scelta = st.select_slider(q["testo"], options=OPZIONI)
            risposte.append(VALORI[OPZIONI.index(scelta)])
        
        submit = st.form_submit_button("Analizza il mio profilo") # [cite: 30]

    if submit or st.session_state.submitted:
        st.session_state.submitted = True
        media = np.mean(risposte)
        livello = get_livello(media)
        
        st.subheader(f"Il tuo profilo: {livello}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(plot_radar(risposte))
        with col2:
            st.write(f"**Analisi:** Hai totalizzato una media di {media:.2f}/4.")
            if livello == "Maestro del Merito":
                st.success("Eccellente! Distingui perfettamente tra necessità e opportunità, dando priorità al riconoscimento del merito.")
            else:
                st.info("Suggerimento: Lavora sulla distinzione tra condotta dovuta e condotta opportuna.")

if __name__ == "__main__": # [cite: 34-36]
    main()
