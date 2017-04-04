#!/bin/bash

# Construcción contenedor por defecto

CONTAINER_OS="debian ubuntu"
SERVERS="alg exams integrates"

# Crea los contenedores dependiendo el OS
for os in ${CONTAINER_OS}; do
    containers/${os}/build.sh
done

# Construye los servers
for server in ${SERVERS}; do
    echo "Ruta master"
    pwd
    echo "ls servers/${server}/vars"
    ls -l /root/fluid-serves/servers/${server}/vars/
    echo "ls servers/${server}/scripts"
    ls -l /root/fluid-serves/servers/${server}/scripts
    sh /root/fluid-serves/servers/${server}/scripts/start.sh
    ansible-playbook /root/fluid-serves/servers/${server}/main.yml -i /root/fluid-serves/servers/${server}/hosts --vault-password-file ~/.vault.txt
done
