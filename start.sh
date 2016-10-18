#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# Setup (ansible)
export PROJECT_DIR=$(git rev-parse --show-toplevel)
export ANSIBLE_HOSTS="$PROJECT_DIR"/config/hosts
export SERVICE="alg"
export IP=127.0.0.1

# Mensaje de inicio
echo "---### Compilando contenedor."

# construir la imagen
docker build -t alg "$PROJECT_DIR"

# Verificacion existencia imagenes
docker images 

# Mensaje de inicio
echo "---### Iniciando contenedor."

# iniciar contenedor si no ha iniciado
if [ -z $(docker ps -q -f name="$SERVICE") ]; then

#  echo "Contenedor no ha iniciado, iniciando contenedor..."	 

  # Crear dinamicamente claves de acceso al contenedor
  # La ruta de configuración SSH tambien esta parametrizado en test/setup/hosts
  mkdir -p ~/.ssh/
  cp "$PROJECT_DIR"/config/ssh_config ~/.ssh/config.facont
  echo -e "y\n" | ssh-keygen -b 2048 -t rsa -f ~/.ssh/facont_id_rsa -q -N ""

  docker run \
		--detach \
		--name="$SERVICE" \
		--hostname="$SERVICE" \
        -p 22000:22 \
        -p 443:443 \
        -p 80:80 \
		-e SSH_KEY="$(cat ~/.ssh/facont_id_rsa.pub)" \
		alg

  echo "Esperando que el puerto 22000 de SSH este abierto."
  until nc -z $IP 22000; do : sleep 5; done
  echo "Puerto SSH (22000) abierto en contenedor."
else
  echo "Contenedor ya inicio, reutilizando contenedor."
fi

# Configurar variables Ansible
