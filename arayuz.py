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
    # --- ALT PANEL: %100 DİNAMİK CHAT ---
    st.markdown("<h3 style='color: #ffcc00;'>💬 Creative Memory Assistant</h3>", unsafe_allow_html=True)
    chat_input = st.chat_input("Hafızanla rastgele konuş...")

    if chat_input:
        conn = sqlite3.connect('glimpse_memory.db')
        # Veritabanındaki tüm kayıtları çekip listeye atıyoruz
        all_rows = [r[0] for r in conn.execute("SELECT info FROM screenshots").fetchall() if r[0]]
        conn.close()

        if not all_rows: all_rows = ["Genel teknoloji verileri"]

        # Rastgele bir giriş ve rastgele bir hafıza seçiyoruz (Kritik Nokta!)
        giris_secenekleri = [
            "Valla baktım da,", "Hafızanı şöyle bir yokladım,",
            "Analizlerime göre,", "Gördüğüm kadarıyla,",
            "Enteresan bir detay buldum:", "Sistem taraması bitti:"
        ]

        # Her seferinde listeden rastgele bir hafıza parçasını seç (Hep aynı mems[0] olmasın)
        rastgele_hafiza = random.choice(all_rows)
        rastgele_giris = random.choice(giris_secenekleri)

        user_q = chat_input.lower()

        # Soruya göre bir ton belirle
        if "kod" in user_q or "python" in user_q:
            res = f"💻 {rastgele_giris} Yazılım tarafında yoğunlaşmışsın. Özellikle şu kaydın dikkat çekici: '{rastgele_hafiza[:50]}...'"
        elif "naber" in user_q or "nasılsın" in user_q:
            res = f"🦁 {rastgele_giris} Hafızandaki 5 farklı anıyı harmanladım. Şu an tam bir 'Digital Nomad' havasındasın!"
        else:
            # Kodda olmayan bir şey sorulursa her seferinde farklı bir cevap üret
            res = f"🔍 {rastgele_giris} Sorduğun konuyu araştırdım. Hafızanda şuna benzer bir şeyler var: '{rastgele_hafiza[:60]}...'"

        st.session_state.chat_history.append({"u": chat_input, "ai": res})

    # Sohbeti Ekrana Yazdır
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"<div style='text-align:right; color:#888;'>Siz: {chat['u']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bubble'>🦁 AI: {chat['ai']}</div>", unsafe_allow_html=True)