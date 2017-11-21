# Imagen base del ultimo linux estable de Debian (jessie)
FROM registry.gitlab.com/fluidsignal/integrates:deps

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ARG ci_commit_ref_name

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva
ENV CI_COMMIT_REF_NAME=$ci_commit_ref_name
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Instala dependencias
RUN gpg --recv-key --keyserver pgp.key-server.io 93C4A3FD7BB9C367 \
    && gpg --export --armor 93C4A3FD7BB9C367 | apt-key add -

# Instalar software-properties y sudo
RUN apt-get update && apt-get install -y software-properties-common sudo

# Agregar ansible repo
RUN sudo echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" | sudo tee -a /etc/apt/sources.list

# Instala dependencias
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --force-yes\
               ansible

# Agrega el playbook
RUN pwd && ls -la

ADD common/main.yml /root/
ADD common/patch_socialauth.py /root/

# Agrega las variables
ADD common/vars* /root/vars

# Agrega el vault
ADD .vault.txt /root/

# Cambia al directorio root
WORKDIR /root/

RUN pwd && ls -la

# Ejecuta el ansible
RUN ansible-playbook main.yml --vault-password-file .vault.txt

# Make port 80 and 443 available to the world outside this container
EXPOSE 443

# Primer comando
CMD service cron start && /usr/sbin/apache2ctl -D FOREGROUND
