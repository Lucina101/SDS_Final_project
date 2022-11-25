FROM python:3.7-buster

RUN apt-get update -y
RUN apt install redis -y

COPY . /root/backend
WORKDIR /root/backend

RUN pip install -r requirements.txt

EXPOSE 1324

CMD  ["python /root/backend/main.py"]
