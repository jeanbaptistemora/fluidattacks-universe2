#!/usr/bin/env bash

replace_env_vars() {

  # Replace envars in a file with their values

  set -Eeuo pipefail

  local FILE

  FILE="$1"

  shift 1

  envsubst < "$FILE" > tmp
  mv tmp "$FILE"
}

aws_login() {

  # Log in to aws

  set -Eeuo pipefail

  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

  aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
  aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"

  TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  TF_VAR_aws_secret_key="$AWS_SECRET_ACCESS_KEY"
}

vault_login() {

  # Log in to vault.

  set -Eeuo pipefail

  export VAULT_ADDR
  export VAULT_HOST
  export VAULT_PORT
  export VAULTENV_SECRETS_FILE
  export ROLE_ID
  export SECRET_ID

  VAULT_ADDR="https://vault.fluidattacks.com"
  VAULT_HOST="vault.fluidattacks.com"
  VAULT_PORT='443'
  VAULTENV_SECRETS_FILE="env.vars"
  ROLE_ID="$SERVES_ROLE_ID"
  SECRET_ID="$SERVES_SECRET_ID"

  export VAULT_TOKEN

  VAULT_TOKEN=$( \
    vault write -field=token auth/approle/login \
      role_id="$ROLE_ID" secret_id="$SECRET_ID" \
  )
}
