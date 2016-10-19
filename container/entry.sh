#!/bin/bash

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# La clave publica para conectarse es pasada por parametros
if [ -z "${SSH_KEY}" ]; then
  echo "Indique su clave publica en la variable de entorno SSH_KEY"
  echo "Ejemplo: $ docker run ... -e SSH_KEY=\"$(cat ~/.ssh/id_rsa.pub)\" ... "
  exit -1
fi

# Creando el usuario no privilegiado
USER=nonpriv
echo "Creando usuario no privilegiado $USER"
useradd "$USER"
passwd -d "$USER"
usermod -s /bin/bash "$USER"
mkdir /home/"$USER"

# Almancenando claves publicas y definiendo permisos requeridos
for DIR in /root /home/"$USER"; do
  echo "Adicionando clave publica SSH a $DIR"
  mkdir -p "$DIR"/.ssh
  chmod go-rwx "$DIR"/.ssh
  echo "$SSH_KEY" > "$DIR"/.ssh/authorized_keys
  chmod go-rw "$DIR"/.ssh/authorized_keys
done

# Confirmando permisos en archivos del usuario no privilegiado
chown -R "$USER":"$USER" /home/"$USER"/

# Otorgandole permisos de SUDO a $USER sin clave para ansible --become
echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/"$USER"

# Imprimiendo banner de inicio del server
echo "FLUIDAsserts - Docker Ansible Base server (SSH, Python, SUDO)"

# Configurando conexión SSH para Ansible (en CI falla con PAM)
sed -i "s/UsePAM yes/UsePAM no/" /etc/ssh/sshd_config

# Iniciando servidor ssh
exec /usr/sbin/sshd -D -e -f /etc/ssh/sshd_config

# Basado en: https://hub.docker.com/r/krlmlr/debian-ssh/
