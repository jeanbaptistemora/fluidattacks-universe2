#!/usr/bin/env sh

build_terraform() {

  # Builds terraform plan

  set -e

  # import functions
  . ci-scripts/helpers/others.sh

  # Logs in to vault in order to read variables
  vault_login

  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY
  export TF_VAR_aws_s3_evidences_bucket
  export TF_VAR_aws_s3_resources_bucket

  AWS_ACCESS_KEY_ID=$(
    vault read -field=aws_terraform_access_key secret/integrates/production
  )
  AWS_SECRET_ACCESS_KEY=$(
    vault read -field=aws_terraform_secret_key secret/integrates/production
  )
  TF_VAR_aws_s3_evidences_bucket=$(
    vault read -field=aws_s3_evidences_bucket secret/integrates/production
  )
  TF_VAR_aws_s3_resources_bucket=$(
    vault read -field=aws_s3_resources_bucket secret/integrates/production
  )
  cd deploy/terraform || return 1
  terraform init --backend-config="bucket=${FS_S3_BUCKET}"
  terraform apply -auto-approve -refresh=true
}

build_terraform
