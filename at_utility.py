
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import json
import os
import time

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
    with open(file_name, 'w+') as wf:
        json.dump(data, wf)


def delete_file(file_name: str):
    if os.path.isfile(file_name):
        os.remove(file_name)
        print('удален: ', file_name)


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


def format_time(sec):    
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %=3600
    min = sec // 60
    sec %=60

    if hour > 0:
        time_string = "%02d:%02d:%02d" % (hour,min,sec)
    else:
        time_string = "%02d:%02d" % (min,sec)
    
    return time_string

def recognize_write(track):
    res = Recognize(track['file'])
    time_start = format_time(track['start']/1000)
    time_end = format_time(track['end']/1000)

    mText = '('+str(track['count'])+') ' + \
        str(time_start)+'-'+str(time_end)+' '+res+'\n'
    track['res'] = mText
    delete_file(track['file'])


def slice_audio(audio_segment, fn_short, start, end, count, file_arr):
    print('сохранение', start, end)
    len_sec = round((end - start)/1000)
    fn_count = r'tmp\tracks\tr_'+fn_short+'_' + \
        str(count)+'_'+str(len_sec)+'_sec.wav'
    Cut_AS(audio_segment, start, end, fn_count)

    file_arr.append({'file': fn_count, 'start': start,
                     'end': end, 'count': count, 'res': ''})


# Блок тестирования
if __name__ == "__main__":
    # file_name = r"tmp\20210227_135213_test.m4a"
    # file_name = r"tmp\AUD-20220518-WA0000.m4a"

    # перекодировка в wav
    # wf = convert_wav(file_name)

    # распознование
    wf = r'tmp\new_59_414_sec.wav'
    res = Recognize(wf)

    # Результат
    print('(G):', res)
