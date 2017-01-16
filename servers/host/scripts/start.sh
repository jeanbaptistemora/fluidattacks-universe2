#!/bin/bash
ansible-playbook -i docker_host servers/host/main.yml --vault-password-file ~/.vault.txt
