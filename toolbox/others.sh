#!/usr/bin/env bash

replace_env_vars() {

  # Replace envars in a file with their values

  set -Eeuo pipefail

  local FILE
  local TEMP_FILE1

  FILE="$1"
  TEMP_FILE1="$(mktemp /tmp/XXXXXXXXXX)"

  shift 1

  envsubst < "$FILE" > "$TEMP_FILE1"
  mv "$TEMP_FILE1" "$FILE"
}

aws_login() {
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

  set -Eeuo pipefail

      aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" \
  &&  TF_VAR_aws_access_key="${AWS_ACCESS_KEY_ID}" \
  &&  TF_VAR_aws_secret_key="${AWS_SECRET_ACCESS_KEY}"
}
