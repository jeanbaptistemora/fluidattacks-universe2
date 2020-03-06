#!/usr/bin/env bash

django_db_apply() {

  set -Eeuo pipefail

  . <(curl -sL https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/sops.sh

  local folder='deploy/django-db/terraform'
  local user='production'

  aws_login "${user}"

  sops_env "secrets-${user}.yaml" default \
    DB_USER \
    DB_PASSWD

  export TF_VAR_db_user="${DB_USER}"
  export TF_VAR_db_password="${DB_PASSWD}"

  pushd "${folder}" || return 1

  terraform init
  terraform apply -auto-approve -refresh=true

  popd || return 1
}

django_db_test() {

  set -Eeuo pipefail

  . <(curl -sL https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/sops.sh

  local folder='deploy/django-db/terraform'
  local user='development'

  aws_login "${user}"

  sops_env "secrets-${user}.yaml" default \
    DB_USER \
    DB_PASSWD

  export TF_VAR_db_user="${DB_USER}"
  export TF_VAR_db_password="${DB_PASSWD}"

  pushd "${folder}" || return 1

  terraform init
  terraform plan -refresh=true
  tflint --deep --module

  popd || return 1
}
