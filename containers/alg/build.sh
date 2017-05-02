#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# Mensaje de inicio
echo "---### Compilando contenedor."

# construir la imagen
cp ~/.vault.txt containers/alg/
docker build -t fluidsignal/fluidservesalg:latest containers/alg
rm containers/alg/.vault.txt
