#!/usr/bin/env bash

kubectl_setup() {

  # Set initial configuration for eks cluster

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . services/eks-cluster/helpers.sh
  . toolbox/others.sh

  # Set envars
  aws_login
  sops_env secrets-prod.yaml default \
    FLUID_TLS_KEY \
    FLUIDATTACKS_TLS_CERT

  # Login to cluster
  kubectl_login services/eks-cluster/terraform fluidattacks-terraform-states-prod

  # Create cluster namespaces
  kubectl apply -f services/eks-cluster/kubectl-setup/namespaces.yaml

  # Create default ssl certificate (official Godaddy cert)
  replace_env_vars \
    services/eks-cluster/kubectl-setup/fluidattacks-default-cert.yaml
  kubectl apply -f \
    services/eks-cluster/kubectl-setup/fluidattacks-default-cert.yaml
}
