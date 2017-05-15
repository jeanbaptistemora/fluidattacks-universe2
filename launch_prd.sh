#!/bin/bash

# Creación instancia AWS

aws s3 cp s3://fluidpersistent/serves/stackname.txt /tmp/stackname_old.txt

servers/host/scripts/create_infrastructure.sh

# Configuracion servidor

servers/host/scripts/deploy.sh
servers/host/scripts/start.sh
