# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

module "cluster" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 18.23.0"
  cluster_name    = local.cluster_name
  cluster_version = "1.22"
  enable_irsa     = true

  # Nodes
  eks_managed_node_group_defaults = {
    disk_size              = 30
    capacity_type          = "SPOT"
    force_update_version   = true
    ebs_optimized          = true
    enable_monitoring      = true
    vpc_security_group_ids = [data.aws_security_group.cloudflare.id]
  }
  eks_managed_node_groups = {
    development = {
      max_size = 100

      instance_types = [
        "m5.xlarge",
        "m5a.xlarge",
        "m5d.xlarge",
        "m5ad.xlarge",
      ]

      labels = {
        worker_group = "development"
      }
    }
    production = {
      max_size = 120

      instance_types = [
        "m5.large",
        "m5a.large",
        "m5d.large",
        "m5ad.large",
      ]

      labels = {
        worker_group = "production"
      }
    }
  }

  # Network
  vpc_id = data.aws_vpc.main.id
  subnet_ids = [
    for subnet in data.aws_subnet.main : subnet.id
  ]
  cluster_security_group_additional_rules = local.cluster_security_groups.master
  node_security_group_additional_rules    = local.cluster_security_groups.nodes

  # Auth
  manage_aws_auth_configmap = true
  aws_auth_accounts         = [data.aws_caller_identity.main.account_id]
  aws_auth_users = [
    for user in local.cluster_users : {
      userarn  = "arn:aws:iam::${data.aws_caller_identity.main.account_id}:user/${user}"
      username = user
      groups   = ["system:masters"]
    }
  ]
  aws_auth_roles = [
    for user in local.cluster_users : {
      rolearn  = "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/${user}"
      username = user
      groups   = ["system:masters"]
    }
  ]

  tags = {
    "Name"                   = "common-kubernetes"
    "Environment"            = "production"
    "GithubRepo"             = "terraform-aws-eks"
    "GithubOrg"              = "terraform-aws-modules"
    "karpenter.sh/discovery" = local.cluster_name
    "Management:Area"        = "cost"
    "Management:Product"     = "common"
    "Management:Type"        = "product"
  }
}
