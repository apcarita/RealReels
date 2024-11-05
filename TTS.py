
#TODO implement 11 labs API
# takes in text, reads it and saves to the provided path using 11 labs api 

from pathlib import Path
from openai import OpenAI
from google.cloud import texttospeech
import assemblyai as aai
import os
from dotenv import load_dotenv
import argparse
import re
from difflib import SequenceMatcher
from moviepy.editor import *
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def speak(text, output_path):
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')

    client = OpenAI(api_key=api_key)
    print(f"getting audio... \n")
    speech_file_path = Path(output_path).parent / "speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input=text)

    response.stream_to_file(output_path)
    return output_path
def epensiveSpeak(text, output_path, voice):
    load_dotenv()
    api_key = os.getenv('ELEVEN_API_KEY')
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2"
    )

    save(audio, output_path)

    return output_path
def makeAudio(lines, output_path, pause_length, voice):
    print("Starting makeAudio function")
    silence = AudioFileClip("Logs/silence.mp3").subclip(0, pause_length)
    audio_paths = []
    for i, line in enumerate(lines):
        print(f"Processing line {i}: {line}")
        audio_path = epensiveSpeak(line, f"temp/temp{i}.mp3", voice)
        print(f"Generated audio for line {i} at {audio_path}")
        audio_paths.append(AudioFileClip(audio_path))
        audio_paths.append(silence)
    print("Concatenating audio clips")
    audio_paths.append(silence)
    audio_paths.append(silence)

    final_audio = concatenate_audioclips(audio_paths)
    final_audio.write_audiofile(output_path)
    print(f"Final audio written to {output_path}")
    return output_path

def cheapSpeak(input_text, output_path):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=input_text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Journey-F",
    )

    audio_config = texttospeech.AudioConfig(
     audio_encoding=texttospeech.AudioEncoding.LINEAR16,
     speaking_rate=1
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

# The response's audio_content is binary.
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {output_path}')


    return output_path

def transcribePause(audio_path, srt_output_path, pause_length, lines):
    aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
    transcriber = aai.Transcriber()
    print("\n Transcribing video... \n")
    transcript = transcriber.transcribe(audio_path)
    words = transcript.words
    srt_lines = []
    lineSoFar = ""
    lines_already_found = 0
    offset_time_start = 0 
    offset_time_end = 0   

    audio = AudioFileClip(audio_path)

    for i, word in enumerate(words, 1):
        if(seeIfLineEnd(lineSoFar, lines_already_found, lines)):
            lineSoFar = ""
            lines_already_found += 1
            offset_time_end+= pause_length
            offset_time_start+= pause_length
            
        start_time = f"{(word.start + offset_time_start) // 3600000:02}:{((word.start + offset_time_start) % 3600000) // 60000:02}:{((word.start + offset_time_start) % 60000) // 1000:02},{(word.start + offset_time_start) % 1000:03}"
        end_time = f"{(word.end + offset_time_end) // 3600000:02}:{((word.end + offset_time_end) % 3600000) // 60000:02}:{((word.end + offset_time_end) % 60000) // 1000:02},{(word.end + offset_time_end) % 1000:03}"

        lineSoFar += word.text + " "
        srt_lines.append(f"{i}\n{start_time} --> {end_time}\n{word.text}\n")

    srt_content = "\n".join(srt_lines)
    with open(srt_output_path, "w") as f:
        f.write(srt_content)

    print("Generated SRT file at: ", srt_output_path)
        
    return srt_output_path

def transcribe(audio_path, srt_output_path):
    aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
    transcriber = aai.Transcriber()
    print("\n Transcribing audio... \n")
    transcript = transcriber.transcribe(audio_path)
    words = transcript.words
    srt_lines = []
    
    audio = AudioFileClip(audio_path)

    for i, word in enumerate(words, 1):
        start_time = f"{(word.start) // 3600000:02}:{((word.start) % 3600000) // 60000:02}:{((word.start) % 60000) // 1000:02},{(word.start) % 1000:03}"
        end_time = f"{(word.end) // 3600000:02}:{((word.end) % 3600000) // 60000:02}:{((word.end) % 60000) // 1000:02},{(word.end) % 1000:03}"

        srt_lines.append(f"{i}\n{start_time} --> {end_time}\n{word.text}\n")

    srt_content = "\n".join(srt_lines)
    with open(srt_output_path, "w") as f:
        f.write(srt_content)

    print("Generated SRT file at: ", srt_output_path)
        
    return srt_output_path

def seeIfLineEnd(lineSoFar, lines_already_found, lines):    
    lineEnd = False
    print(lines[lines_already_found].strip())
    if is_similar(lines[lines_already_found].strip(), lineSoFar.strip()):
        lineEnd = True
        print(f"Line end: {lineSoFar}")
    return lineEnd

def clean_string(s):
        return re.sub(r'\W+', '', s).lower()

def is_similar(a, b, threshold=0.97):
    return SequenceMatcher(None, clean_string(a), clean_string(b)).ratio() >= threshold

if __name__ == "__main__":
    #speak("te#sting testing, 1 2 3", "Generated/Audio/Complete/test.mp3 \n")
    seeIfLineEnd("In the beginning God created the heaven and the.", 0, ["In the beginning God created the heaven and the earth."])