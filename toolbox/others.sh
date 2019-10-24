#!/usr/bin/env bash

replace_env_vars() {

  # Replace envars in a file with their values

  #set -e

  local FILE
  local VARS

  FILE="$1"
  VARS="$2"

  shift 1

  envsubst $2 < "$FILE" > tmp
  mv tmp "$FILE"
}

aws_login() {

  # Log in to aws

  set -e

  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

  TF_VAR_aws_access_key="$AWS_ACCESS_KEY_ID"
  TF_VAR_aws_secret_key="$AWS_SECRET_KEY_ID"
}

vault_login() {

  # Log in to vault.

  set -e

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

aws_okta_login() {

    # Log in to aws via okta
    # i.e: aws_okta_login serves-admin

    set -Eeuo pipefail

    local PROFILE

    PROFILE="$1"

    okta-awscli --profile "$PROFILE"
}

create_sops_file() {

  # Create encrypted file with sops using one aws kms key
  # i.e: create_sops_file vars-production.yaml alias/serves-production serves-admin

  set -Eeuo pipefail

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
  # i.e: decrypt_sops_file vars.production.yaml serves-admin

  set -Eeuo pipefail

  local FILE
  local PROFILE

  FILE="$1"
  PROFILE="$2"

  aws_okta_login "$PROFILE"

  sops --aws-profile "$PROFILE" "$FILE"

}
