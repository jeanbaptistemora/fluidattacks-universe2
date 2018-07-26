#!/usr/bin/env bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="alg"

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
echo 'web_bucket: '"$FW_S3_BUCKET" >> containers/alg/vars/vars.yml
docker build --no-cache \
    --build-arg vault_pass="$ANSIBLE_VAULT" \
	-t "registry.gitlab.com/fluidsignal/serves/alg/dev:$CI_COMMIT_SHA" \
	containers/${SERVER}
