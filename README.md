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

🚀 Schritt-für-Schritt: Lernbuddy Deluxe auf Streamlit Cloud deployen
✅ 1. GitHub-Repository erstellen
Gehe zu https://github.com/new

Gib deinem Projekt einen Namen, z. B. lernbuddy-deluxe

Aktiviere ✅ „Initialize this repository with a README“

Klicke auf Create repository

✅ 2. Projektdateien hinzufügen
Du brauchst mindestens folgende Dateien in deinem GitHub-Repo:

Datei	Funktion
lernbuddy_deluxe.py	Dein Hauptprogramm
requirements.txt	Alle benötigten Python-Bibliotheken
Optional: README.md	Projektbeschreibung (falls nicht im Code selbst)

📦 Beispiel requirements.txt (füge diese Datei in dein Repo):
txt
Kopieren
Bearbeiten
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
📌 Achte auf die richtige Schreibweise! Ohne diese Datei funktioniert der Cloud-Deploy nicht korrekt.

✅ 3. API-Key setzen (OpenAI)
Da du OpenAI verwendest, brauchst du einen API-Key:

Erstelle einen Key unter https://platform.openai.com/account/api-keys

Kopiere den Key

✅ 4. Auf Streamlit Cloud deployen
Gehe zu https://streamlit.io/cloud

Klicke auf "Get Started" → mit GitHub verbinden

Wähle dein Repo lernbuddy-deluxe

Wähle die Datei lernbuddy_deluxe.py als App-Datei

✅ Klicke auf Deploy

✅ 5. Umgebungsvariable setzen (OpenAI API Key)
Nach dem ersten Deploy:

Klicke in der Streamlit Cloud oben rechts auf ⚙️ „Settings“

Gehe zu „Secrets“

Füge hinzu:

ini
Kopieren
Bearbeiten
OPENAI_API_KEY = dein-api-key-hier
Klicke auf „Save“

→ App neu starten 🔁

✅ 6. Fertig 🎉
Deine App ist nun öffentlich erreichbar unter einer URL wie:

cpp
Kopieren
Bearbeiten
https://<dein-username>-lernbuddy-deluxe.streamlit.app/
Wenn du möchtest, kann ich dein GitHub-Repo automatisch vorbereiten (README, requirements.txt, .gitignore etc.). Sag einfach Bescheid!







Du:
anleitung für andere


ChatGPT:
Perfekt – hier ist eine Anleitung für andere Nutzer:innen, die dein Lernbuddy Deluxe Projekt selbst deployen und nutzen möchten. Du kannst diesen Text direkt in dein README.md auf GitHub einfügen oder z. B. auf Moodle oder per Mail teilen.

🎓 Lernbuddy Deluxe – Dein smarter Lernplan-Coach (Streamlit App)
Lernbuddy Deluxe ist eine interaktive Lernplattform für Studierende, die dir hilft, Lernpläne mit KI zu erstellen, Lernzeit zu analysieren, mit ChatGPT zu interagieren und direkten Zugang zur Hochschule Kempten zu erhalten – alles in einer App.

🚀 So nutzt du Lernbuddy Deluxe selbst (mit Streamlit Cloud)
🧰 Voraussetzungen
Kostenloser GitHub-Account: github.com/join

Kostenloser Streamlit Cloud Account: streamlit.io/cloud

Kostenloser OpenAI API-Key: platform.openai.com/account/api-keys

📦 1. Dieses Repository forken oder klonen
👉 Du kannst dieses Repo forken (oben rechts auf GitHub klicken)
Oder lokal klonen und anpassen:

bash
Kopieren
Bearbeiten
git clone https://github.com/<DEIN_USERNAME>/lernbuddy-deluxe.git
🧾 2. Die Datei requirements.txt
Stelle sicher, dass folgende Bibliotheken enthalten sind:

txt
Kopieren
Bearbeiten
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
🧠 3. OpenAI API-Key sichern
Gehe auf: https://platform.openai.com/account/api-keys

Erstelle einen API-Key und kopiere ihn

Füge ihn später in Streamlit Cloud unter "Secrets" ein

🌐 4. Streamlit Cloud Deployment
Gehe zu: https://streamlit.io/cloud

Melde dich mit GitHub an

Klicke auf "New app"

Wähle dein Repo und als Python-Datei: lernbuddy_deluxe.py

Klicke auf Deploy

🔐 5. OpenAI API-Key einfügen (in Streamlit Cloud)
Gehe in der Streamlit App auf → ⚙️ „Settings“

Dann zu → Secrets

Füge folgenden Key ein:

ini
Kopieren
Bearbeiten
OPENAI_API_KEY = sk-xxxxxxx...
Speichern & App neu starten

✅ 6. Fertig!
Deine App läuft jetzt live unter einer eigenen URL:

cpp
Kopieren
Bearbeiten
https://<dein-name>-lernbuddy-deluxe.streamlit.app/
🧩 Features der App
Funktion	Beschreibung
🎓 Startseite	Einführung, Funktionen, Darkmode
💬 GPT-Chat	Frag ChatGPT direkt in der App
🧠 Lernplan-Generator	Fächer + Termine + Schwierigkeit → KI-generierter Lernplan
📊 Statistik	Analyse deiner Lernzeit pro Fach
📥 Exporte	Excel (.xlsx) und Kalender (.ics)
🔍 Suche	Lernplan nach Stichworten durchsuchen
🎓 Hochschule	Links zu Mensaplan, Moodle, Lageplan & mehr

✨ Credits
Entwickelt von Taner Altin & Shefki Kuleta

Powered by Streamlit & OpenAI

Hochschule Kempten Design 💙
