#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="integrates"
CI_COMMIT_REF_NAME=$1
FI_AWS_DYNAMODB_ACCESS_KEY=$2
FI_AWS_DYNAMODB_SECRET_KEY=$3
FI_DJANGO_SECRET_KEY=$4
FI_DB_USER=$5
FI_DB_PASSWD=$6
FI_DB_HOST=$7
FI_AWS_CLOUDWATCH_ACCESS_KEY=$8
FI_AWS_CLOUDWATCH_SECRET_KEY=$9
FI_MIXPANEL_API_TOKEN=${10}
FI_INTERCOM_APPID=${11}
FI_INTERCOM_SECURE_KEY=${12}
FI_SLACK_BOT_TOKEN=${13}
FI_GOOGLE_OAUTH2_KEY=${14}
FI_GOOGLE_OAUTH2_SECRET=${15}
FI_AZUREAD_OAUTH2_KEY=${16}
FI_AZUREAD_OAUTH2_SECRET=${17}
FI_DRIVE_AUTHORIZATION=${18}
FI_FORMSTACK_TOKENS=${19}
FI_AWS_OUTPUT=${20}
FI_DEBUG=${21}
FI_ROLLBAR_ACCESS_TOKEN=${22}
FI_GITLAB_MACHINE=${23}
FI_GITLAB_LOGIN=${24}
FI_GITLAB_PASSWORD=${25}
FI_DOCUMENTROOT=${26}
# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
cp ../.vault.txt .
cp -a ../common .
docker build --no-cache --build-arg ci_commit_ref_name="$CI_COMMIT_REF_NAME" \
						--build-arg aws_access_key_dynamodb="$FI_AWS_DYNAMODB_ACCESS_KEY" \
						--build-arg aws_secret_key_dynamodb="$FI_AWS_DYNAMODB_SECRET_KEY" \
            --build-arg secret_key_env="$FI_DJANGO_SECRET_KEY" \
            --build-arg db_user="$FI_DB_USER" \
            --build-arg db_passwd="$FI_DB_PASSWD" \
            --build-arg db_host="$FI_DB_HOST" \
						--build-arg aws_access_key="$FI_AWS_CLOUDWATCH_ACCESS_KEY" \
						--build-arg aws_secret="$FI_AWS_CLOUDWATCH_SECRET_KEY" \
            --build-arg mixpanel="$FI_MIXPANEL_API_TOKEN" \
						--build-arg intercom="$FI_INTERCOM_APPID" \
						--build-arg intercom_secure_key="$FI_INTERCOM_SECURE_KEY" \
            --build-arg slack_bot="$FI_SLACK_BOT_TOKEN" \
            --build-arg google_oauth2_key="$FI_GOOGLE_OAUTH2_KEY" \
						--build-arg google_oauth2_secret="$FI_GOOGLE_OAUTH2_SECRET" \
						--build-arg azured_oauth2_key="$FI_AZUREAD_OAUTH2_KEY" \
            --build-arg azured_oauth2_secret="$FI_AZUREAD_OAUTH2_SECRET" \
            --build-arg drive_authorization="$FI_DRIVE_AUTHORIZATION" \
            --build-arg formstack_tokens="$FI_FORMSTACK_TOKENS" \
            --build-arg aws_output="$FI_AWS_OUTPUT" \
            --build-arg debug_env="$FI_DEBUG" \
            --build-arg rollbar_access_token="$FI_ROLLBAR_ACCESS_TOKEN" \
            --build-arg gitlab_machine="$FI_GITLAB_MACHINE" \
            --build-arg gitlab_login="$FI_GITLAB_LOGIN" \
            --build-arg gitlab_password="$FI_GITLAB_PASSWORD" \
            --build-arg documentroot="$FI_DOCUMENTROOT" \
						-t registry.gitlab.com/fluidsignal/integrates:base .
rm -rf common
