#!/usr/bin/env bash
set -e

echo 'web_bucket: '"${FW_S3_BUCKET}" >> vars/vars.yml
echo "${FLUID_TLS_KEY}" | base64 -d >> vars/fluid.key
echo "${FLUIDATTACKS_TLS_CERT}" | base64 -d >> vars/fluidattacks.crt
echo "${FLUIDLA_TLS_CERT}" | base64 -d >> vars/fluidla.crt

ansible-playbook main.yml

curl -L https://toolbelt.treasuredata.com/sh/install-debian-jessie-td-agent2.sh | sh
rm /etc/td-agent/td-agent.conf
mv vars/fluent.conf /etc/td-agent/td-agent.conf
rm /etc/init.d/td-agent
mv vars/td-agent /etc/init.d/td-agent
chmod 0755 /etc/init.d/td-agent
mv vars/out_rollbar.rb /etc/td-agent/plugin/
/usr/sbin/td-agent-gem install eventmachine em-http-request fluent-plugin-rewrite-tag-filter

rm -rf /root/* /var/lib/apt/lists/*
