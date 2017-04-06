#!/bin/bash

IP_FILE="/tmp/instance_ip.txt"
HOST_TEMPLATE="servers/host/vars/docker_host.template"
HOST_FILE="docker_host"
KEY_FILE="/tmp/FLUIDServes_Dynamic.pem"

IP=$(cat ${IP_FILE})

sed -e "s/__ip_address__/${IP}/g" ${HOST_TEMPLATE} > ${HOST_FILE}

ssh-add ${KEY_FILE} && scp "/root/.vault.txt" "admin@${IP}:/home/admin/"
