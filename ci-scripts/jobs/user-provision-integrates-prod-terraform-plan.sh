#!/usr/bin/env bash

user_provision_integrates_prod_terraform_plan() {

  # Plan user-provision-integrates/integrates-prod infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-integrates/integrates-prod/terraform \
    fluidattacks-terraform-states-prod \
    plan

}

user_provision_integrates_prod_terraform_plan
