#!/usr/bin/env bash

lint_terraform_resources() {

  # Does terraform lint

  set -Eeuo pipefail

  . ci-scripts/helpers/terraform.sh

  lint_terraform \
    deploy/terraform \
    "$FS_S3_BUCKET" \
    development

}

lint_terraform_resources
