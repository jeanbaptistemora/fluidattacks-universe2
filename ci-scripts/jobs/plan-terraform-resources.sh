#!/usr/bin/env bash

plan_terraform_resources() {

  # Validates terraform plan

  set -Eeuo pipefail

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/terraform \
    "$FS_S3_BUCKET" \
    development \
    plan
}

plan_terraform_resources
