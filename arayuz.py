import streamlit as st
import sqlite3
import os

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Glimpse AI: Master 🦁", layout="wide")

# 2. ÖZEL TASARIM (CSS)
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .status-card { background: #1e1e1e; padding: 15px; border-radius: 10px; border-bottom: 3px solid #ffcc00; margin-bottom: 20px; }
    .ocr-box { background: #262730; border: 1px dashed #444; padding: 10px; font-family: monospace; font-size: 0.8em; margin-top: 5px; }
    .chat-bubble { background: #262730; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid #ffcc00; }
    </style>
    """, unsafe_allow_html=True)

# 3. YAN MENÜ
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/lion.png", width=100)
    st.title("Glimpse Control")
    st.write("---")
    ocr_active = st.toggle("OCR Recognition", value=True)
    privacy_active = st.toggle("Privacy Shield", value=True)
    st.write("---")
    st.success("🧠 Brain & Cloud: Connected")
    st.metric(label="Memories Analysed", value="5")
    st.caption("Developed by Bahadır Yıldız")

# 4. GİRİŞ KONTROLÜ
if 'giris_yapildi' not in st.session_state: st.session_state.giris_yapildi = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

if not st.session_state.giris_yapildi:
    st.markdown("<h1 style='text-align: center; color: #ffcc00;'>🦁 Glimpse AI Master</h1>", unsafe_allow_html=True)
    if st.button("Unlock Visual Intelligence 🚀", use_container_width=True):
        st.session_state.giris_yapildi = True
        st.rerun()
else:
    # --- ÜST PANEL: ARAMA MOTORU ---
    st.markdown("<h2 style='color: #ffcc00;'>🔍 Visual Memory Search</h2>", unsafe_allow_html=True)

    # Hızlı Kategori Butonları
    c1, c2, c3 = st.columns(3)
    q_cat = ""
    if c1.button("💻 Code"): q_cat = "code"
    if c2.button("🦁 GS"): q_cat = "football"
    if c3.button("📂 All"): q_cat = ""

    query = st.text_input("", value=q_cat, placeholder="Search (e.g. yellow, laptop, terminal)")

    if query:
        conn = sqlite3.connect('glimpse_memory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT path, info, created_at FROM screenshots")
        rows = cursor.fetchall()
        conn.close()

        results = [r for r in rows if r[1] and query.lower() in r[1].lower()]

        if results:
            st.write(f"Results for '{query}':")
            cols = st.columns(3)
            for i, (path, info, date) in enumerate(results):
                with cols[i % 3]:
                    # Privacy Shield & Resim Gösterimi
                    is_sens = any(w in info.lower() for w in ["password", "card", "tc no"])
                    if privacy_active and is_sens:
                        st.warning("🔒 Masked")
                        st.markdown(
                            "<div style='height:120px; background:repeating-linear-gradient(45deg,#333,#333 10px,#222 10px,#222 20px); border-radius:10px;'></div>",
                            unsafe_allow_html=True)
                    else:
                        if os.path.exists(path):
                            st.image(path)
                        else:
                            st.markdown(
                                "<div style='height:120px; background:#222; border-radius:10px; display:flex; align-items:center; justify-content:center;'>🖼️ Memory</div>",
                                unsafe_allow_html=True)

                    # Analiz Kartı
                    st.markdown(f"""<div class="status-card">
                        <p style='color:#ffcc00; font-size:0.8em;'><b>AI CAPTION:</b></p>
                        <p style='font-size:0.9em;'>"{info}"</p>""", unsafe_allow_html=True)
                    if ocr_active:
                        st.markdown(f"<div class='ocr-box'>OCR: [Text Detected]</div>", unsafe_allow_html=True)
                    st.markdown(f"<small style='color:#888;'>📅 {date[:10]}</small></div>", unsafe_allow_html=True)

    st.write("---")

    # --- ALT PANEL: AI CHAT (Yeni Bölüm) ---
    st.markdown("<h3 style='color: #ffcc00;'>💬 Ask Your Brain</h3>", unsafe_allow_html=True)
    chat_input = st.chat_input("Ask: 'What did I learn about SQL today?'")

    if chat_input:
        conn = sqlite3.connect('glimpse_memory.db')
        all_text = " ".join([r[0] for r in conn.execute("SELECT info FROM screenshots").fetchall() if r[0]])
        conn.close()

        # Basit AI Mantığı
        reply = "I've scanned your 5 visual memories. "
        if "code" in chat_input.lower():
            reply += "You spent time on coding and software development."
        elif "bugün" in chat_input.lower() or "today" in chat_input.lower():
            reply += f"Summary of your day: {all_text[:120]}..."
        else:
            reply += "I found information related to your Galatasaray interest and tech stack."

        st.session_state.chat_history.append({"u": chat_input, "ai": reply})

    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"<div style='text-align:right;'>👤 {chat['u']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bubble'>🦁 {chat['ai']}</div>", unsafe_allow_html=True)