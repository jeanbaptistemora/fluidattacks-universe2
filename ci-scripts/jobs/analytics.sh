#!/usr/bin/env bash

analytics_terraform_apply() {

  # Deploy analytics infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/analytics/terraform \
    fluidattacks-terraform-states-prod \
    apply
}

analytics_terraform_lint() {

  # Run tflint on analytics terraform folder

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/analytics/terraform \
    fluidattacks-terraform-states-prod
}

analytics_terraform_plan() {

  # Plan analytics infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/analytics/terraform \
    fluidattacks-terraform-states-prod \
    plan
}
