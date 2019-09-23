#!/usr/bin/env bash

install_helm() {

  # Install helm in the cluster sugin TLS and rbac policies.

  set -e

  . services/eks-cluster/helm/installation/tls.sh
  . ci-scripts/others/others.sh

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

  # Create tiller namespace and serviceaccount and role
  create_resource namespace tiller-context
  create_resource serviceaccount tiller --namespace tiller-context

  # Create tiller role and rolebinding
  kubectl apply -f $ROLE_TILLER
  kubectl apply -f $ROLEBINDING_TILLER

  # Create certificates and keys for tls
  set_tls

  # Uninstall tiller if it already exists
  if kubectl get deployment tiller-deploy --namespace=tiller-context; then
    echo 'Tiller already installed. Removing it to renovate certificate.'
    kubectl delete deployment tiller-deploy --namespace=tiller-context
    kubectl delete secret tiller-secret --namespace=tiller-context
    kubectl delete service tiller-deploy --namespace=tiller-context
  fi

  helm init \
    --upgrade \
    --service-account tiller \
    --tiller-namespace tiller-context \
    --tiller-tls \
    --tiller-tls-cert $TILLER_CERT \
    --tiller-tls-key $TILLER_KEY \
    --tls-ca-cert $CA_CERT \
    --tiller-tls-verify

  # Clean tmp
  rm -rf /tmp/*

}
