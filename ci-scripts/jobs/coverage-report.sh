#!/usr/bin/env bash

coverage_report() {

  # Send coverage report to Codecov

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/sops.sh

  local ENV_NAME

  ENV_NAME='development'

  aws_login "$ENV_NAME"

  sops_env "secrets-$ENV_NAME.yaml" default \
    CODECOV_TOKEN

  codecov "--token=$CODECOV_TOKEN"
}

coverage_report
