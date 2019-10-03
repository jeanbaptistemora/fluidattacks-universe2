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

check_deployment_ready() {

  # Check every 5 seconds if a deployment is ready.
  # limit is in minutes
  # Return 0 if it is ready
  # Return 1 if it is not

  set -e

  local DEPLOYMENT
  local NAMESPACE
  local TIME

  DEPLOYMENT="$1"
  NAMESPACE="$2"
  TIME="$3"

  if kubectl rollout status "deployment.apps/$DEPLOYMENT" \
    --namespace "$NAMESPACE" --timeout="${TIME}m"; then
    echo 'Deployment is ready.'
    return 0
  else
    echo 'Deployment was never ready.'
    return 1
  fi
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
