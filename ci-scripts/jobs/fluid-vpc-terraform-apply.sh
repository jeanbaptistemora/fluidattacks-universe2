#!/usr/bin/env bash

fluid_vpc_terraform_apply() {

  # Deploy fluid-vpc infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/fluid-vpc/terraform \
    fluidattacks-terraform-states-prod \
    apply
}

fluid_vpc_terraform_apply
