#!/usr/bin/env bash

# This scripts manages the deployment of the Review Apps,
# which allow to view a live site through a public IP with the
# changes introduced by the developer, before accepting changes into
# production.

# Prepare manifests by replacing the value of Environmental Variables
envsubst < review/ingress.yaml > ingress.yaml && mv ingress.yaml review/ingress.yaml
envsubst < review/deploy-web.yaml > deploy-web.yaml && mv deploy-web.yaml review/deploy-web.yaml
envsubst < review/tls.yaml > tls.yaml && mv tls.yaml review/tls.yaml

# Check if namespace for project exists
if ! kubectl get namespaces | grep -q "$CI_PROJECT_NAME"; then
  echo "Creating namespace for project..."
  kubectl create namespace "$CI_PROJECT_NAME"
fi

# Set namespace preference for kubectl commands
echo "Setting namespace preferences..."
kubectl config set-context "$(kubectl config current-context)" --namespace="$CI_PROJECT_NAME"

# Check secret to pull images from Gitlab Registry and set if not present
if ! kubectl get secret | grep -q "$K8_REG_SECRET"; then
  echo "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry "$K8_REG_SECRET" --docker-server="$CI_REGISTRY" \
  --docker-username="$DOCKER_USER" --docker-password="$DOCKER_PASSWD" --docker-email="$DOCKER_EMAIL"
fi

# Check secret to enable TLS communication
if ! kubectl get secret | grep -q "$K8_SSL_SECRET"; then
  echo "Creating secret to enable communication through HTTPS..."
  kubectl create -f review/tls.yaml
fi

# Delete previous deployments and services of the same branch, if present
if kubectl get deployments | grep -q "$CI_COMMIT_REF_SLUG"; then
  echo "Erasing previous deployments..."
  kubectl delete deployment "review-$CI_COMMIT_REF_SLUG"
  kubectl delete service "service-$CI_COMMIT_REF_SLUG";
  kubectl get ingress "ingress-$CI_PROJECT_NAME" -o yaml | sed '/host: '"$CI_COMMIT_REF_SLUG"'/,+5d' | sed '/-\ '"$CI_COMMIT_REF_SLUG"'/d' > current-ingress.yaml
fi

# Update current ingress resource if it exists, otherwise create it from zero.
if kubectl get ingress "ingress-$CI_PROJECT_NAME"; then
  if [ ! -f current-ingress.yaml ]; then
    echo "Getting current ingress manifest..."
    kubectl get ingress "ingress-$CI_PROJECT_NAME" -o yaml > current-ingress.yaml;
  fi
  echo "Updating ingress manifest..."
  sed -n '/spec:/,/tls:/p' current-ingress.yaml | tail -n +3 | head -n -1 >> review/ingress.yaml
  PREV_HOSTS="$(sed -n '/hosts:/,/secretName:/p' current-ingress.yaml | head -n -1 | tail -n +2)"
  while IFS= read -r LINE; do
    sed -i 's/\ \ \ \ secretName/'"$LINE"'\n\ \ \ \ secretName/' review/ingress.yaml;
  done < <(echo "$PREV_HOSTS")
  kubectl delete ingress "ingress-$CI_PROJECT_NAME"
  kubectl create -f review/ingress.yaml;
else
  kubectl create -f review/ingress.yaml;
fi


# Deploy pod and service
echo "Deploying latest image..."
kubectl create -f review/deploy-web.yaml
