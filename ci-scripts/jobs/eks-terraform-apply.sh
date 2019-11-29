#!/usr/bin/env bash

eks_terraform_apply() {

  # Deploy eks infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/eks-cluster/terraform \
    fluidattacks-terraform-states-prod \
    apply

}

eks_terraform_apply
