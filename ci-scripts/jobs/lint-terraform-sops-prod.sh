#!/usr/bin/env bash

lint_terraform_sops_prod() {

  # Does terraform lint

  set -e

  . ci-scripts/helpers/terraform.sh

  lint_terraform \
    deploy/sops/production/terraform \
    fluidattacks-terraform-states-prod

}

lint_terraform_sops_prod
