#!/usr/bin/env bash

terraform_resources_apply() {

  # Apply terraform-resources module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/terraform-resources \
    "$FS_S3_BUCKET" \
    production \
    apply
}

terraform_resources_lint() {

  # Lint terraform-resources module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  lint_terraform \
    deploy/terraform-resources \
    "$FS_S3_BUCKET" \
    development

}

terraform_resources_plan() {

  # Plan terraform-resources module

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/terraform-resources \
    "$FS_S3_BUCKET" \
    development \
    plan
}
