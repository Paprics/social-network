FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y

RUN mkdir /app

WORKDIR /app

COPY dev-requirements.txt .

COPY ./commands ./commands

RUN python -m pip install --upgrade pip && pip install -r dev-requirements.txt

COPY ./src ./src

CMD ["bash"]