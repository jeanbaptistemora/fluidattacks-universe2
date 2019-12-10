#!/usr/bin/env bash

user_provision_integrates_terraform_apply() {

  # Deploy user-provision-integrates/integrates-dev infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-integrates/integrates-dev/terraform \
    fluidattacks-terraform-states-prod \
    apply

}

user_provision_integrates_terraform_apply
