#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# importar entorno
source /root/fluid-serves/servers/alg/vars/env.sh

# Mensaje de inicio
echo "---### Iniciando contenedor."

# iniciar contenedor si no ha iniciado
if [ -z $(docker ps -q -f name="$SERVICE") ]; then
  echo "Contenedor no ha iniciado, iniciando contenedor..."

  # Crear dinamicamente claves de acceso al contenedor
  # La ruta de configuración SSH tambien esta parametrizado en test/setup/hosts
  mkdir -p ~/.ssh/
  cp "$PROJECT_DIR"/vars/ssh_config ~/.ssh/config.facont."$SERVICE"
  echo -e "y\n" | ssh-keygen -b 2048 -t rsa -f ~/.ssh/"$SERVICE"_facont_id_rsa -q -N ""

  docker run \
		--detach \
		--name="$SERVICE" \
		-p 22000:22 \
		-p 80:80 \
 		-p 443:443 \
		-e SSH_KEY="$(cat ~/.ssh/"$SERVICE"_facont_id_rsa.pub)" \
		fluidsignal/fluidserves:latest

  echo "Esperando que el puerto 22000 de SSH este abierto."
  until nc -z $IP 22000; do : sleep 0.2; done
  echo "Puerto SSH (22000) abierto en contenedor."
else
  echo "Contenedor ya inicio, reutilizando contenedor."
fi
