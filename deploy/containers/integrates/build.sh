#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="integrates"
MASTER_BRANCH="master"
CIRCLE_BRANCH=$1

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
cp ~/.vault.txt deploy/containers/integrates/
ln -sf ../common
sudo docker build --build-arg circle_branch=$CIRCLE_BRANCH -t 205810638802.dkr.ecr.us-east-1.amazonaws.com/integrates:$MASTER_BRANCH deploy/containers/integrates
rm deploy/containers/integrates/.vault.txt
docker run --detach --name="$SERVER" -p 8000:443 205810638802.dkr.ecr.us-east-1.amazonaws.com/integrates:$MASTER_BRANCH
rm common
