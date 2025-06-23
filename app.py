import streamlit as st
import fitz  # PyMuPDF
import spacy
import re
from pathlib import Path

# Sayfa başlığı ve açıklama
st.set_page_config(page_title="CV Analiz Sistemi", layout="wide")
st.title("CV Analiz Sistemi")
st.write("CV'nizi yükleyin ve yapay zeka destekli analizini alın.")

# SpaCy modelini yükle
@st.cache_resource
def load_model():
    return spacy.load("tr_core_news_lg")

nlp = load_model()

def pdf_to_text(pdf_file):
    """PDF dosyasını metne çevirir"""
    text = ""
    try:
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page in pdf_document:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"PDF okuma hatası: {str(e)}")
        return None

def analyze_cv(text):
    """CV metnini analiz eder ve eksikleri belirler"""
    doc = nlp(text)
    analysis = {
        "teknik_beceriler": [],
        "egitim": False,
        "is_deneyimi": False,
        "iletisim_bilgileri": {
            "email": False,
            "telefon": False,
            "linkedin": False
        },
        "dil_becerileri": False,
        "oneriler": []
    }
    
    # E-posta kontrolü
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    if re.search(email_pattern, text):
        analysis["iletisim_bilgileri"]["email"] = True
    else:
        analysis["oneriler"].append("E-posta adresi ekleyin")

    # Telefon kontrolü
    phone_pattern = r'(?:\+90|0)?\s*(?:\d{3}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}|\d{3}[\s-]?\d{3}[\s-]?\d{4})'
    if re.search(phone_pattern, text):
        analysis["iletisim_bilgileri"]["telefon"] = True
    else:
        analysis["oneriler"].append("Telefon numarası ekleyin")

    # LinkedIn kontrolü
    if "linkedin.com" in text.lower():
        analysis["iletisim_bilgileri"]["linkedin"] = True
    else:
        analysis["oneriler"].append("LinkedIn profil bağlantısı ekleyin")

    # Eğitim kontrolü
    egitim_keywords = ["üniversite", "okul", "fakülte", "bölüm", "lisans", "yüksek lisans", "doktora"]
    if any(keyword in text.lower() for keyword in egitim_keywords):
        analysis["egitim"] = True
    else:
        analysis["oneriler"].append("Eğitim bilgilerinizi detaylandırın")

    # İş deneyimi kontrolü
    deneyim_keywords = ["deneyim", "çalıştım", "görev", "pozisyon", "şirket"]
    if any(keyword in text.lower() for keyword in deneyim_keywords):
        analysis["is_deneyimi"] = True
    else:
        analysis["oneriler"].append("İş deneyimlerinizi ekleyin")

    # Teknik becerileri tespit et
    teknik_keywords = ["python", "java", "javascript", "html", "css", "sql", "react", "angular", 
                      "node.js", "docker", "kubernetes", "aws", "azure", "git", "agile", "scrum"]
    
    found_skills = [skill for skill in teknik_keywords if skill in text.lower()]
    analysis["teknik_beceriler"] = found_skills
    
    if len(found_skills) < 3:
        analysis["oneriler"].append("Teknik becerilerinizi artırın veya daha detaylı belirtin")

    # Dil becerileri kontrolü
    dil_keywords = ["ingilizce", "almanca", "fransızca", "ispanyolca", "dil seviyesi", "yabancı dil"]
    if any(keyword in text.lower() for keyword in dil_keywords):
        analysis["dil_becerileri"] = True
    else:
        analysis["oneriler"].append("Yabancı dil becerilerinizi belirtin")

    return analysis

def display_analysis(analysis):
    """Analiz sonuçlarını görsel olarak gösterir"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 CV Değerlendirmesi")
        
        # İletişim Bilgileri
        st.write("##### 📞 İletişim Bilgileri")
        contact_df = {
            "Bilgi": ["E-posta", "Telefon", "LinkedIn"],
            "Durum": [
                "✅ Mevcut" if analysis["iletisim_bilgileri"]["email"] else "❌ Eksik",
                "✅ Mevcut" if analysis["iletisim_bilgileri"]["telefon"] else "❌ Eksik",
                "✅ Mevcut" if analysis["iletisim_bilgileri"]["linkedin"] else "❌ Eksik"
            ]
        }
        st.table(contact_df)
        
        # Temel Bölümler
        st.write("##### 📑 Temel Bölümler")
        sections_df = {
            "Bölüm": ["Eğitim", "İş Deneyimi", "Dil Becerileri"],
            "Durum": [
                "✅ Mevcut" if analysis["egitim"] else "❌ Eksik",
                "✅ Mevcut" if analysis["is_deneyimi"] else "❌ Eksik",
                "✅ Mevcut" if analysis["dil_becerileri"] else "❌ Eksik"
            ]
        }
        st.table(sections_df)

    with col2:
        # Teknik Beceriler
        st.subheader("💻 Teknik Beceriler")
        if analysis["teknik_beceriler"]:
            for skill in analysis["teknik_beceriler"]:
                st.write(f"- {skill.title()}")
        else:
            st.write("❌ Teknik beceriler belirtilmemiş")

        # Öneriler
        st.subheader("💡 Öneriler")
        if analysis["oneriler"]:
            for oneri in analysis["oneriler"]:
                st.write(f"- {oneri}")
        else:
            st.write("✅ CV'niz temel gereksinimleri karşılıyor!")

# Ana uygulama akışı
uploaded_file = st.file_uploader("CV'nizi PDF formatında yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('CV analiz ediliyor...'):
        # PDF'i metne çevir
        cv_text = pdf_to_text(uploaded_file)
        
        if cv_text:
            # CV'yi analiz et
            analysis_results = analyze_cv(cv_text)
            
            # Sonuçları göster
            display_analysis(analysis_results)
