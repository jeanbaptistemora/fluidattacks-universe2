FROM debian:jessie

LABEL mantainer="engineering@fluidattacks.com"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install --no-install-recommends -y \
        apache2 \
        curl \
        g++ \
        gcc \
        libffi-dev \
        libssl-dev \
        python \
        python-dev \
        software-properties-common \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
        && python get-pip.py \
        && rm get-pip.py \
    && pip install ansible

WORKDIR /root/
