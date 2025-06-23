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
    st.header("🧠 Lernplan mit Uhrzeiten, Pausen & GPT-Hinweisen")
    n = st.number_input("Wie viele Prüfungen hast du?", 1, 10)
    subjects = []

    for i in range(int(n)):
        name = st.text_input(f"📘 Fach {i+1}", key=f"subj_{i}")
        date = st.date_input(f"📅 Prüfung {i+1}", key=f"date_{i}")
        diff = st.slider("📊 Schwierigkeit (1–10)", 1, 10, key=f"diff_{i}")
        subjects.append((name, date, diff))

    hinweise = st.text_area("📝 Besondere Wünsche an GPT (optional)", 
        placeholder="Z. B.: Sonntag frei. Mathe doppelt so oft. Informatik nur vormittags...")

    def generate_learning_schedule(subjects, start_hour=9, end_hour=18, session_minutes=45, break_minutes=15):
        schedule = []
        sessions = []
        day_pointer = datetime.date.today()

        for name, exam_date, difficulty in subjects:
            total_minutes = difficulty * 90
            sessions.append({"name": name, "exam_date": exam_date, "remaining": total_minutes})

        for _ in range(28):
            current_time = datetime.datetime.combine(day_pointer, datetime.time(start_hour, 0))
            end_time = datetime.datetime.combine(day_pointer, datetime.time(end_hour, 0))

            while current_time + datetime.timedelta(minutes=session_minutes) <= end_time:
                sessions.sort(key=lambda x: (x["exam_date"], -x["remaining"]))
                for subj in sessions:
                    if subj["remaining"] >= session_minutes and day_pointer < subj["exam_date"]:
                        schedule.append({
                            "Datum": day_pointer.strftime("%A, %d.%m.%Y"),
                            "Fach": subj["name"],
                            "Startzeit": current_time.strftime("%H:%M"),
                            "Endzeit": (current_time + datetime.timedelta(minutes=session_minutes)).strftime("%H:%M"),
                            "Dauer": f"{session_minutes} Min"
                        })
                        subj["remaining"] -= session_minutes
                        current_time += datetime.timedelta(minutes=session_minutes + break_minutes)
                        break
                else:
                    break
            day_pointer += datetime.timedelta(days=1)

        return pd.DataFrame(schedule)

    if st.button("✅ Lernplan mit GPT-Hinweisen erstellen"):
        prompt = f"""
        Du bist ein KI-Planer für Lernpläne. Erstelle eine Aufteilung mit Uhrzeiten und Pausen für folgende Prüfungen:

        {subjects}

        Berücksichtige folgende Wünsche:
        {hinweise}
        """
        try:
            gpt_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            st.markdown("🤖 **GPT-Vorschlag:**")
            st.markdown(gpt_response.choices[0].message.content)
        except Exception as e:
            st.error(f"Fehler bei GPT-Aufruf: {e}")

        df = generate_learning_schedule(subjects)
        st.success("✅ Zeitbasierter Lernplan lokal erstellt:")
        st.dataframe(df)
        df.to_excel("lernplan.xlsx", index=False)
        with open("lernplan.xlsx", "rb") as f:
            st.download_button("📥 Excel herunterladen", f, file_name="lernplan.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

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
- [🧾 MeinCampus](
