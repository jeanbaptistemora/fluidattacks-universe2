#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."
CI_COMMIT_REF_NAME=$1
AWS_REGION=$2
AWS_ACCESS_KEY_DYNAMODB=$3
AWS_SECRET_KEY_DYNAMODB=$4
SECRET_KEY_ENV=$5
DB_USER=$6
DB_PASSWD=$7
DB_HOST=$8
DB_PORT=$9
AWS_ACCESS_KEY=${10}
AWS_SECRET=${11}
MIXPANEL=${12}
INTERCOM=${13}
INTERCOM_SECURE_KEY_ENV=${14}
SLACK_BOT=${15}
GOOGLE_OAUTH2_KEY=${16}
GOOGLE_OAUTH2_SECRET=${17}
AZUREAD_OAUTH2_KEY=${18}
AZUREAD_OAUTH2_SECRET=${19}
DRIVE_AUTHORIZATION=${20}
FORMSTACK_TOKENS=${21}
AWS_OUTPUT=${22}
DEBUG_ENV=${23}
# construir la imagen
cp ../.vault.txt .
cp -a ../common .
docker build --no-cache --build-arg ci_commit_ref_name="$CI_COMMIT_REF_NAME" \
						--build-arg aws_region="$AWS_REGION" \
						--build-arg aws_access_key_dynamodb="$AWS_ACCESS_KEY_DYNAMODB" \
						--build-arg aws_secret_key_dynamodb="$AWS_SECRET_KEY_DYNAMODB" \
            --build-arg secret_key_env="$SECRET_KEY_ENV" \
            --build-arg db_user="$DB_USER" \
            --build-arg db_passwd="$DB_PASSWD" \
            --build-arg db_host="$DB_HOST" \
            --build-arg db_port="$DB_PORT" \
            --build-arg aws_access_key="$AWS_ACCESS_KEY" \
            --build-arg aws_secret="$AWS_SECRET" \
            --build-arg mixpanel="$MIXPANEL" \
            --build-arg intercom="$INTERCOM" \
            --build-arg intercom_secure_key="$INTERCOM_SECURE_KEY_ENV" \
            --build-arg slack_bot="$SLACK_BOT" \
            --build-arg google_oauth2_key="$GOOGLE_OAUTH2_KEY" \
						--build-arg google_oauth2_secret="$GOOGLE_OAUTH2_SECRET" \
						--build-arg azured_oauth2_key="$AZUREAD_OAUTH2_KEY" \
            --build-arg azured_oauth2_secret="$AZUREAD_OAUTH2_SECRET" \
            --build-arg drive_authorization="$DRIVE_AUTHORIZATION" \
            --build-arg formstack_tokens="$FORMSTACK_TOKENS" \
            --build-arg aws_output="$AWS_OUTPUT" \
            --build-arg debug_env="$DEBUG_ENV" \
						-t registry.gitlab.com/fluidsignal/integrates/bot:base .
rm .vault.txt
rm -rf common
