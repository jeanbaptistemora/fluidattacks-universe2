#!/usr/bin/env bash

autoscaling_ci_terraform_apply() {

  # Deploy autoscaling-ci infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/autoscaling-ci/terraform \
    fluidattacks-terraform-states-prod \
    apply
}

autoscaling_ci_terraform_lint() {

  # Run tflint on autoscaling-ci terraform folder

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/autoscaling-ci/terraform \
    fluidattacks-terraform-states-prod
}

autoscaling_ci_terraform_plan() {

  # Plan autoscaling-ci infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/autoscaling-ci/terraform \
    fluidattacks-terraform-states-prod \
    plan
}
