#!/usr/bin/env bash

initial_setup() {

  # Set initial configuration for eks cluster

  # Import functions
  . services/eks-cluster/helpers.sh

  # Login to cluster
  kubectl_login services/eks-cluster/terraform fluidattacks-terraform-states

  # Create cluster namespaces
  kubectl apply -f services/eks-cluster/initial-setup/namespaces.yaml

}
