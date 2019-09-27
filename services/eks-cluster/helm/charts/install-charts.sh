#!/usr/bin/env bash

install_cert_manager() {

  # Install Cert Manager

  set -e

  # Import functions
  . services/eks-cluster/helm/helpers.sh

  # Necessary configurations for cert-manager
  kubectl apply \
    -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.10/deploy/manifests/00-crds.yaml
  kubectl label namespace operations cert-manager.io/disable-validation="true" \
    --overwrite

  # Add helm repo
  helm repo add jetstack https://charts.jetstack.io
  helm repo update

  install_chart \
    jetstack/cert-manager \
    cert-manager \
    operations \
    services/eks-cluster/helm/charts/cert-manager.yaml \
    v0.10.0
}

install_charts() {

  # Install helm charts

  set -e

  # Order matters:
  # cert-manager first
  install_cert_manager

}
