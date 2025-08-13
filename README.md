# FairyTeller AI 📚✨ - Kişiselleştirilmiş Çocuk Hikayeleri Üreticisi

## Proje Tanımı 📝
FairyTeller AI, Google Gemini LLM modeli kullanarak, kullanıcının seçtiği tema ve yaş grubuna uygun kişiselleştirilmiş çocuk hikayeleri oluşturur. Üretilen hikayeler metinden sese (TTS) dönüştürülerek uygulama içinde sesli olarak dinlenebilir ve hikaye TXT formatında indirilebilir. 📖🎧 Ayrıca kullanıcıların yüklediği PDF veya TXT formatındaki eğitim içeriklerinden, Retrieval-Augmented Generation (RAG) yöntemiyle eğitici hikayeler üretir. Agent mimarisi sayesinde kullanıcı, tema bazlı hikayeyi kolayca oluşturabilir ve mail gönderme işlemi için kullanılabilir.
 📖🔊📧

---

## Özellikler ⭐
📜 Klasik hikaye oluşturma: Tema, yaş ve uzunluk seçerek Google Gemini modeli ile hikaye üretimi.
- 📚 Eğitim içeriklerinden hikaye oluşturma (RAG).
- 🎧 Üretilen hikayeyi sesli dinleme (ElevenLabs TTS entegrasyonu).
- 💾 Hikayeyi dosya olarak indirme.
- 📤 PDF/TXT formatında eğitim dosyası yükleyerek hikaye üretme.
- 🤖 Agent mimarisi ile hikaye oluşturup e-posta gönderme.
- 🎨 Kişiselleştirilebilir hikaye ayarları.

---

## Kurulum ⚙️

1. Depoyu klonlayın:
   ```bash
   git clone <repo-url>
   cd -capstoneproject

2.Sanal ortam oluşturun ve aktifleştirin (tercih edilir):

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3.Gerekli paketleri yükleyin:
pip install -r requirements.txt

4..env dosyasını oluşturun ve aşağıdaki değişkenleri ekleyin:
GEMINI_API_KEY=<Google Gemini API anahtarınız>
ELEVEN_API_KEY=<ElevenLabs API anahtarınız>
EMAIL_ADDRESS=<E-posta adresiniz>
EMAIL_PASSWORD=<E-posta uygulama şifreniz>

Kullanım 🚀
Projeyi başlatmak için:
streamlit run app.py

Tarayıcınızda açılan sayfada;

🧙‍♂️ Klasik Hikaye Oluşturma sekmesinden temayı, yaş grubunu, hikaye uzunluğunu ve ses stilini seçip hikaye oluşturabilirsiniz.

📄 Eğitim Bilgisine Dayalı Hikaye sekmesinden PDF veya TXT dosyanızı yükleyip, konu başlığını girerek eğitim tabanlı hikaye oluşturabilirsiniz.

📩 Akıllı Hikaye Gönderimi sekmesinde tema seçip e-posta adresi girerek otomatik hikaye oluşturma ve gönderme işlemi yapabilirsiniz.

Proje Dosya Yapısı 📂
app.py - Streamlit tabanlı ana uygulama dosyası.

educational_story_rag.py - Eğitim içeriklerinden hikaye oluşturma (RAG) modülü.

email_agent.py - Agent mimarisi ile hikaye oluşturma ve e-posta gönderme.

send_story_agent.py - SMTP ile e-posta gönderim fonksiyonları.

.env - API anahtarları ve e-posta bilgileri için gizli ortam dosyası.

