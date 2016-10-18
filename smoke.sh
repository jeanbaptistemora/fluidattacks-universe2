#!/bin/bash

# Exportar variables
export ANSIBLE_HOSTS="$PROJECT_DIR"/config/hosts

# Probar configuracion ansible 
ansible container -m ping -i config/hosts

# Ejecutar playbook
ansible-playbook main.yml -i config/hosts
