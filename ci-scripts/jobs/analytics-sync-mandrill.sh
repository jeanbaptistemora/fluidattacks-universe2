#!/usr/bin/env bash

analytics_sync_mandrill() {

  # Sync analytics with Mandrill

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . toolbox/others.sh

  aws_login

  sops_env secrets-production.yaml default \
    analytics_auth_mandrill \
    analytics_auth_redshift

  pip3 install \
    analytics/singer/streamer_mandrill \
    analytics/singer/tap_json \
    analytics/singer/target_redshift

  echo "$analytics_auth_mandrill" > /stream_secret.json
  echo "$analytics_auth_redshift" > /target_secret.json

  streamer-mandrill --auth /stream_secret.json > mandrill.jsonstream
  cat mandrill.jsonstream \
    | tap-json --date-formats '%Y-%m-%d %H:%M:%S,%Y-%m-%d %H:%M:%S.%f' \
    > mandrill.singer
  cat mandrill.singer \
    | target-redshift --auth /target_secret.json \
    --drop-schema --schema-name 'mandrill'
  rm -rf /stream_secret.json /target_secret.json
}

analytics_sync_mandrill
