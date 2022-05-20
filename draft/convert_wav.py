from pydub import AudioSegment

f_in = r'tmp\20210227_135213.m4a'
f_out = r'tmp\20210227_135213.wav'

wav_audio = AudioSegment.from_file(f_in, format="m4a")

wav_audio.export(f_out, format="wav")    