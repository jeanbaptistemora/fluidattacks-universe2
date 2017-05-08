#!/bin/bash

# Construcción contenedor por defecto

SERVERS="alg exams integrates"

# Crea los contenedores dependiendo el OS
for os in ${SERVERS}; do
    containers/${os}/build.sh
done

# Construye los servers
for server in ${SERVERS}; do
    servers/${server}/scripts/start.sh
done
