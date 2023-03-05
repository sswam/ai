#!/usr/bin/env python3

from google.cloud import texttospeech
import os

# Create a client object
client = texttospeech.TextToSpeechClient()

# Set the text input
text_input = texttospeech.SynthesisInput(text="Hello, world!")

# Set the voice parameters
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Set the audio output format
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request
response = client.synthesize_speech(
    input=text_input,
    voice=voice,
    audio_config=audio_config
)

# Write the response to an MP3 file
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)

# Play the audio file
os.system("start output.mp3")
