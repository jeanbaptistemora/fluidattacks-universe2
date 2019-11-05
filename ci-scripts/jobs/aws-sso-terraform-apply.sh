#!/usr/bin/env bash

aws_sso_terraform_apply() {

  # Deploy eks infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/aws-sso/terraform \
    fluidattacks-terraform-states \
    apply

}

aws_sso_terraform_apply
