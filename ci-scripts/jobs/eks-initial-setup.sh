#!/usr/bin/env bash

eks_initial_setup() {

  # Run cluster initial setup after creating it.
  # It creates namespaces, installs helm and charts

  set -e

  # Import functions
  . services/eks-cluster/kubectl-setup/kubectl-setup.sh
  . services/eks-cluster/helm/installation/deploy-helm.sh

  kubectl_setup
  deploy_helm
}

eks_initial_setup
