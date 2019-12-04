#!/usr/bin/env sh

apply_terraform_resources() {

  # Builds terraform plan

  set -e

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/terraform \
    $FS_S3_BUCKET \
    apply
}

apply_terraform_resources
