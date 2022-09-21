FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get -y upgrade

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
