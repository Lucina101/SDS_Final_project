FROM python:3.7-buster


COPY . /root/frontend
WORKDIR /root/frontend

RUN pip install -r requirements.txt

EXPOSE 3000
CMD  python main.py
