#!/usr/bin/env bash

user_provision_integrates_terraform_lint() {

  # Run tflint on user-provision/integrates-user terraform folder

  set -e

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/user-provision/integrates/terraform \
    fluidattacks-terraform-states

}

user_provision_integrates_terraform_lint
