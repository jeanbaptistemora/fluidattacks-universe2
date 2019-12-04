#!/usr/bin/env bash

plan_terraform_resources() {

  # Validates terraform plan

  set -e

  # import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/terraform \
    $FS_S3_BUCKET \
    plan
}

plan_terraform_resources
