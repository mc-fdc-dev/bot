FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y ffmpeg

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD ["python3", "main.py"]
