import streamlit as st
import tempfile
import random
import subprocess

# video_file_path = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])
def video_upload_file():
    video_upload = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])
    if video_upload is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix="mp4") as file_path:
            file_path.write(video_upload.read())
            video_file_path = file_path.name
        st.write(video_file_path)
        return video_file_path
video_file_path = video_upload_file()
def add_subtitles(srt_file):
    st.info(video_file_path)
    if video_file_path is not None:
        new_filename = [i for i in range(20)]
        choice = random.choice(new_filename)
        file = F"{choice}.mp4"
        ffmpeg_command = [
            'ffmpeg',
            '-i', video_file_path,
            '-vf', f"subtitles={srt_file}",
            '-c:a', 'copy',
            file
        ]
        st.info("starting the process")
        print("Running ffmpeg command:", " ".join(ffmpeg_command))
        subprocess.run(ffmpeg_command, check=True)
        print("Final video with subtitles created:", new_filename)
        if file is not None:
            if st.button("View final file"):
                st.video(file)


if __name__ == "__main__":
    if st.button("add subtitles"):
        st.video("6.mp4")
        add_subtitles("infor.srt")

# import json
#
#
#
# def convert_ms_to_srt_format(milliseconds):
#     seconds, milliseconds = divmod(milliseconds, 1000)
#     minutes, seconds = divmod(seconds, 60)
#     hours, minutes = divmod(minutes, 60)
#     return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
#
# def combine_words_to_sentences(words):
#     full_sentences = []
#     word_sentence = []
#     start_time = words[0]['start'] if words else 0
#
#     for i, word in enumerate(words):
#         if not word_sentence:
#             start_time = word['start']
#         word_sentence.append(word['text'])
#         # Define a pause threshold in milliseconds
#         pause_threshold = 300  # Adjust this value for better sentence detection
#         # Check if this is the last word or if the next word starts after a pause
#         # Also consider punctuation marks as indicators of sentence boundaries
#         is_last_word = i == len(words) - 1
#         next_word_starts_after_pause = (not is_last_word and
#                                         words[i + 1]['start'] - word['end'] > pause_threshold)
#         current_word_ends_with_punctuation = word['text'][-1] in ".!?"
#
#         if is_last_word or next_word_starts_after_pause or current_word_ends_with_punctuation:
#             end_time = word['end']
#             sentences.append({
#                 'start': start_time,
#                 'end': end_time,
#                 'text': ' '.join(word_sentence)
#             })
#             word_sentence = []
#
#     return full_sentences
#
#
# with open("4.json", "r") as file:
#     data = json.load(file)
#     new_data = data.get("words", [])
# combine_words_to_sentences(new_data)
#
# words = data.get('words', [])
# sentences = combine_words_to_sentences(words)
#
# srt_file = "infor.srt"
#
# with open(srt_file, "w") as file:
#     for i, sentence in enumerate(sentences):
#         start_time = convert_ms_to_srt_format(sentence['start'])
#         end_time = convert_ms_to_srt_format(sentence['end'])
#         text = sentence['text']
#         file.write(f"{i + 1}\n{start_time} --> {end_time}\n{text}\n\n")
#
# print("SRT file created:", srt_file)
#
#
#
# #
# # import yt_dlp
# # import time
# # import os
# # import requests
# # import json
# # import pandas as pd
# # import pprint
# # import random
# #
# # youtube_url = None
# # transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
# # API_KEY_ASSEMBLY = os.getenv("assembly_api")
# #
# # filename = "audio_result.wav"
# # headers = {'authorization': API_KEY_ASSEMBLY}
# #
# # ydl = yt_dlp.YoutubeDL()
# #
# #
# # def get_video_infos(url):
# #     with ydl:
# #         result = ydl.extract_info(
# #             url,
# #             download=False
# #         )
# #     if "entries" in result:
# #         pprint.pprint(result)
# #         return result['entries'][0]
# #     return result
# #
# #
# # def get_audio_url(video_info):
# #     for f in video_info['formats']:
# #         if f['ext'] == 'm4a':
# #             return f["url"]
# #
# #
# # def submitting_transcription_request(audio_url, sentiment_analysis):
# #     transcription_request = {"audio_url": audio_url, "punctuate": True, "sentiment_analysis": sentiment_analysis}
# #     transcription_response = requests.post(transcript_endpoint, headers=headers, json=transcription_request)
# #     transcription_id = transcription_response.json()["id"]
# #     return transcription_id
# #
# #
# # def poll(transcription_id):
# #     polling_endpoint = transcript_endpoint + "/" + transcription_id
# #     while True:
# #         polling_response = requests.get(polling_endpoint, headers=headers)
# #         status = polling_response.json()['status']
# #         if status == "completed":
# #             return polling_response.json(), None
# #         elif status == "error":
# #             return polling_response.json(), polling_response.json()['error']
# #         time.sleep(30)
# #
# #
# # def get_trans_results():
# #     url = "https://www.youtube.com/watch?v=o0FCW-iN9OU"
# #     video_infos = get_video_infos(url)
# #     new_audio_url = get_audio_url(video_infos)
# #     task_id = submitting_transcription_request(new_audio_url, sentiment_analysis=True)
# #     data, error = poll(task_id)
# #     return data, error
# #
# #
# # def save_transcript():
# #     data, error = get_trans_results()
# #     numbers = [i for i in range(1, 20, 1)]
# #     file_number = random.choice(numbers)
# #     json_file = f"{file_number}.json"
# #
# #     try:
# #         txt_file = f"{file_number}.txt"
# #         with open(txt_file, "w") as file:
# #             file.write(data["text"])
# #
# #         with open(json_file, "w") as file:
# #             json.dump(data, file, indent=4)
# #
# #     except Exception as e:
# #         print(f"error: {e}")
# #
# #
# # if __name__ == "__main__":
# #     save_transcript()
# #
# # # video_info = get_video_infos("https://www.youtube.com/watch?v=wjaCtcoVHT4")
# # # audio_url = get_audio_url(video_info)
# # # title = video_info['title']
# # # title = title.strip().replace(" ", "_")
# # # print(title)
