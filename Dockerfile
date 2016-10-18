# Imagen base del ultimo linux estable de Debian (jessie)
FROM debian:jessie

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva

# Instala SSH, Python y SUDO para administracion por Ansible
RUN apt-get update \
    && apt-get install -y \
               vim \
               sudo \
               openssh-server \
    && mkdir -p /var/run/sshd

# Copia los archivos que harán parte de la imagen
COPY entry.sh /

# Primer comando que se ejecutara
ENTRYPOINT ["/entry.sh"]