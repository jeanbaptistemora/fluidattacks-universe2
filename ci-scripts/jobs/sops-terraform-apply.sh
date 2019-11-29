#!/usr/bin/env bash

sops_terraform_apply() {

  # Deploy sops infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/sops/terraform \
    fluidattacks-terraform-states-prod \
    apply

}

sops_terraform_apply
