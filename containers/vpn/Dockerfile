# Imagen base del ultimo linux estable de Debian (jessie)
FROM 205810638802.dkr.ecr.us-east-1.amazonaws.com/serves:base

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva

# Instalar software-properties y sudo
RUN apt-get update && apt-get upgrade -y && apt-get install -y software-properties-common sudo

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

# Make port 1194 available to the world outside this container
EXPOSE 443

# Script de inicio
CMD run
