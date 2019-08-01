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
        libssl-dev \
        libffi-dev \
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
        gcc \
        libc6-dev \
        make \
        docker-ce \
        git \
        unzip \
        libxml2-dev \
        libxslt1-dev && \
    python3 -m pip install -U  setuptools \
        wheel \
        pip && \
    python3 -m pip install -U \
        wheel \
        setuptools \
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
    gem install overcommit && \
    dpkg --clear-avail && \
    apt-get clean
