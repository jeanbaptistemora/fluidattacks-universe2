#!/usr/bin/env bash

break_build_terraform_apply() {

  # Deploy break-build infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh
  . toolbox/others.sh
  . services/break-build/helpers.sh

  aws_login

  set_subscriptions_terraform_variable

  run_terraform \
    services/break-build/terraform \
    fluidattacks-terraform-states \
    apply
}

break_build_terraform_apply
