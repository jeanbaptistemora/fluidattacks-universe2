#!/bin/bash

# Construcción contenedor por defecto

SERVERS="alg exams integrates"

# Crea los contenedores y construye los servers
for os in ${SERVERS}; do
    containers/${os}/build.sh
    servers/${server}/scripts/start.sh
done
