#!/usr/bin/env bash

break_build_terraform_lint() {

  # Run tflint on break-build terraform folder

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/break-build/terraform \
    fluidattacks-terraform-states-prod
}

break_build_terraform_lint
