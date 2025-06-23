# 🎓 Lernbuddy Deluxe

**Lernbuddy Deluxe** ist eine smarte, interaktive Studienhilfe – dein persönlicher KI-gestützter Lernassistent, entwickelt mit [Streamlit](https://streamlit.io) und OpenAI GPT-4.

> Entwickelt von Studierenden der Hochschule Kempten – für Studierende aller Fachrichtungen.

---

## 🚀 Features

### 💬 GPT-Chat – Dein KI-Tutor
- Stelle Fragen zum Studium, Alltag oder Fachinhalten
- GPT-4 antwortet im Stil eines Lerncoaches
- Farblich anpassbarer Chat (inkl. Darkmode)

### 🧠 Intelligenter Lernplan-Generator
- Fächer, Prüfungstermine & Schwierigkeitsgrad eingeben
- GPT erstellt automatisierten Lernplan (4 Wochen, mit Uhrzeiten)
- Export als **Excel-Datei** & **.ics-Kalenderdatei**

### 🔍 Suchfunktion
- Durchsuche deinen Lernplan nach Fachbegriffen

### 🎓 Hochschul-Panel (Kempten)
- Direktlinks zu Website, Moodle, Mensaplan, Bibliothek etc.
- Live-Karte & Gebäudeplan (2024)

---

## 🖼️ Vorschau

![Screenshot](https://www.hs-kempten.de/fileadmin/Bildpool/Lageplaene/Lageplan_Hochschule_Kempten_2024_DE.jpg)

---

## 🧰 Installation

### 📦 Voraussetzungen
- Python 3.9 oder höher
- API-Key von [OpenAI](https://platform.openai.com/account/api-keys)

### 🔧 Setup

```bash
git clone https://github.com/deinname/lernbuddy-deluxe.git
cd lernbuddy-deluxe

# Virtuelle Umgebung (optional, empfohlen)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt
