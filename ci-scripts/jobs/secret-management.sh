#!/usr/bin/env bash

secret_management_terraform_apply() {

  set -Eeuo pipefail

  . ci-scripts/helpers/sops.sh

  local folder='deploy/secret-management/terraform'
  local user='production'

  aws_login "${user}"

  pushd "${folder}" || return 1

  terraform init
  terraform apply -auto-approve -refresh=true

  popd || return 1
}

secret_management_terraform_test() {

  set -Eeuo pipefail

  . ci-scripts/helpers/sops.sh

  local folder='deploy/secret-management/terraform'
  local user='development'

  aws_login "${user}"

  pushd "${folder}" || return 1

  terraform init
  terraform plan -refresh=true
  tflint --deep --module

  popd || return 1
}
