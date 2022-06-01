import speech_recognition as sr
from os import path

wav_filename = r'tmp\20210227_135213.wav'

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), wav_filename)

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file


try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))