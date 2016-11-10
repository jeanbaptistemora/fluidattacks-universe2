#!/bin/bash
integrates/container/build.sh
integrates/container/start.sh
ansible-playbook integrates/main.yml -i integrates/provision/hosts --vault-password-file ~/.vault.txt

