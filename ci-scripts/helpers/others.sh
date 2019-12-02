#!/usr/bin/env bash

deploy_integrates() {

  # deploy a new integrates version

  set -Eeuo pipefail

  export INTEGRATES_VAULT_TOKEN

  vault_login

  aws s3 cp \
    "s3://servestf/terraform/kubeconfig" \
    "$HOME/.kube/config"

  INTEGRATES_VAULT_TOKEN="$(curl \
    --request POST \
    --data "{\"role_id\":\"$INTEGRATES_PROD_ROLE_ID\",\"secret_id\":\"$INTEGRATES_PROD_SECRET_ID\"}" \
    "https://vault.fluidattacks.com/v1/auth/approle/login" \
    | jq -r '.auth.client_token')"

  sed -i "s/\$FI_VAULT_HOST/$(echo -n $VAULT_HOST | base64)/g" \
    eks/manifests/deployments/integrates-app.yaml
  sed -i "s/\$FI_VAULT_TOKEN/$(echo -n $INTEGRATES_VAULT_TOKEN | base64)/g" \
    eks/manifests/deployments/integrates-app.yaml
  sed -i "s/\$DATE/$(date)/g" eks/manifests/deployments/*.yaml

  kubectl apply -f eks/manifests/deployments/integrates-app.yaml

  kubectl rollout status deploy/integrates-app --timeout=5m \
    || { kubectl rollout undo deploy/integrates-app && exit 1; }
}

vault_login() {

  # Log in to vault

  set -Eeuo pipefail

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
