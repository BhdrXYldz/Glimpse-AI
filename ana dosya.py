from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ss  # Senin hazırladığın ss.py dosyasını import ediyoruz
import streamlit as st
import os
import sqlite3

# 1. CSS TASARIM KISMI (Daha önce verdiğim CSS kodları burada kalsın)
st.set_page_config(page_title="Glimpse AI", layout="wide")
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #121212 0%, #1a1a1a 100%); color: white; }
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        color: #ffcc00 !important;
    }
    /* Diğer CSS'lerin... */
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE (Giriş kontrolü)
if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False

if not st.session_state.giris_yapildi:
    # --- SPLASH & ONBOARDING (ENGLISH) ---
    st.markdown("<h1 style='text-align: center; color: #ffcc00;'>🦁</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Welcome to Glimpse AI</h1>", unsafe_allow_html=True)

    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📸 **Monitoring:** We track your screen automatically.")
    with col2:
        st.success("🧠 **Analysis:** AI tags everything for you.")
    with col3:
        st.warning("🔍 **Discovery:** Find anything in seconds.")

    st.write("---")
    if st.button("Explore Your Memory 🚀", use_container_width=True):
        st.session_state.giris_yapildi = True
        st.rerun()

else:
    # --- MAIN DASHBOARD (Burası butona basınca açılacak) ---
    st.markdown("<h2 style='color: #ffcc00;'>🔍 Glimpse Memory Panel</h2>", unsafe_allow_html=True)

    sorgu = st.text_input("", placeholder="Search your memory... (e.g. yellow folder, code, meeting)")

    # BURADAN SONRASI SENİN ESKİ ARAMA VE RESİM GÖSTERME KODLARIN
    # (Önemli: Bu kodlar 'else'in içinde yani bir tab içerde durmalı!)

    # Örnek:
    # results = akilli_ara_direkt(sorgu)
    # cols = st.columns(3)
    # for i, res in enumerate(results):
    #     ... resim gösterme kodları ...
app = FastAPI()

# Flutter uygulamasının bağlanabilmesi için CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search(query: str):
    # Senin ss.py içindeki akilli_ara'yı ufak bir modifiye ile
    # print yapmak yerine liste döndürecek hale getireceğiz.
    results = ss.akilli_ara_api(query)
    return {"status": "success", "data": results}

@app.get("/scan")
async def trigger_scan():
    ss.scan_and_analyze('/Users/bahadiryildiz/Desktop/test_ekran')
    return {"status": "scan_completed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)