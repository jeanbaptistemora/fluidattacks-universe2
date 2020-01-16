#!/usr/bin/env bash

user_provision_integrates_dev_terraform_plan() {

  # Plan user-provision-integrates/integrates-dev infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-integrates/integrates-dev/terraform \
    fluidattacks-terraform-states-prod \
    plan

}

user_provision_integrates_dev_terraform_plan
