FROM ubuntu:14.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt install -y \
	nano \
	apache2 \
	git python python-pip \
	libapache2-mod-wsgi libapache2-mod-python \
	libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk \
	libxml2-dev libxslt1-dev python-dev \
	&& pip install django requests openpyxl python-pptx pyyaml
COPY clone.sh /var/www/clone.sh
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
