#!/bin/bash
alg/container/build.sh
alg/container/start.sh
ansible-playbook alg/main.yml -i alg/provision/hosts --vault-password-file ~/.vault.txt

