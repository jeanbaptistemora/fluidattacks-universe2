#!/usr/bin/env bash

fluid_vpc_terraform_lint() {

  # Run tflint on fluid-vpc terraform folder

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/fluid-vpc/terraform \
    fluidattacks-terraform-states-prod
}

fluid_vpc_terraform_lint
