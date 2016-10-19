#!/bin/bash

# Exportar variables
#export ANSIBLE_HOSTS="$PROJECT_DIR"/config/hosts

# Probar configuracion ansible 
ansible container -m ping -vvvv

# Ejecutar playbook
ansible-playbook main.yml -vvvv
