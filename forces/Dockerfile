FROM python:3.8-slim-buster

RUN apt update

RUN apt -y install git

COPY . /pakage

WORKDIR /pakage

RUN pip install .

ENTRYPOINT [ "forces" ]
