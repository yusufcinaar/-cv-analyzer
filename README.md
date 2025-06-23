# 📝 CV Analiz Sistemi - ATS Uyumlu CV Değerlendirme Aracı

CV'nizi iş alanınıza göre analiz eden, gelişim önerileri sunan ve ATS (Applicant Tracking System) uyumluluğunu değerlendiren profesyonel bir araç.

## ✨ Özellikler

- 💼 İş alanına özel değerlendirme (Yazılım, Veri Bilimi, Pazarlama, Tasarım, Yönetim)
- 🏆 ATS Uyumluluk Skoru
- 📈 Gelişim yol haritası
- 📝 CV yazma önerileri
- 💡 Pratik ipucu ve proje önerileri

## 💻 Canlı Demo

[Canlı Demo'yu Deneyin](DEMO_URL) → Kendi CV'nizi yükleyip analiz edebilirsiniz!

## 🛠️ Teknolojiler

- Backend: Python, Flask
- Frontend: HTML, Tailwind CSS, JavaScript
- PDF İşleme: PyMuPDF

## 📝 Kullanım

1. İş alanınızı seçin
2. PDF formatındaki CV'nizi yükleyin
3. Detaylı analiz raporunuzu görün:
   - Öncelikli öğrenmeniz gereken beceriler
   - Gelişiminiz için önerilen konular
   - Uzmanlaşabileceğiniz alanlar
   - Pratik ipucu ve proje önerileri

## ⚙️ Kurulum

```bash
# Repo'yu klonlayın
git clone https://github.com/yusufcinaar/-cv-analyzer.git

# Proje klasörüne girin
cd cv-analyzer

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
python run.py
```

## 👨‍💻 Katkıda Bulunma

1. Bu repo'yu forklayın
2. Feature branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📃 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın

## 👨‍💻 Geliştirici

Yusuf ÇINAR - [LinkedIn Profili](https://www.linkedin.com/in/yusuf-%C3%A7%C4%B1nar-b51684229/)

---

Sorularınız veya geri bildirimleriniz için [Issues](https://github.com/yusufcinaar/-cv-analyzer/issues) bölümünü kullanabilirsiniz.
streamlit run app.py
```

## Kullanım

1. Web tarayıcınızda uygulama açıldığında "CV'nizi PDF formatında yükleyin" butonuna tıklayın
2. PDF formatındaki CV'nizi seçin
3. Sistem otomatik olarak CV'nizi analiz edecek ve sonuçları gösterecektir

## Gereksinimler

- Python 3.8+
- Streamlit
- PyMuPDF
- spaCy
- Türkçe SpaCy modeli (tr_core_news_lg)
