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

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y software-properties-common sudo curl

#Instala Nodejs
RUN curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -    

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