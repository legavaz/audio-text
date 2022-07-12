
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import json

from os import path
import speech_recognition as sr


def Convert_wav(m_file_name: str):

    # находим расширение
    m_ext = m_file_name[len(m_file_name)-3:]
    # создаем новое имя файла с нужным расширением
    wav_filename = m_file_name.replace(m_ext, 'wav')

    print('Конвертация файла', m_file_name, '-->', wav_filename)

    if not path.exists(m_file_name):
        print('не найден:', m_file_name)
    else:

        track = AudioSegment.from_file(m_file_name, m_ext)

        track.export(wav_filename, format='wav')

    return wav_filename


def Recognize(wav_filename):
    print('Распознование файла', wav_filename)
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
            m_result = "Could not request results from Google Speech Recognition service; {0}".format(
                e)

    return m_result


def Cut_AS(audio_segment, start: int, end: int, fn_out: str):
    as_cut = audio_segment[start:end]
    as_cut.export(fn_out, format='wav')


# adjust target amplitude
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def write_json(file_name: str, data):
    with open(file_name, 'w') as wf:
        json.dump(data, wf)


def load_json(file_name: str):
    data = None
    if path.exists(file_name):
        with open(file_name, 'r') as rf:
            data = json.load(rf)

    return data


def file_name_short(fn: str):
    fn_short = ''
    if path.exists(fn):
        fn_short = path.splitext(path.basename(fn))[0]
    return fn_short


# Блок тестирования
if __name__ == "__main__":
    # file_name = r"tmp\20210227_135213_test.m4a"
    # file_name = r"tmp\AUD-20220518-WA0000.m4a"

    # перекодировка в wav
    # wf = convert_wav(file_name)

    # распознование
    wf = r'tmp\new_69_30_sec.wav'
    wf = r'tmp\new_66_251_sec.wav'
    wf = r'tmp\new_59_414_sec.wav'
    res = Recognize(wf)

    # Результат
    print('(G):', res)
