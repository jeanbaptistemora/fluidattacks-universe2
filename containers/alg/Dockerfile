# Imagen base del ultimo linux estable de Debian (jessie)
FROM debian:jessie

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva

# Instalar software-properties y sudo
RUN apt-get update && apt-get install -y software-properties-common sudo

# Agregar ansible repo
RUN sudo echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" | sudo tee -a /etc/apt/sources.list

# Instala dependencias
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

# Instala req de pip
RUN pip install -U --force pip setuptools

# Habilitar modulos necesarios de Apache
RUN a2enmod rewrite ssl proxy_http substitute headers

# Creando configuración Apache
ADD vars/apache2.j2 /etc/apache2/apache2.conf
RUN chmod 0644 etc/apache2/apache2.conf

# Creando sitio por defecto
ADD vars/000-default.j2 /etc/apache2/sites-enabled/000-default.conf
RUN chmod 0644 etc/apache2/sites-enabled/000-default.conf

# Creando fluid.la
ADD vars/fluid.la.j2 /etc/apache2/sites-enabled/fluid.la
RUN chmod 0644 /etc/apache2/sites-enabled/fluid.la

# Creando www.fluid.la
ADD vars/www.fluid.la.j2 /etc/apache2/sites-enabled/www.fluid.la
RUN chmod 0644 /etc/apache2/sites-enabled/www.fluid.la

# Creando www.fluidsignal.com
ADD vars/www.fluidsignal.com.j2 /etc/apache2/sites-enabled/www.fluidsignal.com
RUN chmod 0644 /etc/apache2/sites-enabled/www.fluidsignal.com

# Creando sitio ssl
ADD vars/defaultssl.j2 /etc/apache2/sites-enabled/default-ssl
RUN chmod 0644 /etc/apache2/sites-enabled/default-ssl

# Agrega configuracion a hosts
ADD vars/hosts.j2 /etc/hosts

# Retirar index
RUN rm /var/www/html/index.html

# Agrega el playbook
ADD main.yml /root/

# Agrega las variables
ADD vars* /root/vars

# Agrega el vault
ADD .vault.txt /root/

# Cambia al directorio root
WORKDIR /root

# Ejecuta el ansible
RUN ansible-playbook main.yml --vault-password-file .vault.txt


# Make port 80 and 443 available to the world outside this container
EXPOSE 80
EXPOSE 443
