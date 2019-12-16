#!/usr/bin/env bash

lint_terraform_sops_dev() {

  # Does terraform lint

  set -e

  . ci-scripts/helpers/terraform.sh

  lint_terraform \
    deploy/sops/development/terraform \
    fluidattacks-terraform-states-dev \
    development

}

lint_terraform_sops_dev
