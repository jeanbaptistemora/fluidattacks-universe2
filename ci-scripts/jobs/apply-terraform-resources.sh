#!/usr/bin/env sh

apply_terraform_resources() {

  # Builds terraform plan

  set -e

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/terraform \
    fluidattacks-terraform-states \
    apply
}

apply_terraform_resources
