#!/usr/bin/env sh

build_terraform() {

  # Builds terraform plan

  export AWS_ACCESS_KEY_ID="$(
    vault read -field=aws_terraform_access_key secret/integrates/production
  )"
  export AWS_SECRET_ACCESS_KEY="$(
    vault read -field=aws_terraform_secret_key secret/integrates/production
  )"
  export TF_VAR_aws_s3_resources_bucket="$(
    vault read -field=aws_s3_resources_bucket secret/integrates/production
  )"
  cd deploy/terraform
  terraform init --backend-config="bucket=${FS_S3_BUCKET}"
  terraform apply -auto-approve -refresh=true
}

build_terraform
