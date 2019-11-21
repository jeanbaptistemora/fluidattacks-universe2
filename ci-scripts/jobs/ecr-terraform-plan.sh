#!/usr/bin/env bash

ecr_terraform_plan() {

  # Plan ecr infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/ecr/terraform \
    fluidattacks-terraform-states \
    plan
}

ecr_terraform_plan
