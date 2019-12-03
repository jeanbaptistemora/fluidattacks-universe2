#!/usr/bin/env bash

analytics_sync_ringcentral() {

  # Sync analytics with RingCentral

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
  . toolbox/others.sh

  aws_login

  sops_env secrets-production.yaml default \
    analytics_auth_ringcentral \
    analytics_auth_redshift

  pip3 install \
    analytics/singer/streamer_ringcentral \
    analytics/singer/tap_json \
    analytics/singer/target_redshift

  echo "$analytics_auth_ringcentral" > /stream_secret.json
  echo "$analytics_auth_redshift" > /target_secret.json

  streamer-ringcentral \
    --auth /stream_secret.json --sync-user --sync-calls > .jsonstream
  cat .jsonstream | tap-json > .singer
  cat .singer | \
    target-redshift \
    --auth /target_secret.json --drop-schema --schema-name 'ringcentral'
  rm -rf /stream_secret.json /target_secret.json
}

analytics_sync_ringcentral
