# Imagen base del ultimo linux estable de Debian (jessie)
FROM registry.gitlab.com/fluidsignal/serves:base

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva

ARG vault_pass
# Instalar software-properties y sudo
RUN apt-get update && apt-get upgrade -y --force-yes && apt-get install -y --force-yes software-properties-common sudo

# Agrega el playbook
ADD main.yml /root/

# Agrega las variables
ADD vars* /root/vars

# Cambia al directorio root
WORKDIR /root/

# Ejecuta el ansible
RUN echo "$vault_pass" > .vault.txt \
    && ansible-playbook main.yml --vault-password-file .vault.txt \
    && rm -rf .vault.txt \
        main.yml \
        vars

# Make port 80 and 443 available to the world outside this container
EXPOSE 80

# Primer comando
CMD /usr/sbin/apache2ctl -D FOREGROUND && php /var/www/html/admin/cli/purge_caches.php
