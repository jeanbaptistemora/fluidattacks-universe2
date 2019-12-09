#!/usr/bin/env bash

break_build_terraform_plan() {

  # Plan break-build infra using terraform

  set -Eeuo pipefail

  # Import functions
  . toolbox/terraform.sh
  . toolbox/others.sh
  . services/break-build/helpers.sh
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/sops-source/sops.sh)

  aws_login

  set_terraform_var_break_build_projects
  set_terraform_var_break_build_project_peers

  run_terraform \
    services/break-build/terraform \
    fluidattacks-terraform-states-prod \
    plan
}

break_build_terraform_plan
