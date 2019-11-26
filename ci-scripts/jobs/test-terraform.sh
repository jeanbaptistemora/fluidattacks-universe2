#!/usr/bin/env bash

test_terraform() {

  # Validates terraform plan

  set -e

  # import functions
  . ci-scripts/helpers/others.sh

  # Logs in to vault in order to read variables
  vault_login

  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export TF_VAR_aws_s3_evidences_bucket
  export TF_VAR_aws_s3_resources_bucket
  export TF_VAR_dev_aws_access_key
  export TF_VAR_dev_aws_secret_key

  TF_VAR_dev_aws_access_key="$DEV_AWS_ACCESS_KEY_ID"
  TF_VAR_dev_aws_secret_key="$DEV_AWS_SECRET_ACCESS_KEY"

  AWS_ACCESS_KEY_ID="$(
    vault read -field=aws_terraform_access_key secret/integrates/$ENV_NAME
  )"
  AWS_SECRET_ACCESS_KEY="$(
    vault read -field=aws_terraform_secret_key secret/integrates/$ENV_NAME
  )"
  TF_VAR_aws_s3_evidences_bucket=$(
    vault read -field=aws_s3_evidences_bucket secret/integrates/$ENV_NAME
  )
  TF_VAR_aws_s3_resources_bucket="$(
    vault read -field=aws_s3_resources_bucket secret/integrates/$ENV_NAME
  )"

  cd deploy/terraform || return 1
  terraform init --backend-config="bucket=$FS_S3_BUCKET"
  terraform validate
  terraform plan -refresh=true -out=plan
  terraform show -no-color plan > plan.txt
  mv plan.txt "$CI_PROJECT_DIR"
  rm plan
  cd "$CI_PROJECT_DIR" || return 1
  cd deploy/sops/terraform || return 1
  terraform init --backend-config="bucket=$FS_S3_BUCKET"
  terraform validate
  terraform plan -refresh=true -out=plan
  terraform show -no-color plan > plan.txt
  mv plan.txt "$CI_PROJECT_DIR"
  rm plan
  cd "$CI_PROJECT_DIR" || return 1
}

test_terraform
