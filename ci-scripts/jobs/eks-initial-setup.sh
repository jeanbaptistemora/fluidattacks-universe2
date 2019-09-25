#!/usr/bin/env bash

eks_initial_setup() {

  set -e

  # Run cluster initial setup after creating it

  # Import functions
  . services/eks-cluster/helpers.sh

  # Login to cluster
  kubectl_login services/eks-cluster/terraform fluidattacks-terraform-states

  # Create base namespaces
  kubectl apply -f services/eks-cluster/initial-setup/namespaces.yaml
}

eks_initial_setup
