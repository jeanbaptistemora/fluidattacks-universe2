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
  local B64_AWS_ACCESS_KEY_ID
  local B64_AWS_SECRET_ACCESS_KEY

  BUCKET="fluidattacks-terraform-states-prod"
  TERRAFORM_DIR="services/user-provision-integrates/integrates-prod/terraform"
  TMP_AWS_ACCESS_KEY_ID="$(output_terraform $TERRAFORM_DIR $BUCKET integrates-prod-secret-key-id)"
  TMP_AWS_SECRET_ACCESS_KEY="$(output_terraform $TERRAFORM_DIR $BUCKET integrates-prod-secret-key)"
  B64_AWS_ACCESS_KEY_ID="$(echo -n $TMP_AWS_ACCESS_KEY_ID | base64)"
  B64_AWS_SECRET_ACCESS_KEY="$(echo -n $TMP_AWS_SECRET_ACCESS_KEY | base64)"

  sed -i "s/\$B64_AWS_ACCESS_KEY_ID/$B64_AWS_ACCESS_KEY_ID/g" \
    infrastructure/eks/manifests/deployments/integrates-app.yaml
  sed -i "s/\$B64_AWS_SECRET_ACCESS_KEY/$B64_AWS_SECRET_ACCESS_KEY/g" \
    infrastructure/eks/manifests/deployments/integrates-app.yaml
  sed -i "s/\$DATE/$(date)/g" \
    infrastructure/eks/manifests/deployments/*.yaml

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
  VALUE_PORT='443'
  ROLE_ID="$SERVES_ROLE_ID"
  SECRET_ID="$SERVES_SECRET_ID"
  VAULTENV_SECRETS_FILE='env.vars'

  VAULT_TOKEN="$(vault write \
    -field=token auth/approle/login role_id=$ROLE_ID secret_id=$SECRET_ID \
  )"
}
