
from itertools import count
from tracemalloc import start
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


import convert_Google

print("конвертация")
# fn_1 = r"tmp\conversation_pause.m4a"
fn_1 = r"tmp\AUD-20220518-WA0000.wav"
fn_wav = convert_Google.convert_wav(fn_1)

print("сегментация: ", fn_wav)
audio_segment = AudioSegment.from_wav(fn_wav)

#Print detected non-silent chunks, which in our case would be spoken words.
nonsilent_data = detect_nonsilent(audio_segment, min_silence_len=500, silence_thresh=-20, seek_step=1)

print("вывод")

start_time = 0
count = 0
for chunks in nonsilent_data:    
    print( chunks)
    
    count = count+1    
    fn_count=r'tmp\new_'+str(count)+'_'+str(round((chunks[0]-start_time)/1000))+'_sec.wav'
    as_cut = audio_segment[start_time:chunks[0]]    
    as_cut.export(fn_count, format='wav')
    start_time = chunks[1]


