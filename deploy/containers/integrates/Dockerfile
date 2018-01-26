# Imagen base del ultimo linux estable de Debian (jessie-slim)
FROM registry.gitlab.com/fluidsignal/integrates:deps

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ARG ci_commit_ref_name
ARG aws_access_key_dynamodb
ARG aws_secret_key_dynamodb
ARG secret_key_env
ARG db_user
ARG db_passwd
ARG db_host
ARG aws_access_key
ARG aws_secret
ARG mixpanel
ARG intercom
ARG intercom_secure_key
ARG slack_bot
ARG google_oauth2_key
ARG google_oauth2_secret
ARG azured_oauth2_key
ARG azured_oauth2_secret
ARG drive_authorization
ARG formstack_tokens
ARG aws_output
ARG debug_env
ARG rollbar_access_token
ARG gitlab_machine
ARG gitlab_login
ARG gitlab_password
ARG documentroot

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva
ENV CI_COMMIT_REF_NAME=$ci_commit_ref_name
ENV FI_AWS_DYNAMODB_ACCESS_KEY=$aws_access_key_dynamodb
ENV FI_AWS_DYNAMODB_SECRET_KEY=$aws_secret_key_dynamodb
ENV FI_DJANGO_SECRET_KEY=$secret_key_env
ENV FI_DB_USER=$db_user
ENV FI_DB_PASSWD=$db_passwd
ENV FI_DB_HOST=$db_host
ENV FI_AWS_CLOUDWATCH_ACCESS_KEY=$aws_access_key
ENV FI_AWS_CLOUDWATCH_SECRET_KEY=$aws_secret
ENV FI_MIXPANEL_API_TOKEN=$mixpanel
ENV FI_INTERCOM_APPID=$intercom
ENV FI_INTERCOM_SECURE_KEY=$intercom_secure_key
ENV FI_SLACK_BOT_TOKEN=$slack_bot
ENV FI_GOOGLE_OAUTH2_KEY=$google_oauth2_key
ENV FI_GOOGLE_OAUTH2_SECRET=$google_oauth2_secret
ENV FI_AZUREAD_OAUTH2_KEY=$azured_oauth2_key
ENV FI_AZUREAD_OAUTH2_SECRET=$azured_oauth2_secret
ENV FI_DRIVE_AUTHORIZATION=$drive_authorization
ENV FI_FORMSTACK_TOKENS=$formstack_tokens
ENV FI_AWS_OUTPUT=$aws_output
ENV FI_DEBUG=$debug_env
ENV FI_ROLLBAR_ACCESS_TOKEN=$rollbar_access_token
ENV FI_GITLAB_MACHINE=$gitlab_machine
ENV FI_GITLAB_LOGIN=$gitlab_login
ENV FI_GITLAB_PASSWORD=$gitlab_password
ENV FI_DOCUMENTROOT=$documentroot
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Agrega el playbook
ADD common/main.yml /root/

# Agrega las variables
ADD common/vars* /root/vars

# Agrega el vault
ADD .vault.txt /root/

# Cambia al directorio root
WORKDIR /root/

# Remover archivo index, clonar repositorio Integrates $CI_COMMIT_REF_NAME y ejecuta el ansible
RUN rm -r /var/www/html \
    && git clone -b $CI_COMMIT_REF_NAME https://$FI_GITLAB_LOGIN:$FI_GITLAB_PASSWORD@gitlab.com/fluidsignal/integrates.git  /usr/src/app \
    && gem install asciidoctor-pdf --pre \
    && ls /usr/src/app/app/documentator \
    && chown -R www-data:www-data  /usr/src/app/app/documentator \
    && chmod -R 0744 /usr/src/app/app/documentator  \
    && chown -R www-data:www-data $FI_DOCUMENTROOT \
    && /usr/src/app/manage.py makemigrations \
    && /usr/src/app/manage.py migrate \
    && /usr/src/app/manage.py crontab add \
    && a2dismod python \
    && a2enmod ssl \
    && ansible-playbook main.yml --vault-password-file .vault.txt

# Make port 80 and 443 available to the world outside this container
EXPOSE 443

# Primer comando
CMD service cron start && /usr/sbin/apache2ctl -D FOREGROUND
