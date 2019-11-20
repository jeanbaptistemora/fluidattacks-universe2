#!/usr/bin/env bash

autoscaling_ci_terraform_plan() {

  # Plan autoscaling-ci infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/autoscaling-ci/terraform \
    fluidattacks-terraform-states \
    plan
}

autoscaling_ci_terraform_plan
