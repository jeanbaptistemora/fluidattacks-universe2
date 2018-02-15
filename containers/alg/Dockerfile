# Imagen base del ultimo linux estable de Debian (jessie)
FROM registry.gitlab.com/fluidsignal/serves:base

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva

# Instalar software-properties y sudo
RUN apt-get update && apt-get upgrade -y && apt-get install -y --force-yes software-properties-common sudo

# Agrega el playbook
ADD main.yml /root/

# Agrega las variables
ADD vars* /root/vars

# Agrega el vault
ADD .vault.txt /root/

# Cambia al directorio root
WORKDIR /root/

# Ejecuta el ansible
RUN ansible-playbook main.yml --vault-password-file .vault.txt \
    && curl -L https://toolbelt.treasuredata.com/sh/install-debian-jessie-td-agent2.sh | sh \
    && rm /etc/td-agent/td-agent.conf \
    && mv vars/fluent.conf /etc/td-agent/td-agent.conf \
    && rm /etc/init.d/td-agent \
    && mv vars/td-agent /etc/init.d/td-agent && chmod 0755 /etc/init.d/td-agent  \
    && mv vars/out_rollbar.rb /etc/td-agent/plugin/ \
    && /usr/sbin/td-agent-gem install eventmachine em-http-request fluent-plugin-rewrite-tag-filter


# Make port 80 and 443 available to the world outside this container
EXPOSE 80
EXPOSE 443

# Primer comando
CMD /etc/init.d/td-agent restart \
&& /usr/sbin/apache2ctl -D FOREGROUND
