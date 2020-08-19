FROM python:3.8-slim-buster as forces

RUN apt update

RUN apt -y install git

COPY . /pakage

WORKDIR /pakage

RUN pip install .

FROM forces as break_build

RUN pip install boto3

WORKDIR /forces

COPY break_build.py .

ENTRYPOINT ["python3", "/forces/break_build.py"]
