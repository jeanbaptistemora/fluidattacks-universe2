#!/usr/bin/env bash

sops_terraform_plan() {

  # Plan sops infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/sops/terraform \
    fluidattacks-terraform-states-prod \
    plan

}

sops_terraform_plan
