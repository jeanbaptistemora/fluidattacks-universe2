#!/usr/bin/env bash

get_cluster_name() {

  set -e

  # Get the name of the current running cluster

  curl -o terraform.zip https://releases.hashicorp.com/terraform/0.12.6/terraform_0.12.6_linux_amd64.zip
  unzip terraform.zip
  rm terraform.zip
  mv terraform /usr/local/bin/terraform

  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key
  local BUCKET
  local CURRENT_DIR
  export CLUSTER_NAME

  TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  TF_VAR_aws_secret_key="$AWS_SECRET_ACCESS_KEY"
  BUCKET='fluidattacks-terraform-states'
  CURRENT_DIR=$(pwd)

  cd services/eks-cluster/terraform/ || return 1

  terraform init --backend-config="bucket=$BUCKET"

  CLUSTER_NAME=$(terraform output cluster-name)

  cd "$CURRENT_DIR" || return 1

}

create_resource() {

  # Create resource in cluster using kubectl

  set -e

  if kubectl get --all-namespaces "$1" | grep -q "$2"; then
    echo "$1 $2 already exists."
  else
    echo "Creating $1 $2 ..."
    kubectl create "$@"
  fi
}

function replace_env_vars() {

  # Replace envars in a file with their values

  set -e

  envsubst < "$1" > tmp
  mv tmp "$1"
}

kubectl_login() {

  # Log in to cluster for using kubectl

  set -e

  get_cluster_name

  aws eks update-kubeconfig --name $CLUSTER_NAME --region us-east-1
}
