#!/usr/bin/env bash

user_provision_integrates_prod_terraform_apply() {

  # Deploy user-provision-integrates/integrates-prod infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-integrates/integrates-prod/terraform \
    fluidattacks-terraform-states-prod \
    apply
}

user_provision_integrates_prod_terraform_lint() {

  # Run tflint on user-provision/integrates-prod/terraform folder

  set -e

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/user-provision-integrates/integrates-prod/terraform \
    fluidattacks-terraform-states-prod
}

user_provision_integrates_prod_terraform_plan() {

  # Plan user-provision-integrates/integrates-prod infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-integrates/integrates-prod/terraform \
    fluidattacks-terraform-states-prod \
    plan
}

user_provision_integrates_prod_rotate_aws() {

  # Script to rotate integrates-prod access key

  set -Eeuo pipefail

  local INTEGRATES_REPO_ID
  local TERRAFORM_DIR
  local BUCKET

  BUCKET='fluidattacks-terraform-states-prod'
  TERRAFORM_DIR='services/user-provision-integrates/integrates-prod/terraform'
  INTEGRATES_REPO_ID='4620828'

  # Import functions
  . toolbox/terraform.sh
  . ci-scripts/helpers/others.sh
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/gitlab-variables.sh)

  taint_terraform \
    "$TERRAFORM_DIR" \
    "$BUCKET" \
    aws_iam_access_key.integrates-prod-key

  run_terraform \
    "$TERRAFORM_DIR" \
    "$BUCKET" \
    apply

  VAR_KEY="$(output_terraform $TERRAFORM_DIR $BUCKET integrates-prod-secret-key-id)"
  VAR_SECRET="$(output_terraform $TERRAFORM_DIR $BUCKET integrates-prod-secret-key)"

  set_project_variable "$GITLAB_API_TOKEN" "$INTEGRATES_REPO_ID" PROD_AWS_ACCESS_KEY_ID "$VAR_KEY" true false
  set_project_variable "$GITLAB_API_TOKEN" "$INTEGRATES_REPO_ID" PROD_AWS_SECRET_ACCESS_KEY "$VAR_SECRET" true false

  deploy_integrates
}
