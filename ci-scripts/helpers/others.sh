#!/usr/bin/env bash

deploy_integrates() {

  # deploy a new integrates version

  set -e

  # Import functions
  . toolbox/terraform.sh

  local TERRAFORM_DIR
  local BUCKET
  local TMP_AWS_ACCESS_KEY_ID
  local TMP_AWS_SECRET_ACCESS_KEY
  local b64_aws_access_key_id
  local b64_aws_secret_access_key

  BUCKET="fluidattacks-terraform-states-prod"
  TERRAFORM_DIR="services/user-provision-integrates/integrates-prod/terraform"
  TMP_AWS_ACCESS_KEY_ID="$(output_terraform $TERRAFORM_DIR "${BUCKET}" integrates-prod-secret-key-id)"
  TMP_AWS_SECRET_ACCESS_KEY="$(output_terraform $TERRAFORM_DIR "${BUCKET}" integrates-prod-secret-key)"
  b64_aws_access_key_id="$(echo -n "$TMP_AWS_ACCESS_KEY_ID" | base64)"
  b64_aws_secret_access_key="$(echo -n "$TMP_AWS_SECRET_ACCESS_KEY" | base64)"

  sed -i "s/\$b64_aws_access_key_id/$b64_aws_access_key_id/g" \
    infrastructure/eks/manifests/deployments/integrates-app.yaml
  sed -i "s/\$b64_aws_secret_access_key/$b64_aws_secret_access_key/g" \
    infrastructure/eks/manifests/deployments/integrates-app.yaml
  sed -i "s/\$date/$(date)/g" \
    infrastructure/eks/manifests/deployments/*.yaml

  aws eks update-kubeconfig --name FluidServes --region us-east-1
  kubectl config set-context "$(kubectl config current-context)" --namespace serves

  kubectl apply -f infrastructure/eks/manifests/deployments/integrates-app.yaml

  kubectl rollout status deploy/integrates-app --timeout=5m \
    || { kubectl rollout undo deploy/integrates-app && exit 1; }
}

vault_login() {

  # Log in to vault

  set -e

  export VAULT_ADDR
  export VAULT_HOST
  export VAULT_PORT
  export ROLE_ID
  export SECRET_ID
  export VAULTENV_SECRETS_FILE
  export VAULT_TOKEN

  VAULT_ADDR='https://vault.fluidattacks.com'
  VAULT_HOST='vault.fluidattacks.com'
  VAULT_PORT='443'
  ROLE_ID="$SERVES_ROLE_ID"
  SECRET_ID="$SERVES_SECRET_ID"
  VAULTENV_SECRETS_FILE='env.vars'

  VAULT_TOKEN="$(vault write \
    -field=token auth/approle/login "role_id=${ROLE_ID}" "secret_id=${SECRET_ID}" \
  )"
}
