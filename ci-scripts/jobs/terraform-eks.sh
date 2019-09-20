#!/usr/bin/env bash

terraform_eks(){

  set -e -v

  # This function either applies or plans a terraform configuration
  # on the eks cluster

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
    services/eks-cluster/terraform/

  # Set either apply or plan terraform setting based on branch
  if [ "$CI_COMMIT_REF_NAME" = 'master' ]; then
    terraform apply -auto-approve -refresh=true services/eks-cluster/terraform/
  else
    terraform plan -refresh=true services/eks-cluster/terraform/
  fi

}

terraform_eks
