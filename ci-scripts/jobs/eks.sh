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

eks_terraform_lint() {

  # Run tflint on eks terraform folder

  set -e

  # Import functions
  . toolbox/terraform.sh

  lint_terraform \
    services/eks-cluster/terraform \
    fluidattacks-terraform-states-prod
}

eks_initial_setup() {

  # Run cluster initial setup after creating it.
  # It creates namespaces, installs helm and charts

  set -e

  # Import functions
  . services/eks-cluster/kubectl-setup/kubectl-setup.sh
  . services/eks-cluster/helm/installation/deploy-helm.sh

  kubectl_setup
  deploy_helm
}
