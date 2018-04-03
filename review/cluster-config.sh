#!/usr/bin/env sh

# This scripts manages the deployment of the Review Apps,
# which allow to view a live site through a public IP with the
# changes introduced by the developer, before accepting changes into
# production.

# Set namespace preference for kubectl commands
echo "Setting namespace preferences..."
kubectl config set-context "$(kubectl config current-context)" --namespace=gitlab-managed-apps

# Check secret to pull images from Gitlab Registry and set if not present
if ! kubectl get secret | grep -q "$KUBE_SECRET"; then
  echo "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry "$KUBE_SECRET" --docker-server="$CI_REGISTRY" \
  --docker-username="$DOCKER_USER" --docker-password="$DOCKER_PASSWD" --docker-email="$DOCKER_EMAIL"
fi

# Delete previous deployments and services of the same branch, if present
if kubectl get deployments | grep -q "review-$CI_COMMIT_REF_SLUG"; then
  echo "Erasing previous deployments..."
  kubectl delete deployment "review-$CI_COMMIT_REF_SLUG"
  kubectl delete service "web-service-$CI_COMMIT_REF_SLUG";
  kubectl get ingress ingress-review -o yaml | sed '/'"$CI_COMMIT_REF_SLUG.$CI_PROJECT_NAME"'/,+5d' > current-ingress.yaml
fi

# Prepare manifests by replacing the value of Environmental Variables
envsubst < review/ingress.yaml > ingress.yaml && mv ingress.yaml review/ingress.yaml
sed -i 's/CI_COMMIT_REF_SLUG/'"$CI_COMMIT_REF_SLUG"'/g' review/deploy-web.yaml

# Update current ingress resource if it exists, otherwise create it from zero.
if kubectl get ingress | grep 'review'; then
  if [ ! -f current-ingress.yaml ]; then
    echo "Getting current ingress manifest..."
    kubectl get ingress ingress-review -o yaml > current-ingress.yaml;
  fi
  echo "Updating ingress manifest..."
  sed -n '/spec:/,/status:/p' current-ingress.yaml | head -n -1 | tail -n +3 >> review/ingress.yaml
  kubectl delete ingress ingress-review
  kubectl create -f review/ingress.yaml;
else
  kubectl create -f review/ingress.yaml;
fi

# Deploy pod and service
echo "Deploying latest image..."
kubectl create -f review/deploy-web.yaml
