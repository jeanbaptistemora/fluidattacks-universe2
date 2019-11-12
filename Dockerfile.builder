FROM debian:buster-slim

WORKDIR /usr/src/asserts

RUN apt-get -o Acquire::Check-Valid-Until=false update -qq && \
    apt-get install -qqy --no-install-recommends \
        curl \
        apt-transport-https \
        ca-certificates \
        gpg gpg-agent && \
    dpkg --clear-avail && \
    apt-get clean

RUN echo "deb [arch=amd64] https://download.docker.com/linux/debian stretch stable" > /etc/apt/sources.list.d/docker.list

RUN curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add -

RUN apt-get -o Acquire::Check-Valid-Until=false update -qq && \
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
        libmagic-dev \
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
        wget \
        unzip \
        libxml2-dev \
        libxslt1-dev \
        libxmlsec1-dev \
        freetds-dev \
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
        chromedriver==2.24.1 \
    wget https://github.com/webnicer/chrome-downloads/raw/master/x64.deb/google-chrome-stable_72.0.3626.121-1_amd64.deb && \
            apt install -y ./google-chrome-stable_72.0.3626.121-1_amd64.deb && \
            rm -f ./google-chrome-stable_72.0.3626.121-1_amd64.deb && \
        wget https://chromedriver.storage.googleapis.com/72.0.3626.69/chromedriver_linux64.zip && \
            unzip chromedriver_linux64.zip -d /usr/bin && \
            rm -f chromedriver_linux64.zip && \
            chmod +x /usr/bin/chromedriver && \
    gem install rake overcommit && \
    dpkg --clear-avail && \
    apt-get clean


# How to update selenium, chromedriver and chrome safely:
#   1. Pick your chrome version from: https://github.com/webnicer/chrome-downloads/tree/master/x64.deb
#       we pick 72.0.3626.121 because is the highest available at alpine:
#     2. take the first 3 parts, it means 72.0.3626
#     3. go here: https://chromedriver.storage.googleapis.com/LATEST_RELEASE_72.0.3626
#   4. Pick your version of chromedriver from text in body of (3) (it means 72.0.3626.69):
#     5. go here: https://chromedriver.storage.googleapis.com/index.html?path=72.0.3626.69/
#     6. install that
