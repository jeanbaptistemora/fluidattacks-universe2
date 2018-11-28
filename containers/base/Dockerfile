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
        jq \
        libffi-dev \
        libssl-dev \
        make \
        netbase \
        python \
        python-dev \
        software-properties-common \
        sudo \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
        && python get-pip.py \
        && rm get-pip.py \
    && pip install ansible \
    && curl -LsSo vaultenv.deb https://github.com/channable/vaultenv/releases/download/v0.9.0/vaultenv-0-9-0.deb \
        && dpkg -i vaultenv.deb \
        && rm vaultenv.deb

WORKDIR /root/
