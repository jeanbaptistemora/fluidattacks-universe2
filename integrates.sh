#!/bin/bash
integrates/container/build.sh
integrates/container/start.sh
ansible-playbook alg/main.yml -i alg/provision/hosts --vault-password-file ~/.vault.txt

