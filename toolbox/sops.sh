#!/usr/bin/env bash

create_sops_file() {

  # Create encrypted file with sops using one aws kms key
  # e.g: create_sops_file vars-production.yaml alias/serves-production serves-admin

  set -Eeuo pipefail

  # Import functions
  . toolbox/others.sh

  local FILE
  local KEY_ALIAS
  local PROFILE

  FILE="$1"
  KEY_ALIAS="$2"
  PROFILE="$3"

  aws_okta_login "$PROFILE"

  export SOPS_KMS_ARN
  SOPS_KMS_ARN=$( \
    aws --profile "$PROFILE" kms describe-key --key-id "$KEY_ALIAS" \
    | jq -r .KeyMetadata.Arn \
  )

  sops --aws-profile "$PROFILE" "$FILE"
}

decrypt_sops_file() {

  # Decrypt a sops file
  # e.g: decrypt_sops_file vars.production.yaml serves-admin

  set -Eeuo pipefail

  # Import functions
  . toolbox/others.sh

  local FILE
  local PROFILE

  FILE="$1"
  PROFILE="$2"

  aws_okta_login "$PROFILE"

  sops --aws-profile "$PROFILE" -d "$FILE"

}

sops_env() {

  # Export variables from sops file
  # e.g: secrets-production.yaml serves-admin

  set -Eeuo pipefail

  # Import functions
  . toolbox/others.sh

  local FILE
  local PROFILE
  local TMP_FILE

  FILE="$1"
  PROFILE="$2"
  TMP_FILE="$(mktemp /tmp/XXXXXXXXXX.yaml)"

  # Decrypt file and store it in a temporary location
  decrypt_sops_file "$FILE" "$PROFILE" > "$TMP_FILE"

  # Walk through the yaml and create a bash export command,
  # Create a list with the export command and source it
  . <(./toolbox/sops_env_yaml.py "$TMP_FILE")

  rm -rf "$TMP_FILE"

}
