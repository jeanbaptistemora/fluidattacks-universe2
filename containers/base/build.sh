#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="base"

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
docker build --no-cache \
	-t registry.gitlab.com/fluidsignal/serves/base/dev:${CI_COMMIT_SHA} \
	containers/${SERVER}
