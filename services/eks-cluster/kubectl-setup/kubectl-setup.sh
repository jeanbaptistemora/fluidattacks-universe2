#!/usr/bin/env bash

kubectl_setup() {

  # Set initial configuration for eks cluster

  # Import functions
  . services/eks-cluster/helpers.sh

  # Login to cluster
  kubectl_login services/eks-cluster/terraform fluidattacks-terraform-states

  # Create cluster namespaces
  kubectl apply -f services/eks-cluster/kubectl-setup/namespaces.yaml

}
