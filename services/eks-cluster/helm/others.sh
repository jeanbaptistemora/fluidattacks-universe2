#!/usr/bin/env bash

get_cluster_name() {

  set -e -v

  # Get the name of the current running cluster

  curl -o terraform.zip https://releases.hashicorp.com/terraform/0.12.6/terraform_0.12.6_linux_amd64.zip
  unzip terraform.zip
  rm terraform.zip
  mv terraform /usr/local/bin/terraform

  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key
  local BUCKET
  local CURRENT_DIR
  local CLUSTER_NAME

  TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  TF_VAR_aws_secret_key="$AWS_SECRET_KEY_ID"
  BUCKET='fluidattacks-terraform-states'
  CURRENT_DIR=$(pwd)

  cd services/eks-cluster/terraform/ || return 1

  terraform init --backend-config="bucket=$BUCKET"

  CLUSTER_NAME=$(terraform output cluster-name)

  cd "$CURRENT_DIR" || return 1

  echo "$CLUSTER_NAME"

}
