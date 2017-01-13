#!/bin/bash

IP_FILE="/tmp/instance_ip.txt"
HOST_TEMPLATE="docker_host.template"
HOST_FILE="docker_host"

IP=$(cat ${IP_FILE})

sed -e "s/__ip_address__/${IP}/g" ${HOST_TEMPLATE} > ${HOST_FILE}
