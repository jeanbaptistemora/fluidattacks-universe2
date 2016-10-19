#!/bin/bash

# Exportar variables
export ANSIBLE_HOSTS="$PROJECT_DIR"/config/hosts

# Probar configuracion ansible 
ansible container -m ping -i config/hosts -vvvv

# Ejecutar playbook
ansible-playbook main.yml -i config/hosts -vvvv
