#!/usr/bin/env bash

lint_eks(){

  set -e -v

  # Run tflint on eks terraform module

  curl -o terraform.zip https://releases.hashicorp.com/terraform/0.12.6/terraform_0.12.6_linux_amd64.zip
  unzip terraform.zip
  rm terraform.zip
  mv terraform /usr/local/bin/terraform

  curl -Lo tflint.zip https://github.com/wata727/tflint/releases/download/v0.9.3/tflint_linux_amd64.zip
  unzip tflint.zip
  rm tflint.zip
  install tflint /usr/local/bin/

  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key
  local BUCKET

  TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  TF_VAR_aws_secret_key="$AWS_SECRET_KEY_ID"
  BUCKET='fluidattacks-terraform-states'

  terraform init \
    --backend-config="bucket=$BUCKET" \
    infrastructure/terraform/eks
  tflint infrastructure/terraform/eks

}

lint_eks
