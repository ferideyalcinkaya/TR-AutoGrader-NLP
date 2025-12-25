import streamlit as st
from sentence_transformers import SentenceTransformer, util
from markitdown import MarkItDown
import os
import re

# Sayfa Ayarları
st.set_page_config(page_title="TÜBİTAK 2209-A NLP Projesi", layout="wide")

# CSS ile buton ve başlıkları özelleştirme (Uğraşılmışlık hissi için)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_engine():
    model = SentenceTransformer('dbmdz/bert-base-turkish-cased')
    md = MarkItDown()
    return model, md

model, md = load_engine()

# --- METİN TEMİZLEME FONKSİYONU (Mühendislik Dokunuşu) ---
def clean_text(text):
    # Kurum isimlerini, tarihleri ve gereksiz boşlukları temizle
    text = re.sub(r'T\.C\.|YÜKSEKÖĞRETİM|KURULU|BAŞKANLIĞI|ANKARA|2023|2024|2025', '', text)
    text = re.sub(r'\d+', '', text) # Sayıları temizle
    text = re.sub(r'\s+', ' ', text).strip() # Fazla boşlukları sil
    return text

st.sidebar.title("🛠️ Kontrol Paneli")
st.sidebar.info("Bu proje TÜBİTAK 2209-A kapsamında geliştirilmektedir.")
confidence_threshold = st.sidebar.slider("Başarı Eşiği (%)", 0, 100, 70)

st.title("🎯 Otomatik Puanlama Sistemi v2.0")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔑 Cevap Anahtarı")
    cevap_anahtari = st.text_area("Hocanın beklediği doğru cevap:", height=200)

with col2:
    st.subheader("📄 Öğrenci PDF'i")
    uploaded_file = st.file_uploader("Dosyayı buraya bırakın", type=['pdf'])

if st.button("🚀 Detaylı Analizi Başlat"):
    if cevap_anahtari and uploaded_file:
        with st.spinner('Yapay zeka katmanları çalıştırılıyor...'):
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 1. Adım: PDF'ten metin çıkarma
            raw_text = md.convert("temp.pdf").text_content
            
            # 2. Adım: Metin Temizleme (İşte fark yaratan kısım)
            cleaned_student_text = clean_text(raw_text)
            cleaned_teacher_text = clean_text(cevap_anahtari)
            
            # 3. Adım: Vektörel Karşılaştırma
            v1 = model.encode(cleaned_teacher_text, convert_to_tensor=True)
            v2 = model.encode(cleaned_student_text, convert_to_tensor=True)
            score = util.pytorch_cos_sim(v1, v2).item() * 100
            
            # --- SONUÇ EKRANI ---
            st.markdown("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("Anlamsal Benzerlik", f"%{score:.2f}")
            m2.metric("Kelime Sayısı", len(cleaned_student_text.split()))
            
            status = "BAŞARILI ✅" if score >= confidence_threshold else "YETERSİZ ❌"
            m3.subheader(f"Durum: {status}")
            
            with st.expander("🔍 Karşılaştırma Detaylarını Gör"):
                c1, c2 = st.columns(2)
                c1.write("**Analiz Edilen Cevap Anahtarı:**")
                c1.caption(cleaned_teacher_text)
                c2.write("**PDF'ten Ayıklanan Öğrenci Cevabı:**")
                c2.caption(cleaned_student_text)
            
            os.remove("temp.pdf")
    else:
        st.error("Lütfen tüm alanları doldurun!")