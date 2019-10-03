#!/usr/bin/env bash

install_cert_manager() {

  # Install Cert Manager chart

  set -e

  # Import functions
  . services/eks-cluster/helm/helpers.sh
  . toolbox/others.sh

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
    services/eks-cluster/helm/charts/cert-manager/cert-manager.yaml \
    v0.10.0

  # Install LetsEncrypt Cluster Issuer
  kubectl apply -f \
    services/eks-cluster/helm/charts/cert-manager/cluster-issuer-fluid.yaml
}

install_nginx() {

  # Install nginx chart

  set -e

  # Import functions
  . services/eks-cluster/helm/helpers.sh

  install_chart \
    stable/nginx-ingress \
    nginx-ingress \
    operations \
    services/eks-cluster/helm/charts/nginx/nginx.yaml \
    0.25.1
}

install_charts() {

  # Install helm charts

  set -e

  # Order matters!

  # Cert manager and nginx first as they are used by most other applications
  install_cert_manager
  install_nginx

}
