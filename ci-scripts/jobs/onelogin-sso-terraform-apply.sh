#!/usr/bin/env bash

onelogin_sso_terraform_apply() {

  # Deploy eks infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/onelogin-sso/terraform \
    fluidattacks-terraform-states \
    apply

}

onelogin_sso_terraform_apply
