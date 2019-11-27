#!/usr/bin/env bash

init_terraform() {

  # This function  initializes a terraform folder
  # init_terraform <dir> <bucket>
  # Example:
  # init_terraform services/eks-cluster/terraform fluidattacks-terraform-states

  set -e

  # Import functions
  . ci-scripts/helpers/others.sh

  local STARTING_DIR

  STARTING_DIR=$(pwd)

  local TARGET_DIR
  local BUCKET

  TARGET_DIR="$1"
  BUCKET="$2"

 aws_login

  cd "$TARGET_DIR" || return 1

  terraform init --backend-config="bucket=$FS_S3_BUCKET"

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
    terraform validate
    terraform plan -refresh=true -out=plan
    terraform show -no-color plan > plan.txt
    mv plan.txt "$CI_PROJECT_DIR"
    rm plan
  else
    echo 'Only apply and plan allowed for $3'
    return 1
  fi

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
