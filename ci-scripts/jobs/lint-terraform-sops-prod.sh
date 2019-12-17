#!/usr/bin/env bash

lint_terraform_sops_prod() {

  # Does terraform lint

  set -Eeuo pipefail

  . ci-scripts/helpers/terraform.sh

  lint_terraform \
    deploy/sops/production/terraform \
    fluidattacks-terraform-states-prod \
    production

}

lint_terraform_sops_prod
