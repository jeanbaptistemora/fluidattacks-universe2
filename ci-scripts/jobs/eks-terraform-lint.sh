#!/usr/bin/env bash

eks_terraform_lint() {

  # Run tflint on eks terraform folder

  set -e

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/eks-cluster/terraform \
    fluidattacks-terraform-states-prod

}

eks_terraform_lint
