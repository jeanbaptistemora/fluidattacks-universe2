#!/usr/bin/env bash

deploy_integrates() {

  # deploy a new integrates version

  set -Eeuo pipefail

  export INTEGRATES_VAULT_TOKEN

  aws s3 cp \
    "s3://$FS_S3_BUCKET_NAME/terraform/kubeconfig" \
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
