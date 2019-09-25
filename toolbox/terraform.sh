#!/usr/bin/env bash

init_terraform() {

  # This function  initializes a terraform folder
  # init_terraform <dir> <bucket>
  # Example:
  # init_terraform services/eks-cluster/terraform fluidattacks-terraform-states

  set -e

  # Import functions
  . toolbox/others.sh

  curl -o terraform.zip https://releases.hashicorp.com/terraform/0.12.6/terraform_0.12.6_linux_amd64.zip
  unzip terraform.zip
  rm terraform.zip
  mv terraform /usr/local/bin/terraform

  curl -Lo tflint.zip https://github.com/wata727/tflint/releases/download/v0.9.3/tflint_linux_amd64.zip
  unzip tflint.zip
  rm tflint.zip
  install tflint /usr/local/bin/

  local STARTING_DIR

  STARTING_DIR=$(pwd)

  local TARGET_DIR
  local BUCKET

  TARGET_DIR="$1"
  BUCKET="$2"

  aws_login

  cd "$TARGET_DIR" || return 1

  terraform init --backend-config="bucket=$BUCKET"

  cd "$STARTING_DIR" || return 1
}

lint_terraform() {

  # run tflint on terraform folder
  # lint_terraform <dir> <bucket>
  # Example:
  # lint_terraform services/eks-cluster/terraform fluidattacks-terraform-states

  set -e

  local STARTING_DIR

  STARTING_DIR=$(pwd)

  local TARGET_DIR
  local BUCKET

  TARGET_DIR="$1"
  BUCKET="$2"

  init_terraform "$TARGET_DIR" "$BUCKET"

  cd "$TARGET_DIR" || return 1

  tflint

  cd "$STARTING_DIR" || return 1
}

run_terraform() {

  # run terraform plan or apply configuration
  # plan_terraform <dir> <bucket> <command>
  # Example:
  # plan_terraform \
  #   services/eks-cluster/terraform fluidattacks-terraform-states apply

  set -e

  local STARTING_DIR

  STARTING_DIR=$(pwd)

  local TARGET_DIR
  local BUCKET
  local COMMAND

  TARGET_DIR="$1"
  BUCKET="$2"
  COMMAND="$3"

  init_terraform "$TARGET_DIR" "$BUCKET"

  cd "$TARGET_DIR" || return 1

  if [ "$COMMAND" = 'apply' ]; then
    terraform apply -auto-approve -refresh=true
  elif [ "$COMMAND" = 'plan' ]; then
    terraform plan -refresh=true
  else
    echo 'Only apply and plan allowed for $3'
    return 1
  fi

  cd "$STARTING_DIR" || return 1
}
