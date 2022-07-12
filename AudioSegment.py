
from itertools import count
from tracemalloc import start
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

# кастомные
import at_utility


# Блок тестирования
if __name__ == "__main__":
    # print("конвертация")
    fn_1 = r"tmp\conversation_pause.wav"
    fn_1 = r"tmp\AUD-20220518-WA0000.wav"
    # fn_1 = at_utility.Convert_wav(fn_1)

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
                            'end': end, 'count': count})
            start = chunks[1]

    # сохраняем последний отрезок
    print('сохранение посл', start, end)
    len_sec = round((end - start)/1000)
    fn_count = r'tmp\1\tr_'+fn_short+'_' + \
        str(count+1)+'_'+str(len_sec)+'_sec.wav'
    at_utility.Cut_AS(audio_segment, start, end, fn_count)
    file_arr.append({'file': fn_count, 'start': start,
                    'end': end, 'count': count+1})

    # распознование файла
    mText = ''
    for track in file_arr:
        res = at_utility.Recognize(track['file'])
        mText = mText+'('+str(track['count'])+'):'+str(track['start'] /
                                                       1000)+'-'+str(track['end']/1000)+' сек: '+res+'\n'

    print('(G):\n', mText)
