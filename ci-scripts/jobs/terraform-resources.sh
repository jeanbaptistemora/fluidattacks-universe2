#!/usr/bin/env bash

terraform_resources_apply() {

  set -Eeuo pipefail

  . ci-scripts/helpers/sops.sh

  local folder='deploy/terraform-resources'
  local user='production'

  aws_login "${user}"

  pushd "${folder}" || return 1

  terraform init
  terraform apply -auto-approve -refresh=true

  popd || return 1
}

terraform_resources_test() {

  set -Eeuo pipefail

  . ci-scripts/helpers/sops.sh

  local folder='deploy/terraform-resources'
  local user='development'

  aws_login "${user}"

  pushd "${folder}" || return 1

  terraform init
  terraform plan -refresh=true
  tflint --deep --module

  popd || return 1
}
