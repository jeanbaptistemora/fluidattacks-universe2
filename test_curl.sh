#!/bin/bash

IP_FILE="/tmp/instance_ip.txt"
IP=$(cat ${IP_FILE})

curl http://${IP}
curl http://${IP}:8080/admin/index.php
