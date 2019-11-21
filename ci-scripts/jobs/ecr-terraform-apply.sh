#!/usr/bin/env bash

ecr_terraform_apply() {

  # Deploy ecr infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/ecr/terraform \
    fluidattacks-terraform-states \
    apply
}

ecr_terraform_apply
