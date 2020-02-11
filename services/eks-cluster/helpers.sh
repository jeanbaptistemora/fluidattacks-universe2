#!/usr/bin/env bash

get_cluster_name() {

  # Get the name of a running cluster
  # get_cluster_name <dir> <bucket>
  # Example:
  # get_cluster_name services/eks-cluster/terraform fluidattacks-terraform-states-prod

  set -e

  # Import functions
  . toolbox/terraform.sh

  local STARTING_DIR

  STARTING_DIR=$(pwd)

  local TARGET_DIR
  local BUCKET

  TARGET_DIR="$1"
  BUCKET="$2"

  # Initialize terraform
  init_terraform "$TARGET_DIR" "$BUCKET"

  cd "$TARGET_DIR" || return 1

  CLUSTER_NAME=$(terraform output cluster-name)

  cd "$STARTING_DIR" || return 1
}

kubectl_login() {

  # Log in to a cluster for using kubectl
  # kubectl_login <dir> <bucket>
  # Example:
  # kubectl_login services/eks-cluster/terraform fluidattacks-terraform-states-prod

  set -e

  local TARGET_DIR
  local BUCKET

  TARGET_DIR="$1"
  BUCKET="$2"

  get_cluster_name "$TARGET_DIR" "$BUCKET"

  aws eks update-kubeconfig --name "${CLUSTER_NAME}" --region us-east-1
}
