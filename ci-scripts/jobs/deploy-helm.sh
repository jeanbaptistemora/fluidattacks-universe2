#!/usr/bin/env bash

deploy_helm(){

  set -e

  # Install helm in cluster

  . ci-scripts/others/others.sh
  . services/eks-cluster/helm/installation/install-helm.sh

  kubectl_login

  install_helm
}

deploy_helm
