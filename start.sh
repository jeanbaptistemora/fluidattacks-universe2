#!/bin/bash

# Construcción contenedor por defecto

SERVERS="alg exams integrates"

# Crea los contenedores dependiendo del server
for server in ${SERVERS}; do
    containers/${server}/build.sh
    servers/${server}/scripts/start.sh
done
