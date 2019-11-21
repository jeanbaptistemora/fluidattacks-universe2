#!/usr/bin/env bash

ecr_terraform_lint() {

  # Run tflint on ecr terraform folder

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/ecr/terraform \
    fluidattacks-terraform-states
}

ecr_terraform_lint
