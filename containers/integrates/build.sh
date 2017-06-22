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
cp ~/.vault.txt containers/${SERVER}/
docker build -t 205810638802.dkr.ecr.us-east-1.amazonaws.com/${SERVER}:base containers/${SERVER}
rm containers/${SERVER}/.vault.txt

