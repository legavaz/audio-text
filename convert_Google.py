from asyncio.windows_events import NULL
from operator import le
from pydub import AudioSegment
import speech_recognition as sr
from os import path


def convert_wav(m_file_name: str):

    # находим расширение
    m_ext = file_name[len(m_file_name)-3:]
    # создаем новое имя файла с нужным расширением
    wav_filename = m_file_name.replace(m_ext, 'wav')

    print('1) конвертация файла', m_file_name, '-->', wav_filename)

    if not path.exists(m_file_name):
        print('не найден:', m_file_name)
    else:

        track = AudioSegment.from_file(m_file_name, m_ext)

        track.export(wav_filename, format='wav')

    return wav_filename


def Recognize(wav_filename):
    print('2) распознование файла', wav_filename)
    if not path.exists(wav_filename):
        print('не найден:', wav_filename)

    else:
        AUDIO_FILE = path.join(path.dirname(
            path.realpath(__file__)), wav_filename)

        m_result = ''
        # use the audio file as the audio source
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            m_result = r.recognize_google(audio, language='ru-RU')
        except sr.UnknownValueError:
            m_result = "Google Speech Recognition could not understand audio"            
        except sr.RequestError as e:
            m_result = "Could not request results from Google Speech Recognition service; {0}".format(e)
    
    return m_result

file_name = r"tmp\20210227_135213_test.m4a"
# file_name = r"tmp\AUD-20220518-WA0000.m4a"

# 11111111111111111
# wf = convert_wav(file_name)
# res = Recognize(wf)
# print('(G):',res)

# 22222222222222222222222



