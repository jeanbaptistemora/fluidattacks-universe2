#!/usr/bin/env bash

eks_terraform_lint() {

  set -e

  # Run tflint on eks terraform folder

  # Import functions
  . toolbox/terraform.sh

  lint_terraform services/eks-cluster/terraform fluidattacks-terraform-states

}

eks_terraform_lint
