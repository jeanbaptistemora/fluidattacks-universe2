#!/usr/bin/env bash

build_sops_terraform_dev() {

  # Validates terraform plan

  set -e

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/sops/terraform \
    fluidattacks-terraform-states \
    plan

}

build_sops_terraform_dev
