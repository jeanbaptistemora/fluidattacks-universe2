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
    servers/${server}/scripts/start.sh
    ansible-playbook servers/${server}/main.yml -i servers/${server}/hosts --vault-password-file ~/.vault.txt
done

#Crea cron para backup de exams
command="ansible-playbook /root/fluid-serves/servers/exams/scripts/backup.yml -i /root/fluid-serves/servers/exams/hosts --vault-password-file ~/.vault.txt"
job="00 01 * * * $command"
cat <(fgrep -i -v "$command" <(crontab -l)) <(echo "$job") | crontab -
