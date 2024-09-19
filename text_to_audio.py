import glob
import streamlit as st
from gtts import gTTS
import os
from random import randint
from PIL import Image
import tempfile
import  mysql.connector



# Establish MySQL connection (ensure credentials and database are correct)
try:
    password = os.environ.get('PASSWORD')
except:
    st.error("Could not retrieve db passwd")
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="media_files"
    )
    
    my_cursor = connection.cursor()
except Exception as e:
    st.warning(f"Database error: {e}")

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


def save_audio(text, file_type):
    file_name = st.text_input("enter file name to save the audio")
    if st.button("Save audio"):
        if file_name:
            try:
                with st.spinner("Saving audio..."):
                    return_saved_audio_file(text, file_type, file_name)
            except Exception as e:
                st.error(f"Error: {e}")
                return None
        else:
            st.error("Please provide a name for your file")


def delete_audio():
    file_name = st.text_input("enter file name to delete the audio")
    if st.button("Delete audio"):
        try:
            if file_name:
                my_cursor.execute("select audio_data from t_data where audio_filename=%s", (file_name, ))
                results = my_cursor.fetchone()
                if results:
                    my_cursor.execute("delete from t_data")
                    connection.commit()
                    file_path_name = results[0]
                    os.remove(file_path_name)
                else:
                    st.error("No saved audio file")
            else:
                st.error("No file name entered")
        except Exception as e:
            st.error(f"Error: {e}")


def confirm_file():
    file = st.text_input("Access your file by name and play.")
    if st.button("play audio"):
        try:
            if file:
                query = "select audio_data from t_data where audio_filename=%s"
                values = (file,)
                my_cursor.execute(query, values)
                results = my_cursor.fetchone()
                if results:
                    file_path_name = results[0]
                    st.audio(file_path_name)
                else:
                    st.error("No saved audio file")
            else:
                st.error("Please enter a file_name")

        except Exception as e:
            st.error(f"Error: {e}")


def download_audio_file():
    file = st.text_input("Enter the name of your file to download it.")
    try:
        if file:
            my_cursor.execute("select audio_data from t_data where audio_filename=%s", (file, ))
            results = my_cursor.fetchone()
            if results:
                file2 = results[0]
                with open(file2, 'rb') as f:
                    st.download_button(
                        label="Download audio file",
                        data=f.read(),
                        file_name=os.path.basename(file2),
                        mime="audio/mpeg"
                    )
            else:
                st.info("No audio file saved")
        else:
            st.info("Please enter the name of the file you want to download")

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
    <div style="background-color: #aab7b8; padding: 30px; border-top: 2px solid #e9ecef; text-align: center;">
        <h3 style="font-size: 20px; color: #343a40; margin-bottom: 15px;">Thank You for Using Our Application!</h3>
        <p style="font-size: 16px; color: #495057; margin-bottom: 20px;">
            We hope our tool has helped streamline your workflow. Your feedback is essential to our growth and continued improvement.
        </p>
        <div style="margin-bottom: 25px;">
            <p style="font-size: 14px; color: #6c757d; margin-bottom: 10px;">
                Have questions or need support? Get in touch with us via email or follow us on social media for the latest updates and support:
            </p>
            <p style="font-size: 14px;">
                <a href="mailto:support@webapp.com" style="color: #007bff; text-decoration: none; margin-right: 15px;">support@webapp.com</a> | 
                <a href="https://twitter.com/webapp" target="_blank" style="color: #007bff; text-decoration: none; margin-right: 15px;">Twitter</a> | 
                <a href="https://www.facebook.com/harrison.njogu.94/" target="_blank" style="color: #007bff; text-decoration: none;">Facebook</a>
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


def create_and_save_audio(text, ext, file_name):
    tts = gTTS(text=text, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}")
    tts.save(temp_file.name)
    query = "INSERT INTO t_data(audio_filename, audio_data) VALUES(%s,%s)"
    values = (file_name, temp_file.name)
    my_cursor.execute(query, values)
    connection.commit()


def return_saved_audio_file(string_file, file_type, file_name):
    create_and_save_audio(string_file, file_type, file_name)
    st.success(f"{file_name} saved to database")


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


def convert_text_to_audio():
    button_style()
    page_header()
    col1, col3, col6 = st.columns([1, 1, 1])
    with col1:
        display_images("static/13.jpg")
    with col3:
        display_images("static/12.jpg")
    with col6:
        display_images("static/13.jpg")
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
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            save_audio(text, file_type)
        with col2:
            delete_audio()
        with col3:
            confirm_file()
        with col4:
            download_audio_file()


if __name__ == "__main__":
    pass
