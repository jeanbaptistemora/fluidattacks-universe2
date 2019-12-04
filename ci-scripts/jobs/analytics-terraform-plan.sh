#!/usr/bin/env bash

autoscaling_ci_terraform_plan() {

  # Plan analytics infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/analytics/terraform \
    fluidattacks-terraform-states-prod \
    plan
}

autoscaling_ci_terraform_plan
