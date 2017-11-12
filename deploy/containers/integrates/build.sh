#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="integrates"
MASTER_BRANCH="master"

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
cp ../.vault.txt .
cp -a ../common .
docker build -t registry.gitlab.com/fluidsignal/integrates:base .
rm -rf common
#docker run --detach --name="$SERVER" -p 8000:443 205810638802.dkr.ecr.us-east-1.amazonaws.com/integrates:$MASTER_BRANCH
