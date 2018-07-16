#!/usr/bin/env bash

# Install NGINX Ingress chart to route traffic within the cluster
if ! helm list --tls | grep 'controller'; then
  helm init --client-only
  helm repo update
  helm install stable/nginx-ingress \
    --name controller --namespace serves \
    --set rbac.create=true --tls
fi

sed -i 's/$TLS_KEY/'"$TLS_KEY"'/;
  s/$TLS_CERT/'"$TLS_CERT"'/' \
  eks/manifests/ingress-tls.yaml
kubectl apply -f eks/manifests/ingress-tls.yaml

kubectl config set-context $(kubectl config current-context) \
  --namespace serves

# Provide information to access Gitlab Container Registry and pull images
if ! kubectl get secret gitlab-reg; then
  echo "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry gitlab-reg \
    --docker-server="$CI_REGISTRY" --docker-username="$DOCKER_USER" \
    --docker-password="$DOCKER_PASS" --docker-email="$DOCKER_EMAIL"
fi

# Pass variables to Integrates to access Torus
sed -i 's/$FI_TORUS_TOKEN_ID/'"$(echo -n $FI_TORUS_TOKEN_ID | base64)"'/; 
  s/$FI_TORUS_TOKEN_SECRET/'"$(echo -n $FI_TORUS_TOKEN_SECRET | base64)"'/;
  s/$TORUS_ORG/'"$(echo -n $TORUS_ORG | base64)"'/;
  s/$FI_TORUS_PROJECT/'"$(echo -n $FI_TORUS_PROJECT | base64)"'/;
  s/$FI_TORUS_ENVIRONMENT/'"$(echo -n $FI_TORUS_ENVIRONMENT | base64)"'/' \
  eks/manifests/integrates.yaml

# Deploy apps containers
kubectl apply -f eks/manifests/alg.yaml
kubectl apply -f eks/manifests/exams.yaml
kubectl apply -f eks/manifests/integrates.yaml
