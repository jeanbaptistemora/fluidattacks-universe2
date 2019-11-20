#!/usr/bin/env bash

autoscaling_ci_terraform_apply() {

  # Deploy autoscaling-ci infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/autoscaling-ci/terraform \
    fluidattacks-terraform-states \
    apply
}

autoscaling_ci_terraform_apply
