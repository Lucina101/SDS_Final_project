FROM python:3.7-buster

RUN apt-get update -y
RUN apt install redis -y
RUN service redis-server start

COPY . /root/backend
WORKDIR /root/backend


RUN pip install -r requirements.txt

EXPOSE 1323
CMD  python main.py
