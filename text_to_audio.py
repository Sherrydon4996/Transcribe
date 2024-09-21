import streamlit as st
from gtts import gTTS
import os
from PIL import Image
import tempfile
from sqlite_db import save_audio_filename, get_audio_filename

image_size = (1000, 900)


def page_header():
    st.markdown("""
    <div style="background-color:#4CAF50; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: white; font-family: 'Arial', sans-serif;">
            🎤 Convert your Text-to-Speech here 🎧
        </h1>
        <p style="color: white; font-size: 18px;">
            Transform your text into natural-sounding speech easily. Choose from a variety of voices and languages.
        </p>
    </div>
    <br></br>
    """, unsafe_allow_html=True)


def display_images(image):
    img = Image.open(image)
    display_image = img.resize(image_size, Image.LANCZOS)
    st.image(display_image)


def save_audio(text, file_type, username):
    if st.button("Save audio"):
        try:
            with st.spinner("Saving audio..."):
                return_saved_audio_file(text, file_type, username)
        except Exception as e:
            st.error(f"Error: {e}")
            return None


def confirm_file(username):
    if st.button("play audio"):
        try:
            results = get_audio_filename(username)
            if results:
                file_path_name = results
                st.audio(file_path_name)
            else:
                st.error("No saved audio file")

        except Exception as e:
            st.error(f"Error: {e}")


def download_audio_file(username):
    try:
        results = get_audio_filename(username)
        if results:
            file2 = results["audio_filename"]
            with open(file2, 'rb') as f:
                st.download_button(
                    label="Download audio file",
                    data=f.read(),
                    file_name=os.path.basename(file2),
                    mime="audio/mpeg"
                )
        else:
            st.info("No audio file saved")


    except Exception as e:
        st.error(f"Error: {e}")


def banner_text(text):
    st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            text-align: center;
            height: 60px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 10px;
            margin-bottom: 20px;
        ">
            <h3 style="
                color: white;
                font-family: 'Arial', sans-serif;
                font-size: 24px;
                font-weight: 600;
                margin: 0;
            ">
                {text}
            </h3>
        </div>
    """, unsafe_allow_html=True)


def footer_notes():
    st.markdown("""
    <div style="background-color: rgba(255,0,0,0.3); padding: 30px; border-top: 2px solid #e9ecef; text-align: center;">
        <h3 style="font-size: 20px; color: white; margin-bottom: 15px;">Thank You for Using Our Application!</h3>
        <h4 style="font-size: 16px; color: black; margin-bottom: 20px;">
            We hope our tool has helped streamline your workflow. Your feedback is essential to our growth and continued improvement.
        </h4>
        <div style="margin-bottom: 25px;">
            <h4 style="font-size: 14px; color: black; margin-bottom: 10px;">
                Have questions or need support? Get in touch with us via email or follow us on social media for the latest updates and support:
            </h4>
            <p style="font-size: 14px;">
                <a href="#" style="color: #007bff; text-decoration: none; margin-right: 15px;">support@webapp.com</a> | 
                <a href="#" target="_blank" style="color: #007bff; text-decoration: none; margin-right: 15px;">Twitter</a> | 
                <a href="#" target="_blank" style="color: #007bff; text-decoration: none;">Facebook</a>
            </p>
        </div>
        <hr style="border-top: 1px solid #e9ecef; margin-bottom: 20px;">
        <div style="font-size: 14px; color: #6c757d; margin-bottom: 15px;">
            <p>&copy; 2024 WebApp Inc. All rights reserved.</p>
            <p>
                Privacy Policy | Terms of Service | <a href="https://webapp.com/faq" target="_blank" style="color: #007bff; text-decoration: none;">FAQs</a>
            </p>
        </div>
        <div style="font-size: 12px; color: #6c757d;">
            <p>Built with ❤️ using <a href="https://streamlit.io" target="_blank" style="color: #007bff; text-decoration: none;">Streamlit</a> and open-source technologies.</p>
            <p>Version 1.0.0</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_and_save_audio(text, ext, username):
    tts = gTTS(text=text, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}")
    tts.save(temp_file.name)
    save_audio_filename(temp_file.name, username)


def return_saved_audio_file(string_file, file_type, username):
    create_and_save_audio(string_file, file_type, username)
    st.success(f"file saved to database")


def upload_file():
    text = "Upload a document with the formats below or write in text area below to continue .."
    banner_text(text)
    uploaded_file = st.file_uploader("Upload a file to convert to speech", type=["csv", "txt", "xlsx"])
    if uploaded_file is not None:
        string_file = uploaded_file.read().decode("utf-8")
        return string_file


def button_style():
    st.markdown("""
        <style>
            .stButton button {
                font-size: 16px;
                height:60px;
                background-color: #ff6f61;
                color: #ffffff;
                border: 2px solid #ff6f61;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .stButton button:hover {
                background-color: #ff4f41;
                transform: translateY(-2px);
                box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
            }
        </style>
    """, unsafe_allow_html=True)


def convert_text_to_audio(username):
    button_style()
    page_header()
    col1, col3, col6 = st.columns([1, 1, 1])
    with col1:
        display_images("images/13.jpg")
    with col3:
        display_images("images/12.jpg")
    with col6:
        display_images("images/13.jpg")
    text = "Choose the extension that you would want your file to end with.."
    banner_text(text)
    file_type = st.selectbox("Choose file format", ["mp3", "wav"])
    string_file = upload_file()
    if string_file is not None:
        text = st.text_area("Text", string_file, height=250)
    else:
        st.markdown("""
            <div style="background-color:#ADD8E6; padding:10px; border-radius:5px;">
                <h3 style="color:#000000; text-align:center;">Text to Speech</h3>
                <p style="color:#000000; text-align:center;">Enter text to convert to speech</p>
            </div>
        """, unsafe_allow_html=True)

        text = st.text_area("Add Text and press Ctrl + Enter to continue", height=250)
    if text:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            save_audio(text, file_type, username)
        with col2:
            confirm_file(username)
        with col3:
            download_audio_file(username)


if __name__ == "__main__":
    pass
