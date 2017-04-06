#!/bin/bash

# Creación instancia AWS

python servers/host/scripts/create_instance2.py

# Configuracion servidor

servers/host/scripts/deploy.sh
servers/host/scripts/start.sh
