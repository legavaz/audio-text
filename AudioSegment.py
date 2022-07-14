
from itertools import count
from tracemalloc import start
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from threading import Thread, Timer
import threading
import time

# кастомные
import at_utility


# блок переменных
time_cat = 60


# Блок Функциональности
def audio_to_text(file_name: str):

    fn_1 = at_utility.Convert_wav(file_name)
    fn_short = at_utility.file_name_short(fn_1)

    print("Сегментация: ", fn_short)
    audio_segment = AudioSegment.from_wav(fn_1)

    # Нормализация аудио
    print("Нормализация:", fn_short)
    audio_segment = at_utility.match_target_amplitude(audio_segment, -20.0)

    # дорожки непрерывного звука
    print("Анализ тишины пропусков:", fn_short)
    # fn_json = r'tmp\json\temp'+fn_short+".json"
    # nonsilent_data = at_utility.load_json(fn_json)
    # if nonsilent_data == None:
    nonsilent_data = detect_nonsilent(
            audio_segment, min_silence_len=500, silence_thresh=-20, seek_step=1)
    #     at_utility.write_json(fn_json, nonsilent_data)

    # Формируем нарезки аудио
    count = 1
    start = 0
    end = 0
    file_arr = []
    for chunks in nonsilent_data:
        end = chunks[1]
        len_sec = (end - start)/1000

        if len_sec > time_cat:
            # сохраняем очередной отрезок
            at_utility.slice_audio(
                audio_segment, fn_short, start, end, count, file_arr)

            count = count+1
            start = chunks[1]

    # сохраняем последний отрезок
    at_utility.slice_audio(audio_segment, fn_short,
                           start, end, count, file_arr)

    # распознование файла
    mText = ''
    m_array_th = []
    if len(file_arr) > 1:
        countThred = threading.active_count()
        for track in file_arr:
            th = Thread(target=at_utility.recognize_write, args=(track,))
            th.start()
            m_array_th.append(th)

        print('Запущено потоков:', len(m_array_th))
        for th in m_array_th:
            th.join()

    else:
        at_utility.recognize_write(file_arr[0])

    # Удаляем файлы
    at_utility.delete_file(fn_1)

    return file_arr


# Блок тестирования
if __name__ == "__main__":

    fn_1 = r"tmp\ОришакАнтон.m4a"
    
    rezult = audio_to_text(fn_1)
    for track in rezult:
            print(track['res'])

    
