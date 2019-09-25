#!/usr/bin/env bash

eks_terraform_plan() {

  set -e

  # Plan eks infra using terraform

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/eks-cluster/terraform \
    fluidattacks-terraform-states \
    plan

}

eks_terraform_plan
