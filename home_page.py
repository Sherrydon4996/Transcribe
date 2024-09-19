import tempfile
import streamlit as st
from PIL import Image
from io import BytesIO
import json
import os
import glob
from pathlib import Path
import pandas as pd
import random
import mysql.connector
from streamlit_option_menu import option_menu
from pydub import AudioSegment
import speech_recognition as sr
import io
from moviepy.editor import VideoFileClip


try:
    from english_backend import save_english_transcript
    from swahili_backend import save_transcript_swahili
    from video_to_audio import export_full_audio
    from upload_video_convert_audio_format import upload_video_and_convert_audio_format
    from text_to_audio import convert_text_to_audio, footer_notes
    from language_translate import translate_language, get_json_from_database
    from text_analysis import call_functions
    from video_subtitles import call_subtitle_functions
except:
    st.info("Unexpected error occurred, try refreshing the page!")

numbers = [number for number in range(300)]
number_file = random.choice(numbers)


password = os.environ.get('PASSWORD')
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="media_files"
)

my_cursor = connection.cursor()


def web_app_appearance():
    st.markdown("""
    <style>
        .stApp {
            background-color:#aab7b8 ;
        }
    </style>

    """, unsafe_allow_html=True)


def introductory_section():
    text = ("This platform allows you to accurately and quickly transcribe audio files. Using our advanced"
            " speech recognition technology, you can easily convert audio into text. Whether you are a student,"
            " writer, or researcher, here you get text from your audio files effortlessly. We offer"
            " transcription services in English and Swahili to meet your needs. Thank you for visiting our site,"
            " and we hope you enjoyed our services.")
    st.markdown(f"""
    <div style="background-color:#4CAF50; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: white; font-family: 'Arial', sans-serif;">
            Brief Introduction
        </h1>
        <p style="color: white; font-size: 18px;">
            {text}
        </p>
    </div>
    <br></br>
    """, unsafe_allow_html=True)


def microphone_icon_appearance():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col1:
        image_size = (800, 600)
        img = Image.open("static/microphone.jpeg")
        resized_image = img.resize(image_size, Image.LANCZOS)
        st.image(resized_image)
    with col2:
        image_size = (700, 350)
        img = Image.open("static/transcribe.webp")
        resized_image = img.resize(image_size, Image.LANCZOS)
        st.image(resized_image)
        st.markdown("""
                <div style="text-align: center; padding: 20px;">
                    <div style="font-size: 36px; color: #333; margin-top: 10px;">
                    <q>Transcribe Today</q>
                    </div>
                </div>


            """, unsafe_allow_html=True)

    with col3:
        image_size = (800, 600)
        img = Image.open("static/microphone.jpeg")
        resized_image = img.resize(image_size, Image.LANCZOS)
        st.image(resized_image)


