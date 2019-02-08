#!/usr/bin/env bash
set -e

echo "${ANSIBLE_VAULT}" > vault.txt

apt-get update
apt-get install --no-install-recommends -y \
  iptables \
  openvpn

ansible-playbook main.yml --vault-password-file vault.txt

rm -rf \
  /root/* \
  /var/lib/apt/lists/*
