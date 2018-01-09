# Imagen base del ultimo linux estable de Debian (jessie)
FROM debian:jessie-slim

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Instala dependencias
RUN gpg --recv-key --keyserver pgp.key-server.io 93C4A3FD7BB9C367 \
    && gpg --export --armor 93C4A3FD7BB9C367 | apt-key add -

# Instalar software-properties y sudo
RUN apt-get update && apt-get install -y software-properties-common sudo

# Agregar ansible repo
RUN sudo echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" | sudo tee -a /etc/apt/sources.list
RUN curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -

# Instala dependencias
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --force-yes\
               git ansible curl \
               python-dev python-pip apache2 \
               python-setuptools python-tk nodejs \
               build-essential python-numpy python-scipy \
               python-matplotlib ruby npm \
               liblcms2-dev libwebp-dev tcl8.6-dev \
               tk8.6-dev libxml2 libxml2-dev \
               libxslt1-dev libapache2-mod-wsgi libtiff5-dev \
               zlib1g-dev libfreetype6-dev libapache2-mod-python \
               libmysqlclient-dev cron autoconf \
               bison build-essential libssl-dev \
               libyaml-dev libreadline6-dev libncurses5-dev \
               libffi-dev libgdbm3 libgdbm-dev nodejs

# Instala dependencias pip
ADD requirements.txt /root/
RUN pip install --upgrade cffi
RUN pip install --upgrade setuptools
RUN pip install --upgrade pip
RUN pip install --upgrade -r /root/requirements.txt

# SocialAuth Patch
ADD patch_socialauth.py /root/
RUN python /root/patch_socialauth.py

# Cambia al directorio root
WORKDIR /root/
