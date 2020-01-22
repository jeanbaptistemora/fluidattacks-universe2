#!/usr/bin/env bash

user_provision_continuous_dev_terraform_apply() {

  # Deploy user-provision-continuous/continuous-dev infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-continuous/continuous-dev/terraform \
    fluidattacks-terraform-states-dev \
    apply
}

user_provision_continuous_dev_terraform_lint() {

  # Run tflint on user-provision-continuous/continuous-dev terraform folder

  set -e

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/user-provision-continuous/continuous-dev/terraform \
    fluidattacks-terraform-states-dev
}

user_provision_continuous_dev_terraform_plan() {

  # Plan user-provision-continuous/continuous-dev infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-continuous/continuous-dev/terraform \
    fluidattacks-terraform-states-dev \
    plan
}

user_provision_continuous_dev_rotate_aws() {

  # Script to rotate continuous-dev access key

  set -Eeuo pipefail

  local CONTINUOUS_REPO_ID
  local TERRAFORM_DIR
  local BUCKET

  BUCKET='fluidattacks-terraform-states-dev'
  TERRAFORM_DIR='services/user-provision-continuous/continuous-dev/terraform'
  CONTINUOUS_REPO_ID='4603023'

  # Import functions
  . toolbox/terraform.sh
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/gitlab-variables.sh)

  taint_terraform \
    "$TERRAFORM_DIR" \
    "$BUCKET" \
    aws_iam_access_key.continuous-dev-key

  run_terraform \
    "$TERRAFORM_DIR" \
    "$BUCKET" \
    apply

  VAR_KEY="$(output_terraform $TERRAFORM_DIR $BUCKET continuous-dev-secret-key-id)"
  VAR_SECRET="$(output_terraform $TERRAFORM_DIR $BUCKET continuous-dev-secret-key)"

  set_project_variable "$GITLAB_API_TOKEN" "$CONTINUOUS_REPO_ID" DEV_AWS_ACCESS_KEY_ID "$VAR_KEY" false true
  set_project_variable "$GITLAB_API_TOKEN" "$CONTINUOUS_REPO_ID" DEV_AWS_SECRET_ACCESS_KEY "$VAR_SECRET" false true
}
