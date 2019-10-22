#!/usr/bin/env bash

onelogin_sso_terraform_lint() {

  # Run tflint on eks terraform folder

  set -e

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/aws-sso/terraform \
    fluidattacks-terraform-states

}

onelogin_sso_terraform_lint
