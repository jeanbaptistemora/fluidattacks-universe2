#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="bot"
MASTER_BRANCH="master"
CIRCLE_BRANCH=$1

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
cp ~/.vault.txt .
cp -a ../common .
sudo docker build --build-arg circle_branch=$CIRCLE_BRANCH -t 205810638802.dkr.ecr.us-east-1.amazonaws.com/integratesbot:$MASTER_BRANCH .
rm .vault.txt
rm -rf common
docker run --detach --name="$SERVER" 205810638802.dkr.ecr.us-east-1.amazonaws.com/integratesbot:$MASTER_BRANCH
