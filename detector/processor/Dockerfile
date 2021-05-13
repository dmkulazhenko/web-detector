FROM python:3.9-buster

RUN mkdir /app
WORKDIR /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY detector/processor/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
