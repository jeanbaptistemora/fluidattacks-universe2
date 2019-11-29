#!/usr/bin/env bash

plan_terraform_resources() {

  # Validates terraform plan

  set -e

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/terraform \
    fluidattacks-terraform-states-prod \
    plan
}

plan_terraform_resources
