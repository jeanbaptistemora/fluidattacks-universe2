#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

SERVER="vpn"

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
cp ~/.vault.txt containers/${SERVER}/
docker build -t registry.gitlab.com/fluidsignal/serves/${SERVER}:base containers/${SERVER}
rm containers/${SERVER}/.vault.txt
