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

# construir la imagen
cp ../.vault.txt .
cp -a ../common .
docker build --no-cache --build-arg ci_commit_ref_name="$CI_COMMIT_REF_NAME" \
						--build-arg aws_region="$AWS_REGION" \
						--build-arg aws_access_key_dynamodb="$AWS_ACCESS_KEY_DYNAMODB" \
						--build-arg aws_secret_key_dynamodb="$AWS_SECRET_KEY_DYNAMODB" \
						-t registry.gitlab.com/fluidsignal/integrates/bot:base .
rm .vault.txt
rm -rf common