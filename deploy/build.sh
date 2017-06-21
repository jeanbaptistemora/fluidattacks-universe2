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
cp ~/.vault.txt deploy/
sudo docker build -t technologyatfluid/integrates:$MASTER_BRANCH deploy/
rm deploy/.vault.txt
docker run --detach --name="$SERVER" -p 8000:443 technologyatfluid/integrates:$MASTER_BRANCH
