import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import qrcode
import io
from pytube import YouTube
import random

# --- Setup ---
translator = Translator()
lang_dict = LANGUAGES
lang_names = list(lang_dict.values())
lang_code_dict = {v.title(): k for k, v in lang_dict.items()}

st.set_page_config(page_title="MultiTool App", layout="centered")
st.title("🛠️ MultiTool App")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🈯 Translator + TTS", "📱 QR Code Generator", "🤖 Mini AI Chatbot"])

# --- Translator + TTS ---
with tab1:
    st.subheader("🈯 Translator & 🔊 Text-to-Speech")

    col1, col2 = st.columns(2)
    with col1:
        src_lang = st.selectbox("From Language", lang_names, index=lang_names.index("english"))
    with col2:
        dest_lang = st.selectbox("To Language", lang_names, index=lang_names.index("tamil"))

    text_input = st.text_area("Enter text to translate")

    if st.button("Translate"):
        try:
            src_code = lang_code_dict.get(src_lang.title(), "en")
            dest_code = lang_code_dict.get(dest_lang.title(), "en")
            translated = translator.translate(text_input, src=src_code, dest=dest_code)
            st.success(f"Translation: {translated.text}")
            st.session_state['last_translation'] = translated.text
            st.session_state['last_tts_lang'] = dest_lang.title()
        except Exception as e:
            st.error(f"Translation failed: {e}")

    if 'last_translation' in st.session_state:
        if st.button("🔊 Speak Translation"):
            try:
                tts_lang = lang_code_dict.get(st.session_state['last_tts_lang'], "en")
                tts = gTTS(text=st.session_state['last_translation'], lang=tts_lang)
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                st.audio(mp3_fp, format='audio/mp3')
            except Exception as e:
                st.error(f"TTS Error: {e}")

# --- QR Code Generator ---
with tab2:
    st.subheader("📱 QR Code Generator")
    qr_text = st.text_input("Enter link or text to generate QR code:")
    if st.button("Generate QR"):
        if qr_text.strip() == "":
            st.warning("Please enter some text or link.")
        else:
            qr_img = qrcode.make(qr_text)
            qr_buffer = io.BytesIO()
            qr_img.save(qr_buffer, format="PNG")
            st.image(qr_buffer.getvalue(), caption="QR Code", width=200)

# --- Mini AI Chatbot ---
with tab3:
    st.subheader("🤖 Mini AI Chatbot")

    # --- Bot Logic ---
    responses = {
        "hello": ["Hi there!", "Hello!", "Hey! How can I help?"],
        "how are you": ["I'm just a bot, but I'm doing great!", "All good here!"],
        "bye": ["Goodbye!", "See you later!", "Bye! Take care!"],
        "thanks": ["You're welcome!", "No problem!", "Anytime!"],
        "default": ["Sorry, I don't understand that.", "sorry I am just mini project of 1styear bca student", "Hmm, I'm not sure.","you asking lot to me I am just a mini project"]
        "who created you":["my creator name was krishna.","my creator name was gokul","my creator name was lakshimi"}
    }

    def get_response(user_input):
        user_input = user_input.lower()
        for key in responses:
            if key in user_input:
                return random.choice(responses[key])
        return random.choice(responses["default"])

    if "chat_history" not in st.session_state:
        st.session_state.chat
