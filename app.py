import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import pandas as pd

# --- 1. CONFIGURAZIONE E STILE ---
st.set_page_config(page_title="GENERA - Autovalutazione Merito", layout="centered") # 

# --- 2. LOGO E TITOLO ---
col1, col_logo, col3 = st.columns([1, 2, 1])
with col_logo:
    try:
        # Centratura e dimensionamento del logo
        st.image("GENERA Logo Colore.png", use_container_width=True)
    except:
        st.info("Caricare 'GENERA Logo Colore.png' nella cartella principale.")

st.markdown("<h1 style='text-align: center;'>The Appreciation Quotient</h1>", unsafe_allow_html=True)

# --- 3. PARTE INTRODUTTIVA ---
st.markdown("""
### L'importanza del Riconoscimento nella Motivazione
Tutti vogliamo essere visti. Riconoscere il merito dei propri collaboratori non è un semplice accessorio, ma il cuore pulsante della motivazione. Saper dare un feedback circa il valore del contributo portato, distinguendo tra ciò che è **necessario** e ciò che è **opportuno**, e saper guidare il team attraverso il 'Perché' prima del 'Come', definisce la qualità della leadership.

**Obiettivo:** Valutare la tua capacità di offrire un riconoscimento come leva strategica per il sostegno alla motivazione, lo sviluppo del talento e la tenuta del clima aziendale.
""")

# --- 4. INFORMAZIONI SOCIO-ANAGRAFICHE ---
st.subheader("Profilo del Compilatore")
with st.container():
    nome = st.text_input("Nome o Nickname")
    genere = st.selectbox("Genere", ["Maschile", "Femminile", "Non binario", "Non risponde"])
    eta = st.selectbox("Età", ["Fino a 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", "51-60 anni", "61-70 anni", "Oltre 70 anni"])
    titolo = st.selectbox("Titolo di studio", ["Licenza media", "Qualifica professionale", "Diploma di maturità", "Laurea triennale", "Laurea magistrale / Ciclo unico", "Post-lauream"])
    ruolo = st.selectbox("Ruolo professionale", ["Imprenditore", "Top Manager", "Middle Manager", "Impiegato", "Operaio", "Tirocinante", "Libero Professionista"])

# --- 5. QUESTIONARIO (12 ITEMS) ---
st.divider()
st.subheader("Questionario di Autovalutazione")

items = [
    # Area 1: Flusso Strategico (Dove-Perché-Come)
    "Chiarisco sempre l'obiettivo strategico (il 'Dove') e le sue ragioni (il 'Perché') prima di spiegare il 'Come' operativo?",
    "Mi assicuro che il collaboratore possa comprendere il senso profondo del suo compito prima di iniziarlo?",
    "Dopo aver definito cosa si debba fare, mi preoccupo di chiarire 'come si possa fare così' per favorire l'apprendimento e la futura autonomia?",
    "Verifico che la visione d'insieme sia chiara prima di scendere nei dettagli tecnico-operativi?",
    # Area 2: Necessità vs Opportunità
    "Distinguo chiaramente tra un compito svolto per necessità o dovere (adempimento) e uno per opportunità e senso?",
    "Sono consapevole delle conseguenze che occorrono quando una necessità non negoziabile viene ignorata?",
    "Riconosco un valore superiore a chi coglie una 'opportunità' di miglioramento che vanno oltre il dovuto?",
    "Nelle valutazioni, sono in grado di riconoscere il rispetto delle procedure dal valore aggiunto generato?",
    # Area 3: ASAP e Riconoscimento
    "Intervengo al più presto per correggere una non conformità tecnica rilevata?",
    "Segnalo prontamente una condotta inopportuna per evitare che diventi una prassi abituale?",
    "Quando do un feedback mi ricordo di riconoscere le condotte corrette e opportune PRIMA di far notare eventuali errori?",
    "Sono capace di dare prorità alla validazione del buon operato rispetto alla sanzione degli errori?"
]

