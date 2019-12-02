#!/usr/bin/env bash

change_keys_aws() {

  # Regenerate aws keys for other repos

  set -Eeuo pipefail

  # Import functions
  . infrastructure/vault-wrapper.sh

  vault_generate_aws_keys integrates-cloudwatch
  vault_generate_aws_keys integrates-dynamodb
  vault_generate_aws_keys integrates-s3
  vault_generate_aws_keys integrates-terraform
  vault_generate_aws_keys web-s3
}

change_keys_aws
