#!/usr/bin/env bash

envsubst < ingress-tls.yaml > ingress.yaml \
  && mv ingress.yaml ingress-tls.yaml
kubectl apply -f ingress-tls.yaml

kubectl config set-context $(kubectl config current-context) \
  --namespace serves

if ! kubectl get secret gitlab-reg; then
  echo "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry gitlab-reg \
    --docker-server="$REGISTRY" --docker-username="$USER" \
    --docker-password="$PASS" --docker-email="$EMAIL"
fi

kubectl apply -f alg.yaml
kubectl apply -f exams.yaml
kubectl apply -f integrates.yaml
