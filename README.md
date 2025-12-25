# TR-AutoGrader-NLP
🎓 Türkçe Açık Uçlu Soru Puanlama Sistemi (NLP)
Bu proje, TÜBİTAK 2209-A (2025/1. Dönem)  kapsamında yürütücülüğünü üstlendiğim akademik bir araştırmanın uygulama prototipidir. 
Amacı, öğrencilerin verdiği Türkçe yanıtları, bir öğretmenin cevap anahtarı anlamsal olarak puanlamaktır.

🚀 Öne Çıkan Özellikler

Anlamsal Analiz: Sadece kelime eşleşmesine değil, Sentence-BERT (SBERT) mimarisi kullanarak metnin derin anlamına odaklanır.
Türkçe Desteği: Türkçe'nin eklemeli morfolojik yapısına  uygun modellerle (BERTurk vb.) optimize edilmiştir.
Gürültü Filtreleme: PDF ve taranmış belgelerden gelen kurumsal "gürültüleri" (T.C., Üniversite ismi vb.) temizleyen özel bir ön işleme katmanı içerir.
Esnek Değerlendirme: Kosinüs Benzerliği  yöntemiyle 0-100 arası nesnel puanlama önerisi sunar.

🛠️ Kullanılan Teknolojiler
Dil: Python
Modeller: Sentence-Transformers (BERT tabanlı) 
Veri Çıkarımı: MarkItDown (Microsoft) & olmOCR (AllenAI) 


Arayüz: Streamlit

📈 Hedeflenen Yaygın Etki
Bu çalışma, 12. Kalkınma Planı'ndaki "Yapay Zekâ Tabanlı Eğitim Uygulamaları" hedefiyle uyumlu olarak , eğitimde ölçme-değerlendirme süreçlerini dijitalleştirmeyi ve nesnelleştirmeyi amaçlamaktadır.
