#!/usr/bin/env bash

check_first_thursday() {

  # Check if it is the first thursday of the month

  local DAY_NAME
  local DAY_NUMBER

  DAY_NAME="$(date +%A)"
  DAY_NUMBER="$(date +%d)"

  if [ "$DAY_NAME" == 'Thursday' && "$DAY_NUMBER" -le 7 ]; then
    return 0
  else
    return 1
  fi
}

clean_registry_caches() {

  # Remove all registries to force from scratch regeneration

  set -e

  if check_first_thursday; then
    # Import functions
    . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)
    . ci-scripts/helpers/others.sh
    . ci-scripts/helpers/sops.sh

    # Set necessary envars
    local ENV_NAME

    ENV_NAME='production'

    aws_login "$ENV_NAME"

    sops_env "secrets-$ENV_NAME.yaml" default \
      GITLAB_API_TOKEN

    # Delete registriess
    reg_registry_delete deps-production "$GITLAB_API_TOKEN"
  fi
}

clean_registry_caches
