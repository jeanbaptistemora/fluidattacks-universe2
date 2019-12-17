#!/usr/bin/env bash

apply_terraform_sops_dev() {

  # Builds terraform plan

  set -Eeuo pipefail

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/sops/development/terraform \
    fluidattacks-terraform-states-dev \
    development \
    apply
}

apply_terraform_sops_dev
