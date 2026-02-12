import streamlit as st
import sqlite3
import os

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Glimpse AI Dashboard 🦁", layout="wide")

# 2. YAN MENÜ (SIDEBAR)
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/lion.png", width=100)
    st.title("Glimpse Control")
    st.write("---")

    # İstatistik çekme
    try:
        conn = sqlite3.connect('glimpse_memory.db')
        total_count = conn.execute("SELECT COUNT(*) FROM screenshots").fetchone()[0]
        conn.close()
        st.metric(label="Total Memories 📸", value=total_count)
    except:
        st.metric(label="Total Memories 📸", value="0")

    st.write("---")
    st.info("🦁 **Status:** System Active")
    st.success("🔗 **Cloud:** Connected")
    st.write("---")
    st.caption("Developed by Bahadır Yıldız")

# 3. TASARIM (CSS)
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .main-title { color: #ffcc00; text-align: center; font-size: 3em; font-weight: bold; }
    .image-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 15px;
        border-bottom: 4px solid #ffcc00;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False

# 4. AKIŞ KONTROLÜ
if not st.session_state.giris_yapildi:
    st.markdown("<h1 class='main-title'>🦁 Glimpse AI</h1>", unsafe_allow_html=True)
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧠 Your Second Brain")
        st.write("Everything you see on your screen is now searchable. Powered by AI.")
    with col2:
        if st.button("Explore Your Memory 🚀", use_container_width=True):
            st.session_state.giris_yapildi = True
            st.rerun()
else:
    # --- ANA PANEL ---
    st.markdown("<h2 style='color: #ffcc00;'>🔍 Memory Search Engine</h2>", unsafe_allow_html=True)

    # Hızlı Kategori Butonları (YBS Şovu)
    st.write("Quick Categories:")
    c1, c2, c3, c4 = st.columns(4)
    q_cat = ""
    if c1.button("💻 Coding"): q_cat = "code"
    if c2.button("🦁 Galatasaray"): q_cat = "football"
    if c3.button("📊 Data"): q_cat = "graph"
    if c4.button("📁 All"): q_cat = ""

    query = st.text_input("", value=q_cat, placeholder="Type to search... (e.g. yellow, laptop, terminal)")

    if query:
        with st.spinner('Thinking...'):
            conn = sqlite3.connect('glimpse_memory.db')
            cursor = conn.cursor()
            cursor.execute("SELECT path, info, created_at FROM screenshots")
            rows = cursor.fetchall()
            conn.close()

            results = [r for r in rows if r[1] and query.lower() in r[1].lower()]

            if results:
                st.success(f"{len(results)} matches found!")
                cols = st.columns(3)
                for i, (path, info, date) in enumerate(results):
                    with cols[i % 3]:
                        # Resim kontrolü
                        if os.path.exists(path):
                            st.image(path, use_container_width=True)
                        else:
                            st.markdown(
                                "<div style='height:100px; background:#333; border-radius:10px; display:flex; align-items:center; justify-content:center;'>🖼️ Memory Image</div>",
                                unsafe_allow_html=True)

                        # Açıklama kartı
                        st.markdown(f"""
                            <div class="image-card">
                                <p style='color: #ffcc00; font-size: 0.8em; font-weight: bold;'>AI ANALYSIS:</p>
                                <p style='font-size: 0.9em; font-style: italic;'>"{info}"</p>
                                <p style='color: #888; font-size: 0.7em;'>📅 {date[:10]}</p>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No matches in memory, knk.")