def button_styling():
    # CSS for styling
    st.markdown("""
        <style>
            .stButton button {
                font-size: 18px;
                padding: 12px 20px;
                border-radius: 12px;
                background: linear-gradient(45deg, #6b73ff, #000dff);
                color: white;
                border: 2px solid #ffffff;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .stButton button:hover {
                background: linear-gradient(45deg, #000dff, #6b73ff);
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)


def remove_audio_files(directory, extensions=("*.mp3", "*.wav")):
    for ext in extensions:
        files = glob.glob(os.path.join(directory, ext))
        for file in files:
            try:
                os.remove(file)
                # st.info(f"Removed file: {file}")
            except Exception as e:
                st.error(f"Error removing file {file}: {e}")


def english_transcription():
    button_styling()
    english_icon = Image.open("static/English.png")
    new_icon_size = (650, 400)
    english_image = english_icon.resize(new_icon_size, Image.LANCZOS)
    # if st.button("Transcribe English"):
    col10, col11, col12 = st.columns([1, 1, 1])
    with col10:
        content = (
            "Upload your video or audio files, and we'll transcribe the content for you! Our service supports multiple formats and provides accurate text outputs."
            " Experience the power of our advanced transcription app for seamless and accurate audio-to-text conversion.")
        banner_html = f"""
        <div style="padding: 15px; background-color: #4CAF50; border-radius: 5px;">
            <h2 style="color: white; text-align: center;">🎙️ Transcription Service</h2>
            <h4 style="color: white; text-align: center;">
             {content}
            </h4>
        </div>
        """
        st.markdown(banner_html, unsafe_allow_html=True)
    with col11:
        st.image(english_image)

    with col12:
        content = ("Enjoy unparalleled accuracy with our Premium English Transcription App. Delivering "
                   "high-quality output, ensuring precision and ease of use for professionals and enthusiasts alike.")
        banner_html = f"""
             <div style="padding: 15px; background-color: #4CAF50; border-radius: 5px;">
                 <h2 style="color: white; text-align: center;">🎙️ Transcription Service</h2>
                 <h4 style="color: white; text-align: center;">
                  {content}
                 </h4>
             </div>
           """
        st.markdown(banner_html, unsafe_allow_html=True)
    st.markdown("""<div style="background-color:#1C2833; width:700px; text-align:center;
     height: 40px; border-radius:15px;">
        <h3 style="color:#F9E79F;">English Transcription:: Upload your audio file below..</h3>
    </div>""", unsafe_allow_html=True)


def upload_english_audio_files():
    uploaded_audio = st.file_uploader(f"Upload an english file", type=["mp3", "wav"])
    st.markdown("""<div style="background-color:#D35400; text-align:center;
           height: 40px;">
              <h3 style="color:#00D3BE;"> Upload a video instead..</h3>
          </div>""", unsafe_allow_html=True)
    english_video_upload = st.file_uploader("Choose an english video file to upload",
                                            type=["mp4", "mov", "avi", "mkv"])
    audio_bytes_file = upload_video_and_convert_audio_format(english_video_upload)
    return uploaded_audio, audio_bytes_file


def upload_swahili_audio_files():
    uploaded_audio = st.file_uploader("Upload swahili_file", type=["mp3", "wav"])
    st.markdown("""<div style="background-color:#D35400; text-align:center;
          height: 40px;">
             <h3 style="color:#00D3BE;"> Upload a video instead..</h3>
         </div>""", unsafe_allow_html=True)
    english_video_upload = st.file_uploader("Choose a swahili video file to upload", type=["mp4", "mov", "avi", "mkv"])
    audio_bytes_file = upload_video_and_convert_audio_format(english_video_upload)
    return uploaded_audio, audio_bytes_file


def process_english_audio_files(audio_bytes_file, english_uploaded_audio):
    if english_uploaded_audio is not None:
        bytes_file = english_uploaded_audio.read()
        clean_audio_file = BytesIO(bytes_file)
        file_format = "." + english_uploaded_audio.name.split(".")[-1]
        return clean_audio_file, file_format
    elif audio_bytes_file is not None:
        uploaded_file = audio_bytes_file
        st.success("Converted file detected")
        file_format = ".mp3"
        return uploaded_file, file_format
    else:
        st.warning("No audio available to transcribe")
def transcription_banner():
    st.markdown(
        """
        <div style="background-color: #e0e0e0; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h2 style="color: purple; text-align: center;">Here are three different transcription types</h2>
            <ul style="font-size: 16px; line-height: 1.5;">
                <li><strong>English High-Quality Transcription:</strong> Quality transcription of English audio @ <strong> Ksh. 10 per audio minute only.</strong></li>
                <li><strong>Swahili High-Quality Transcription:</strong> Charges are <strong>Ksh. 10 per audio minute</strong>.</li>
                <li><strong>Economy Plan Transcription:</strong> Charges are <strong>Ksh. 3 per audio minute</strong>. 
                <br>Note: Economy plan has lower quality results with no punctuation but is helpful for basic needs.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
def pricing_plans():
     st.markdown("""
        <style>
        .pricing-container {
            display: flex;
            # justify-content: space-between;
            width: 100%;
            height: 300px;
        }
        .plan {
            width: 300px;
            height: 100%;
        }
        .plan-1 {
            background-color: brown;
            color: black;
            font-weight:bolder;
            border: 2px solid green;
            padding: 10px 20px;
            width:400px;
            margin-right:20px;
        }
        .plan-2 {
            background-color: silver;
            font-weight:bolder;
            border: 2px solid green;
            padding: 10px 20px;
            width: 400px;
            margin-right:20px;
        }
        .plan-3 {
            background-color: gold;
            width: 400px; /* You can adjust the size of the last plan */
            font-weight:bolder;
            border: 2px solid green;
            padding: 10px 20px;
             margin-right:20px;
        }
            .plan-4 {
            background-color: green;
            width: 400px; /* You can adjust the size of the last plan */
            font-weight:bolder;
            border: 2px solid green;
            padding: 10px 20px;
            color:white;
        }
        </style>

        <div class="pricing-container"> 
            <div class="plan plan-1"> 
            <h2>Plan A </h2>
            <h4>Get 30 minutes @ discounted price of ksh.250</h4>
            <h4>Get 50 minutes @ discounted price of ksh.450</h4>
            </div>
            <div class="plan plan-2">
             <h2>Plan B </h2>
             <h4>Get 70 minutes @ discounted price of ksh.600 </h4>
             <h4>Get 100 minutes @ discounted price of ksh.900 </h4>
            </div>
            <div class="plan plan-3">
              <h2>Plan C </h2>
             <h4>Get more than 100 minutes @ discount of 20% </h4>
            </div>
            <div class="plan plan-4">
              <h2>For more infor: </h2>
             <h4> contact phone_no: +254711140899</h4>
             <h4> contact email: harrynjogu4996@gmail.com  </h4>
            </div>
        </div>
        """, unsafe_allow_html=True)


def economy_transcription_plan(login_username):
    st.markdown(
    """
    <div style="background-color: #2C3E50; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: #ECF0F1; text-align: center;">Unlock the Power of Readable Transcriptions</h2>
        <p style="color: #BDC3C7; font-size: 18px; text-align: center; line-height: 1.6;">
            Seamlessly convert your audio and video content into clear, concise, and readable text. 
            Our cutting-edge technology ensures that every word is captured with precision, 
            making your content more accessible and searchable. Whether it's an interview, podcast, 
            or video lecture, we've got you covered.
        </p>
        <h3 style="color: #ECF0F1; text-align: center;">Reliable, Efficient, and Ready for Your Needs</h3>
        <p style="color: #BDC3C7; font-size: 16px; text-align: center;">
            Experience the ease of transcribing your media files into text effortlessly. 
            Simply upload your audio or video files, and let our system handle the rest.
        </p>
    </div>
    """,
    unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose an audio or video file", type=["mp3", "wav", "ogg", "mp4", "avi", "mov"])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        if file_extension in ["mp4", "avi", "mov"]:
            # Convert video to audio
            video = VideoFileClip(temp_file_path)
            audio = video.audio
            audio_path = temp_file_path.rsplit(".", 1)[0] + ".wav"
            audio.write_audiofile(audio_path)
            video.close()
        else:
            audio_path = temp_file_path

        # Convert to WAV if not already
        if st.button("start_transcribing"):
            with st.spinner("Processing and transcribing..."):
           
                audio = AudioSegment.from_file(audio_path)
                duration = audio.duration_seconds
                minutes, duration = divmod(duration, 60)
                time_needed = (int(duration) + (60 * int(minutes))) / 12
                total_amount = round(time_needed * 0.6, 2)
                my_cursor.execute("select balance from user_details where username=%s", (login_username, ))
                amount = my_cursor.fetchone()
                balance = None
                if amount:
                    balance = amount[0]

                if balance >= total_amount:
                    wav_path = audio_path.rsplit(".", 1)[0] + ".wav"
                    audio.export(wav_path, format="wav")

                    recognizer = sr.Recognizer()
                    with sr.AudioFile(wav_path) as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.record(source)
                    try:
                        text = recognizer.recognize_google(audio)
                        st.text_area("Transcribed text", text, height=300)
                        my_cursor.execute("update user_details set balance = balance - %s where username=%s", (total_amount, login_username))
                        connection.commit()
                        st.success(f"You audio file has been successfully transcribed. total amount deducted: ksh. {total_amount}")
                    except sr.UnknownValueError:
                        return "Google Speech Recognition could not understand the audio"
                    except sr.RequestError:
                        return "Could not request results from Google Speech Recognition service"
                else:
                    st.warning("Oops! insufficient balance! Please contact 0711140899 for recharge.")

                               

def load_english_files(login_username):
    english_transcription()
    english_uploaded_audio, audio_bytes_file = upload_english_audio_files()
    if english_uploaded_audio is not None or audio_bytes_file is not None:
        available_file, file_extension = process_english_audio_files(audio_bytes_file, english_uploaded_audio)
        if available_file is not None:
            col2, col3, col4 = st.columns([1, 2, 1])
            with col2:
                if st.button("confirm file"):
                    st.audio(available_file)
            with col4:
                tr_button = st.button("Start Transcribing")
            if tr_button:
                def temp_storage(file_name, file_extension):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio_file:
                        if isinstance(file_name, bytes):
                            temp_audio_file.write(file_name)
                        else:
                            temp_audio_file.write(file_name.read())
                        temp_audio_file_path = temp_audio_file.name
                        return temp_audio_file_path

                temp_audio_path = temp_storage(available_file, file_extension)
                try:
                    audio = AudioSegment.from_file(temp_audio_path)
                    # CALCULATE TIME AND MONEY
                    duration = audio.duration_seconds
                    minutes, duration = divmod(duration, 60)
                    time_needed = (int(duration) + (60 * int(minutes))) / 12
                    total_amount = round(time_needed * 2, 2)
                    my_cursor.execute("select balance from user_details where username=%s", (login_username, ))
                    amount = my_cursor.fetchone()
                    balance = None
                    if amount:
                        balance = amount[0]

                    if balance >= total_amount:
                        json_data, error = save_english_transcript(temp_audio_path, file_extension)
                        try:
                            # my_cursor.execute("update user_details set json_files= NULL where username=%s", (login_username, ))
                            my_cursor.execute("update user_details set balance = balance - %s where username=%s", (total_amount, login_username))
                            connection.commit()
                        except:
                            st.error("Database error: error removing file from database")
                        if error:
                            st.warning(f"error: {error}")
                        else:
                            transcribed_text = json_data['text']
                            st.success(f"You audio file has been successfully transcribed. total amount deducted: ksh. {total_amount}")
                            remove_audio_files("./")
                            text_data = st.text_area("Transcribed data", transcribed_text, height=400)
                            st.balloons()
                            st.info(f"Your total transcribed words are: {len(text_data.split())}")
                            if len(text_data.split()) > 100:
                                st.warning("")
                                    
                            if english_uploaded_audio is not None:
                                document_names = ["data", "notes", "summary", "draft", "content", "info", "textfile",
                                                  "description",
                                                  "document", "outline", "log", "record", "report", "details",
                                                  "plain_text"]
                                file_name = random.choice(document_names)
                                st.download_button(
                                    label="Download text file",
                                    data=transcribed_text,
                                    file_name=f"{file_name}.txt",
                                    mime="text/plain"

                                )
                            else:
                                possible_filenames = ["data", "Your_info", "clean_data", "plain_text", "text", "info"]
                                file_name = random.choice(possible_filenames)
                                st.download_button(
                                    label="Download text file",
                                    data=transcribed_text,
                                    file_name=f"{file_name}.txt",
                                    mime="text/plain"

                                )

                            json_datafile = json.dumps(json_data)
                            json_filename = "json_file"

                            my_cursor.execute("update user_details set json_files=%s where username=%s",(json_datafile, login_username))
                            connection.commit()
                            st.success("json file saved to database")
                    else:
                        minutes, duration = divmod(duration, 60)
                        st.error(f"Oops! your balance is insufficient! Contact 0711140899 for recharge.")

                except Exception as e:
                    st.warning(f"error: {e}")


def swahili_transcription():
    button_styling()
    swahili_icon = Image.open("static/swahili.webp")
    swahili_icon_size = (650, 400)
    swahili_image = swahili_icon.resize(swahili_icon_size, Image.LANCZOS)
    col7, col8, col9 = st.columns([1, 1, 1])
    with col7:
        content = f"Karibu kwenye Tovuti Yetu ya Kutafsiri Sauti! Tovuti hii inakupa uwezo wa kutafsiri faili za sauti kwa usahihi na haraka."
        banner_html = f"""
             <div style="padding: 15px; background-color: #4CAF50; border-radius: 5px;">
                 <h2 style="color: white; text-align: center;">🎙️ Transcription Service</h2>
                 <h4 style="color: white; text-align: center;">
                  {content}
                 </h4>
             </div>
        """
        st.markdown(banner_html, unsafe_allow_html=True)
    with col8:
        st.image(swahili_image)
    with col9:
        content = "Tunatoa tafsiri kwa lugha ya Kiingereza na Kiswahili ili kukidhi mahitaji yako. Asante kwa kutembelea tovuti yetu na tunatumai utapata huduma zetu kuwa za manufaa."
        banner_html = f"""
             <div style="padding: 15px; background-color: #4CAF50; border-radius: 5px;">
                 <h2 style="color: white; text-align: center;">🎙️ Transcription Service</h2>
                 <h4 style="color: white; text-align: center;">
                  {content}
                 </h4>
             </div>
          """
        st.markdown(banner_html, unsafe_allow_html=True)


def process_uploaded_swahili_files(audio_bytes_file, swahili_uploaded_audio):
    if swahili_uploaded_audio is not None:
        bytes_file = swahili_uploaded_audio.read()
        clean_audio_file = BytesIO(bytes_file)
        file_format = "." + swahili_uploaded_audio.name.split(".")[-1]
        return clean_audio_file, file_format
    elif audio_bytes_file is not None:
        uploaded_file = audio_bytes_file
        st.success("Converted file detected")
        file_format = ".mp3"
        return uploaded_file, file_format
    else:
        st.warning("No audio available to transcribe")


def load_swahili_files(login_username):
    swahili_transcription()
    swahili_uploaded_audio, audio_bytes_file = upload_swahili_audio_files()
    if swahili_uploaded_audio is not None or audio_bytes_file is not None:
        available_file, file_extension = process_uploaded_swahili_files(audio_bytes_file, swahili_uploaded_audio)
        if available_file is not None:
            col2, col3, col4 = st.columns([1, 2, 1])
            with col2:
                if st.button("confirm file"):
                    st.audio(available_file)
            with col4:
                tr_button = st.button("Start Transcribing")
            if tr_button:
                def temp_storage(file_name, file_extension):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio_file:
                        if isinstance(file_name, bytes):
                            temp_audio_file.write(file_name)
                        else:
                            temp_audio_file.write(file_name.read())
                        temp_audio_file_path = temp_audio_file.name
                        return temp_audio_file_path

                temp_audio_path = temp_storage(available_file, file_extension)
                try:
                    audio = AudioSegment.from_file(temp_audio_path)
                    duration = audio.duration_seconds
                    minutes, duration = divmod(duration, 60)
                    time_needed = (int(duration) + (60 * int(minutes))) / 12
                    total_amount = round(time_needed * 2, 2)
                    my_cursor.execute("select balance from user_details where username=%s", (login_username, ))
                    amount = my_cursor.fetchone()
                    balance = None
                    if amount:
                        balance = amount[0]

                    if balance >= total_amount:
                        data, error = save_transcript_swahili(temp_audio_path, file_extension)
                        my_cursor.execute("delete from text_files where json_filename=%s", ("json_file",))
                        my_cursor.execute("update user_details set balance = balance - %s where username=%s", (total_amount, login_username))
                        connection.commit()
                        if error:
                            st.warning(f"error: {error}")
                        else:
                            transcribed_text = data['text']
                            st.success("You audio file has been successfully transcribed")
                            text_data = st.text_area("Transcribed data", transcribed_text, height=400)
                            st.balloons()
                            st.info(f"Your total transcribed words are: {len(text_data.split())}")
                            if len(text_data.split()) > 10:
                                st.warning(
                                    "You've exhausted the maximum free words given, connect your payment method to continue"
                                    "enjoying the services!")

                            if swahili_uploaded_audio is not None:
                                document_names = ["data", "notes", "summary", "draft", "content", "info", "textfile",
                                                  "description",
                                                  "document", "outline", "log", "record", "report", "details",
                                                  "plain_text"]
                                file_name = random.choice(document_names)
                                st.download_button(
                                    label="Download text file",
                                    data=transcribed_text,
                                    file_name=f"{file_name}.txt",
                                    mime="text/plain"

                                )

                            else:
                                possible_filenames = ["data", "info", "clean_data", "plain_text", "text"]
                                file_name = random.choice(possible_filenames)
                                st.download_button(
                                    label="Download text file",
                                    data=transcribed_text,
                                    file_name=f"{file_name}.txt",
                                    mime="text/plain"

                                )
                            st.warning("Note: swahili files are not saved in database, therefor not accessible for video subtitles")
                    else:
                        minutes, duration = divmod(duration, 60)
                        st.error("insufficient balance, contact admin")
                except Exception as e:
                    st.warning(f"error: {e}")


def menu_bar():
    with st.container():
        options_menu_bar = option_menu(
            menu_title="Transcription menu",
            options=["English_Swahili Transcription", "text_analysis", "add_video_subtitles", "Text to audio files",
                     "Detect and translate language", "admins_page"],
            icons=["bi-emoji-smile", "bi-search", "bi-shield-lock", "bi-key", "bi-journal-text"],
            orientation="horizontal",
            key="transcription_menu_key"
        )
        return options_menu_bar


def session_state(options_menu_bar, user_name):
    if "swahili_transcription" not in st.session_state:
        st.session_state.swahili_transcription = False
    if "free_plan" not in st.session_state:
        st.session_state.free_plan = False


    if options_menu_bar == "English_Swahili Transcription":
        button_styling()
        transcription_banner()
        with st.expander(":blue[Check for alternative and cheaper pricing plans]"):
            pricing_plans()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("Transcribe English"):
                st.session_state.swahili_transcription = False
                st.session_state.free_plan = False

        with col2:
            if st.button("Economy_plan"):
                st.session_state.free_plan = True
                st.session_state.swahili_transcription = False
        with col3:
            if st.button("Transcribe Swahili"):
                st.session_state.swahili_transcription = True
                st.session_state.free_plan = False

        if st.session_state.swahili_transcription:
            load_swahili_files(user_name)
        elif st.session_state.free_plan:
            economy_transcription_plan(user_name)
        else:
            load_english_files(user_name)


def manage_users(username):
    # user_name = st.text_input("Enter admins username and press enter to gain access")
    if username:
        if username == "harry_transcriber":
            my_cursor.execute("select * from user_details")
            results = my_cursor.fetchall()
            with st.expander("user registration details"):
                if results:
                    df = pd.DataFrame(results, columns=["id", "username", "email", "full_names", "amount", "json_filename", "srt_file", "password", "time"])
                    df.reset_index(drop=True, inplace=True)
                    st.dataframe(df)
                    selected_user = st.selectbox("Select user", results)
                    user_name_selected = (selected_user[1])
                    if user_name_selected:
                        if st.button("Delete user"):
                            my_cursor.execute("delete from user_details where username=%s", (user_name_selected,))
                            connection.commit()
                            st.success("User has been deleted successfully")
                else:
                    st.info("no registration details yet")
            with st.expander("User amount"):
                selected_user = st.selectbox("Select user to add amount", results)
                if selected_user:
                    user_name_selected = (selected_user[1])
                    sign = st.selectbox("select sign", ["+","-"])
                    amount = st.number_input("Enter amount", min_value=0)
                    if user_name_selected:
                        if st.button("press to + or - amount"):
                            if amount > 9:
                                my_cursor.execute(f"update user_details set balance= balance {sign} %s where username=%s", ( amount, user_name_selected))
                                connection.commit()
                                if sign == "+":
                                    st.success(f"{amount} was added to the user user successfully")
                                else:
                                    st.success(f" {amount} was deducted from the user successfully")
                            else:
                                st.error("Kindly enter the amount you want to pass to the user")
                else:
                    st.error("No users to add amount!")

            with st.expander("all users login history"):
                my_cursor.execute("select * from login_info")
                results = my_cursor.fetchall()
                if results:
                    df = pd.DataFrame(results, columns=["id", "username", "full_names", "time"])
                    df.reset_index(drop=True, inplace=True)
                    st.dataframe(df)
                    if st.button("Clear history"):
                        my_cursor.execute("delete from login_info")
                        connection.commit()
                        st.success("User has been deleted successfully")

                else:
                    st.info("No login info yet")
        else:
            st.error(f"You are not authorized to access this data!")
    else:
        st.info("Access key is admin username.")


def expanded_menu_bar(options_menu_bar, json_file, username):
    if options_menu_bar == "text_analysis":
        call_functions(json_file)
    elif options_menu_bar == "Text to audio files":
        convert_text_to_audio()
    elif options_menu_bar == "Detect and translate language":
        translate_language()
    elif options_menu_bar == "add_video_subtitles":
        call_subtitle_functions(json_file, username)
    elif options_menu_bar == "admins_page":
        manage_users(username)


def recall_functions(user_name):
    web_app_appearance()
    introductory_section()
    microphone_icon_appearance()
    button_styling()
    menu_bar_options = menu_bar()
    session_state(menu_bar_options, user_name)
    json_file = get_json_from_database(user_name)
    expanded_menu_bar(menu_bar_options, json_file, user_name)
    st.markdown("---")
    st.markdown("© 2024 Audio Transcription App | Developed by @Harry")
    footer_notes()


if __name__ == "__main__":
    recall_functions("")
