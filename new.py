import speech_recognition as sr
from pydub import AudioSegment
from os import path

file_name = r"tmp\20210227_135213.m4a"
# file_name = r"tmp\AUD-20220518-WA0000.m4a"


if not path.exists(file_name):
    print('не найден:',file_name)  

else:  
    
    wav_filename = file_name+'.wav'
    print('1) конвертация файла',wav_filename)
    track = AudioSegment.from_file(file_name, "m4a")

    track.export(wav_filename, format='wav')

    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), wav_filename)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google result:>>> " + r.recognize_google(audio,language='ru-RU'))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
