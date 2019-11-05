#!/usr/bin/env bash

aws_sso_terraform_plan() {

  # Plan eks infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/aws-sso/terraform \
    fluidattacks-terraform-states \
    plan

}

aws_sso_terraform_plan
