#!/bin/bash

USERNAME="core"
IP_FILE="/tmp/instance_ip.txt"
HOST_TEMPLATE="servers/host/vars/docker_host.template"
HOST_FILE="docker_host"
KEY_FILE="/tmp/FLUIDServes_Dynamic.pem"

IP=$(cat ${IP_FILE})

sed -e "s/__ip_address__/${IP}/g" ${HOST_TEMPLATE} > ${HOST_FILE}

echo "Esperando que el puerto 22 de SSH este abierto."
sleep 20
ssh-add ${KEY_FILE}
sudo scp -i ${KEY_FILE} "/tmp/.vault.txt" "${USERNAME}@${IP}:/home/${USERNAME}/"
scp -i ${KEY_FILE} "servers/host/scripts/install_python.sh" "${USERNAME}@${IP}:/home/${USERNAME}/"
python servers/host/scripts/install_python.py
