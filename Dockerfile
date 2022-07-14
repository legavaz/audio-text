
FROM python:3.8-slim-buster

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pydub
RUN pip install SpeechRecognition
RUN pip install pytelegrambotapi
RUN apt-get update && apt-get install -y ffmpeg

ADD at_telebot.py /app/
ADD at_utility.py /app/
ADD AudioSegment.py /app/
ADD test.py /app/

CMD [ "python", "/app/at_telebot.py" ]