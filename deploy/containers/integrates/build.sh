#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="integrates"
CI_COMMIT_REF_NAME=$1
FI_GITLAB_LOGIN=$2
FI_GITLAB_PASSWORD=$3
FI_DRIVE_AUTHORIZATION=$4
FI_DOCUMENTROOT=$5
FI_SSL_CERT=$6
FI_SSL_KEY=$7
FI_DRIVE_AUTHORIZATION_CLIENT=$8

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
cp -a ../common .
docker build --no-cache --build-arg ci_commit_ref_name="$CI_COMMIT_REF_NAME" \
            --build-arg gitlab_login="$FI_GITLAB_LOGIN" \
            --build-arg gitlab_password="$FI_GITLAB_PASSWORD" \
            --build-arg drive_authorization="$FI_DRIVE_AUTHORIZATION" \
            --build-arg documentroot="$FI_DOCUMENTROOT" \
            --build-arg ssl_cert="$FI_SSL_CERT" \
            --build-arg ssl_key="$FI_SSL_KEY" \
            --build-arg drive_authorization_client="$FI_DRIVE_AUTHORIZATION_CLIENT" \
						-t registry.gitlab.com/fluidsignal/integrates:base .
rm -rf common
