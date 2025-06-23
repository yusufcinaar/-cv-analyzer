document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('cv-file');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingSection = document.getElementById('loading');
    const resultsSection = document.getElementById('results');
    const uploadSection = document.getElementById('upload-section');

    // Dosya seçildiğinde analiz butonunu göster
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            analyzeBtn.classList.remove('hidden');
        } else {
            analyzeBtn.classList.add('hidden');
        }
    });

    // Analiz butonuna tıklandığında
    analyzeBtn.addEventListener('click', async function() {
        if (!fileInput.files.length) return;

        const file = fileInput.files[0];
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            alert('Lütfen PDF dosyası yükleyin');
            return;
        }

        // Loading durumunu göster
        uploadSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', file);
        formData.append('job_field', document.getElementById('job-field').value);

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Analiz sırasında bir hata oluştu');
            }

            const results = await response.json();
            // Tarih bilgisini güncelle
            document.getElementById('report-date').textContent = new Date().toLocaleDateString('tr-TR');
            
            displayResults(results);
            displayATSAnalysis(results);

            // Sonuçları göster
            loadingSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');
            resultsSection.classList.add('fade-in');

        } catch (error) {
            alert(error.message);
            loadingSection.classList.add('hidden');
            uploadSection.classList.remove('hidden');
        }
    });

    function displayResults(results) {
        // İletişim bilgilerini göster
        const contactInfo = document.getElementById('contact-info');
        contactInfo.innerHTML = `
            <div class="status-badge ${results.iletisim_bilgileri.email ? 'success' : 'warning'}">
                <span>E-posta</span>
                <span>${results.iletisim_bilgileri.email ? '✓' : '✗'}</span>
            </div>
            <div class="status-badge ${results.iletisim_bilgileri.telefon ? 'success' : 'warning'}">
                <span>Telefon</span>
                <span>${results.iletisim_bilgileri.telefon ? '✓' : '✗'}</span>
            </div>
            <div class="status-badge ${results.iletisim_bilgileri.linkedin ? 'success' : 'warning'}">
                <span>LinkedIn</span>
                <span>${results.iletisim_bilgileri.linkedin ? '✓' : '✗'}</span>
            </div>
        `;

        // Temel bölümleri göster
        const sections = document.getElementById('sections');
        sections.innerHTML = `
            <div class="status-badge ${results.egitim ? 'success' : 'warning'}">
                <span>Eğitim</span>
                <span>${results.egitim ? '✓' : '✗'}</span>
            </div>
            <div class="status-badge ${results.is_deneyimi ? 'success' : 'warning'}">
                <span>İş Deneyimi</span>
                <span>${results.is_deneyimi ? '✓' : '✗'}</span>
            </div>
            <div class="status-badge ${results.dil_becerileri ? 'success' : 'warning'}">
                <span>Dil Becerileri</span>
                <span>${results.dil_becerileri ? '✓' : '✗'}</span>
            </div>
        `;

        // CV skorunu göster
        document.getElementById('cv-score').textContent = results.cv_score;

        // Teknik becerileri göster
        const skills = document.getElementById('skills');
        skills.innerHTML = results.teknik_beceriler.length > 0
            ? results.teknik_beceriler.map(skill => `
                <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                    <div class="flex justify-between items-center mb-2">
                        <span class="font-semibold text-gray-700">${skill.name.charAt(0).toUpperCase() + skill.name.slice(1)}</span>
                        <div class="flex gap-1">
                            ${Array(3).fill().map((_, i) => `
                                <div class="w-2 h-2 rounded-full ${i < skill.level ? 'bg-green-500' : 'bg-gray-200'}"></div>
                            `).join('')}
                        </div>
                    </div>
                    ${skill.sub_skills.length > 0 ? `
                        <div class="text-sm text-gray-500">
                            ${skill.sub_skills.map(sub => `
                                <span class="inline-block bg-gray-100 rounded px-2 py-1 mr-1 mb-1">${sub}</span>
                            `).join('')}
                        </div>
                    ` : ''}
                </div>
            `).join('')
            : '<p class="text-gray-500">Teknik beceriler belirtilmemiş</p>';

        // Önerileri göster
        const suggestions = document.getElementById('suggestions');
        suggestions.innerHTML = results.oneriler.length > 0
            ? results.oneriler.map(oneri => `
                <li class="text-gray-600">${oneri}</li>
            `).join('')
            : '<li class="text-green-600">Tebrikler! CV\'niz temel gereksinimleri karşılıyor.</li>';
    }

    // PDF indirme fonksiyonu


    function displayATSAnalysis(results) {
        const atsAnalysis = document.getElementById('ats-analysis');
        const atsScore = document.getElementById('ats-score');
        const atsSuggestions = document.getElementById('ats-suggestions');

        if (results.job_match) {
            atsAnalysis.classList.remove('hidden');
            
            // ATS skoru
            atsScore.textContent = `${results.job_match.ats_score}%`;
            
            // ATS önerileri
            let suggestionsHtml = '<div class="space-y-4">';
            
            // Kritik eksikler
            if (results.job_match.missing_skills.critical && results.job_match.missing_skills.critical.length > 0) {
                suggestionsHtml += `
                    <div class="p-3 bg-red-50 rounded-lg">
                        <h4 class="font-medium text-red-800 mb-2">⚠️ Öncelikle Öğrenmeniz Gerekenler:</h4>
                        <p class="text-red-600">${results.job_match.missing_skills.critical.join(', ')}</p>
                    </div>
                `;
            }
            
            // Önemli eksikler
            if (results.job_match.missing_skills.important && results.job_match.missing_skills.important.length > 0) {
                suggestionsHtml += `
                    <div class="p-3 bg-yellow-50 rounded-lg">
                        <h4 class="font-medium text-yellow-800 mb-2">ℹ️ Gelişiminiz İçin Önerilen Beceriler:</h4>
                        <p class="text-yellow-600">${results.job_match.missing_skills.important.join(', ')}</p>
                    </div>
                `;
            }
            
            // İsteğe bağlı eksikler
            if (results.job_match.missing_skills.nice_to_have && results.job_match.missing_skills.nice_to_have.length > 0) {
                suggestionsHtml += `
                    <div class="p-3 bg-blue-50 rounded-lg">
                        <h4 class="font-medium text-blue-800 mb-2">⭐ Uzmanlaşabileceğiniz Alanlar:</h4>
                        <p class="text-blue-600">${results.job_match.missing_skills.nice_to_have.join(', ')}</p>
                    </div>
                `;
            }
            
            suggestionsHtml += '</div>';
            atsSuggestions.innerHTML = suggestionsHtml;
        }
    }

});
