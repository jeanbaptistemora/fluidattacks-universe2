#!/usr/bin/env bash

backup_terraform_apply() {

  set -Eeuo pipefail
  local ENV_NAME
  
  ENV_NAME='production'
  
  # Import functions
  . ci-scripts/helpers/sops.sh
  aws_login "$ENV_NAME"

  pushd 'deploy/backup/terraform'

  terraform init
  terraform apply -auto-approve -refresh=true
}

backup_terraform_test() {
  
  # Apply backup module

  set -Eeuo pipefail
  local ENV_NAME
  
  ENV_NAME='development'
  
  # Import functions
  . ci-scripts/helpers/sops.sh
  aws_login "$ENV_NAME"
  
  pushd 'deploy/backup/terraform'
  terraform init
  tflint --deep --module
  terraform plan
}
