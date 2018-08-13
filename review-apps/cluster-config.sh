#!/usr/bin/env bash

# This scripts manages the deployment of the Review Apps,
# which allow to view a live site through a public IP with the
# changes introduced by the developer, before accepting changes into
# production.

# Set namespace preference for kubectl commands
echo "Setting namespace preferences..."
kubectl config set-context "$(kubectl config current-context)" --namespace="$CI_PROJECT_NAME"

# Check resources to enable TLS communication
if ! kubectl get issuer cert-issuer; then
  echo "Generating dynamic AWS credentials..."
  vault read -format=json aws/creds/integrates-review > review.json
  export RA_ACCESS_KEY="$(cat review.json | jq -r '.data.access_key')"
  export RA_SECRET_KEY="$(cat review.json | jq -r '.data.secret_key')"
  rm review.json
  sleep 15
  echo "Creating secret with AWS credentials..."
  kubectl create secret generic ra-aws --type=opaque \
    --from-literal=sec-key="$RA_SECRET_KEY"
  echo "Creating Issuer and Certificate to enable communication through HTTPS..."
  envsubst < review-apps/tls.yaml > tls.yaml && \
    mv tls.yaml review-apps/tls.yaml
  kubectl apply -f review-apps/tls.yaml
fi


# Prepare manifests by replacing the value of Environmental Variables
envsubst < review-apps/ingress.yaml > ingress.yaml && mv ingress.yaml review-apps/ingress.yaml
envsubst < review-apps/deploy-integrates.yaml > deploy-integrates.yaml && mv deploy-integrates.yaml review-apps/deploy-integrates.yaml

# Check secret to pull images from Gitlab Registry and set if not present
if ! kubectl get secret gitlab-reg; then
  echo "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry gitlab-reg \
    --docker-server="$CI_REGISTRY" \
    --docker-username="$DOCKER_USER" --docker-password="$DOCKER_PASS" \
    --docker-email="$DOCKER_EMAIL"
fi

# Check secret to pass env variables to container
echo "Creating secrets to pass Environmental Variables..."
sed -i 's/$VAULT_HOST/'"$(echo -n $VAULT_HOST | base64)"'/;
  s/$VAULT_TOKEN/'"$(echo -n $VAULT_TOKEN | base64)"'/' \
  review-apps/variables.yaml
kubectl apply -f review-apps/variables.yaml

# Delete previous deployments and services of the same branch, if present
if kubectl get deployments | grep -q "$CI_COMMIT_REF_SLUG"; then
  echo "Erasing previous deployments..."
  kubectl delete deployment "review-$CI_COMMIT_REF_SLUG"
  kubectl delete service "service-$CI_COMMIT_REF_SLUG";
  kubectl get ingress "ingress-$CI_PROJECT_NAME" -o yaml | sed '/host: '"$CI_COMMIT_REF_SLUG"'/,+5d' | sed '/-\ '"$CI_COMMIT_REF_SLUG"'/d' > current-ingress.yaml
  sleep 30
fi

# Update current ingress resource if it exists, otherwise create it from zero.
if kubectl get ingress | grep "$CI_PROJECT_NAME"; then
  if [ ! -f current-ingress.yaml ]; then
    echo "Getting current ingress manifest..."
    kubectl get ingress "ingress-$CI_PROJECT_NAME" -o yaml > current-ingress.yaml;
  fi
  echo "Updating ingress manifest..."
  sed -n '/spec:/,/tls:/p' current-ingress.yaml | tail -n +3 | head -n -1 >> review-apps/ingress.yaml
  PREV_HOSTS="$(sed -n '/hosts:/,/secretName:/p' current-ingress.yaml | head -n -1 | tail -n +2)"
  while IFS= read -r LINE; do
    sed -i 's/\ \ \ \ secretName/'"$LINE"'\n\ \ \ \ secretName/' review-apps/ingress.yaml;
  done < <(echo "$PREV_HOSTS")
  kubectl apply -f review-apps/ingress.yaml;
else
  kubectl apply -f review-apps/ingress.yaml;
fi

# Deploy pod and service
echo "Deploying latest image..."
kubectl apply -f review-apps/deploy-integrates.yaml

while ! kubectl logs $(kubectl get pods | grep -o ".*$CI_COMMIT_REF_SLUG[^ ]*") | grep 'AH00558'; do
  sleep 15;
done

# Erase file with keys
rm review-apps/variables.yaml