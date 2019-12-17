#!/usr/bin/env bash

apply_terraform_resources() {

  # Builds terraform plan

  set -Eeuo pipefail

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/terraform \
    "$FS_S3_BUCKET" \
    resources \
    apply
}

apply_terraform_resources
