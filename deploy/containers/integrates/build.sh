#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="integrates"
CI_COMMIT_REF_NAME=$1

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
cp ../.vault.txt .
cp -a ../common .
docker build --no-cache --build-arg ci_commit_ref_name=$CI_COMMIT_REF_NAME -t registry.gitlab.com/fluidsignal/integrates:base .
rm -rf common
