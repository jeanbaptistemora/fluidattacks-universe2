#!/usr/bin/env bash

autoscaling_ci_terraform_apply() {

  # Deploy analytics infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/analytics/terraform \
    fluidattacks-terraform-states-prod \
    apply
}

autoscaling_ci_terraform_apply
