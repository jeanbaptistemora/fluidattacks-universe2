#!/usr/bin/env bash

eks_terraform_apply() {

  set -e

  # Deploy eks infra using terraform

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/eks-cluster/terraform \
    fluidattacks-terraform-states \
    apply

}

eks_terraform_apply
