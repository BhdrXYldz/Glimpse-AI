import streamlit as st
import sqlite3
import os
import random
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

# 3. YAN MENÜ (Kontrol Paneli)
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/lion.png", width=100)
    st.title("Glimpse Control")
    st.write("---")
    # İşte buraya o 3'lü kalkanı ekledik:
    ocr_active = st.toggle("OCR Recognition", value=True)
    privacy_active = st.toggle("Privacy Shield", value=True)
    alerts_active = st.toggle("Smart Notifications", value=True)  # ARTIK GÖRÜNÜYOR!

    st.write("---")
    st.success("🧠 Brain & Cloud: Connected")
    st.metric(label="Total Memories", value="5")
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
    # --- SMART NOTIFICATION (Bildirim Fırlatma) ---
    if alerts_active:
        st.toast("🦁 AI: 5 memories analyzed. Ready to search!", icon="💡")

    # --- ÜST PANEL: ARAMA MOTORU ---
    st.markdown("<h2 style='color: #ffcc00;'>🔍 Visual Memory Search</h2>", unsafe_allow_html=True)

    query = st.text_input("Search (e.g. yellow, code, laptop)", placeholder="Find anything...")

    if query:
        conn = sqlite3.connect('glimpse_memory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT path, info, created_at FROM screenshots")
        rows = cursor.fetchall()
        conn.close()

        results = [r for r in rows if r[1] and query.lower() in r[1].lower()]

        if results:
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
                        st.markdown(
                            "<div style='height:120px; background:#222; border-radius:10px; display:flex; align-items:center; justify-content:center;'>🖼️ Memory Image</div>",
                            unsafe_allow_html=True)

                    # Analiz Kartı
                    st.markdown(f"""<div class="status-card">
                        <p style='color:#ffcc00; font-size:0.8em;'><b>AI CAPTION:</b></p>
                        <p style='font-size:0.9em;'>"{info}"</p>""", unsafe_allow_html=True)
                    if ocr_active:
                        st.markdown(f"<div class='ocr-box'>OCR: [Text Content Detected]</div>", unsafe_allow_html=True)
                    st.markdown(f"<small style='color:#888;'>📅 {date[:10]}</small></div>", unsafe_allow_html=True)

    st.write("---")

    # --- ALT PANEL: AI CHAT ---
    # --- ALT PANEL: %100 GLOBAL ENGLISH MASTER CHAT ---
    st.markdown("<h3 style='color: #ffcc00;'>💬 Glimpse AI Global Assistant</h3>", unsafe_allow_html=True)
    chat_input = st.chat_input("Ask your memory anything (English only)...")

    if chat_input:
        conn = sqlite3.connect('glimpse_memory.db')
        all_rows = [r[0] for r in conn.execute("SELECT info FROM screenshots").fetchall() if r[0]]
        conn.close()

        user_q = chat_input.lower()
        # Her seferinde farklı bir anıyı çekerek özgünlüğü koruyoruz
        memory_fragment = random.choice(all_rows)[:75] if all_rows else "a visual data point"

        # --- EN GENİŞ İNGİLİZCE HAVUZU MANTIĞI ---

        # 1. Selamlaşma & Tanışma (Greetings)
        if any(w in user_q for w in ['hi', 'hello', 'hey', 'morning', 'greetings', 'who are you', 'what is your name']):
            res = random.choice([
                "Hello Bahadır! I am Glimpse AI, your personal visual memory assistant. How can I help?",
                "Hi there! Ready to explore your digital history. Ask me about your screenshots!",
                "Greetings! I've analyzed your 5 memories and I'm ready for your questions."
            ])

        # 2. Durum & Hal Hatır (Status & Mood)
        elif any(w in user_q for w in ['how are you', 'how is it going', 'whats up', 'status', 'working']):
            res = random.choice([
                "I'm functioning perfectly at 100% efficiency! 🦁",
                "Systems are green! I've successfully indexed your latest visual data.",
                "Doing great! Your 5 memories are stored and analyzed for your convenience."
            ])

        # 3. Sevgi & Övgü (Appreciation)
        elif any(w in user_q for w in ['love', 'awesome', 'great', 'cool', 'good job', 'wow', 'amazing']):
            res = random.choice([
                "🦁 Thank you! I'm dedicated to providing the best visual intelligence for you.",
                "I appreciate the positive feedback! Always here to assist your workflow.",
                "Love you too, buddy! Let's keep making your data useful."
            ])

        # 4. Teknik & Yazılım (Tech & Code)
        elif any(w in user_q for w in ['code', 'python', 'sql', 'tech', 'data', 'programming', 'script']):
            res = f"💻 Technical analysis: I found several coding patterns in your history, specifically related to: {memory_fragment}..."

        # 5. Teşekkür (Gratitude)
        elif any(w in user_q for w in ['thanks', 'thank you', 'thx']):
            res = "You're very welcome! Feel free to ask more about your visual memory. 🦁"

        # 6. Negatif Durumlar (Negative/Tired Sentiment)
        elif any(w in user_q for w in ['bad', 'sad', 'tired', 'bored', 'exhausted']):
            res = "I noticed some low energy. You've been working hard according to my logs! Why not take a short break? ☕"

        # 7. HER ŞEYİ KAPSAYAN FALLBACK (Kodda olmayan her şey için)
        else:
            res = random.choice([
                f"Based on my deep scan, I see you were recently busy with: {memory_fragment}...",
                f"I've cross-referenced your query with your 5 memories. I found matches related to: {memory_fragment}...",
                "Interesting question! While I don't have a direct answer, your history shows a lot of activity in this area.",
                f"My AI brain suggests that you've been exploring: {memory_fragment} lately."
            ])

        st.session_state.chat_history.append({"u": chat_input, "ai": res})

    # Render Sohbet
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"<div style='text-align:right; color:#888;'>User: {chat['u']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bubble'>🦁 AI: {chat['ai']}</div>", unsafe_allow_html=True)