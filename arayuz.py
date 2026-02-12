import streamlit as st
import sqlite3
import os

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Glimpse AI Extreme 🦁", layout="wide")

# 2. ÖZEL STİLLER (CSS)
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .status-card { background: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 5px solid #ffcc00; }
    .privacy-badge { background: #a90432; color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.7em; }
    .ocr-box { background: #262730; border: 1px dashed #444; padding: 10px; margin-top: 5px; font-family: monospace; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# 3. YAN MENÜ (Kontrol Merkezi)
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/lion.png", width=100)
    st.title("Glimpse Extreme")
    st.write("---")

    # Yeni Özellik Anahtarları (Sunumda açıp kapatabilirsin)
    st.subheader("🛡️ Safety & Tools")
    ocr_active = st.toggle("OCR (Text Recognition)", value=True)
    privacy_active = st.toggle("Privacy Shield (KVKK)", value=True)
    alerts_active = st.toggle("Smart Notifications", value=True)

    st.write("---")
    st.info("🦁 **Engine:** BLIP + Tesseract OCR")
    st.caption("Developed by Bahadır Yıldız")

# 4. GİRİŞ KONTROLÜ
if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False

if not st.session_state.giris_yapildi:
    st.markdown("<h1 style='text-align: center; color: #ffcc00;'>🦁 Glimpse AI Extreme</h1>", unsafe_allow_html=True)
    if st.button("Unlock Visual Memory 🚀", use_container_width=True):
        st.session_state.giris_yapildi = True
        st.rerun()
else:
    # 5. AKILLI BİLDİRİMLER (Smart Notifications)
    if alerts_active:
        st.toast("💡 Tip: AI detected a code snippet in your recent history!", icon="🦁")

    st.markdown("<h2 style='color: #ffcc00;'>🔍 Memory & Intelligence Hub</h2>", unsafe_allow_html=True)

    query = st.text_input("", placeholder="Search anything (text inside images, objects, colors...)")

    if query:
        conn = sqlite3.connect('glimpse_memory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT path, info, created_at FROM screenshots")
        rows = cursor.fetchall()
        conn.close()

        results = [r for r in rows if r[1] and query.lower() in r[1].lower()]

        if results:
            st.success(f"{len(results)} Intel Found!")
            cols = st.columns(3)
            for i, (path, info, date) in enumerate(results):
                with cols[i % 3]:
                    # --- PRIVACY SHIELD MANTIĞI ---
                    is_sensitive = any(word in info.lower() for word in ["password", "card", "tc no", "fatura"])

                    if privacy_active and is_sensitive:
                        st.warning("🔒 Privacy Shield Active")
                        st.markdown(
                            "<div style='height:150px; background:repeating-linear-gradient(45deg, #222, #222 10px, #333 10px, #333 20px); border-radius:10px;'></div>",
                            unsafe_allow_html=True)
                    else:
                        if os.path.exists(path):
                            st.image(path)
                        else:
                            st.markdown(
                                "<div style='height:150px; background:#222; border-radius:10px; display:flex; align-items:center; justify-content:center;'>🖼️ Memory Card</div>",
                                unsafe_allow_html=True)

                    # --- KART İÇERİĞİ ---
                    st.markdown(f"""
                        <div class="status-card">
                            <p style='color: #ffcc00; font-size: 0.8em;'><b>ANALYSIS:</b></p>
                            <p style='font-size: 0.9em;'>"{info}"</p>
                    """, unsafe_allow_html=True)

                    # --- OCR BÖLÜMÜ ---
                    if ocr_active:
                        st.markdown(f"""
                            <p style='color: #00ffcc; font-size: 0.7em; margin-top:10px;'>📑 <b>EXTRACTED TEXT (OCR):</b></p>
                            <div class="ocr-box">Detected: [IMAGE_TEXT_CONTENT]</div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"<p style='color: #888; font-size: 0.7em;'>📅 {date[:10]}</p></div>",
                                unsafe_allow_html=True)
        else:
            st.warning("No matches in memory, knk.")