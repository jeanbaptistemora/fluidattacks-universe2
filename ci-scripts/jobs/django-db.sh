#!/usr/bin/env bash

django_db_apply() {

  set -Eeuo pipefail

  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/sops.sh

  local folder='deploy/django-db/terraform'
  local user='production'

  aws_login "${user}"

  sops_env "secrets-${user}.yaml" default \
    TF_VAR_db_user \
    TF_VAR_db_password

  pushd "${folder}" || return 1

  terraform init
  terraform apply -auto-approve -refresh=true

  popd || return 1
}

django_db_test() {

  set -Eeuo pipefail

  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/sops.sh

  local folder='deploy/django-db/terraform'
  local user='development'

  aws_login "${user}"

  sops_env "secrets-${user}.yaml" default \
    TF_VAR_db_user \
    TF_VAR_db_password

  pushd "${folder}" || return 1

  terraform init
  terraform plan -refresh=true
  tflint --deep --module

  popd || return 1
}
