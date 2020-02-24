#!/usr/bin/env bash

django_db_apply() {

  # Apply deploy/django-db/terraform

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/django-db/terraform \
    fluidattacks-terraform-states-prod \
    production \
    apply
}

django_db_test() {

  # Plan and lint deploy/django-db/terraform

  set -Eeuo pipefail

  # Import functions
  . ci-scripts/helpers/terraform.sh

  run_terraform \
    deploy/django-db/terraform \
    fluidattacks-terraform-states-prod \
    development \
    plan
  lint_terraform \
    deploy/django-db/terraform \
    fluidattacks-terraform-states-prod \
    development
}
