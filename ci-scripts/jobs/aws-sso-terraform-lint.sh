#!/usr/bin/env bash

aws_sso_terraform_lint() {

  # Run tflint on eks terraform folder

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/aws-sso/terraform \
    fluidattacks-terraform-states-prod

}

aws_sso_terraform_lint
