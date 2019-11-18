#!/usr/bin/env bash

user_provision_integrates_terraform_plan() {

  # Plan user-provision/integrates-user infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision/integrates-user/terraform \
    fluidattacks-terraform-states \
    plan

}

user_provision_integrates_terraform_plan
