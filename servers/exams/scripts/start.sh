#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# importar entorno
#source $(git rev-parse --show-toplevel)/servers/exams/vars/env.sh
source servers/exams/vars/env.sh

# Mensaje de inicio
echo "---### Iniciando contenedor."

# iniciar contenedor si no ha iniciado
if [ -z $(docker ps -q -f name="$SERVICE") ]; then
  echo "Contenedor no ha iniciado, iniciando contenedor..."

  docker run \
		--detach \
		--name="$SERVICE" \
		-p 8080:80 \
		fluidsignal/fluidserves$SERVICE:latest

else
  echo "Contenedor ya inicio, reutilizando contenedor."
fi
