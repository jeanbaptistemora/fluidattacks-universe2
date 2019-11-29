#!/usr/bin/env bash

sops_terraform_lint() {

  # Run tflint on sops terraform folder

  set -e

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/sops/terraform \
    fluidattacks-terraform-states-prod

}

sops_terraform_lint
