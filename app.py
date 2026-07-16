import streamlit as st
import pandas as pd
import datetime
import requests
import json

# --- CONFIGURARE GOOGLE WEB APP ---
# Pune între ghilimele link-ul tău complet copiat la Pasul 2 (cel cu /exec la sfârșit):
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzH4dn0ui_gFT4ygni-I72YWeom363jhndmtJp8IlCc34-8Wa8IIu1K_xzhwpgv9g0Q/exec"

# Funcție pentru a încărca programările direct din Web App
def incarca_programari():
    try:
        raspuns = requests.get(WEB_APP_URL, timeout=10)
        if raspuns.status_code == 200:
            date_json = raspuns.json()
            df = pd.DataFrame(date_json)
            coloane_necesare = ["Data", "Ora", "Nume", "Telefon", "Marca", "Model", "Nr_Masina"]
           
            if df.empty:
                return pd.DataFrame(columns=coloane_necesare)
               
            for col in coloane_necesare:
                if col not in df.columns:
                    df[col] = ""
            return df[coloane_necesare]
    except Exception:
        pass
    return pd.DataFrame(columns=["Data", "Ora", "Nume", "Telefon", "Marca", "Model", "Nr_Masina"])

# Funcție pentru a salva o programare nouă prin Web App
def salveaza_programare(data, ora, nume, telefon, marca, model, nr_masina):
    date_programare = {
        "Data": str(data),
        "Ora": ora,
        "Nume": nume,
        "Telefon": telefon,
        "Marca": marca,
        "Model": model,
        "Nr_Masina": nr_masina
    }
    try:
        raspuns = requests.post(WEB_APP_URL, data=json.dumps(date_programare), headers={"Content-Type": "application/json"}, timeout=10)
        if raspuns.status_code == 200:
            return True
    except Exception as e:
        st.error(f"Eroare la trimiterea datelor către Google Sheets: {e}")
    return False

# Configurare pagină Streamlit
st.set_page_config(
    page_title="Programări ITP - AUTOLUDWIG SRL",
    page_icon="🚗",
    layout="centered"
)

