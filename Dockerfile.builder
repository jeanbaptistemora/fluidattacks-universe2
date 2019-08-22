FROM debian:buster-slim

WORKDIR /usr/src/asserts

RUN apt-get update -qq && \
    apt-get install -qqy --no-install-recommends \
        curl \
        apt-transport-https \
        ca-certificates \
        gpg gpg-agent && \
    dpkg --clear-avail && \
    apt-get clean

RUN echo "deb [arch=amd64] https://download.docker.com/linux/debian stretch stable" > /etc/apt/sources.list.d/docker.list

RUN curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add -

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-dev \
        python3-pip \
        python3-lxml \
        python3-wheel \
        apt-utils \
        build-essential \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        scons \
        python3-virtualenv \
        sed \
        grep \
        gawk \
        lsb-release \
        netcat-traditional \
        python3-setuptools \
        tesseract-ocr \
        ruby \
        ruby2.5-dev \
        libffi-dev \
        pkg-config \
        docker-ce \
        git \
        unzip \
        libxml2-dev \
        libxslt1-dev \
        libxmlsec1-dev \
        libfreetype6-dev && \
    python3 -m pip install -U  setuptools \
        wheel \
        pip && \
    python3 -m pip install -U \
        tox \
        tox-pyenv \
        pylint \
        flake8 \
        yamllint \
        pycodestyle \
        pydocstyle \
        pep257 \
        twine \
        mandrill-really-maintained \
        certifi \
        gitdb2 \
        smmap2 \
        gitpython \
        pyflakes \
        requirements-detector \
        mypy && \
    gem install rake overcommit && \
    dpkg --clear-avail && \
    apt-get clean
