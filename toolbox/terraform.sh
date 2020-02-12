#!/usr/bin/env bash

init_terraform() {

  # This function  initializes a terraform folder
  # init_terraform <dir> <bucket>
  # Example:
  # init_terraform services/eks-cluster/terraform fluidattacks-terraform-states-prod

  set -e

  # Import functions
  . toolbox/others.sh

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
  # lint_terraform services/eks-cluster/terraform fluidattacks-terraform-states-prod

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
  #   services/eks-cluster/terraform fluidattacks-terraform-states-prod apply

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

taint_terraform() {

  # Run terraform taint to mark as taint necessary resources
  # Example:
  # terraform taint aws_security_group.allow_all
  # The resource aws_security_group.allow_all in the module root has been marked as tainted.

  set -Eeuo pipefail

  local STARTING_DIR

  STARTING_DIR="$(pwd)"

  local TARGET_DIR
  local BUCKET
  local MARKED_VALUE

  TARGET_DIR="$1"
  BUCKET="$2"
  MARKED_VALUE="$3"

  init_terraform "$TARGET_DIR" "$BUCKET"

  cd "$TARGET_DIR" || return 1

  terraform refresh

  terraform taint "$MARKED_VALUE"

  cd "$STARTING_DIR" || return 1
}

output_terraform() {

  # Run terraform output to show resources values specified in outputs.tf
  # Example:
  # If an IAM user is created by a resource called "user-example" and it's
  # Defined in outputs.tf as "user-example-key-id", run this command
  # terraform output user-example-key-id

  local TARGET_DIR
  local BUCKET
  local OUTPUT_VALUE
  local STARTING_DIR

  STARTING_DIR="$(pwd)"

  TARGET_DIR="$1"
  BUCKET="$2"
  OUTPUT_VALUE="$3"

  init_terraform "$TARGET_DIR" "$BUCKET" > /dev/null

  cd "$TARGET_DIR" || return 1

  terraform output "$OUTPUT_VALUE"

  cd "$STARTING_DIR" || return 1
}
