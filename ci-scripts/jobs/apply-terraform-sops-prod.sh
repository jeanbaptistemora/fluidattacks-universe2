#!/usr/bin/env bash

apply_terraform_sops_prod() {

  # Builds terraform plan

  set -Eeuo pipefail

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/sops/production/terraform \
    fluidattacks-terraform-states-prod \
    production \
    apply
}

apply_terraform_sops_prod
