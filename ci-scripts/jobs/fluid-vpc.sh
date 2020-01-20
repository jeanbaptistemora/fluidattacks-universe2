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

fluid_vpc_terraform_lint() {

  # Run tflint on fluid-vpc terraform folder

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/fluid-vpc/terraform \
    fluidattacks-terraform-states-prod
}

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
