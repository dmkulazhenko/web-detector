FROM python:3.9-buster


RUN mkdir /app
WORKDIR /app


COPY web/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn
