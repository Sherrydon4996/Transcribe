import tempfile
import requests
import time
import os
import streamlit as st


API_KEY_ASSEMBLY = os.environ.get('ASSEMBLY_API_KEY')

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

filename = "audio_result.wav"
headers = {'authorization': API_KEY_ASSEMBLY}


def read_file(file_name, file_extension, chunk_size=5242880):
    """Read the provided audio file"""
    with open(file_name, "rb") as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def upload_file(audio_file, file_extension):
    """Uploading the file for transcription"""
    upload_response = requests.post(upload_endpoint, headers=headers, data=read_file(audio_file, file_extension))
    audio_url = upload_response.json()['upload_url']
    return audio_url


def submitting_transcription_request(audio_url):
    transcription_request ={
            "audio_url": audio_url,
            "entity_detection": True,
            "sentiment_analysis": True,
            "iab_categories": True,
            "content_safety": True,
            "summarization": True,
            "speaker_labels": True,
            "summary_model": "informative",
            "summary_type": "bullets"

        }
    transcription_response = requests.post(transcript_endpoint, headers=headers, json=transcription_request)
    transcription_id = transcription_response.json()['id']
    return transcription_id


def poll(transcription_id):
    polling_endpoint = transcript_endpoint + "/" + transcription_id
    start_time = time.time()
    while True:
        with st.spinner("\nFinalising transcription results in about 30 secs....."):
            time.sleep(3)
        polling_response = requests.get(polling_endpoint, headers=headers)
        status = polling_response.json()['status']

        if status == "completed":
            end_time = time.time() - start_time
            st.info(f"Total transcription time: {end_time:.2f} seconds")
            return polling_response.json(), None
        elif status == "error":
            end_time = time.time() - start_time
            st.info(f"Total transcription time: {end_time:.2f} seconds")
            return polling_response.json(), polling_response.json()['error']
        with st.spinner("Wait for 30 seconds"):
            time.sleep(3)
        time.sleep(30)


def save_english_transcript(audio_file, file_extension):
    new_audio_url = upload_file(audio_file, file_extension)
    task_id = submitting_transcription_request(new_audio_url)
    data, error = poll(task_id)
    return data, error
