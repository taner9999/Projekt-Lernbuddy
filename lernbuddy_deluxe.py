import streamlit as st
import datetime
import pandas as pd
import os
import requests
from streamlit_lottie import st_lottie
from fpdf import FPDF
from ics import Calendar, Event
from openai import OpenAI
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows

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
- ✅ Lernhilfe & Verständnisfragen  
- ✅ Zusammenfassungen & Erklärungen  
- ✅ Studienorganisation oder Alltagssorgen  

### 🧠 Automatischer Lernplan-Generator  
- Trage Fächer, Prüfungen & Hinweise ein  
- Erhalte automatisch einen 4-Wochen-Plan  
- Export als PDF / Excel / Kalender

### 🔎 Suchfunktion  
- Finde Inhalte im Lernplan blitzschnell

### 🎓 Hochschule Kempten  
- 📚 Studiengänge  
- 🍽️ Mensaplan  
- 💻 Moodle  
- 📖 Bibliothek  
- 🧾 MeinCampus
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

# Lernplan-Generator
elif menu == "🧠 Lernplan":
    st.header("🧠 Lernplan mit GPT-Hinweisen, Excel- & Kalender-Export")

    n = st.number_input("Wie viele Prüfungen hast du?", 1, 10)
    subjects = []
    for i in range(int(n)):
        name = st.text_input(f"📘 Fach {i+1}", key=f"subj_{i}")
        date = st.date_input(f"📅 Prüfung {i+1}", key=f"date_{i}")
        diff = st.slider("📊 Schwierigkeit (1–10)", 1, 10, key=f"diff_{i}")
        hint = st.text_area(f"🧠 Hinweis für GPT zu '{name or 'Fach'}'", key=f"hint_{i}")
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
                f"- {s['name']} (Prüfung: {s['exam_date']}, Schwierigkeit: {s['difficulty']}) – Hinweis: {s['hint']}"
                for s in subjects
            )
            prompt = f"""
Du bist ein Lerncoach. Erstelle einen 4-Wochen-Plan mit Uhrzeiten (z. B. 10:00–10:45), Pausen und max. 4 Blöcken pro Tag.

Fächer & Hinweise:
{fachliste}

Format:
Montag, 01.07.2025
- 12:00–12:45: Mathe
- 14:00–14:45: BWL
"""

            with st.spinner("GPT erstellt deinen Plan …"):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = response.choices[0].message.content
                    st.markdown("### 📅 Lernplan von GPT:")
                    st.markdown(result)

                    import re

                    def parse_gpt_plan(text):
                        date_re = re.compile(r"^([A-Za-zäöüÄÖÜß]+)[, ]+\s*(\d{2}[./]\d{2}[./]\d{4})")
                        session_re = re.compile(
                            r"-?\s*(\d{2}[:\.]\d{2})\s*(?:–|-|bis)\s*(\d{2}[:\.]\d{2})\s*[:\-–]?\s*(.+)",
                            re.IGNORECASE
                        )
                        rows = []
                        current = {}
                        for line in text.splitlines():
                            line = line.strip()
                            if not line or "pause" in line.lower():
                                continue
                            dm = date_re.match(line)
                            sm = session_re.match(line)
                            if dm:
                                current = {"Wochentag": dm.group(1), "Datum": dm.group(2)}
                            elif sm and current:
                                start, end, fach = sm.groups()
                                rows.append({
                                    "Wochentag": current["Wochentag"],
                                    "Datum": current["Datum"],
                                    "Fach": fach.strip(),
                                    "Startzeit": start.replace(".", ":"),
                                    "Endzeit": end.replace(".", ":"),
                                    "Dauer": "45 Min"
                                })
                        return pd.DataFrame(rows)

                    df_gpt = parse_gpt_plan(result)

                    if df_gpt.empty:
                        st.warning("⚠️ GPT-Plan konnte nicht als Tabelle erkannt werden.")
                    else:
                        st.markdown("### 🧠 Farbliche Lernübersicht")
                        palette = ["#FFD700", "#00CED1", "#FF8C00", "#ADFF2F",
                                   "#DA70D6", "#FFA07A", "#7FFFD4", "#D2691E"]
                        fachfarben = {f: palette[i % len(palette)] for i, f in enumerate(df_gpt["Fach"].unique())}

                        for _, r in df_gpt.iterrows():
                            c = fachfarben.get(r["Fach"], "#EEE")
                            st.markdown(f"""
                                <div style='background-color:{c};padding:8px;border-radius:6px;margin-bottom:6px'>
                                  <strong>{r["Datum"]} ({r["Wochentag"]})</strong><br>
                                  {r["Startzeit"]}–{r["Endzeit"]}: <b>{r["Fach"]}</b>
                                </div>
                            """, unsafe_allow_html=True)

                        st.markdown("### 📊 Lernzeit-Statistik")
                        df_stats = df_gpt.copy()
                        df_stats["Minuten"] = df_stats["Dauer"].str.extract(r"(\\d+)").astype(int)
                        stats = df_stats.groupby("Fach").agg(
                            Sessions=("Fach", "count"),
                            Total_Minuten=("Minuten", "sum")
                        ).reset_index()
                        st.dataframe(stats)

                        # Excel-Export
                        def export_excel(df, stats_df, filename="lernplan.xlsx"):
                            wb = openpyxl.Workbook()
                            ws1 = wb.active
                            ws1.title = "Plan"
                            for i, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
                                ws1.append(row)
                                for j, cell in enumerate(ws1[i], 1):
                                    if i == 1:
                                        cell.font = Font(bold=True)
                                    elif df.columns[j-1] == "Fach":
                                        col = fachfarben.get(cell.value, "#EEEEEE").lstrip("#")
                                        cell.fill = PatternFill(start_color=col, end_color=col, fill_type="solid")
                            ws2 = wb.create_sheet("Statistik")
                            for i, row in enumerate(dataframe_to_rows(stats_df, index=False, header=True), 1):
                                ws2.append(row)
                                if i == 1:
                                    for cell in ws2[i]:
                                        cell.font = Font(bold=True)
                            for ws in (ws1, ws2):
                                for col in ws.columns:
                                    width = max(len(str(c.value)) for c in col) + 2
                                    ws.column_dimensions[col[0].column_letter].width = width
                            wb.save(filename)
                            with open(filename, "rb") as f:
                                st.download_button("📥 Excel herunterladen", f, file_name=filename)

                        export_excel(df_gpt, stats)

                        # ICS-Export
                        def export_ics(df, filename="lernplan.ics"):
                            cal = Calendar()
                            for _, r in df.iterrows():
                                d = datetime.datetime.strptime(r["Datum"], "%d.%m.%Y").date()
                                stime = datetime.datetime.strptime(r["Startzeit"], "%H:%M").time()
                                etime = datetime.datetime.strptime(r["Endzeit"], "%H:%M").time()
                                ev = Event()
                                ev.name = f"{r['Fach']} – Lernen"
                                ev.begin = datetime.datetime.combine(d, stime)
                                ev.end = datetime.datetime.combine(d, etime)
                                ev.description = f"{r['Fach']} am {r['Datum']} ({r['Wochentag']})"
                                cal.events.add(ev)
                            with open(filename, "w", encoding="utf-8") as f:
                                f.writelines(cal)
                            with open(filename, "rb") as f:
                                st.download_button("📆 ICS herunterladen", f, file_name=filename, mime="text/calendar")

                        export_ics(df_gpt)

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
