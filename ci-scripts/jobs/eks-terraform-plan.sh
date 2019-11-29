#!/usr/bin/env bash

eks_terraform_plan() {

  # Plan eks infra using terraform

  set -e

  # Import functions
  . toolbox/terraform.sh

  run_terraform \
    services/eks-cluster/terraform \
    fluidattacks-terraform-states-prod \
    plan

}

eks_terraform_plan
