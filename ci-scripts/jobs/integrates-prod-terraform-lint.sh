#!/usr/bin/env bash

integrates_prod_terraform_lint() {

  # Run tflint on sops terraform folder

  set -e

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/user-provision-integrates/integrates-prod/terraform \
    fluidattacks-terraform-states-prod

}

integrates_prod_terraform_lint
