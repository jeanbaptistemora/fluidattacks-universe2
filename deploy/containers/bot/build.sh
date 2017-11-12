#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# Mensaje de inicio
echo "---### [${SERVER}] Compilando contenedor."

# construir la imagen
cp ../.vault.txt .
cp -a ../common .
docker build -t registry.gitlab.com/fluidsignal/integrates/bot:base .
rm .vault.txt
rm -rf common
