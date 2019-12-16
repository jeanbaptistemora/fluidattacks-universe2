#!/usr/bin/env sh

apply_terraform_sops_prod() {

  # Builds terraform plan

  set -e

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/sops/production/terraform \
    fluidattacks-terraform-states-prod \
    production \
    apply
}

apply_terraform_sops_prod
