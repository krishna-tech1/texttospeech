import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import qrcode
import io

# --- Setup ---
translator = Translator()
lang_dict = LANGUAGES
lang_names = list(lang_dict.values())
lang_code_dict = {v.title(): k for k, v in lang_dict.items()}

st.set_page_config(page_title="MultiTool App", layout="centered")
st.title("🛠️ MultiTool App")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🈯 Translator + TTS", "📱 QR Code Generator", "📏 Unit Converter"])

# --- Tab 1: Translator + TTS ---
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

# --- Tab 2: QR Code Generator ---
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

# --- Tab 3: Unit Converter ---
with tab3:
    st.subheader("📏 Unit Converter")

    conversion_type = st.selectbox("Select Conversion Type", ["Length", "Weight", "Temperature"])

    if conversion_type == "Length":
        units = {
            "Meter": 1,
            "Kilometer": 1000,
            "Centimeter": 0.01,
            "Millimeter": 0.001,
            "Inch": 0.0254,
            "Foot": 0.3048,
            "Yard": 0.9144,
            "Mile": 1609.34
        }

    elif conversion_type == "Weight":
        units = {
            "Gram": 1,
            "Kilogram": 1000,
            "Milligram": 0.001,
            "Pound": 453.592,
            "Ounce": 28.3495
        }

    elif conversion_type == "Temperature":
        units = {}

    if conversion_type != "Temperature":
        amount = st.number_input("Enter value", value=0.0)
        from_unit = st.selectbox("From", list(units.keys()))
        to_unit = st.selectbox("To", list(units.keys()))

        if st.button("Convert"):
            result = amount * units[from_unit] / units[to_unit]
            st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
    else:
        temp = st.number_input("Enter temperature", value=0.0)
        from_temp = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
        to_temp = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])

        def convert_temperature(value, from_u, to_u):
            if from_u == to_u:
                return value
            if from_u == "Celsius":
                if to_u == "Fahrenheit":
                    return value * 9/5 + 32
                elif to_u == "Kelvin":
                    return value + 273.15
            elif from_u == "Fahrenheit":
                if to_u == "Celsius":
                    return (value - 32) * 5/9
                elif to_u == "Kelvin":
                    return (value - 32) * 5/9 + 273.15
            elif from_u == "Kelvin":
                if to_u == "Celsius":
                    return value - 273.15
                elif to_u == "Fahrenheit":
                    return (value - 273.15) * 9/5 + 32

        if st.button("Convert"):
            converted_temp = convert_temperature(temp, from_temp, to_temp)
            st.success(f"{temp} {from_temp} = {converted_temp:.2f} {to_temp}")
