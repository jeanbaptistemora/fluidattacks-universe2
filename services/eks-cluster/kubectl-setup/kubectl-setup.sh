#!/usr/bin/env bash

kubectl_setup() {

  # Set initial configuration for eks cluster

  # Import functions
  . services/eks-cluster/helpers.sh
  . toolbox/others.sh

  # Login to cluster
  kubectl_login services/eks-cluster/terraform fluidattacks-terraform-states

  # Create cluster namespaces
  kubectl apply -f services/eks-cluster/kubectl-setup/namespaces.yaml

  # Create default ssl certificate (official Godaddy cert)
  replace_env_vars \
    services/eks-cluster/kubectl-setup/fluidattacks-default-cert.yaml
  kubectl apply -f \
    services/eks-cluster/kubectl-setup/fluidattacks-default-cert.yaml
}
