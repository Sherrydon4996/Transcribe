import streamlit as st
from video_to_audio import export_full_audio
from io import BytesIO
import tempfile
import time
from english_backend import save_english_transcript
import os
import glob
from pydub import AudioSegment


def upload_video_and_convert_audio_format(random_video_upload):
    def convert_audiosegment_to_bytes(audio_file):
        audio_bytes_io = BytesIO()
        audio_file.export(audio_bytes_io, format="mp3")
        audio_bytes = audio_bytes_io.getvalue()
        return audio_bytes
    # Upload video file
    video_upload = random_video_upload
    #

    if "audio" not in st.session_state:
        st.session_state.audio = None
    if video_upload is not None:
        if st.button("Convert to audio"):
            if video_upload is not None:
                with st.spinner("Converting video to audio please wait..."):
                    start_time = time.time()
                    file_extension = "." + video_upload.name.split(".")[-1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_video_file:
                        temp_video_file.write(video_upload.read())
                        temp_video_file_path = temp_video_file.name

                    audio = export_full_audio(temp_video_file_path)
                    end_time = time.time() - start_time
                    st.info(f"Finished converting in {end_time:.2f} seconds")
                    st.session_state.audio = audio
            else:
                st.error("Please upload a video file.")
        audio = st.session_state.audio
        if audio is not None:
            audio_bytes = convert_audiosegment_to_bytes(audio)
            return audio_bytes


