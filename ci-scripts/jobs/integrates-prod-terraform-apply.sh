#!/usr/bin/env bash

integrates_prod_terraform_apply() {

  # Deploy user-provision-integrates/integrates-dev infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-integrates/integrates-prod/terraform \
    fluidattacks-terraform-states-prod \
    apply

}

integrates_prod_terraform_apply
