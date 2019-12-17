#!/usr/bin/env bash

plan_terraform_sops_dev() {

  # Validates terraform plan

  set -Eeuo pipefail

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/sops/development/terraform \
    fluidattacks-terraform-states-dev \
    development \
    plan

}

plan_terraform_sops_dev
