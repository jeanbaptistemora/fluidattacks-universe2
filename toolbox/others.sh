#!/usr/bin/env bash

replace_env_vars() {

  # Replace envars in a file with their values

  set -e

  envsubst < "$1" > tmp
  mv tmp "$1"
}

aws_login() {

  # Log in to aws

  set -e

  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

  TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  TF_VAR_aws_secret_key="$AWS_SECRET_KEY_ID"
}
