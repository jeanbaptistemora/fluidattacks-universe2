#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# La clave publica para conectarse es pasada por parametros
if [ -z "${SSH_KEY}" ]; then
  echo "Indique su clave publica en la variable de entorno SSH_KEY"
  echo "Ejemplo: $ docker run ... -e SSH_KEY=\"$(cat ~/.ssh/id_rsa.pub)\" ... "
  exit -1
fi

# Almancenando claves publicas y definiendo permisos requeridos
  echo "Adicionando clave publica SSH a /root"
  mkdir -p ~/.ssh
  chmod go-rwx ~/.ssh
  echo "$SSH_KEY" > ~/.ssh/authorized_keys
  chmod go-rw ~/.ssh/authorized_keys

# Imprimiendo banner de inicio del server
echo "FLUID-serves Docker Ansible Base server"

# Configurando conexión SSH para Ansible (en CI falla con PAM)
sed -i "s/UsePAM yes/UsePAM no/" /etc/ssh/sshd_config

# Iniciando servidor ssh
exec /usr/sbin/sshd -D -e -f /etc/ssh/sshd_config

# Basado en: https://hub.docker.com/r/krlmlr/debian-ssh/
