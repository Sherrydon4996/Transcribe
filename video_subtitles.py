import json
import streamlit as st
import random
import tempfile
import subprocess
import os
from language_translate import return_translated_text
from pymongo import MongoClient

password = os.getenv("PASSWORD")

string_word = "mongodb+srv://edwinnjogu4996:ghvfCPPaVYVaMWgd@transcription.sezw1.mongodb.net/?retryWrites=true&w=majority&appName=Transcription"
client = MongoClient(string_word)
db = client["Transcription"]
db_collection = db["user_registration"]

file_name = [i for i in range(50)]
choice = random.choice(file_name)


def read_json_file(data):
    if data is not None:
        filtered_data = data.get("words", [])
        return data, filtered_data


def convert_ms_to_srt_format(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def combine_words_to_sentences(words):
    if words is not None:
        full_sentences = []
        word_sentence = []
        start_time = words[0]['start'] if words else 0

        for i, word in enumerate(words):
            if not word_sentence:
                start_time = word['start']
            word_sentence.append(word['text'])
            # Define a pause threshold in milliseconds
            pause_threshold = 300  # Adjust this value for better sentence detection
            # Check if this is the last word or if the next word starts after a pause
            # Also consider punctuation marks as indicators of sentence boundaries
            is_last_word = i == len(words) - 1
            next_word_starts_after_pause = (not is_last_word and
                                            words[i + 1]['start'] - word['end'] > pause_threshold)
            current_word_ends_with_punctuation = word['text'][-1] in ".!?"

            if is_last_word or next_word_starts_after_pause or current_word_ends_with_punctuation:
                end_time = word['end']
                full_sentences.append({
                    'start': start_time,
                    'end': end_time,
                    'text': ' '.join(word_sentence)
                })
                word_sentence = []

        return full_sentences


def video_upload_file():
    st.subheader(":blue[Note: Upload The correct video for your subtitles]")
    video_upload = st.file_uploader(".", type=["mp4", "mov", "avi", "mkv"])
    if video_upload is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix="mp4") as file_path:
            file_path.write(video_upload.read())
            video_file_path = file_path.name
        return video_file_path


def create_srt_file(sentences, user_target_language, user_name):
    if sentences is not None:
        srt_data_file = ""
        for i, sentence in enumerate(sentences):
            start_time = convert_ms_to_srt_format(sentence['start'])
            end_time = convert_ms_to_srt_format(sentence['end'])
            text = return_translated_text(sentence["text"], user_target_language)
            # text = sentence['text']
            srt_data_file += f"{i + 1}\n{start_time} --> {end_time}\n{text}\n\n"
        db_collection.update_one({"username": user_name}, {"$set": {"srt_file": srt_data_file}})
        st.success("srt file saved successfully")



def retrieve_srt_file_from_database(user_name):
    try:
        results = db_collection.find_one({"username": user_name}, {"srt_file": 1, "_id": 0})
        if results is not None:
            srt_file = results["srt_file"]
            with tempfile.NamedTemporaryFile(delete=False, suffix=".srt") as temp_srt:
                temp_srt.write(srt_file.encode('utf-8'))
                temp_srt_path = temp_srt.name
                return temp_srt_path
    except:
        return


def add_subtitles(video_file_path, srt_file):
    if srt_file is not None:
        temp_srt_file = "new_file.srt"
        with open(srt_file, "r", encoding="utf8") as file:
            srt_data = file.read()
        with open(temp_srt_file, "w") as file:
            file.write(srt_data)

        if video_file_path and srt_file:
            # Create a temporary file for the output video
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                output_path = temp_file.name

            if os.path.exists(output_path):
                os.remove(output_path)

            # Define the ffmpeg command
            ffmpeg_command = [
                'ffmpeg',
                '-i', video_file_path,
                '-vf', f"subtitles={temp_srt_file}",
                '-c:a', 'copy',
                output_path
            ]
            try:
                # Run the ffmpeg command
                subprocess.run(ffmpeg_command, check=True)
                if os.path.exists(srt_file):
                    os.remove(srt_file)

                if os.path.exists(temp_srt_file):
                    os.remove(temp_srt_file)
                return output_path
            except subprocess.CalledProcessError as e:
                st.error(f"Error running ffmpeg: {e}")
                return None
    else:
        st.error("One or both of the files might be missing")


def view_final_video(file):
    if file is not None:
        st.video(file, start_time=0, format="video/mp4")


def get_user_target_language():
    with open("languages.json", "r") as file:
        json_language = json.load(file)
    st.subheader(":blue[Note: your subtitles will be created in the language you select here]")
    with open("languages_value.json", "r") as file5:
        language_list = json.load(file5)
    user_list = st.selectbox("", list(json_language.values()))
    user_target_language = language_list[user_list]
    if user_target_language:
        language = f"Your information will be translated to: {json_language[user_target_language]}"
        st.success(language)
        return user_target_language


def page_appearance():
    st.markdown(f"""
        <div style="background-color:#4CAF50; padding: 20px; border-radius: 10px; text-align: center;">
            <h2 style="color:#FFFFFF; text-align:center; margin-bottom:15px;">Welcome to the Subtitle Generator Tool. Add Subtitles to Your Videos in a Few Easy Steps</h2>
            <h3 style="color:#F0F8FF; font-size:20px; margin-bottom:10px;">Instructions:</h3>
            <h2 style="color:gold; font-size:18px; margin-top:20px;">Note: this subtitles will be created from the video/audio you have transcribed in the transcription section</h2>
            <div>
                <p style="color:#FFFFFF;">Upload your video and select a target language for subtitle translation. Supported formats include .mp4, .mov, .avi, and .mkv.</p>
                <p style="color:#FFFFFF;">After generating subtitles, preview your video on the platform and download the final version or subtitle file for future use.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def call_subtitle_functions(json_file, username):
    page_appearance()
    filtered_data = None
    if json_file is not None:
        data, filtered_data = read_json_file(json_file)
    else:
        st.info("you do not have a transcribed file data. Upload and transcribe a file")
    full_sentences = combine_words_to_sentences(filtered_data)
    srt_file = retrieve_srt_file_from_database(username)
    col1, col2 = st.columns(2)
    with col1:
        user_target_language = get_user_target_language()
    with col2:
        video_file_path = video_upload_file()
    st.write("##")
    st.write("___")
    col3, col4 = st.columns(2)
    button_subs = st.button("add_subtitles")
    with col3:
        if button_subs:
            if json_file:
                if video_file_path:
                    create_srt_file(full_sentences, user_target_language, username)
                    final_video = add_subtitles(video_file_path, srt_file)
                    view_final_video(final_video)
                else:
                    st.error("Please upload a video to add subtitles")
            else:
                st.error("There is no transcribed file. Please upload and transcribe a file")
    with col4:
        st.image("images/sub.webp")


if __name__ == "__main__":
    call_subtitle_functions("")
