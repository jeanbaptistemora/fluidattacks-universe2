# Imagen base del ultimo linux estable de Debian (jessie)
FROM debian:jessie

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva

RUN apt-get update && apt-get install -y software-properties-common sudo
RUN sudo echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" | sudo tee -a /etc/apt/sources.list

# Instala SSH, Python y SUDO para administracion por Ansible
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --force-yes\
               sudo \
               python \
               apache2 \
               ansible \
               curl \
               python-pip \
               python-dev \
               libffi-dev \
               libssl-dev \
               g++ \
               gcc

# Install any needed packages specified in requirements.txt
RUN pip install -U --force pip setuptools

# Habilitar modulos necesarios de Apache
RUN a2enmod rewrite ssl proxy_http substitute headers


ADD vars/apache2.j2 /etc/apache2/apache2.conf
RUN chmod 0644 etc/apache2/apache2.conf

ADD vars/000-default.j2 /etc/apache2/sites-enabled/000-default.conf
RUN chmod 0644 etc/apache2/sites-enabled/000-default.conf

ADD vars/fluid.la.j2 /etc/apache2/sites-enabled/fluid.la
RUN chmod 0644 /etc/apache2/sites-enabled/fluid.la

ADD vars/www.fluid.la.j2 /etc/apache2/sites-enabled/www.fluid.la
RUN chmod 0644 /etc/apache2/sites-enabled/www.fluid.la

ADD vars/www.fluidsignal.com.j2 /etc/apache2/sites-enabled/www.fluidsignal.com
RUN chmod 0644 /etc/apache2/sites-enabled/www.fluidsignal.com

ADD vars/defaultssl.j2 /etc/apache2/sites-enabled/default-ssl
RUN chmod 0644 /etc/apache2/sites-enabled/default-ssl


RUN rm /var/www/html/index.html

ADD main.yml /root/
ADD vars /root/
ADD .vault.txt /root/

WORKDIR /root
RUN ansible-playbook main.yml -i localhost --vault-password-file .vault.txt


# Make port 80 and 443 available to the world outside this container
EXPOSE 80
EXPOSE 443
