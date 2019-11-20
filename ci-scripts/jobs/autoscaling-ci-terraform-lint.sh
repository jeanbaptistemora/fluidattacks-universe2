#!/usr/bin/env bash

autoscaling_ci_terraform_lint() {

  # Run tflint on autoscaling-ci terraform folder

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/autoscaling-ci/terraform \
    fluidattacks-terraform-states
}

autoscaling_ci_terraform_lint
