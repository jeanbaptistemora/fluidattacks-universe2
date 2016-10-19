#!/bin/bash

# habilitar depuración
if [ -n "$VERBOSE" ]; then
  set -x
fi

# Mensaje de inicio
echo "---### Pruebas básicas sobre contenedor."

# Salir inmediatamente si algun comando retorna diferente de cero.
set -e

# Probando conexion SSH
ssh -F ~/.ssh/config.facont 127.0.0.1 -p 22000 -l alg \
    echo "Conexión SSH como usuario nonpriv al contenedor esta funcionando"
ssh -F ~/.ssh/config.facont 127.0.0.1 -p22000 -l root \
    echo "Conexión SSH como usuario root al contenedor esta funcionando"
