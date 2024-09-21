

import streamlit as st
from googletrans import Translator
import json
from sqlite_db import get_json_database

if "results" not in st.session_state:
    st.session_state.results = ""
if 'data_text' not in st.session_state:
    st.session_state.data_text = ""
if 'uploaded' not in st.session_state:
    st.session_state.uploaded = ""
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""


def detect_language(text):
    detected_language = Translator()
    detection = detected_language.detect(text)
    return detection.lang


# Function to translate text
def return_translated_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, target_language)
    return translation.text



# Function to select language
def select_language():
    with open("languages.json", "r") as file:
        json_language = json.load(file)
    introduction = ("Welcome to the Language Translation Section! This tool allows you to easily translate text or "
                    "documents into a wide range of languages. Whether you're translating a simple text or a whole document,"
                    " this application uses Google's translation service to deliver accurate translations right within the app.")

    instructions = "Instructions for Translation"
    p1 = "Select Your Target Language: Begin by choosing the language you want your text or document to be translated into. Use the dropdown menu to pick from a list of available languages."
    p2 = "Input Your Text: You can either type or paste your text into the text area provided or upload a .txt file using the file uploader."
    p3 = "Translate: After inputting your text or uploading a file, click the 'Translate' button. The app will automatically detect the language of the input text and display the translation in your selected target language."
    p4 = "View the Translation: The translated text will appear in the text area on the right. If your input text is already in the target language, the app will notify you."
    int = "This tool is perfect for quick translations, whether you're working on a project, reading foreign documents, or simply learning a new language. Enjoy your translation experience!"

    st.markdown(f"""
        <div style="background-color:#1E90FF; padding:20px; border-radius:10px; margin-bottom:20px;">
            <h2 style="color:#FFFFFF; text-align:center; margin-bottom:15px;">🌍 Translate Text or Documents to Your Chosen Language 🌍</h2>
            <h4 style="color:#F0F8FF; font-size:18px; margin-bottom:15px;">{introduction}</h4>
            <h3 style="color:#F0F8FF; font-size:20px; margin-bottom:10px;">Instructions:</h3>
            <ol style="color:#F8F8FF; font-size:16px; margin-left:20px;">
                <li>{p1}</li>
                <li>{p2}</li>
                <li>{p3}</li>
                <li>{p4}</li>
            </ol>
            <h4 style="color:#F0F8FF; font-size:18px; margin-top:20px;">{int}</h4>
        </div>
    """, unsafe_allow_html=True)

    col11, col12, col13 = st.columns([3, 1, 3])
    with col11:
        st.image("static/58.jpg")
    with col13:
        st.image("static/59.jpg")
    st.subheader(":green[Select and set your target language]")
    with open("languages_value.json", "r") as file5:
        language_list = json.load(file5)
    user_list = st.selectbox("", list(json_language.values()))
    user_target_language = language_list[user_list]
    if user_target_language:
        language = f"Your information will be translated to: {json_language[user_target_language]}"
        st.success(language)
        return json_language, user_target_language


def translate_language(username):
    users_languages, users_target_language = select_language()
    st.markdown("""
        <div style="background-color:#1E90FF; padding:10px; border-radius:5px; margin-top:10px;">
            <h2 style="color:#000000; text-align:center; color:purple;">Translate</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Use transcribed data"):
        json_data = get_json_database(username)
        if json_data is not None:
            st.session_state.data_text = json_data['text']
            st.write(f"data: {json_data['text']}")
            st.info("Transcribed data loaded successfully.")
        else:
            st.error("No transcribe file available")

    uploaded_file_in = st.file_uploader("Upload a file to translate", type=["txt"])
    if uploaded_file_in is not None:
        try:
            st.session_state.uploaded = uploaded_file_in.read().decode("utf-8")
        except:
            return

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        try:
            if st.session_state.uploaded:
                text = st.text_area("This space holds the transcribed text data", st.session_state.uploaded,
                                    height=200)
                st.warning("Remember to cancel uploaded files to avoid translating the wrong files")
            elif st.session_state.data_text:
                text = st.text_area("Enter text or upload file to translate", st.session_state.data_text, height=200)
                st.warning("Remember to cancel uploaded files to avoid translating the wrong files")
            else:
                text = st.text_area("Enter text or upload file to translate", "", height=200)
                st.warning("Remember to cancel any previous uploaded files to avoid translating the wrong files")
        except:
            return

    with col2:
        if st.button(f"Translate to {users_languages[users_target_language]}"):
            st.markdown("""
            <style>
            .stButton button {
                background-color: blue;
                color: white;
                border: 3px solid gold;
                padding: 10px 10px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 25px;
                width: 300px;
                height: 10px;
            }
            .stButton button:hover {
                background-color: green;
                color: black;
                border: 2px solid #4CAF50;
            }
            </style>
            """, unsafe_allow_html=True)

            if text:
                detected_language = detect_language(text)
                try:
                    st.info(f"Current detected language: {users_languages[detected_language]}")
                except KeyError:
                    st.error("Detected language not in the database list.")
                if detected_language != users_target_language:
                    st.session_state.translated_text = return_translated_text(text, users_target_language)
                else:
                    st.error(
                        f"The input text is already in {users_target_language}. Or you might have entered an unrecognized language")
            else:
                st.error("Please enter text to translate.")

    with col3:
        st.text_area("Translated Text", st.session_state.translated_text or "", height=200)


if __name__ == "__main__":
    translate_language()
