import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = os.path.join(
    os.path.dirname(__file__),
    'dumps',
    'The Binding of Isaac - AFTERBIRTH+ - Northernlion Plays - Episode 272 [Compromise] (Daily)-Hb6fkOt3sNo_cropped.flac')

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

encoding = enums.RecognitionConfig.AudioEncoding.FLAC
sample_rate_hertz = 48000
language_code = 'en-US'
speech_contexts = [types.SpeechContext(phrases=['Northern lion', 'Binding of Isaac'])]
config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code, "speech_contexts" : speech_contexts}


# Detects speech in the audio file
response = client.recognize(config, audio)

for result in response.results:
    print(u'Transcript: {}'.format(result.alternatives[0].transcript))
