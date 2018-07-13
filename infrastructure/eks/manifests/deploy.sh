#!/usr/bin/env bash

# Install NGINX Ingress chart to route traffic within the cluster
helm install stable/nginx-ingress \
  --name controller --namespace serves \
  --set rbac.create=true --tls
helm install stable/cert-manager \
  --name tls --namespace kube-system --tls

# Set rule to redirect domain traffic to the ALG
envsubst < manifests/ingress-tls.yaml > ingress.yaml \
  && mv ingress.yaml manifests/ingress-tls.yaml
kubectl apply -f manifests/ingress-tls.yaml

kubectl config set-context $(kubectl config current-context) \
  --namespace serves

# Provide information to access Gitlab Container Registry and pull images
if ! kubectl get secret gitlab-reg; then
  echo "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry gitlab-reg \
    --docker-server="$REGISTRY" --docker-username="$USER" \
    --docker-password="$PASS" --docker-email="$EMAIL"
fi

# Deploy apps containers
kubectl apply -f manifests/alg.yaml
kubectl apply -f manifests/exams.yaml
kubectl apply -f manifests/integrates.yaml
