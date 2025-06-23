from flask import Blueprint, render_template, request, jsonify
import pdfplumber
import re
from pathlib import Path
import os
import io
import traceback
import sys

main = Blueprint('main', __name__)

def pdf_to_text(pdf_file):
    """PDF dosyasını metne çevirir"""
    text = ""
    try:
        pdf_content = io.BytesIO(pdf_file.read())
        with pdfplumber.open(pdf_content) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        return None

def calculate_cv_score(analysis):
    """CV skorunu hesaplar"""
    score = 0
    
    # İletişim bilgileri (30 puan)
    if analysis["iletisim_bilgileri"]["email"]: score += 10
    if analysis["iletisim_bilgileri"]["telefon"]: score += 10
    if analysis["iletisim_bilgileri"]["linkedin"]: score += 10
    
    # Temel bölümler (45 puan)
    if analysis["egitim"]: score += 15
    if analysis["is_deneyimi"]: score += 20
    if analysis["dil_becerileri"]: score += 10
    
    # Teknik beceriler (25 puan)
    skill_count = len(analysis["teknik_beceriler"])
    if skill_count >= 5: score += 25
    elif skill_count >= 3: score += 15
    elif skill_count >= 1: score += 5
    
    return score

def get_job_requirements(job_field):
    """Seçilen iş alanına göre gelişim yol haritasını döndürür"""
    # Her alandaki beceriler gelişim önceliğine göre kategorize edilmiştir
    requirements = {
        'software': {
            'must_have': [
                'git',         # Versiyon kontrolü
                'sql',         # Veritabanı yönetimi
                'api',         # Servis entegrasyonları
                'oop',         # Nesne yönelimli programlama
                'test'         # Test otomasyonu
            ],
            'good_to_have': [
                'agile',       # Çevik metodolojiler
                'scrum',       # Proje yönetimi
                'ci/cd',       # Sürekli entegrasyon/dağıtım
                'docker',      # Konteynerizasyon
                'kubernetes'    # Konteyner orkestrasyon
            ],
            'specializations': [
                'python',      # Backend geliştirme
                'java',        # Kurumsal uygulamalar
                'javascript',  # Frontend geliştirme
                'c#',         # Windows/.NET geliştirme
                'php'         # Web geliştirme
            ],
            'tools': [
                'react',       # Modern UI geliştirme
                'angular',     # Kurumsal frontend
                'vue',         # Hızlı UI geliştirme
                'django',      # Python web framework
                'spring',      # Java framework
                'laravel'      # PHP framework
            ]
        },
        'data-science': {
            'must_have': [
                'python',           # Temel programlama
                'sql',             # Veri sorgulama
                'statistics',      # İstatistiksel analiz
                'machine learning', # Makine öğrenmesi
                'data analysis'    # Veri analizi
            ],
            'good_to_have': [
                'deep learning',    # Derin öğrenme
                'nlp',             # Doğal dil işleme
                'computer vision',  # Görüntü işleme
                'big data'         # Büyük veri
            ],
            'tools': [
                'pandas',          # Veri manipulasyonu
                'numpy',           # Sayısal işlemler
                'scikit-learn',    # ML modelleri
                'tensorflow',      # Derin öğrenme
                'pytorch'          # Derin öğrenme
            ],
            'visualization': [
                'matplotlib',       # Temel görselleştirme
                'seaborn',         # İstatistiksel görseller
                'tableau',         # İş analitiği
                'power bi'         # Raporlama
            ]
        },
        'marketing': {
            'must_have': ['marketing strategy', 'social media', 'analytics', 'content marketing'],
            'good_to_have': ['seo', 'sem', 'email marketing', 'crm'],
            'tools': ['google analytics', 'facebook ads', 'mailchimp', 'hubspot'],
            'skills': ['copywriting', 'market research', 'brand management']
        },
        'design': {
            'must_have': ['ui/ux', 'typography', 'color theory', 'layout design'],
            'good_to_have': ['motion design', 'prototyping', 'design systems'],
            'tools': ['figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator'],
            'skills': ['wireframing', 'user research', 'visual design']
        },
        'management': {
            'must_have': ['leadership', 'project management', 'team management', 'strategy'],
            'good_to_have': ['agile', 'scrum', 'risk management', 'stakeholder management'],
            'tools': ['jira', 'trello', 'asana', 'microsoft project'],
            'skills': ['communication', 'negotiation', 'problem solving', 'decision making']
        }
    }
    return requirements.get(job_field, {})

