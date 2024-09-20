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


