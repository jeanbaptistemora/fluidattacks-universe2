#!/usr/bin/env bash

autoscaling_ci_terraform_lint() {

  # Run tflint on analytics terraform folder

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/analytics/terraform \
    fluidattacks-terraform-states-prod
}

autoscaling_ci_terraform_lint
