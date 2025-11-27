from gtts import gTTS
import streamlit as st
import tempfile

LANGUAGES = {
    "English" : "en",
    "Hindi" : "hi",
    "Telugu" : "te",
    "Tamil" : "ta",
    "Kannada" : "kn",
    "Malayalam" : "ml",
    "Spanish" : "es",
    "French" : "fr",
    "German" : "de"
}

st.set_page_config(page_title="Tect To Speech", page_icon="🎤",layout="centered")
st.title("-> Streamlit Text to Speech Generator...")
st.write("Convert text into speech with language selection and download option.")

text = st.text_input("Enter The Text Here:")    

language = st.selectbox("Sellect The Language...", list(LANGUAGES.keys()))

if st.button("Click To Generate.."):
    if text.strip() == "":
        st.warning("Please Enter The Text...")
    else:
        tts = gTTS(text=text, lang=LANGUAGES[language])
        temp_file = tempfile.NamedTemporaryFile(delete=False,suffix=".mp3")
        tts.save(temp_file.name)

        st.success("-> Audio Generated <-")
        st.audio(temp_file.name)

        with open(temp_file.name, "rb") as f:
            st.download_button(
                label="Downlode Audio",
                data=f.read(),
                file_name="audio.mp3",
                mime="audio/mp3"
            )   