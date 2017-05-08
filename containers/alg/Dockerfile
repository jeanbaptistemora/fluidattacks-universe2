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
               ansible


# Agrega el playbook
ADD main.yml /root/

# Agrega las variables
ADD vars* /root/vars

# Agrega el vault
ADD .vault.txt /root/

# Cambia al directorio root
WORKDIR /root/

# Ejecuta el ansible
RUN ansible-playbook main.yml --vault-password-file .vault.txt


# Make port 80 and 443 available to the world outside this container
EXPOSE 80
EXPOSE 443

# Copia los archivos que harán parte de la imagen
COPY entry.sh /

# Primer comando que se ejecutara
ENTRYPOINT ["/entry.sh"]

# Primer comando
CMD /usr/sbin/apache2ctl -D FOREGROUND
