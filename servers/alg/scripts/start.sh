#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# importar entorno
source servers/alg/vars/env.sh

# Mensaje de inicio
echo "---### [$SERVICE] Iniciando contenedor."

# iniciar contenedor si no ha iniciado
if [ -z $(docker ps -q -f name="$SERVICE") ]; then
  echo "Contenedor no ha iniciado, iniciando contenedor..."

  docker run \
		--detach \
		--name="$SERVICE" \
		-p 80:80 \
 		-p 443:443 \
		fluidsignal/fluidserves$SERVICE:latest

else
  echo "Contenedor ya inicio, reutilizando contenedor."
fi
