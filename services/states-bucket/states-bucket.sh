#!/usr/bin/env bash

check_bucket() {
  # Check if the $1 bucket exists.

  set -e

  aws s3api list-buckets --query 'Buckets[].Name' | grep -q "$1"
}

create_bucket() {
  # Create the $1 bucket if it does not exist already.

  set -e

  if ! check_bucket "$1"; then
    echo "creating $1 for terraform tfstates."

    SSE_CONFIG='{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

    # Create bucket with private acl
    aws s3api create-bucket \
      --bucket "$1" \
      --region us-east-1 \
      --acl private
    # Activate versioning for bucket
    aws s3api put-bucket-versioning \
      --bucket "$1" \
      --versioning-configuration Status=Enabled
    # Activate server-side-encryption for bucket
    aws s3api put-bucket-encryption \
      --bucket "$1" \
      --server-side-encryption-configuration "$SSE_CONFIG"
  else
    echo "$1 already exists."
  fi
}

create_states_bucket(){
  # Deploy backend bucket for storing terraform tfstate files

  set -e

  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key
  local BUCKET

  TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  TF_VAR_aws_secret_key="$AWS_SECRET_ACCESS_KEY"
  BUCKET="$1"

  create_bucket "$BUCKET"
}
