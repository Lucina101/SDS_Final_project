FROM python:3.7-alpine3.15

COPY . .

RUN apk update && apk add bash

RUN pip install -r requirements.txt

EXPOSE 3000

cmd python main.py

