#!/bin/bash

USERNAME="core"
IP_FILE="/tmp/instance_ip.txt"
HOST_TEMPLATE="servers/host/vars/docker_host.template"
HOST_FILE="docker_host"
KEY_FILE="/tmp/FLUIDServes_Dynamic.pem"

IP=$(cat ${IP_FILE})

sed -e "s/__ip_address__/${IP}/g" ${HOST_TEMPLATE} > ${HOST_FILE}

ssh-add ${KEY_FILE}
echo "Esperando que el puerto 22 de SSH este abierto."
until nc -z $IP 22; do : sleep 0.2; done
sudo scp "~/.vault.txt" "${USERNAME}@${IP}:/home/${USERNAME}/"
scp "servers/host/scripts/install_python.sh" "${USERNAME}@${IP}:/home/${USERNAME}/"
python servers/host/scripts/install_python.py