# --- DESIGN FORȚAT (TOATE BUTOANELE ALBASTRE CU TEXT GALBEN) ---
st.markdown("""
<style>
    /* Fundalul principal al aplicației - Albastru Închis */
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #172a45 100%) !important;
        color: #ffffff !important;
    }
   
    /* Banner-ul Galben pentru Titlul Firmei */
    .banner-titlu {
        background-color: #fec107 !important;
        padding: 20px !important;
        border-radius: 12px !important;
        text-align: center !important;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 25px !important;
        border: 2px solid #ffffff;
    }
   
    /* Textul din interiorul bannerului galben */
    .banner-titlu h1 {
        color: #0a192f !important;
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        margin: 0 !important;
    }
   
    /* Subtitlurile (STAȚIA DE ITP SJ020) */
    .text-galben {
        color: #fec107 !important;
        font-weight: bold !important;
        text-align: center;
        font-size: 1.5rem !important;
        margin-top: 10px;
        margin-bottom: 15px;
    }
   
    /* Etichetele câmpurilor din formular */
    label {
        color: #fec107 !important;
        font-weight: bold !important;
    }
   
    /* Căsuțele de introducere text - Fundal ALB cu text NEGRU */
    input, select, textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #fec107 !important;
        border-radius: 6px !important;
        padding: 10px !important;
    }
   
    /* Rezolvare text în căsuțele standard */
    .stTextInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
   
    /* FORȚARE DIV-URI DE BUTOANE SIMPLE ȘI DE DESCĂRCARE (Fără excepții) */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #0d6efd !important; /* Albastru regal solid */
        color: #fec107 !important; /* Text galben */
        border: 2px solid #fec107 !important; /* Contur galben */
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
        display: block !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important;
        text-transform: uppercase !important;
    }

    /* Ne asigurăm că orice element text din interiorul butoanelor este galben */
    div.stButton > button *, div.stDownloadButton > button * {
        color: #fec107 !important;
        font-weight: 900 !important;
    }
   
    /* Personalizare meniu lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #081426 !important;
        border-right: 3px solid #fec107 !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Meniu de navigare lateral
pagini = ["Fă o programare", "Panou Administrare (Doar pt. Firmă)"]
optiune = st.sidebar.radio("Navigare", pagini)

# Toate intervalele de lucru
TOATE_ORELE = [
    "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
    "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
]

# --- PAGINA 1: PENTRU CLIENȚI ---
if optiune == "Fă o programare":
    st.markdown("""
        <div class="banner-titlu">
            <h1>🚗 AUTOLUDWIG SRL</h1>
        </div>
    """, unsafe_allow_html=True)
   
    st.markdown("<div class='text-galben'>STAȚIA DE ITP SJ020</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #fec107;'>", unsafe_allow_html=True)
   
    st.write("Completează formularul de mai jos pentru a rezerva un loc la ITP. Programul nostru este de la **08:00 la 17:00** (Pauză de masă: 12:00 - 13:00).")
   
    data_selectata = st.date_input("1. Alege ziua:", min_value=datetime.date.today())
   
    df_actual = incarca_programari()
   
    # Verificăm dacă avem deja programări pentru data respectivă
    if not df_actual.empty:
        ore_ocupate_in_zi = df_actual[df_actual["Data"] == str(data_selectata)]["Ora"].tolist()
    else:
        ore_ocupate_in_zi = []
       
    ore_libere = [ora for ora in TOATE_ORELE if ora not in ore_ocupate_in_zi]
   
    if len(ore_libere) == 0:
        st.warning("Ne pare rău, nu mai sunt locuri disponibile în această zi. Te rugăm să alegi altă dată.")
    else:
        ora_aleasa = st.selectbox("2. Alege ora dorită:", ore_libere)
        nume = st.text_input("Nume complet client:")
        telefon = st.text_input("Număr de telefon:")
       
        col1, col2 = st.columns(2)
        with col1:
            marca = st.text_input("Marca mașinii (ex: Renault, Audi, Dacia):")
        with col2:
            model = st.text_input("Modelul mașinii (ex: Clio, A4, Logan):")
           
        nr_masina = st.text_input("Număr înmatriculare (ex: SJ 01 LUD):").upper()
       
        st.write("")
        trimite = st.button("CONFIRMĂ PROGRAMAREA")
       
        if trimite:
            if nume.strip() == "" or telefon.strip() == "" or marca.strip() == "" or model.strip() == "" or nr_masina.strip() == "":
                st.error("Te rugăm să completezi toate câmpurile expuse!")
            else:
                cu_succes = salveaza_programare(data_selectata, ora_aleasa, nume, telefon, marca, model, nr_masina)
                if cu_succes:
                    st.success(f"🎉 Programare reușită! Te așteptăm la AUTOLUDWIG SRL în data de {data_selectata} la ora {ora_aleasa}.")
                    st.balloons()
                    st.rerun()

# --- PAGINA 2: PENTRU FIRMĂ ---
elif optiune == "Panou Administrare (Doar pt. Firmă)":
    st.markdown("""
        <div class="banner-titlu">
            <h1>🔑 PANOU ADMINISTRARE</h1>
        </div>
    """, unsafe_allow_html=True)
   
    st.markdown("<div class='text-galben'>STAȚIA DE ITP SJ020 - AUTOLUDWIG SRL</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #fec107;'>", unsafe_allow_html=True)
   
    parola = st.text_input("Introdu parola pentru a vedea programările:", type="password")
   
    if parola == "itp2026":
        st.subheader("📋 Toate programările înregistrate în sistem")
        df_actual = incarca_programari()
       
        if df_actual.empty or len(df_actual) == 0:
            st.info("Nu există nicio programare înregistrată încă în Google Sheets.")
        else:
            # Sortare automată cronologică
            df_actual = df_actual.sort_values(by=["Data", "Ora"])
            st.dataframe(df_actual, use_container_width=True)
           
            # BUTONUL DE DESCĂRCARE
            csv = df_actual.to_csv(index=False).encode('utf-8')
            st.write("")
            st.download_button(
                label="📥 Descarcă tabelul (Format Excel/CSV)",
                data=csv,
                file_name=f"programari_AUTOLUDWIG_{datetime.date.today()}.csv",
                mime="text/csv",
            )
    elif parola != "":
        st.error("Parolă incorectă!")
