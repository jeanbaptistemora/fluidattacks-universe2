# Imagen base del ultimo linux estable de Debian (jessie)
FROM 205810638802.dkr.ecr.us-east-1.amazonaws.com/integrates:base

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ARG circle_branch

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva
ENV CIRCLE_BRANCH=$circle_branch
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Instala dependencias
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y software-properties-common sudo

# Agrega el playbook
ADD main.yml /root/
ADD patch_socialauth.py /root/

# Agrega las variables
ADD vars* /root/vars

# Agrega el vault
ADD .vault.txt /root/

# Cambia al directorio root
WORKDIR /root/

# Ejecuta el ansible
RUN ansible-playbook main.yml --vault-password-file .vault.txt

# Make port 80 and 443 available to the world outside this container
EXPOSE 443

# Primer comando
CMD service cron start && /usr/sbin/apache2ctl -D FOREGROUND
