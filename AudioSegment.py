
from itertools import count
from tracemalloc import start
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from threading import Thread, Timer
import threading
import time

# кастомные
import at_utility

# Блок Функциональности
def audio_to_text(file_name:str):
    # print("конвертация")

    fn_1 = at_utility.Convert_wav(file_name)
    fn_short = at_utility.file_name_short(fn_1)

    print("сегментация: ", fn_short)
    audio_segment = AudioSegment.from_wav(fn_1)

    # Нормализация аудио
    print("Нормализация")
    audio_segment = at_utility.match_target_amplitude(audio_segment, -20.0)

    # дорожки непрерывного звука
    print("Анализ тишины пропусков")
    fn_json = r'tmp\1\temp'+fn_short+".json"
    nonsilent_data = at_utility.load_json(fn_json)
    if nonsilent_data == None:
        nonsilent_data = detect_nonsilent(
            audio_segment, min_silence_len=500, silence_thresh=-20, seek_step=1)
        at_utility.write_json(fn_json, nonsilent_data)

    # Формируем нарезки аудио
    print("вывод")
    count = 0
    len_sec_300 = 0
    start = 0
    end = 0
    file_arr = []
    for chunks in nonsilent_data:

        end = chunks[1]
        len_sec_300 = (end - start)/1000
        if len_sec_300 > 180:

            # сохраняем отрезок
            print('сохранение пром', start, end)
            count = count+1
            len_sec = round((end - start)/1000)
            fn_count = r'tmp\1\tr_'+fn_short+'_' + \
                str(count)+'_'+str(len_sec)+'_sec.wav'
            at_utility.Cut_AS(audio_segment, start, end, fn_count)

            file_arr.append({'file': fn_count, 'start': start,
                            'end': end, 'count': count, 'res': ''})
            start = chunks[1]

    # сохраняем последний отрезок
    print('сохранение посл', start, end)
    len_sec = round((end - start)/1000)
    fn_count = r'tmp\1\tr_'+fn_short+'_' + \
        str(count+1)+'_'+str(len_sec)+'_sec.wav'
    at_utility.Cut_AS(audio_segment, start, end, fn_count)
    file_arr.append({'file': fn_count, 'start': start,
                     'end': end, 'count': count, 'res': ''})

    # распознование файла
    mText = ''
    if len(file_arr)>1:
        countThred = threading.active_count()
        for track in file_arr:
            th = Thread(target=at_utility.recognize_write, args=(track,))
            th.start()

        while threading.active_count() > countThred:
            print('в работе: ', threading.active_count(),'потока(ов)', 'в резерве:', countThred)
            time.sleep(3)
    else:
        at_utility.recognize_write(file_arr[0])

    for track in file_arr:
        mText = mText + track['res']

    return mText


# Блок тестирования
if __name__ == "__main__":
    
    fn_1 = r"tmp\Богословская.m4a"
    # fn_1 = r"tmp\AUD-20220518-WA0000.wav"
    
    rezult = audio_to_text(fn_1)
    print(rezult)
    
    
