#!/usr/bin/env bash

analytics_sync_zoho() {

  # Sync analytics with Zoho

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
  . toolbox/others.sh

  local email
  local token
  local space

  aws_login

  sops_env secrets-production.yaml default \
    analytics_zoho_email \
    analytics_zoho_token \
    analytics_zoho_space \
    analytics_auth_redshift \
    analytics_zoho_tables

  pip3 install --upgrade requests
  pip3 install \
    analytics/singer/tap_json \
    analytics/singer/target_redshift

  email="$analytics_zoho_email"
  token="$analytics_zoho_token"
  space="$analytics_zoho_space"

  echo "$analytics_auth_redshift" > secret.json

  echo -e "$analytics_zoho_tables" | while read -r table
  do
    ./analytics/singer/converter_zoho_csv.py \
      --email "$email" --token "$token" \
      --space "$space" --table "$table" --target "$table" && \
    ./analytics/singer/streamer_csv.py "$table" >> .jsonstream;
  done

  cat .jsonstream | tap-json --date-formats '%Y-%m-%d %H:%M:%S' > .singer
  cat .singer | target-redshift --schema-name 'zoho' \
    --auth secret.json \
    --drop-schema
  rm -rf secret.json
  unset email token space
}

analytics_sync_zoho
