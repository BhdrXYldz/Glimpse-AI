import unicodedata

import pytesseract
from PIL import Image
import os
import sqlite3
import datetime
import torch
import subprocess
from transformers import BlipProcessor, BlipForConditionalGeneration
import numpy as np
# 1. SİSTEM VE MODEL KURULUMU (M2 Pro GPU Aktif)
print("🧠 Glimpse AI Master Engine V11.0 Yükleniyor... (M2 Pro Aktif)")

# Apple Silicon (MPS) Kontrolü
device = "mps" if torch.backends.mps.is_available() else "cpu"

# Modelleri yüklüyoruz
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)


def get_tesseract_path():
    try:
        return subprocess.check_output(['which', 'tesseract']).decode('utf-8').strip()
    except:
        return "/opt/homebrew/bin/tesseract"


pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

def normalize_text(text):
    """Türkçe karakterleri normalize et"""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()
def init_db():
    conn = sqlite3.connect('glimpse_memory.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS screenshots')
    cursor.execute('''CREATE TABLE screenshots 
                      (id INTEGER PRIMARY KEY, path TEXT, info TEXT, created_at TEXT)''')
    conn.commit()
    conn.close()


# 2. DERİN ANALİZ (Deep Scan)
def scan_and_analyze(folder_path):
    init_db()
    conn = sqlite3.connect('glimpse_memory.db')
    cursor = conn.cursor()
    print(f"📂 Analiz başlıyor: {folder_path}")

    for file in os.listdir(folder_path):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            full_path = os.path.join(folder_path, file)
            try:
                dt_str = datetime.datetime.fromtimestamp(os.path.getctime(full_path)).isoformat()
                img = Image.open(full_path).convert("RGB")

                # Vision AI: num_beams=5 ile en ince detayları tarıyoruz
                inputs = processor(img, return_tensors="pt").to(device)
                out = model.generate(**inputs, max_new_tokens=60, num_beams=5, repetition_penalty=1.5)
                vision_desc = processor.decode(out[0], skip_special_tokens=True)

                # OCR: Metin içeriğini oku
                text_content = pytesseract.image_to_string(img).strip()

                full_info = f"{file} {vision_desc} {text_content}".lower()

                cursor.execute("INSERT INTO screenshots (path, info, created_at) VALUES (?, ?, ?)",
                               (full_path, full_info, dt_str))
                print(f"✅ Analiz Başarılı: {file} | AI Gördü: {vision_desc}")
            except Exception as e:
                print(f"❌ Hata ({file}): {e}")

    conn.commit()
    conn.close()
    print("\n🔥 HAFIZA OLUŞTURULDU! Artık her şeyi bulabilirsin knk.")


# 3. GLOBAL SEMANTİK PUANLAMALI ARAMA (Esnek Arama Sistemi)
def pixel_color_check(img_path, target_color):
    try:
        img = Image.open(img_path).convert('RGB')
        img = img.resize((60, 60))
        data = np.array(img).astype(float)
        r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]
        if target_color == "sarı":
            mask = (r > 160) & (g > 160) & (b < 130)
        elif target_color == "mavi":
            # Mavi pikseller: B (mavi) değeri R ve G'den belirgin şekilde yüksek olmalı
            # Beyaz piksellerde R, G, B birbirine çok yakındır (örn: 240, 240, 240)
            # Mavi piksellerde ise B yüksektir (örn: 100, 120, 220)
            mask = (b > 130) & (b > r + 30) & (b > g + 30)
        elif target_color == "kırmızı":
            mask = (r > 150) & (g < 110) & (b < 110)
        elif target_color == "yeşil":
            mask = (g > 140) & (r < 160) & (b < 160)
        elif target_color == "pembe":
            mask = (r > 180) & (g < 180) & (b > 150)
        elif target_color == "turuncu":
            mask = (r > 180) & (g > 100) & (b < 100)
        elif target_color == "mor":
            mask = (r > 120) & (g < 100) & (b > 120)
        elif target_color == "beyaz":
            mask = (r > 220) & (g > 220) & (b > 220)
        elif target_color == "siyah":
            mask = (r < 50) & (g < 50) & (b < 50)
        elif target_color == "gri":
            mask = (r > 100) & (r < 160) & (g > 100) & (g < 160) & (b > 100) & (b < 160)
        else:
            return False

        return np.sum(mask) > 10  # 15 piksel bile yakalasa "sarı var" diyor
    except:
        return False


