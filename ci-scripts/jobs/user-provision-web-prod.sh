#!/usr/bin/env bash

user_provision_web_prod_terraform_apply() {

  # Deploy user-provision-web/web-prod infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-web/terraform \
    fluidattacks-terraform-states-prod \
    apply
}

user_provision_web_prod_terraform_lint() {

  # Run tflint on user-provision/web-prod/terraform folder

  set -e

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/user-provision-web/terraform \
    fluidattacks-terraform-states-prod
}

user_provision_web_prod_terraform_plan() {

  # Plan user-provision-web/web-prod infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-web/terraform \
    fluidattacks-terraform-states-prod \
    plan
}

user_provision_web_prod_rotate_aws() {

  # Script to rotate web-prod access key

  set -Eeuo pipefail

  local WEB_REPO_ID
  local TERRAFORM_DIR
  local BUCKET

  BUCKET='fluidattacks-terraform-states-prod'
  TERRAFORM_DIR='services/user-provision-web/terraform'
  WEB_REPO_ID='4649627'

  # Import functions
  . toolbox/terraform.sh
  . ci-scripts/helpers/others.sh
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/gitlab-variables.sh)

  taint_terraform \
    "$TERRAFORM_DIR" \
    "$BUCKET" \
    aws_iam_access_key.web-prod-key

  run_terraform \
    "$TERRAFORM_DIR" \
    "$BUCKET" \
    apply

  VAR_KEY="$(output_terraform $TERRAFORM_DIR $BUCKET web-prod-secret-key-id)"
  VAR_SECRET="$(output_terraform $TERRAFORM_DIR $BUCKET web-prod-secret-key)"

  set_project_variable "$GITLAB_API_TOKEN" "$WEB_REPO_ID" AWS_ACCESS_KEY_ID "$VAR_KEY" true true
  set_project_variable "$GITLAB_API_TOKEN" "$WEB_REPO_ID" AWS_SECRET_ACCESS_KEY "$VAR_SECRET" true true
}