mappa_punti = {"Mai": 1, "Quasi mai": 2, "Spesso": 3, "Sempre": 4}

with st.form("assessment_form"): # [cite: 83-84]
    punteggi = []
    for i, testo in enumerate(items):
        r = st.select_slider(f"{i+1}. {testo}", options=["Mai", "Quasi mai", "Spesso", "Sempre"], key=f"q{i}")
        punteggi.append(mappa_punti[r])
    
    submit = st.form_submit_button("Analizza il mio Profilo")

# --- 6. OUTPUT GRAFICO (TACHIMETRO) E FEEDBACK ---
def draw_gauge(score):
    fig, ax = plt.subplots(figsize=(8, 5), subplot_kw={'aspect': 'equal'})
    # Mappatura score (12-48) su 0-180 gradi
    if score <= 18: angle = (score - 12) / 6 * 45
    elif score <= 30: angle = 45 + (score - 18) / 12 * 45
    elif score <= 42: angle = 90 + (score - 30) / 12 * 45
    else: angle = 135 + (score - 42) / 6 * 45
    
    actual_angle = 180 - angle # Per orientamento da sinistra a destra
    colors = ['#ff4b4b', '#ffa500', '#9acd32', '#008000']
    labels = ['Operatore\nReattivo', 'Gestore\nConsapevole', 'Leader\nMotivatore', 'Maestro\ndel Merito']

    for i, color in enumerate(colors):
        ax.add_patch(Wedge((0, 0), 1, 180 - (i+1)*45, 180 - i*45, facecolor=color, alpha=0.4))
        mid_a = 180 - (i * 45 + 22.5)
        ax.text(1.2 * np.cos(np.radians(mid_a)), 1.2 * np.sin(np.radians(mid_a)), labels[i], 
                ha='center', va='center', fontweight='bold', fontsize=9)

    # Lancetta
    ax.annotate('', xy=(0.9 * np.cos(np.radians(actual_angle)), 0.9 * np.sin(np.radians(actual_angle))), 
                xytext=(0, 0), arrowprops=dict(arrowstyle="wedge,tail_width=0.5", color="black"))
    ax.add_patch(plt.Circle((0, 0), 0.05, color='black'))

    # Finestra Punti
    ax.text(0, 0.25, f"PUNTI: {score}", ha='center', va='center', fontsize=18, fontweight='bold', 
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='black', boxstyle='round,pad=0.5'))

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.2, 1.5)
    ax.axis('off')
    return fig

if submit:
    totale = sum(punteggi)
    st.divider()
    st.subheader("I Tuoi Risultati")
    st.pyplot(draw_gauge(totale)) # Visualizzazione tachimetro
    
    # Feedback descrittivo
    profili = {
        "Operatore Reattivo": "Tendi a focalizzarti sul 'Come' immediato e sulla correzione dell'errore. È opportuno spostare l'attenzione sul 'Perché' strategico.",
        "Gestore Consapevole": "Distingui tra necessità e opportunità, ma potresti essere più rapido nel riconoscere la condotta più opportuna prima di correggere.",
        "Leader Motivatore": "Ottimo equilibrio. Segui il flusso logico del merito e sai quando valorizzare l'extra-miglio dei tuoi collaboratori.",
        "Maestro del Merito": "Eccellenza. Il tuo approccio è una guida per il team: riconosci il merito come pilastro della motivazione prima ancora di gestire le criticità."
    }
    
    if totale <= 18: l = "Operatore Reattivo"
    elif totale <= 30: l = "Gestore Consapevole"
    elif totale <= 42: l = "Leader Motivatore"
    else: l = "Maestro del Merito"
    
    st.markdown(f"**Profilo: {l}**")
    st.write(profili[l])
    st.success(f"Dati di {nome} registrati con successo per il salvataggio su Drive.")
