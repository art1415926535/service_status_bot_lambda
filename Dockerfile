FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /bot
WORKDIR /bot
COPY . /bot/

RUN pip3 install -r requirements.txt

CMD python3 main.py
