#!/usr/bin/env bash

analytics_sync_intercom() {

  # Sync analytics with Intercom

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . toolbox/others.sh

  aws_login

  new_sops_env secrets-prod.yaml default \
    analytics_auth_intercom \
    analytics_auth_redshift

  pip3 install \
    analytics/singer/streamer_intercom \
    analytics/singer/tap_json \
    analytics/singer/target_redshift

  echo "$analytics_auth_intercom" > /stream_secret.json
  echo "$analytics_auth_redshift" > /target_secret.json

  streamer-intercom --auth /stream_secret.json > .jsonstream
  cat .jsonstream | tap-json --enable-timestamps > .singer
  cat .singer | \
    target-redshift \
    --auth /target_secret.json --drop-schema --schema-name 'intercom'
  rm -rf /stream_secret.json /target_secret.json
}

analytics_sync_intercom
