#!/bin/bash

# Definir lista de hosts
cat config/hosts >> /etc/ansible/hosts
cat /etc/ansible/hosts

# Probar configuracion ansible 
ansible container -m ping -vvvv

# Ejecutar playbook
ansible-playbook main.yml -vvvv
