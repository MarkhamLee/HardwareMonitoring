FROM python:3.11-slim as build

RUN apt-get update -y && apt-get install -y gcc python3-dev libgpiod2

COPY requirements.txt main.py /
RUN pip install -r /requirements.txt

CMD python3 main.py