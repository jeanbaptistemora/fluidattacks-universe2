#!/usr/bin/env bash

plan_terraform_sops_dev() {

  # Validates terraform plan

  set -e

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/sops/development/terraform \
    fluidattacks-terraform-states-dev \
    plan

}

plan_terraform_sops_dev
