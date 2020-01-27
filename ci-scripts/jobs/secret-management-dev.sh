#!/usr/bin/env bash

secret_management_dev_terraform_apply() {

  # Deploy secret-management/development module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/secret-management/dev/terraform \
    fluidattacks-terraform-states-dev \
    development \
    apply
}

secret_management_dev_terraform_lint() {

  # Lint secret-management/development module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  lint_terraform \
    deploy/secret-management/dev/terraform \
    fluidattacks-terraform-states-dev \
    development
}

secret_management_dev_terraform_plan() {

  # Plan secret-management/development module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/secret-management/dev/terraform \
    fluidattacks-terraform-states-dev \
    development \
    plan
}
