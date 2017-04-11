#!/bin/bash

# Creación instancia AWS

servers/host/scripts/create_infrastructure.sh

# Configuracion servidor

servers/host/scripts/deploy.sh
servers/host/scripts/start.sh
