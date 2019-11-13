#!/usr/bin/env bash

get_last_tls_keys() {

  # Get the last tls keys from helm

  local JSON_FILE='/tmp/fulljson'
  local CA_B64='/tmp/ca.pem.b64'
  local CRT_B64='/tmp/cert.pem.b64'
  local KEY_B64='/tmp/key.pem.b64'

  # Create helm folder
  mkdir -p ~/.helm

  # Get json with secret
  kubectl get secret tiller-secret \
    --namespace=kube-system -o json \
    > "$JSON_FILE"

  # Get b64 keys
  jq -r '.data."ca.crt"' "$JSON_FILE" > "$CA_B64"
  jq -r '.data."tls.crt"' "$JSON_FILE" > "$CRT_B64"
  jq -r '.data."tls.key"' "$JSON_FILE" > "$KEY_B64"

  # Decode b64 keys to text and move them to helm
  base64 -d "$CA_B64" > ~/.helm/ca.pem
  base64 -d "$CRT_B64" > ~/.helm/cert.pem
  base64 -d "$KEY_B64" > ~/.helm/key.pem

  # Remove unnecessary files
  rm "$JSON_FILE" "$CA_B64" "$CRT_B64" "$KEY_B64"
}

install_helm() {

  # Install helm and tiller in the cluster with TLS and rbac policies.

  set -e

  # Import functions
  . services/eks-cluster/helpers.sh
  . services/eks-cluster/helm/installation/tls.sh

  local INSTALL_FOLDER
  local ROLE_TILLER
  local ROLEBINDING_TILLER
  local TILLER_CERT
  local TILLER_KEY
  local CA_CERT

  curl -o helm.tar.gz https://get.helm.sh/helm-v2.14.3-linux-amd64.tar.gz
  tar xf helm.tar.gz
  mv linux-amd64/helm /usr/local/bin/
  rm -rf linux-amd64 helm.tar.gz

  INSTALL_FOLDER='services/eks-cluster/helm/installation'
  ROLE_TILLER="$INSTALL_FOLDER/role-tiller.yaml"
  ROLEBINDING_TILLER="$INSTALL_FOLDER/rolebinding-tiller.yaml"
  TILLER_CERT='/tmp/tiller.crt'
  TILLER_KEY='/tmp/tiller.key'
  CA_CERT='/tmp/ca.cert'

  kubectl_login services/eks-cluster/terraform fluidattacks-terraform-states

  # Create tiller service account
  kubectl apply -f services/eks-cluster/helm/installation/sa-tiller.yaml

  # Create certificates and keys for tls
  set_tls

  # Uninstall tiller if it already exists
  if kubectl get deployment tiller-deploy --namespace=kube-system; then
    echo 'Tiller already installed. Removing it to renovate certificate.'
    # Get last keys from helm in order tu run helm commands
    get_last_tls_keys
    helm reset --force --tls
  fi

  helm init \
    --upgrade \
    --tiller-tls \
    --service-account tiller \
    --tiller-tls-cert $TILLER_CERT \
    --tiller-tls-key $TILLER_KEY \
    --tls-ca-cert $CA_CERT \
    --tiller-tls-verify

  get_last_tls_keys

  # Remove unnecessary files
  rm "$TILLER_CERT" "$TILLER_KEY" "$CA_CERT"
}

deploy_helm() {
  # Install helm and charts

  set -e

  # Import functions
  . services/eks-cluster/helm/charts/install-charts.sh

  # Install tiller in cluster
  install_helm

  # Wait until tiller is deployed
  kubectl rollout status deployment.apps/tiller-deploy \
    --namespace kube-system \
    --timeout=1m

  # Install charts
  install_charts
}
