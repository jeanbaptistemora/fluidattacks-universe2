#!/bin/bash

# Construcción contenedor por defecto 
containers/build.sh

# Inicio contenedor ALG
servers/alg/scripts/start.sh
ansible-playbook servers/alg/main.yml -i servers/alg/hosts --vault-password-file ~/.vault.txt

# Inicio contenedor Exams
servers/exams/scripts/start.sh
ansible-playbook servers/exams/main.yml -i servers/exams/hosts --vault-password-file ~/.vault.txt

# Inicio contenedor Integrates
containers/integrates/build.sh
servers/integrates/scripts/start.sh
ansible-playbook servers/integrates/main.yml -i servers/integrates/hosts --vault-password-file ~/.vault.txt