def analyze_cv(text, job_field):
    """CV metnini analiz eder ve eksikleri belirler"""
    text = text.lower()
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

    # Teknik becerileri tespit et ve seviyelerini belirle
    teknik_keywords = {
        "python": ["django", "flask", "fastapi", "pandas", "numpy", "tensorflow", "pytorch"],
        "java": ["spring", "hibernate", "maven", "junit", "servlet", "jdbc"],
        "javascript": ["react", "vue", "angular", "node.js", "express", "typescript"],
        "html": ["css", "sass", "bootstrap", "tailwind", "responsive"],
        "sql": ["mysql", "postgresql", "oracle", "mongodb", "database design"],
        "devops": ["docker", "kubernetes", "jenkins", "aws", "azure", "ci/cd"],
        "version control": ["git", "github", "gitlab", "bitbucket"],
        "methodologies": ["agile", "scrum", "kanban", "waterfall"]
    }
    
    found_skills = []
    for main_skill, sub_skills in teknik_keywords.items():
        if main_skill in text.lower():
            # Ana beceri bulundu
            skill_level = 1
            found_sub_skills = [s for s in sub_skills if s in text.lower()]
            
            # Alt becerilere göre seviye belirleme
            if len(found_sub_skills) >= 3:
                skill_level = 3  # İleri seviye
            elif len(found_sub_skills) >= 1:
                skill_level = 2  # Orta seviye
            
            found_skills.append({
                "name": main_skill,
                "level": skill_level,
                "sub_skills": found_sub_skills
            })
    
    analysis["teknik_beceriler"] = found_skills
    
    if len(found_skills) < 3:
        analysis["oneriler"].append("Teknik becerilerinizi artırın veya daha detaylı belirtin")

    # Dil becerileri kontrolü
    dil_keywords = ["ingilizce", "almanca", "fransızca", "ispanyolca", "dil seviyesi", "yabancı dil"]
    if any(keyword in text.lower() for keyword in dil_keywords):
        analysis["dil_becerileri"] = True
    else:
        analysis["oneriler"].append("Yabancı dil becerilerinizi belirtin")

    
    # İş alanına özel analiz
    job_reqs = get_job_requirements(job_field)
    if job_reqs:
        analysis['job_match'] = {
            'field': job_field,
            'matched_skills': [],
            'missing_skills': [],
            'ats_score': 0
        }
        
        # Gerekli becerileri kontrol et
        all_skills = set()
        for category in job_reqs.values():
            if isinstance(category, list):
                all_skills.update(category)
            else:
                for skills in category.values():
                    all_skills.update(skills)
        
        matched_skills = [skill for skill in all_skills if skill in text]
        missing_skills = [skill for skill in all_skills if skill not in text]
        
        analysis['job_match']['matched_skills'] = matched_skills
        analysis['job_match']['missing_skills'] = missing_skills
        
        # ATS skoru hesapla (ağırlıklı puanlama)
        if all_skills:
            total_weight = 0
            matched_weight = 0
            
            # Must-have becerileri kontrol et (3x ağırlık)
            must_have = set(job_reqs.get('must_have', []))
            matched_must = sum(1 for skill in must_have if skill in text)
            total_weight += len(must_have) * 3
            matched_weight += matched_must * 3
            
            # Good-to-have becerileri kontrol et (2x ağırlık)
            good_to_have = set(job_reqs.get('good_to_have', []))
            matched_good = sum(1 for skill in good_to_have if skill in text)
            total_weight += len(good_to_have) * 2
            matched_weight += matched_good * 2
            
            # Diğer becerileri kontrol et (1x ağırlık)
            other_skills = set()
            for key, value in job_reqs.items():
                if key not in ['must_have', 'good_to_have']:
                    other_skills.update(value)
            matched_other = sum(1 for skill in other_skills if skill in text)
            total_weight += len(other_skills)
            matched_weight += matched_other
            
            # Ağırlıklı ATS skoru hesapla
            if total_weight > 0:
                ats_score = (matched_weight / total_weight) * 100
                analysis['job_match']['ats_score'] = round(ats_score, 1)
                
                # Eksik becerileri önem sırasına göre raporla
                analysis['job_match']['missing_skills'] = {
                    'critical': [skill for skill in must_have if skill not in text],
                    'important': [skill for skill in good_to_have if skill not in text],
                    'nice_to_have': [skill for skill in other_skills if skill not in text]
                }
        
        # Öneriler oluştur
        if missing_skills:
            if job_field == 'software':
                analysis['oneriler'].append(
                    '💡 Gelişim İpucu: Temel becerileri pekiştirmek için küçük bir proje geliştirebilirsiniz. '
                    'Örneğin: "Python ve Django ile basit bir API geliştirip, Git ile versiyon kontrolünü yönetebilir, '
                    'Docker ile konteynerize edebilirsiniz."')
                analysis['oneriler'].append(
                    '📝 CV Önerisi: Deneyimlerinizi şu formatta yazabilirsiniz: '
                    '"[Teknoloji] kullanarak [Problem] için [Çözüm] geliştirdim. [Sonuç] elde ettim."')
            elif job_field == 'data-science':
                analysis['oneriler'].append(
                    '💡 Gelişim İpucu: Kaggle\'da bir veri seti seçip uçtan uca bir analiz projesi geliştirebilirsiniz. '
                    'Pandas ile veri temizleme, Scikit-learn ile model geliştirme ve Matplotlib ile görselleştirme yapabilirsiniz.')
                analysis['oneriler'].append(
                    '📝 CV Önerisi: Projelerinizi şu formatta yazabilirsiniz: '
                    '"[Veri Seti] üzerinde [Analiz/Model] geliştirerek [Sonuç/Başarı Oranı] elde ettim."')
    
    return analysis

