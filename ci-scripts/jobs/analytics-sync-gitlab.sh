#!/usr/bin/env bash

analytics_sync_intercom() {

  # Sync analytics with Gitlab

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . toolbox/others.sh

  aws_login

  export GITLAB_PASS
  local GITLAB_PROJECTS

  new_sops_env secrets-prod.yaml default \
    analytics_gitlab_token \
    analytics_auth_redshift

  echo "$analytics_auth_redshift" > /target_secret.json
  GITLAB_PASS="$analytics_gitlab_token"
  GITLAB_PROJECTS=(
    'autonomicmind/default' 'autonomicmind/training'
    'fluidattacks/continuous' 'fluidattacks/public'
    'fluidattacks/serves' 'fluidattacks/asserts' 'fluidattacks/public'
    'fluidattacks/integrates' 'fluidattacks/web' 'fluidattacks/writeups'
  )

  pip3 install \
    analytics/singer/tap_json \
    analytics/singer/target_redshift

  for project in ${GITLAB_PROJECTS[*]}; do
    ./analytics/singer/streamer_gitlab.py "$project" >> .jsonstream;
  done

  cat .jsonstream | tap-json > .singer
  cat .singer | \
    target-redshift \
    --auth /target_secret.json --drop-schema --schema-name 'gitlab-ci'
  unset GITLAB_PASS
  rm -rf /target_secret.json
}

analytics_sync_intercom
