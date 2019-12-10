#!/usr/bin/env bash

integrates_prod_key_rotation() {
  # Script to rotate integrates-prod access key

  set -Eeuo pipefail

  local INTEGRATES_REPO_ID
  INTEGRATES_REPO_ID=4620828

  # Import functions
  . toolbox/terraform.sh
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/gitlab-variables.sh)

  taint_terraform \
    services/user-provision-integrates/integrates-prod/terraform \
    fluidattacks-terraform-states-prod \
    aws_iam_access_key.integrates-dev-key

  VAR_KEY="$(terraform output integrates-prod-secret-key-id)"
  VAR_SECRET="$(terraform output integrates-prod-secret-key)"
  set_project_variable "$GITLAB_API_TOKEN" "$INTEGRATES_REPO_ID" DEV_AWS_ACCESS_KEY_ID "$VAR_KEY" true false
  set_project_variable "$GITLAB_API_TOKEN" "$INTEGRATES_REPO_ID" DEV_AWS_SECRET_ACCESS_KEY "$VAR_SECRET" true false

}

integrates_prod_key_rotation
