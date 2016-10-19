#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Mensaje de inicio
echo "---### Pruebas básicas sobre contenedor."

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# importar entorno (SSH_AUTH_SOCK reseteado)
source $(git rev-parse --show-toplevel)/env.sh

# Probando conexion SSH
ssh -p22000 ${VERBOSE:+-vvv} -F ~/.ssh/config.facont "$IP" -l nonpriv \
    echo "Conexión SSH como usuario nonpriv al contenedor esta funcionando"
ssh -p22000 ${VERBOSE:+-vvv} -F ~/.ssh/config.facont "$IP" -l root \
    echo "Conexión SSH como usuario root al contenedor esta funcionando"
