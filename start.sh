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
    ls -l servers/${server}/scripts
    servers/${server}/scripts/start.sh
    ansible-playbook servers/${server}/main.yml -i servers/${server}/hosts --vault-password-file ~/.vault.txt
done
