#!/usr/bin/env bash

plan_terraform_sops_production() {

  # Validates terraform plan

  set -e

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/sops/production/terraform \
    fluidattacks-terraform-states-prod \
    production \
    plan

}

plan_terraform_sops_prod
