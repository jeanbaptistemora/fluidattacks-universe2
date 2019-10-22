#!/usr/bin/env bash

onelogin_sso_terraform_plan() {

  # Plan eks infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/aws-sso/terraform \
    fluidattacks-terraform-states \
    plan

}

onelogin_sso_terraform_plan