def akilli_ara(sorgu):
    sozluk = {
        "tişört": ["tshirt", "t-shirt", "tee", "top", "clothing", "apparel", "jersey"],
        "gömlek": ["shirt", "button down", "blouse", "polo", "collar", "apparel"],
        "kısa kol": ["short sleeve", "half sleeve", "summer clothing"],
        "uzun kol": ["long sleeve", "hoodie", "sweater", "sweatshirt", "cardigan", "jacket"],
        "çizgili": ["striped", "lines", "pattern", "linear", "texture", "grid"],
        "kareli": ["checkered", "plaid", "pattern"],
        "kot": ["denim", "jeans", "blue jeans"],
        "pantolon": ["pants", "trousers", "denim", "shorts", "slacks", "bottoms"],
        "ayakkabı": ["shoes", "sneakers", "boots", "footwear", "kicks", "heels"],
        "gözlük": ["glasses", "sunglasses", "eyewear", "spectacles", "frames"],
        "şapka": ["hat", "cap", "beanie", "headwear", "helmet"],
        "çanta": ["bag", "backpack", "handbag", "purse", "luggage", "briefcase"],
        "takım": ["suit", "tie", "formal", "tuxedo", "jacket", "blazer"],
        "bilgisayar": ["computer", "laptop", "macbook", "pc", "desktop", "notebook"],
        "ekran": ["screen", "monitor", "display", "interface", "panel", "lcd", "oled"],
        "telefon": ["phone", "mobile", "smartphone", "iphone", "android", "cellphone"],
        "saat": ["watch", "clock", "smartwatch", "timepiece", "analog", "digital"],
        "grafik": ["graph", "chart", "diagram", "data", "analytics", "stats", "plot", "dashboard"],
        "kod": ["code", "programming", "python", "terminal", "software", "development", "script"],
        "para": ["money", "cash", "currency", "dollar", "euro", "bitcoin", "crypto", "wallet"],
        "belge": ["document", "paper", "text", "invoice", "receipt", "pdf", "sheet", "form"],
        "dosya": ["file", "folder", "archive", "storage"],
        "devre": ["circuit", "pcb", "electronics", "board", "hardware", "motherboard"],
        "hata": ["error", "bug", "crash", "warning", "exception"],
        "mavi": ["blue", "azure", "navy", "cyan", "teal", "sky"],
        "sarı": ["yellow", "gold", "golden", "lemon", "sunshine"],
        "kırmızı": ["red", "crimson", "scarlet", "maroon", "ruby"],
        "yeşil": ["green", "emerald", "forest", "lime", "olive"],
        "siyah": ["black", "dark", "ebony", "charcoal", "shadow"],
        "beyaz": ["white", "bright", "snow", "ivory", "clean"],
        "gri": ["grey", "gray", "silver", "metallic", "platinum"],
        "pembe": ["pink", "magenta", "rose", "fuchsia"],
        "turuncu": ["orange", "amber", "peach", "coral"],
        "masa": ["table", "desk", "furniture", "surface", "workstation"],
        "sandalye": ["chair", "seat", "furniture", "stool", "sofa"],
        "bardak": ["cup", "glass", "mug", "drink", "coffee", "tea", "beverage"],
        "tabak": ["plate", "dish", "bowl", "kitchenware", "cutlery"],
        "yemek": ["food", "meal", "pizza", "burger", "cuisine", "snack", "sandwich"],
        "meyve": ["fruit", "apple", "banana", "orange", "berry"],
        "adam": ["man", "guy", "male", "person", "adult"],
        "kadın": ["woman", "lady", "female", "person", "adult"],
        "çocuk": ["child", "kid", "boy", "girl", "baby", "toddler"],
        "sakallı": ["beard", "bearded", "facial hair", "mustache"],
        "doğa": ["nature", "landscape", "trees", "forest", "outdoor", "wildlife"],
        "deniz": ["sea", "ocean", "water", "beach", "waves", "coast"],
        "ev": ["house", "building", "architecture", "home", "exterior"],
        "araba": ["car", "vehicle", "automobile", "road", "street", "engine"],
        "plan": ["diagram", "blueprint", "plan", "map", "floorplan", "layout"],
        "mavi": ["blue", "azure", "navy", "cyan", "teal", "indigo", "cobalt", "turquoise", "sky blue"],
        "sarı": ["yellow", "gold", "golden", "lemon", "amber", "mustard", "sunshine"],
        "kırmızı": ["red", "crimson", "scarlet", "maroon", "burgundy", "ruby"],
        "yeşil": ["green", "emerald", "forest", "lime", "olive", "mint", "sage"],
        "siyah": ["black", "dark", "ebony", "charcoal", "shadow", "onyx"],
        "beyaz": ["white", "bright", "snow", "ivory", "clean"],
        "gri": ["grey", "gray", "silver", "metallic", "platinum", "ash"],
        "pembe": ["pink", "magenta", "rose", "fuchsia", "coral"],
        "turuncu": ["orange", "amber", "peach", "tangerine"],
        "mor": ["purple", "violet", "lavender", "plum"],
        "lacivert": ["navy", "dark blue", "midnight blue"],
    }
    sorgu_normalized = normalize_text(sorgu)
    words = sorgu_normalized.split()

    conn = sqlite3.connect('glimpse_memory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT path, info, created_at FROM screenshots")
    rows = cursor.fetchall()

    api_results = []  # Streamlit'e gidecek liste

    for path, info, date in rows:
        if info is None: continue
        score = 0
        matched_words = []
        for word in words:
            synonyms = [word]
            if word in sozluk: synonyms.extend(sozluk[word])

            if any(syn in info.lower() for syn in synonyms):
                score += 1
                matched_words.append(word)
            elif word in ["sarı", "mavi", "kırmızı", "yeşil", "beyaz", "siyah", "pembe", "turuncu", "gri", "mor"]:
                if pixel_color_check(path, word):
                    score += 2.5
                    matched_words.append(f"{word}(pixel)")

        if score > 0:
            api_results.append({
                "score": score,
                "path": path,
                "date": date[:10] if date else "Bilinmiyor",
                "ai_desc": info,
                "matches": matched_words
            })

    api_results.sort(key=lambda x: x['score'], reverse=True)
    conn.close()
    return api_results
if __name__ == "__main__":
    MY_FOLDER = '/Users/bahadiryildiz/Desktop/test_ekran'
    if not os.path.exists(MY_FOLDER):
        print(f"Klasör yolu hatalı knk: {MY_FOLDER}")
    else:
        scan_and_analyze(MY_FOLDER)
        while True:
            target = input("\n🔍 Ne hatırlıyorsun? (Çıkış: q): ")
            if target.lower() == 'q': break
            akilli_ara(target)