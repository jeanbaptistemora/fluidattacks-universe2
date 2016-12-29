#!/bin/bash
asserts/container/build.sh
asserts/container/start.sh
ansible-playbook asserts/main.yml -i asserts/provision/hosts --vault-password-file ~/.vault.txt

