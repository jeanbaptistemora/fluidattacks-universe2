#!/usr/bin/env bash

aws_sso_terraform_apply() {

  # Deploy aws-sso terraform module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/aws-sso/terraform \
    fluidattacks-terraform-states-prod \
    production \
    apply
}

aws_sso_terraform_lint() {

  # Lint aws-sso terraform module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  lint_terraform \
    deploy/aws-sso/terraform \
    fluidattacks-terraform-states-prod \
    production
}

aws_sso_terraform_plan() {

  # Plan aws-sso terraform module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/aws-sso/terraform \
    fluidattacks-terraform-states-prod \
    production \
    plan
}
