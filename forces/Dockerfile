FROM python:3.8-slim-buster as base

RUN apt update

RUN apt -y install git

COPY . /pakage

WORKDIR /pakage

RUN pip install .

FROM base as complete

ENTRYPOINT [ "forces" ]
