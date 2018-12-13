FROM debian:stretch

# update system and packages
RUN apt-get update -q
RUN apt-get upgrade -q -y

# install base packages
RUN apt-get install -y apt-utils
RUN apt-get install -y locales
RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev
RUN apt-get install -y curl
RUN curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
RUN python3 /tmp/get-pip.py
RUN python3 -m pip install psutil

# set the locale to english UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
RUN locale-gen en_US.UTF-8
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

# install singer targets
RUN python3 -m pip install target-stitch

# copy authentication files
COPY auth_formstack.json    /auth/auth_formstack.json
COPY auth_stitchdata.json   /auth/auth_stitchdata.json

# deploy singer taps
COPY singer                 /singer
RUN python3 -m pip install  /singer/tap_formstack
RUN mkdir logs
