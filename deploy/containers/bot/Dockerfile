# Imagen base del ultimo linux estable de Debian (jessie-slim)
FROM registry.gitlab.com/fluidsignal/integrates:deps

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ARG ci_commit_ref_name
ARG aws_region
ARG aws_access_key_dynamodb
ARG aws_secret_key_dynamodb
ARG secret_key_env
ARG db_user
ARG db_passwd
ARG db_host
ARG db_port
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

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva
ENV CI_COMMIT_REF_NAME=$ci_commit_ref_name
ENV AWS_REGION=$aws_region
ENV AWS_ACCESS_KEY_DYNAMODB=$aws_access_key_dynamodb
ENV AWS_SECRET_KEY_DYNAMODB=$aws_secret_key_dynamodb
ENV SECRET_KEY_ENV=$secret_key_env
ENV DB_USER=$db_user
ENV DB_PASSWD=$db_passwd
ENV DB_HOST=$db_host
ENV DB_PORT=$db_port
ENV AWS_ACCESS_KEY=$aws_access_key
ENV AWS_SECRET=$aws_secret
ENV MIXPANEL=$mixpanel
ENV INTERCOM=$intercom
ENV INTERCOM_SECURE_KEY_ENV=$intercom_secure_key
ENV SLACK_BOT=$slack_bot
ENV GOOGLE_OAUTH2_KEY=$google_oauth2_key
ENV GOOGLE_OAUTH2_SECRET=$google_oauth2_secret
ENV AZUREAD_OAUTH2_KEY=$azured_oauth2_key
ENV AZUREAD_OAUTH2_SECRET=$azured_oauth2_secret
ENV DRIVE_AUTHORIZATION=$drive_authorization
ENV FORMSTACK_TOKENS=$formstack_tokens
ENV AWS_OUTPUT=$aws_output
ENV DEBUG_ENV=$debug_env
ENV FI_ROLLBAR_ACCESS_TOKEN=$rollbar_access_token
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

# Ejecuta el ansible
RUN ansible-playbook main.yml --vault-password-file .vault.txt

# Primer comando
CMD /usr/src/app/manage.py bot
