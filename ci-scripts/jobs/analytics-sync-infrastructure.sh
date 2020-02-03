#!/usr/bin/env bash

analytics_sync_infrastructure() {

  # Sync analytics with infrastructure

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . toolbox/others.sh

  aws_login

  new_sops_env secrets-prod.yaml default \
    analytics_auth_infra \
    analytics_auth_redshift

  pip3 install \
    analytics/singer/streamer_infrastructure \
    analytics/singer/tap_json \
    analytics/singer/target_redshift

  echo "$analytics_auth_infra" > /stream_secret.json
  echo "$analytics_auth_redshift" > /target_secret.json

  streamer-infrastructure --auth /stream_secret.json > infra.jsonstream
  cat infra.jsonstream | tap-json > infra.singer
  cat infra.singer | \
    target-redshift \
    --auth /target_secret.json --drop-schema --schema-name 'infrastructure'
  rm -rf /stream_secret.json /target_secret.json
}

analytics_sync_infrastructure
