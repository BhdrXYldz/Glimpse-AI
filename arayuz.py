import streamlit as st
import sqlite3
import os

# 1. SAYFA AYARLARI VE CSS
st.set_page_config(page_title="Glimpse AI 🦁", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #121212 0%, #1a1a1a 100%);
        color: white;
    }
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: #ffcc00 !important;
        padding: 15px !important;
    }
    /* Resim Kartı Tasarımı */
    .image-card {
        background-color: #222;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #ffcc00;
        margin-bottom: 20px;
        min-height: 200px;
    }
    .placeholder-box {
        height: 150px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px dashed #444;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False


def akilli_ara_direkt(sorgu):
    sorgu = sorgu.lower().strip()
    words = sorgu.split()
    # GitHub'da dosya adı direkt ana dizinde olacağı için yol kontrolü
    db_path = 'glimpse_memory.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT path, info, created_at FROM screenshots")
    rows = cursor.fetchall()
    results = []
    for path, info, date in rows:
        if info is None: continue
        score = 0
        info_lower = info.lower()
        for word in words:
            if word in info_lower: score += 1
            if word in ["sarı", "mavi", "kırmızı", "yeşil", "yellow", "red", "blue"] and word in info_lower:
                score += 2
        if score > 0:
            results.append({"path": path, "ai_desc": info, "date": date[:10] if date else "Unknown", "score": score})
    results.sort(key=lambda x: x['score'], reverse=True)
    conn.close()
    return results


if not st.session_state.giris_yapildi:
    st.markdown("<h1 style='text-align: center; color: #ffcc00; font-size: 80px;'>🦁</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #ffcc00;'>Welcome to Glimpse AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaa;'>Your Intelligent Screen Memory Assistant</p>",
                unsafe_allow_html=True)
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📸 **Monitoring**\n\nAutomated capture.")
    with col2:
        st.success("🧠 **AI Analysis**\n\nVisual understanding.")
    with col3:
        st.warning("🔍 **Search**\n\nFind instantly.")
    st.write("---")
    if st.button("Explore Your Memory 🚀", use_container_width=True):
        st.session_state.giris_yapildi = True
        st.rerun()
else:
    st.markdown("<h2 style='text-align: center; color: #ffcc00;'>🔍 Memory Search</h2>", unsafe_allow_html=True)
    query = st.text_input("", placeholder="What are you looking for, knk? (e.g. yellow, code, graph)")

    if query:
        with st.spinner('Searching your memory...'):
            sonuclar = akilli_ara_direkt(query)
            if sonuclar:
                st.success(f"{len(sonuclar)} results found!")
                cols = st.columns(3)
                for i, res in enumerate(sonuclar):
                    with cols[i % 3]:
                        # --- GÖRSEL KONTROLÜ VE YER TUTUCU ---
                        if os.path.exists(res['path']):
                            st.image(res['path'], use_container_width=True)
                        else:
                            # Resim yoksa şık bir yer tutucu kutu gösteriyoruz
                            st.markdown(f"""
                                <div class="placeholder-box">
                                    <span style="font-size: 30px;">🖼️</span>
                                </div>
                            """, unsafe_allow_html=True)

                        # Açıklama kartı
                        st.markdown(f"""
                            <div class="image-card">
                                <p style='color: #ffcc00; margin-bottom: 5px;'><b>AI Intelligence:</b></p>
                                <p style='font-style: italic; font-size: 0.9em; color: #eee;'>"{res['ai_desc']}"</p>
                                <hr style='border: 0.1px solid #333; margin: 10px 0;'>
                                <p style='font-size: 0.8em; color: #888;'>📅 Detected on: {res['date']}</p>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No matches found in your memory.")