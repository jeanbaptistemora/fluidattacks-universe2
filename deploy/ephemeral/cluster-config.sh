#!/usr/bin/env bash

# This scripts manages the deployment of the ephemeral environment,
# which allow to view a live site through a public IP with the
# changes introduced by the developer, before accepting changes into
# production.

# Prepare manifests by replacing the value of Environmental Variables
envsubst < deploy/ephemeral/ingress.yaml > ingress.yaml \
  && mv ingress.yaml deploy/ephemeral/ingress.yaml
envsubst < deploy/ephemeral/deploy-web.yaml > deploy-web.yaml \
  && mv deploy-web.yaml deploy/ephemeral/deploy-web.yaml

# Set namespace preference for kubectl commands
echo "Setting namespace preferences..."
kubectl config set-context \
  "$(kubectl config current-context)" --namespace="${CI_PROJECT_NAME}"

# Check secret to pull images from Gitlab Registry and set if not present
if ! kubectl get secret 'gitlab-reg'; then
  echo "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry 'jfrog-reg' \
  --docker-server="${CI_REGISTRY}" --docker-username="${CI_REGISTRY_USER}" \
  --docker-password="${CI_REGISTRY_PASSWORD}" --docker-email="${CI_REGISTRY_EMAIL}"
fi

# Delete previous deployments and services of the same branch, if present
if kubectl get deployments | grep -q "${CI_COMMIT_REF_SLUG}"; then
  echo "Erasing previous deployments..."
  kubectl delete deployment "ephemeral-${CI_COMMIT_REF_SLUG}"
  kubectl delete service "service-${CI_COMMIT_REF_SLUG}";
  kubectl get ingress "ingress-${CI_PROJECT_NAME}" -o yaml | tac | sed '/path:\ \/'"${CI_COMMIT_REF_SLUG}"'/,+3d' | tac > current-ingress.yaml
fi

# Update current ingress resource if it exists, otherwise create it from zero.
if kubectl get ingress "ingress-${CI_PROJECT_NAME}"; then
  if [ ! -f current-ingress.yaml ]; then
    echo "Getting current ingress manifest..."
    kubectl get ingress "ingress-${CI_PROJECT_NAME}" -o yaml > current-ingress.yaml;
  fi
  echo "Updating ingress manifest..."
  sed -n '/spec:/,/tls:/p' current-ingress.yaml | tail -n +6 | head -n -1 >> deploy/ephemeral/ingress.yaml
  kubectl apply -f deploy/ephemeral/ingress.yaml;
else
  kubectl apply -f deploy/ephemeral/ingress.yaml;
fi

# Check resources to enable TLS communication
kubectl apply -f deploy/ephemeral/tls.yaml

# Deploy pod and service
echo "Deploying latest image..."
kubectl create -f deploy/ephemeral/deploy-web.yaml
kubectl rollout status "deploy/ephemeral-${CI_COMMIT_REF_SLUG}"
