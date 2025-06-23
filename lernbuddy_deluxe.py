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

# OpenAI Client
client = OpenAI(api_key="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")

PRIMARY = "#003865"
ACCENT = "#F39200"

if "darkmode" not in st.session_state:
    st.session_state.darkmode = False

st.set_page_config(page_title="Lernbuddy Deluxe", layout="wide")

def toggle_darkmode():
    st.session_state.darkmode = not st.session_state.darkmode

st.markdown(f'''
    <style>
    body {{
        background-color: {"#1e1e1e" if st.session_state.darkmode else "#ffffff"};
        color: {"#ffffff" if st.session_state.darkmode else "#000000"};
    }}
    </style>
''', unsafe_allow_html=True)

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

if menu == "🏠 Start":
    st.title("🎓 Willkommen bei Lernbuddy Deluxe")
    show_lottie("https://assets2.lottiefiles.com/packages/lf20_myejiggj.json")
    st.markdown("Erstelle Lernpläne, chatte mit GPT oder exportiere deinen Kalender.")

elif menu == "💬 GPT-Chat":
    st.header("💬 GPT-Chat")
    user_color = st.color_picker("Farbe für deine Nachrichten", "#00A3E0")
    bot_color = st.color_picker("Farbe für GPT", "#F39200")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("🗨️ Deine Frage:")
    if user_input:
        st.session_state.chat.append(("user", user_input))
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": r, "content": m} for r, m in st.session_state.chat]
            )
            reply = response.choices[0].message.content
            st.session_state.chat.append(("assistant", reply))
        except Exception as e:
            reply = f"Fehler: {e}"
            st.session_state.chat.append(("assistant", reply))

    for role, msg in st.session_state.chat[::-1]:
        color = user_color if role == "user" else bot_color
        name = "👤 Du" if role == "user" else "🤖 GPT"
        st.markdown(f"<div style='background-color:{color};padding:10px;border-radius:10px;margin-bottom:10px;color:white'><strong>{name}:</strong><br>{msg}</div>", unsafe_allow_html=True)