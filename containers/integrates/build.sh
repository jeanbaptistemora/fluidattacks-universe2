#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="integrates"

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
docker build -t registry.gitlab.com/fluidsignal/${SERVER}:base containers/${SERVER}

