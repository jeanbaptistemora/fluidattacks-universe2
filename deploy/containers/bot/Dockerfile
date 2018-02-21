# Imagen base del ultimo linux estable de Debian (jessie-slim)
FROM registry.gitlab.com/fluidsignal/integrates:deps

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluidattacks.com>

ARG ci_commit_ref_name
ARG gitlab_login
ARG gitlab_password
ARG drive_authorization
ARG documentroot
ARG ssl_cert
ARG ssl_key
ARG drive_authorization_client

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva
ENV CI_COMMIT_REF_NAME=$ci_commit_ref_name
ENV FI_GITLAB_LOGIN=$gitlab_login
ENV FI_GITLAB_PASSWORD=$gitlab_password
ENV FI_DRIVE_AUTHORIZATION=$drive_authorization
ENV FI_DOCUMENTROOT=$documentroot
ENV FI_SSL_CERT=$ssl_cert
ENV FI_SSL_KEY=$ssl_key
ENV FI_DRIVE_AUTHORIZATION_CLIENT=$drive_authorization_client
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Agrega las variables
ADD common/vars* /root/vars

# Cambia al directorio root
WORKDIR /root/

# Remover archivo index, clonar repositorio Integrates $CI_COMMIT_REF_NAME y ejecuta el ansible
RUN rm -r /var/www/html \
    && git clone -b $CI_COMMIT_REF_NAME https://$FI_GITLAB_LOGIN:$FI_GITLAB_PASSWORD@gitlab.com/fluidsignal/integrates.git  /usr/src/app \
    && gem install asciidoctor-pdf --pre \
    && mkdir /usr/src/app/app/documentator/images  \
    && mkdir /usr/src/app/app/documentator/tpls  \
    && mkdir /usr/src/app/app/documentator/results  \
    && chown -R www-data:www-data  /usr/src/app/app/documentator \
    && chmod -R 0744 /usr/src/app/app/documentator \
    && python /usr/src/app/deploy/containers/common/vars/render.py \
    && chown -R www-data:www-data $FI_DOCUMENTROOT \
    && a2dismod python \
    && a2enmod ssl \
    && cd /usr/src/app/app/assets && npm install && cd \
    && echo "$FI_SSL_CERT" | base64 -di > "/etc/ssl/certs/fluidla.crt" \
    && echo "$FI_SSL_KEY" | base64 -di > "/etc/ssl/private/fluidla.key"

# Primer comando
CMD env > /etc/environment  \
&& a2ensite integrates-ssl.conf \
&& a2ensite 000-default.conf \
&& /usr/src/app/manage.py makemigrations \
&& /usr/src/app/manage.py migrate \
&& /usr/src/app/manage.py crontab add \
&& service cron start \
&& /usr/src/app/manage.py bot
