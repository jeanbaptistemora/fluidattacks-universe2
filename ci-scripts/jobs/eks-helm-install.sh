#!/usr/bin/env bash

eks_helm_install() {

  set -e

  # Install helm in eks cluster

  # Import functions
  . services/eks-cluster/helpers.sh
  . services/eks-cluster/helm/installation/install-helm.sh

  kubectl_login services/eks-cluster/terraform fluidattacks-terraform-states

  install_helm
}

eks_helm_install
