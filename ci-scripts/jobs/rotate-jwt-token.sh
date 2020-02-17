#!/usr/bin/env bash

update_jwt_key() {

  # Rotate jwt key in gitlab ci variables

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/gitlab-variables.sh)
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/sops.sh

  local ENV_NAME
  local INTEGRATES_ID
  local JWT_TOKEN_NAME
  local JWT_TOKEN
  local MASKED
  local PROTECTED

  ENV_NAME='production'
  INTEGRATES_ID='4620828'
  JWT_TOKEN_NAME='JWT_TOKEN'
  JWT_TOKEN="$(head -c 32 /dev/urandom | base64)"
  MASKED='true'
  PROTECTED='false'

  aws_login "$ENV_NAME"

  sops_env "secrets-$ENV_NAME.yaml" default \
    GITLAB_API_TOKEN

  set_project_variable \
    "${GITLAB_API_TOKEN}" \
    "${INTEGRATES_ID}" \
    "${JWT_TOKEN_NAME}" \
    "${JWT_TOKEN}" \
    "${PROTECTED}" \
    "${MASKED}"
}

update_jwt_key
