# Last stable Debian base image (jessie).
FROM debian:jessie-slim

# Doubts about the image in question.
MAINTAINER FLUID Engineering Team <engineering@fluidattacks.com>

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Add server key.
RUN gpg --recv-key --keyserver pgp.key-server.io 93C4A3FD7BB9C367 \
    && gpg --export --armor 93C4A3FD7BB9C367 | apt-key add -

# Install software-properties and sudo.
RUN apt-get update && apt-get install -y software-properties-common sudo

# Add ansible repository.
RUN sudo echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" | sudo tee -a /etc/apt/sources.list

# Install dependencies.
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --force-yes\
               git ansible curl \
               python-dev apache2 \
               python-setuptools python-tk \
               build-essential python-numpy python-scipy \
               python-matplotlib ruby \
               liblcms2-dev libwebp-dev tcl8.6-dev \
               tk8.6-dev libxml2 libxml2-dev \
               libxslt1-dev libapache2-mod-wsgi libtiff5-dev \
               zlib1g-dev libfreetype6-dev libapache2-mod-python \
               libmysqlclient-dev cron autoconf \
               bison libssl-dev libyaml-dev \
               libreadline6-dev libncurses5-dev \
               libffi-dev libgdbm3 libgdbm-dev ruby-dev

# Install nodejs.
RUN curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --force-yes\
               nodejs

# Install vaultenv
RUN curl -LsSo vaultenv.deb https://github.com/channable/vaultenv/releases/download/v0.7.1/vaultenv-0.7.1.deb \
    && dpkg -i vaultenv.deb \
    && rm vaultenv.deb

# Install Torus
RUN DISTRO=$(lsb_release -i | awk '{print tolower($3)}') \
    && CODENAME=$(lsb_release -c | awk '{print $2}') \
    && sudo echo "deb https://get.torus.sh/$DISTRO/ $CODENAME main" | sudo tee -a /etc/apt/sources.list.d/torus.list \
    && apt-get update \
    && apt-get install --allow-unauthenticated -y torus \
    && gem install asciidoctor-pdf --pre 

# Install dependencies and pip.
ADD requirements.txt /root/
ADD package.json /root/
RUN easy_install pip
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r /root/requirements.txt --ignore-installed \
    && cd /root/ && npm install -g \
    && cp --symbolic-link /root/node_modules/.bin/* /usr/local/bin

# SocialAuth Patch.
ADD patch_socialauth.py /root/
RUN python /root/patch_socialauth.py


# Change root directory.
WORKDIR /root/