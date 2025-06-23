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

# === GPT ===
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Sprachauswahl ===
if "lang" not in st.session_state:
    st.session_state.lang = st.selectbox("Choose your language / Sprache auswählen / Elige tu idioma", ["Deutsch", "English", "Español"])

lang = st.session_state.lang

T = {
    "Deutsch": {
        "start": "Willkommen bei Lernbuddy Deluxe",
        "nav": ["Start", "GPT-Chat", "Lernplan", "Suche", "Hochschule"],
        "chat_title": "GPT-Chat",
        "ask": "Deine Frage:",
        "language_label": "Sprache auswählen",
    },
    "English": {
        "start": "Welcome to Lernbuddy Deluxe",
        "nav": ["Home", "GPT Chat", "Planner", "Search", "University"],
        "chat_title": "GPT Chat",
        "ask": "Your question:",
        "language_label": "Select Language",
    },
    "Español": {
        "start": "Bienvenido a Lernbuddy Deluxe",
        "nav": ["Inicio", "Chat GPT", "Planificador", "Buscar", "Universidad"],
        "chat_title": "Chat GPT",
        "ask": "Tu pregunta:",
        "language_label": "Selecciona el idioma",
    }
}

labels = T[lang]

# === Farbpalette Hochschule Kempten ===
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
    menu = st.radio("Navigation", labels["nav"])

# === Seiteninhalte ===

if menu == labels["nav"][0]:  # Start
    st.title(f"🎓 {labels['start']}")
    show_lottie("https://assets2.lottiefiles.com/packages/lf20_myejiggj.json")
    st.markdown("""
    **Lernbuddy Deluxe** ist dein digitaler Studienassistent. Wähle oben aus dem Menu, um zu starten.
    """)

elif menu == labels["nav"][1]:  # GPT Chat
    st.header(f"💬 {labels['chat_title']}")
    user_color = st.color_picker("Farbe für deine Nachrichten", "#00A3E0")
    bot_color = st.color_picker("Farbe für GPT", "#F39200")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input(f"🗨️ {labels['ask']}")
    if user_input:
        st.session_state.chat.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.chat
            )
            reply = response.choices[0].message.content
            st.session_state.chat.append({"role": "assistant", "content": reply})
        except Exception as e:
            reply = f"Fehler: {e}"
            st.session_state.chat.append({"role": "assistant", "content": reply})

    for msg in st.session_state.chat[::-1]:
        color = user_color if msg["role"] == "user" else bot_color
        sender = "👤 Du" if msg["role"] == "user" else "🤖 GPT"
        st.markdown(f"""
        <div style='background-color:{color};padding:10px;border-radius:10px;margin-bottom:10px;color:white'>
        <strong>{sender}:</strong><br>{msg['content']}
        </div>
        """, unsafe_allow_html=True)

elif menu == labels["nav"][2]:
    st.header("🧠 Lernplan kommt hier …")
    st.info("Dieser Abschnitt wird bald übersetzt und angepasst.")

elif menu == labels["nav"][3]:
    st.header("🔍 Suche")
    st.info("Suchfunktion folgt bald …")

elif menu == labels["nav"][4]:
    st.header("🎓 Hochschule Kempten")
    show_lottie("https://assets10.lottiefiles.com/packages/lf20_3rwasyjy.json", 180)
    st.markdown("""
    - [🌐 Website](https://www.hs-kempten.de/)
    - [📚 Studiengänge](https://www.hs-kempten.de/studium/studienangebot)
    - [🍽️ Mensaplan](https://www.stw-swt.de/essen-trinken/speiseplaene/)
    """)
