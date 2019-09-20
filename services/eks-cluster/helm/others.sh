#!/usr/bin/env bash

get_cluster_name() {
  curl -o terraform.zip https://releases.hashicorp.com/terraform/0.12.6/terraform_0.12.6_linux_amd64.zip
  unzip terraform.zip
  rm terraform.zip
  mv terraform /usr/local/bin/terraform

  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key
  local BUCKET

  TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  TF_VAR_aws_secret_key="$AWS_SECRET_KEY_ID"
  BUCKET='fluidattacks-terraform-states'

  terraform init \
    --backend-config="bucket=$BUCKET" \
    eks-cluster/terraform/

  terraform output cluseter-name
}
