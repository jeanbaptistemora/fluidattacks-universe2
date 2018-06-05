#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="exams"

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
docker build --no-cache \
    --build-arg vault_pass="$VAULT" \
	-t "registry.gitlab.com/fluidsignal/serves/exams/dev:$CI_COMMIT_SHA" \
	containers/${SERVER}
