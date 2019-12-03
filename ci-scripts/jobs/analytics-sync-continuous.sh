#!/usr/bin/env bash

analytics_sync_continuous() {

  # Sync analytics with continuous

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
  . toolbox/others.sh

  local GITLAB_USER
  local GITLAB_PASS

  aws_login

  sops_env secrets-production.yaml default \
    analytics_gitlab_user \
    analytics_gitlab_token \
    analytics_auth_redshift

  pip3 install \
    analytics/singer/tap_json
    analytics/singer/target_redshift

  cd analytics/continuous

  GITLAB_USER="$analytics_gitlab_user"
  GITLAB_PASS="$analytics_gitlab_token"
  echo "$analytics_auth_redshift" > /target_secret.json

  git clone --depth 1 --single-branch \
    "https://$GITLAB_USER:$GITLAB_PASS@gitlab.com/fluidattacks/continuous.git"

  ./streamer_toe.py > .jsonstream
  cat .jsonstream | tap-json > .singer
  cat .singer | target-redshift \
    --auth /target_secret.json \
    --drop-schema \
    --schema-name continuous_toe

  unset GITLAB_USER GITLAB_PASS
  rm -rf /target_secret.json
}

analytics_sync_continuous