@main.route('/')
def index():
    try:
        import os
        print(f"Current directory: {os.getcwd()}", file=sys.stderr)
        print(f"Directory contents: {os.listdir()}", file=sys.stderr)
        print(f"App directory contents: {os.listdir('app')}", file=sys.stderr)
        print(f"Templates directory contents: {os.listdir('app/templates')}", file=sys.stderr)
        return render_template('index.html')
    except Exception as e:
        print(f"Error in index(): {str(e)}\n{traceback.format_exc()}", file=sys.stderr)
        return f"Error: {str(e)}", 500

@main.route('/analyze', methods=['POST'])
def analyze():
    try:
        job_field = request.form.get('job_field', 'software')
        if 'file' not in request.files:
            return jsonify({'error': 'Dosya yüklenmedi'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Dosya seçilmedi'}), 400
        
        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'Sadece PDF dosyaları kabul edilmektedir'}), 400

        cv_text = pdf_to_text(file)
        if not cv_text:
            return jsonify({'error': 'PDF dosyası okunamadı'}), 400

        print(f"CV Text: {cv_text[:500]}", file=sys.stderr)  # İlk 500 karakteri logla

        analysis_results = analyze_cv(cv_text, job_field)
        # CV skorunu hesapla
        cv_score = calculate_cv_score(analysis_results)
        analysis_results["cv_score"] = cv_score
        
        return jsonify(analysis_results)
    except Exception as e:
        error_msg = f"Error in analyze(): {str(e)}\n{traceback.format_exc()}"
        print(error_msg, file=sys.stderr)
        return jsonify({'error': 'Bir hata oluştu: ' + str(e)}), 500
