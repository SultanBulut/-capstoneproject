import os
import time
import tempfile
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from elevenlabs import generate, set_api_key

from send_story_agent import send_story_via_email
from educational_story_rag import generate_story_from_uploaded_file
import email_agent

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

VOICE_MAPPING = {
    "Anne": "ZT9u07TYPVl83ejeLakq",
    "Baba": "gfRt6Z3Z8aTbpLfexQ7N",
    "Genç Kız": "piI8Kku0DcvcL6TTSeQt",
    "Masal Anlatıcısı": "8dRG2ER7ThdAWJwK71hG"
}

def generate_story(theme, age, length, custom_prompt=""):
    client = genai.Client(api_key=GEMINI_API_KEY)
    timestamp = int(time.time())
    prompt = f"{age} yaşındaki çocuk için {length} kelimelik, {theme} temalı bir hikaye oluştur. Zaman damgası: {timestamp}"

    if custom_prompt:
        prompt += f"\nAşağıdaki öğeleri de ekle: {custom_prompt}"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
        )
    ]

    config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part(text="Belirtilen yaş grubuna uygun, eğlenceli ve anlaşılır bir hikaye oluştur.")

        ],
        temperature=0.9,
    )

    story = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=contents,
        config=config,
    ):
        story += chunk.text
    #return story

    # İstenmeyen satırları temizle
    lines = story.split("\n")
    # Açıklama satırları ya da "Zaman damgası" geçen satırları çıkar
    filtered_lines = [line for line in lines if not (
        line.lower().startswith("zaman damgası") or
        "işte" in line.lower() or
        "tamamdır" in line.lower()
    )]

    clean_story = "\n".join(filtered_lines).strip()
    return clean_story

def generate_tts(story_text, voice_name):
    set_api_key(ELEVEN_API_KEY)
    audio = generate(
        text=story_text,
        voice=voice_name,
        model="eleven_multilingual_v2"
    )
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.write(audio)
    temp_file.close()
    return temp_file.name

def main():
    st.set_page_config(page_title="FairyTeller AI", page_icon="📚", layout="wide")

    st.markdown("""
        <style>
        .stApp { max-width: 1200px; margin: auto; }
        .story-container {
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            background-color: #e0e0e0;
            border: 1px solid #ccc;
            white-space: pre-wrap;
            font-size: 18px;
            line-height: 1.5;
            color: #000000;   
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📚FairyTeller AI")
    st.write("Yapay zeka ile kişiselleştirilmiş hikayeler yaratın!")

    
    tab1, tab2, tab3 = st.tabs(["Klasik Hikaye Oluşturma", "Eğitim Bilgisine Dayalı Hikaye", "Akıllı Hikaye Gönderimi"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Hikaye Ayarları")
            theme = st.selectbox(
                "Hikaye Teması Seçin",
            ["Macera", "Fantastik", "Bilim Kurgu", "Romantik", "Ahlaki Hikaye",
             "Peri Masalı", "Gizem", "Eğitici", "Tarihi", "Komedi", "Hayvan Hikayesi"]
            )
            age = st.slider("Yaş Seçin", 3, 10, 6)

        with col2:
            st.markdown("### Hikaye Uzunluğu & Ses")
            story_length_choice = st.selectbox(
                "🕒 Hikaye Uzunluğunu Seçin:",
                ["Kısa", "Orta"]
            )
            length = 300 if story_length_choice ==  "Kısa" else 600
            voice_style = st.selectbox("🔊 Ses Tarzı Seçin:", list(VOICE_MAPPING.keys()))

        st.markdown("### Hikayenizi Özelleştirin")
        custom_prompt = st.text_area("Yaratıcı öğeler ekleyin (isteğe bağlı)")

        if "story" not in st.session_state:
            st.session_state.story = ""
        if "audio_path" not in st.session_state:
            st.session_state.audio_path = ""

        if st.button("✨ Hikaye Oluştur", use_container_width=True):
            with st.spinner("Crafting your magical story..."):
                st.session_state.story = generate_story(theme, age, length, custom_prompt)
                st.session_state.audio_path = ""

        if st.session_state.story:
            st.markdown("### 📖 Hikayeniz")
            st.markdown(f"<div class='story-container'>{st.session_state.story}</div>", unsafe_allow_html=True)
            st.download_button("📥  Hikayeyi İndir", st.session_state.story, file_name=f"{theme.lower()}_story.txt")

            if st.button("🔊 Hikayeyi Dinle", use_container_width=True):
                with st.spinner("Generating voice..."):
                    st.session_state.audio_path = generate_tts(st.session_state.story, VOICE_MAPPING[voice_style])

            

        if st.session_state.audio_path:
            st.audio(st.session_state.audio_path, format="audio/mp3")

    with tab2:
        st.header("📘 Eğitim Bilgisine Dayalı Hikaye Oluştur")
        uploaded_file = st.file_uploader("📄 Eğitim içeriği (TXT veya PDF) yükleyin", type=["txt", "pdf"])
        topic = st.text_input("📚 Konu başlığı (örn: Güneş Sistemi, Deprem vb.):")

        if uploaded_file and topic:
            if st.button("✨ Hikayeyi Oluştur"):
                with st.spinner("Hikaye oluşturuluyor..."):
                    try:
                        story = generate_story_from_uploaded_file(uploaded_file, topic)
                        st.success("Hikaye başarıyla oluşturuldu!")
                        st.subheader("📖 Oluşturulan Hikaye")
                        st.write(story)
                    except Exception as e:
                        st.error(f"Hikaye oluşturulurken bir hata oluştu: {e}")

    with tab3:
        st.header("📩 Hikaye Oluştur ve Mail Gönder")
        agent_theme = st.selectbox("Hikaye Teması",["Macera", "Fantastik", "Bilim Kurgu", "Romantik",
                                                  "Ahlaki Hikaye", "Peri Masalı", "Gizem", "Eğitici",
                                                  "Tarihi", "Komedi", "Hayvan Hikayesi"])
        agent_email = st.text_input("Gönderilecek E-posta Adresi")
        if st.button("Agent’ı Çalıştır"):
            if agent_email:
                with st.spinner("Agent çalışıyor, lütfen bekleyin..."):
                    import email_agent  # agent fonksiyonlarını içeren modül
                    try:
                        result = email_agent.run_email_agent(agent_theme, agent_email)
                        st.success(result)
                    except Exception as e:
                        st.error(f"Agent çalıştırılırken hata oluştu: {e}")
            else:
                st.warning("Lütfen geçerli bir e-posta adresi girin.")

if __name__ == "__main__":
    main()
