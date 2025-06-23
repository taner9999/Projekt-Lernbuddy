import streamlit as st 
import datetime
import pandas as pd
import json
import os
import requests
from streamlit_lottie import st_lottie
from fpdf import FPDF
from ics import Calendar, Event
from openai import OpenAI
from bs4 import BeautifulSoup

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PRIMARY = "#003865"
SECONDARY = "#00A3E0"
ACCENT = "#F39200"

if "darkmode" not in st.session_state:
    st.session_state.darkmode = False

def toggle_darkmode():
    st.session_state.darkmode = not st.session_state.darkmode

st.set_page_config(page_title="Lernbuddy Deluxe", layout="wide")

st.markdown(f"""
    <style>
    body {{
        background-color: {"#1e1e1e" if st.session_state.darkmode else "#ffffff"};
        color: {"#ffffff" if st.session_state.darkmode else "#000000"};
    }}
    .stButton>button {{
        background-color: {ACCENT};
        color: white;
        border-radius: 5px;
    }}
    </style>
""", unsafe_allow_html=True)

def show_lottie(url, h=200):
    r = requests.get(url)
    if r.status_code == 200:
        st_lottie(r.json(), height=h)
    else:
        st.warning("⚠️ Animation konnte nicht geladen werden.")

with st.sidebar:
    st.title("📚 Lernbuddy Deluxe")
    st.button("🌗 Darkmode umschalten", on_click=toggle_darkmode)
    menu = st.radio("Navigation", ["🏠 Start", "💬 GPT-Chat", "🧠 Lernplan", "🔎 Suche", "🎓 Hochschule"])

if menu == "🎓 Hochschule":
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:1rem;">
          <img src="https://www.hs-kempten.de/fileadmin/favicon/android-chrome-192x192.png"
               style="width:60px; border-radius:12px;">
          <h1 style="margin:0; font-size:2.2rem;">🎓 Hochschule Kempten</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    lottie_json = requests.get("https://assets10.lottiefiles.com/packages/lf20_3rwasyjy.json")
    if lottie_json.status_code == 200:
        st_lottie(lottie_json.json(), height=200)
    else:
        st.error("📌 Konnte Animation nicht laden.")

    c1, c2, c3 = st.columns(3)
    c1.metric("📚 Studiengänge", "40+")
    c2.metric("👩‍🎓 Studierende", "5.000+")
    c3.metric("🏫 Fakultäten", "5")

    tabs = st.tabs(["🔗 Links", "🍽️ Mensaplan", "📖 Bibliothek", "💻 Moodle", "🗺️ Campus-Karte"])

    with tabs[0]:
        st.subheader("🔗 Wichtige Links")
        cards = [
            ("🌐 Website", "https://www.hs-kempten.de/"),
            ("📚 Studiengänge", "https://www.hs-kempten.de/studium/studiengaenge"),
            ("🍽️ Mensaplan", "https://www.hs-kempten.de/campusgastronomie"),
            ("📖 Bibliothek", "https://www.hs-kempten.de/bibliothek"),
            ("💻 Moodle", "https://moodle.hs-kempten.de/login/"),
            ("🧾 MeinCampus", "https://meincampus.hs-kempten.de/qisserver/pages/cs/sys/portal/hisinoneStartPage.faces")
        ]
        cols = st.columns(3)
        for i, (label, url) in enumerate(cards):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="
                    border:1px solid #ddd;
                    border-radius:8px;
                    padding:1rem;
                    text-align:center;
                    box-shadow:2px 2px 6px rgba(0,0,0,0.1);
                    transition:transform .2s;
                  "
                  onmouseover="this.style.transform='scale(1.03)';"
                  onmouseout="this.style.transform='scale(1)';"
                >
                  <h4 style="margin-bottom:0.5rem;">{label}</h4>
                  <a href="{url}" target="_blank" style="color:#00CED1;">{url}</a>
                </div>
                """, unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("🍽️ Mensaplan der Woche")
        try:
            url = "https://www.hs-kempten.de/campusgastronomie"
            res = requests.get(url)
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                table = soup.find("table")
                if table:
                    df = pd.read_html(str(table))[0]
                    df.columns = ["Wochentag", "Mensa A", "Mensa B", "Bio-Mensa"]
                    st.dataframe(
                        df.style.set_table_styles([
                            {"selector": "th", "props": [("background-color", "#00CED1"), ("color", "white")]}
                        ]),
                        height=300
                    )
                else:
                    st.warning("⚠️ Keine Tabelle gefunden.")
            else:
                st.error("❌ Fehler beim Abrufen der Mensa-Webseite.")
        except Exception as e:
            st.error(f"❌ Fehler beim Parsen des Mensaplans: {e}")

    with tabs[2]:
        with st.expander("📖 Öffnungszeiten & Services"):
            st.markdown("""
            - Mo–Fr: 08:00–20:00  
            - Sa: 10:00–16:00  
            - Buchkatalog: [online suchen](https://opac.hs-kempten.de)  
            """)
        st.download_button("📄 PDF-Katalog herunterladen", data=b"", file_name="bibliothek_katalog.pdf")

    with tabs[3]:
        st.subheader("💻 Moodle-Quicklink")
        user = st.text_input("Benutzername")
        pw   = st.text_input("Passwort", type="password")
        if st.button("Login"):
            st.success("🔒 Simulierter Login erfolgreich")

    with tabs[4]:
        st.subheader("🗺️ Campus-Karte")
        df_map = pd.DataFrame({"lat":[47.726], "lon":[10.312]})
        st.map(df_map, zoom=16)

    st.markdown("---")
    st.info("🌟 Designed by dein Studi-Buddy 🚀")
