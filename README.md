# 🎓 Lernbuddy Deluxe – Dein smarter Studienassistent

**Lernbuddy Deluxe** ist mehr als nur ein Chatbot – es ist ein digitaler Studienassistent, persönlicher Tutor und Motivator in einem. Die App wurde speziell für Studierende entwickelt, die smarter, strukturierter und stressfreier lernen möchten.

Mit einem modernen Design, intuitiver Bedienung und leistungsstarker KI (GPT) hilft Lernbuddy dir dabei, dein Studium im Griff zu behalten – egal ob du Fragen zu Vorlesungen hast, deinen Lernplan organisieren willst oder einfach Motivation brauchst.

---

## 🚀 Was macht Lernbuddy Deluxe so besonders?

### 💬 GPT-gestützter Chat: Dein persönlicher Tutor 24/7

- 📘 Fachliche Erklärungen auf Augenhöhe  
- 🧠 Zusammenfassungen & Mindmaps  
- 🗂 Lernstrategien & Eselsbrücken  
- 💡 Ratschläge für Studium, Alltag & Motivation  
- 🙋 Private Fragen? Kein Problem – der Bot bleibt freundlich und diskret  

---

### 🧠 Intelligente Lernplan-Funktion

- ✅ Fächer, Prüfungstermine & Schwierigkeit eingeben  
- 📆 Automatische Lernzeitberechnung  
- ⏱ Tägliche Lerneinheiten mit Uhrzeiten  
- 📄 Export als PDF oder 📅 Kalenderdatei (.ics)  
- 🔍 Lernplan-Durchsuchung & Speicherung  

---

### 🎨 Anpassbares Design

- 🌗 Darkmode  
- 🎨 Farbwahl für Chat-Design  
- 🏫 Hochschul-Theme (Kempten)  
- ✨ Animationen für Motivation  

---

### 🎓 Hochschule Kempten Integration

- [📚 Studiengänge](https://www.hs-kempten.de/studium/studienangebot)  
- [🍽️ Mensaplan](https://www.stw-swt.de/essen-trinken/speiseplaene/)  
- [💻 Moodle](https://moodle.hs-kempten.de/)  
- [📖 Bibliothek](https://www.hs-kempten.de/einrichtungen/bibliothek)  
- [🧾 MeinCampus](https://campus.hs-kempten.de/)  

---

## 🖥️ Installation & Start (Windows & macOS)

### 🔧 Voraussetzungen

- Python 3.8 oder neuer  
- OpenAI API-Key: https://platform.openai.com/account/api-keys

---

### 📦 Schritt-für-Schritt-Anleitung

```bash
# 1. Projekt klonen oder ZIP entpacken
git clone https://github.com/deinname/lernbuddy-deluxe.git
cd lernbuddy-deluxe

# 2. Virtuelle Umgebung (optional aber empfohlen)
python -m venv venv
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt
# oder einzeln:
pip install streamlit openai pandas fpdf ics streamlit-lottie requests

# 4. API-Key in lernbuddy_deluxe.py einfügen:
# openai.api_key = "DEIN_API_KEY"

# 5. App starten
streamlit run lernbuddy_deluxe.py
