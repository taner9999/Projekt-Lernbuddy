# 📘 Lernbuddy Deluxe – Dein smarter Studienbegleiter

**Lernbuddy Deluxe** ist eine interaktive Streamlit-Webapp, die Studierenden hilft, effizienter und smarter zu lernen. Sie bietet Lernplanerstellung, KI-Chat, Hochschulinformationen, Exportmöglichkeiten und eine schöne UI mit Darkmode.

---

## 🚀 Features

- **🏠 Startseite** mit Vorstellung & Features
- **💬 GPT-Chat** mit ChatGPT (GPT-3.5/4) für Studienfragen, Erklärungen etc.
- **🧠 Lernplan-Generator** mit GPT-gestützter Planung basierend auf Fächern, Prüfungen, Hinweisen & Schwierigkeitsgrad
  - Farbige Tagesübersicht
  - Export als Excel oder ICS-Kalender
- **🔎 Suchfunktion** für Lernplan-Einträge
- **🎓 Hochschul-Panel** mit:
  - 📚 Studiengänge
  - 🍽️ Mensaplan (PDF)
  - 💻 Moodle
  - 📖 Bibliothek
  - 🗺️ Lageplan (Karte + PDF)

---

## 🔧 Installation & Nutzung

### 📦 Benötigte Pakete (requirements.txt):
```bash
streamlit
pandas
openpyxl
requests
streamlit-lottie
fpdf
ics
openai
lxml
html5lib
beautifulsoup4
```

### ▶️ Starten (lokal)
```bash
streamlit run app.py
```

### ☁️ Streamlit Cloud:
- Projekt + `app.py` + `requirements.txt` auf GitHub laden
- In Streamlit Cloud deployen

---

## 🔐 OpenAI API Key
Für den GPT-Chat & Lernplan wird ein API Key benötigt. Diesen über Umgebungsvariable bereitstellen:
```bash
export OPENAI_API_KEY="dein-key"
```
Oder `.streamlit/secrets.toml` nutzen:
```toml
OPENAI_API_KEY = "dein-key"
```

---

## 👨‍💻 Entwickler
- Taner Altin
- Shefki Kuleta

> "Designed by Studierende – für Studierende"

---

## 🖼️ Vorschau
- 🧠 Automatisierter Lernplan
- 🌗 Darkmode & Farbpalette
- 📅 Kalenderexport (.ics)
- 📥 Excel mit Farbcodierung
- 💬 ChatGPT-Dialog
- 🗺️ Lageplan der Hochschule Kempten

---

# ✅ Code der App (Start)

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

...
