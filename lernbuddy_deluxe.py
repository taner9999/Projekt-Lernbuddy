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
    st.title("🎓 Willkommen bei Lernbuddy Deluxe 👋")
    show_lottie("https://assets2.lottiefiles.com/packages/lf20_myejiggj.json")
    st.markdown("""

**Lernbuddy Deluxe** ist **mehr als nur ein Chatbot** – er ist dein persönlicher Studien-Coach, digitaler Lernpartner und smarter Assistent, der dich durch das gesamte Semester begleitet! 🚀📚

---

## 💡 Was Lernbuddy Deluxe für dich tun kann:

### 💬 GPT-Chat – Dein KI-Tutor  
Stelle Fragen rund ums Studium – oder auch zum Leben. Ob:  
- ✅ Lernhilfe & Verständnisfragen  
- ✅ Zusammenfassungen & Erklärungen  
- ✅ Studienorganisation oder Alltagssorgen  
**Der GPT-Tutor ist für dich da!**

### 🧠 Automatischer Lernplan-Generator  
- Du trägst deine Fächer, Prüfungen & Schwierigkeitsgrad ein  
- Der Bot erstellt dir automatisch einen effizienten Lernplan – taggenau mit Zeitvorgaben  
- **Exportiere den Plan als PDF oder .ics-Kalenderdatei**

### 🔎 Intelligente Suchfunktion  
Finde blitzschnell Inhalte und Fächer im Lernplan wieder – perfekt zum Wiederholen!

### 🎨 Farben & Darkmode  
Wähle deinen Style:  
- 🌗 Darkmode  
- 🎨 5 moderne Farbpaletten  
- Inspiriert vom Design der **Hochschule Kempten**

### 🎓 Hochschul-Panel  
Direkte Links zu:  
- 📚 Studiengänge  
- 🍽️ Mensaplan  
- 💻 Moodle  
- 📖 Bibliothek  
- 🧾 MeinCampus  

---

## ✨ Entwickelt für Studierende – von Studierenden  
> Mit ❤️ von **Taner Altin** & **Shefki Kuleta**  
> Powered by **Streamlit** & **OpenAI GPT-4**
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
    st.header("🧠 Lernplan mit GPT-Hinweisen pro Fach")

    n = st.number_input("Wie viele Prüfungen hast du?", 1, 10)
    subjects = []

    for i in range(int(n)):
        name = st.text_input(f"📘 Fach {i+1}", key=f"subj_{i}")
        date = st.date_input(f"📅 Prüfung {i+1}", key=f"date_{i}")
        diff = st.slider("📊 Schwierigkeit (1–10)", 1, 10, key=f"diff_{i}")
        hint = st.text_area(f"🧠 Hinweis für GPT zu '{name or 'Fach'}'", key=f"hint_{i}",
                            placeholder="z. B.: nur ab 12 Uhr, nicht sonntags …")
        if name.strip():
            subjects.append({
                "name": name.strip(),
                "exam_date": str(date),
                "difficulty": diff,
                "hint": hint.strip() or "keine"
            })

    if st.button("✅ GPT-Lernplan generieren"):
        if not subjects:
            st.warning("⚠️ Bitte gib mindestens ein Fach ein.")
        else:
            fachliste = "\n".join(
                [f"- {s['name']} (Prüfung: {s['exam_date']}, Schwierigkeit: {s['difficulty']}) – Hinweis: {s['hint']}"
                 for s in subjects]
            )

            prompt = f"""
Du bist ein Lerncoach und erstelle bitte einen Lernplan für die folgenden Fächer, Prüfungen und persönlichen Hinweise.

Erstelle einen 4‑Wochen-Plan mit Uhrzeiten (z. B. 10:00–10:45), Pausen und maximal 4 Blöcken pro Tag. Verteile die Fächer sinnvoll, beachte die individuellen Wünsche, und vermeide Doppelbelegungen.

Fächer & Hinweise:
{fachliste}

Erstelle den Plan strukturiert nach Tagen. Nutze deutsche Wochentage und gib den Plan in folgendem Format aus:

Montag, 01.07.2025  
- 12:00–12:45: Mathe  
- 13:15–14:00: BWL  
...
"""

            with st.spinner("GPT plant deinen Lernplan …"):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = response.choices[0].message.content
                    st.markdown("### 📅 Vorschlag von GPT:")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Fehler beim GPT-Aufruf: {e}")


# Suche
elif menu == "🔎 Suche":
    st.header("🔎 Lernplan durchsuchen")
    term = st.text_input("🔍 Suchbegriff:")
    if os.path.exists("lernplan.xlsx"):
        df = pd.read_excel("lernplan.xlsx")
        result = df[df["Fach"].str.contains(term, case=False, na=False)]
        if not result.empty:
            st.success(f"{len(result)} Einträge gefunden:")
            st.dataframe(result)
        else:
            st.warning("Keine Treffer.")
    else:
        st.info("Noch kein Lernplan vorhanden.")

# Hochschule
elif menu == "🎓 Hochschule":
    st.header("🎓 Hochschule Kempten")
    show_lottie("https://assets10.lottiefiles.com/packages/lf20_3rwasyjy.json", 180)
st.markdown("""
**🔗 Wichtige Links:**
- [🌐 Website](https://www.hs-kempten.de/)
- [📚 Studiengänge](https://www.hs-kempten.de/studium/studienangebot)
- [🍽️ Mensaplan](https://www.stw-swt.de/essen-trinken/speiseplaene/)
- [📖 Bibliothek](https://www.hs-kempten.de/einrichtungen/bibliothek)
- [💻 Moodle](https://moodle.hs-kempten.de/)
- [🧾 MeinCampus](https://campus.hs-kempten.de/)
""")

import re
def parse_gpt_plan(plan_text):
    data = []
    current_day = None
    date_pattern = re.compile(r"^([A-Za-zäöüÄÖÜß]+), (\d{2}\.\d{2}\.\d{4})$")
    session_pattern = re.compile(r"(\d{2}:\d{2})–(\d{2}:\d{2}): (.+)")

    lines = plan_text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("Prüfung") or "Pause" in line:
            continue
        date_match = date_pattern.match(line)
        if date_match:
            current_day = {"Wochentag": date_match.group(1), "Datum": date_match.group(2)}
        elif session_pattern.match(line) and current_day:
            start, end, fach = session_pattern.findall(line)[0]
            data.append({
                "Wochentag": current_day["Wochentag"],
                "Datum": current_day["Datum"],
                "Fach": fach,
                "Startzeit": start,
                "Endzeit": end,
                "Dauer": "45 Min"
            })
    return pd.DataFrame(data)

df_gpt = parse_gpt_plan(result)
if df_gpt.empty:
    st.warning("⚠️ GPT-Plan konnte nicht in eine Tabelle umgewandelt werden.")
else:
    st.markdown("### 🧠 GPT-Plan als Tabelle:")
    st.dataframe(df_gpt)

    import openpyxl
    from openpyxl.styles import Font
    from openpyxl.utils.dataframe import dataframe_to_rows

    def export_excel_formatted(df, filename="gpt_plan.xlsx"):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "GPT-Lernplan"

        for i, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
            ws.append(row)
            if i == 1:
                for cell in ws[i]:
                    cell.font = Font(bold=True)

        for col in ws.columns:
            max_len = max(len(str(c.value)) if c.value else 0 for c in col)
            ws.column_dimensions[col[0].column_letter].width = max_len + 2

        wb.save(filename)
        with open(filename, "rb") as f:
            st.download_button("📥 GPT-Plan als Excel herunterladen", f, file_name=filename)

    export_excel_formatted(df_gpt)

