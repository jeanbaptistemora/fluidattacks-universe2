#!/usr/bin/env bash
set -e

echo "${ANSIBLE_VAULT}" > vault.txt

apt-get update
apt-get install --no-install-recommends -y \
  cron \
  git \
  php5 \
  php5-curl \
  php5-gd \
  php5-intl \
  php5-mysql \
  php5-xmlrpc \
  python-mysqldb \
  unzip

ansible-playbook main.yml --vault-password-file vault.txt

rm -rf \
  /root/* \
  /var/lib/apt/lists/*
