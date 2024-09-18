
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import tempfile
from pathlib import Path


def export_full_audio(video_file):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_output_file:
        output_file = temp_output_file.name

    # Load the entire video
    video = VideoFileClip(video_file)

    # Extract the audio
    audio = video.audio
    audio.write_audiofile(output_file)

    # Load the audio file to AudioSegment for further operations
    combined_audio = AudioSegment.from_file(output_file)

    return combined_audio


if __name__ == "__main__":
    combined_audio, audio_path = export_full_audio("English.mp4")
    print(f"Final audio file created at: {audio_path}")



















# from moviepy.editor import VideoFileClip
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# from pydub import AudioSegment
# import os
# from pathlib import Path
#
#
# def convert_to_audio(video_path, segment_length=60):
#     video = VideoFileClip(video_path)
#     duration = int(video.duration)
#     audio_paths = []
#     for start_time in range(0, duration, segment_length):
#         end_time = min(start_time + segment_length, duration)
#         temp_video_file = f"video_segment_{start_time}_{end_time}.mp4"
#
#         ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=temp_video_file)
#
#         video_segment = VideoFileClip(temp_video_file)
#         audio_segment = video_segment.audio
#         audio_path = f"audio_segment_{start_time}_{end_time}.wav"
#         audio_segment.write_audiofile(audio_path)
#         audio_paths.append(audio_path)
#
#         video_segment.reader.close()
#         video_segment.audio.reader.close_proc()
#         os.remove(temp_video_file)
#     return audio_paths
#
#
# def export_full_audio(video_file):
#     audio_paths = convert_to_audio(video_file)
#     combine_audio = AudioSegment.empty()
#     for audio_part in audio_paths:
#         segment1 = AudioSegment.from_file(audio_part)
#         combine_audio += segment1
#         os.remove(audio_part)
#     naming_file = Path(video_file).stem
#     output_file = f"{naming_file}.mp3"
#     combine_audio.export(output_file, format="mp3")
#     audio_file = AudioSegment.from_file(output_file)
#     return audio_file
#
#
# if __name__ == "__main__":
#     export_full_audio("English.mp4")