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

# GPT-Client initialisieren
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Farben ===
PRIMARY = "#003865"
SECONDARY = "#00A3E0"
ACCENT = "#F39200"

# === Darkmode ===
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

# Startseite
if menu == "🏠 Start":
    st.title("🎓 Willkommen bei Lernbuddy Deluxe")
    show_lottie("https://assets2.lottiefiles.com/packages/lf20_myejiggj.json")
    st.markdown("""
    **Lernbuddy Deluxe** ist dein smarter Studienassistent:
    - 💬 GPT-Chat für Studien- & Lebenshilfe
    - 🧠 Lernplan mit Tagesverteilung
    - 📤 PDF- & Kalender-Export
    - 🔎 Suchfunktion
    - 🎨 Darkmode & Farben
    - 🎓 Infos zur Hochschule Kempten
    """)

# GPT-Chat
elif menu == "💬 GPT-Chat":
    st.header("💬 GPT-Chat")
    user_color = st.color_picker("Farbe für deine Nachrichten", "#00A3E0")
    bot_color = st.color_picker("Farbe für GPT", "#F39200")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("🗨️ Deine Frage:")
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

# Lernplan
elif menu == "🧠 Lernplan":
    st.header("📅 Lernplan erstellen")
    n = st.number_input("Wie viele Prüfungen hast du?", 1, 10)
    subjects = []
    for i in range(int(n)):
        name = st.text_input(f"📘 Fach {i+1}", key=f"name{i}")
        date = st.date_input(f"📅 Prüfung {i+1}", key=f"date{i}")
        diff = st.slider("📊 Schwierigkeit (1–10)", 1, 10, key=f"diff{i}")
        subjects.append((name, date, diff))

    def save_plan(plan):
        with open("lernplan.json", "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2)

    if st.button("✅ Lernplan erstellen"):
        plan = []
        for name, date, diff in subjects:
            tage = int(diff * 1.5)
            start = date - datetime.timedelta(days=tage)
            days = pd.date_range(start=start, end=date - datetime.timedelta(days=1)).to_list()
            std = max(1, round(diff / len(days))) if days else 1
            for d in days:
                plan.append({
                    "Tag": d.strftime("%A, %d.%m.%Y"),
                    "Fach": name,
                    "Stunden": f"{std}h"
                })
        save_plan(plan)
        df = pd.DataFrame(plan)
        st.success("✅ Lernplan gespeichert!")
        st.dataframe(df)

# Suche
elif menu == "🔎 Suche":
    st.header("🔍 Lernplan durchsuchen")
    term = st.text_input("Suchbegriff:")
    if os.path.exists("lernplan.json"):
        with open("lernplan.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        result = [e for e in data if term.lower() in e["Fach"].lower()]
        if result:
            st.success(f"{len(result)} Einträge gefunden:")
            st.dataframe(pd.DataFrame(result))
        else:
            st.warning("Keine Treffer.")
    else:
        st.info("Kein Lernplan vorhanden.")

# Hochschule
elif menu == "🎓 Hochschule":
    st.header("🎓 Hochschule Kempten")
    show_lottie("https://assets10.lottiefiles.com/packages/lf20_3rwasyjy.json", 180)
    st.markdown("""
    Willkommen bei der [**Hochschule Kempten**](https://www.hs-kempten.de)

    🔗 **Wichtige Links**
    - [🌐 Website](https://www.hs-kempten.de/)
    - [📚 Studiengänge](https://www.hs-kempten.de/studium/studienangebot)
    - [🍽️ Mensaplan](https://www.stw-swt.de/essen-trinken/speiseplaene/)
    - [📖 Bibliothek](https://www.hs-kempten.de/einrichtungen/bibliothek)
    - [💻 Moodle](https://moodle.hs-kempten.de/)
    - [🧾 MeinCampus](https://campus.hs-kempten.de/)
    """)
