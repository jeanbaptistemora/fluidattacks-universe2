#!/usr/bin/env bash

fluid_vpc_terraform_plan() {

  # Plan fluid-vpc infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/fluid-vpc/terraform \
    fluidattacks-terraform-states-prod \
    plan
}

fluid_vpc_terraform_plan
