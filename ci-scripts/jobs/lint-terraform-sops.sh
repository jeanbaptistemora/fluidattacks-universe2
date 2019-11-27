#!/usr/bin/env bash

lint_terraform_sops() {

  # Does terraform lint

  set -e

  . ci-scripts/helpers/terraform.sh

  lint_terraform \
    deploy/sops/terraform \
    fluidattacks-terraform-states

}

lint_terraform_sops
