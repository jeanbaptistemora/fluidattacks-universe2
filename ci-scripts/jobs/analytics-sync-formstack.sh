#!/usr/bin/env bash

analytics_sync_formstack() {

  # Sync analytics with Formstack

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
  . toolbox/others.sh

  aws_login

  sops_env secrets-production.yaml default \
    analytics_auth_redshift \
    analytics_auth_formstack

  mkdir /logs
  pip3 install \
    boto3 \
    analytics/singer/tap_formstack \
    analytics/singer/target_redshift

  echo "$analytics_auth_formstack" > /tap_secret.json
  echo "$analytics_auth_redshift" > /target_secret.json

  tap-formstack --auth /tap_secret.json --conf analytics/conf/formstack.json > formstack.singer

  cat formstack.singer | target-redshift --auth /target_secret.json --drop-schema --schema-name "formstack"

  rm -fr /tap_secret.json /target_secret.json
}

analytics_sync_formstack
