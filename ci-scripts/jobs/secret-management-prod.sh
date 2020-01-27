#!/usr/bin/env bash

secret_management_prod_terraform_apply() {

  # Apply secret-management/development module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/secret-management/prod/terraform \
    fluidattacks-terraform-states-prod \
    production \
    apply
}

secret_management_prod_terraform_lint() {

  # Lint secret-management/development module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  lint_terraform \
    deploy/secret-management/prod/terraform \
    fluidattacks-terraform-states-prod \
    production
}

secret_management_prod_terraform_plan() {

  # Plan secret-management/development module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/secret-management/prod/terraform \
    fluidattacks-terraform-states-prod \
    production \
    plan
}
