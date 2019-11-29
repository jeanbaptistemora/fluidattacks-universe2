#!/usr/bin/env bash

lint_terraform_resources() {

  # Does terraform lint

  set -e

  . ci-scripts/helpers/terraform.sh

  lint_terraform \
    deploy/terraform \
    fluidattacks-terraform-states-prod

}

lint_terraform_resources
