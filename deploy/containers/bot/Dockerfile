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
RUN gpg --recv-key --keyserver pgp.key-server.io 93C4A3FD7BB9C367 \
    && gpg --export --armor 93C4A3FD7BB9C367 | apt-key add -

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y software-properties-common sudo

# Agrega el playbook
ADD common/main.yml /root/
ADD common/patch_socialauth.py /root/

# Agrega las variables
ADD common/vars* /root/vars

# Agrega el vault
ADD .vault.txt /root/

# Cambia al directorio root
WORKDIR /root/

# Ejecuta el ansible
RUN ansible-playbook main.yml --vault-password-file .vault.txt

# Primer comando
CMD /usr/src/app/manage.py bot
