#!/usr/bin/env bash

user_provision_integrates_prod_terraform_apply() {

  # Deploy user-provision-integrates/integrates-prod infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/user-provision-integrates/integrates-prod/terraform \
    fluidattacks-terraform-states-prod \
    apply
}

user_provision_integrates_prod_terraform_lint() {

  # Run tflint on user-provision/integrates-prod/terraform folder

  set -e

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/user-provision-integrates/integrates-prod/terraform \
    fluidattacks-terraform-states-prod
}

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
