module "cluster" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 18.23.0"
  cluster_name    = local.cluster_name
  cluster_version = "1.22"
  enable_irsa     = true

  eks_managed_node_group_defaults = {
    disk_size              = 30
    capacity_type          = "SPOT"
    force_update_version   = true
    ebs_optimized          = true
    enable_monitoring      = true
    vpc_security_group_ids = [data.aws_security_group.cloudflare.id]
  }
  eks_managed_node_groups = {
    karpenter = {
      max_size = 3

      instance_types = [
        "t3.medium",
        "t3a.medium",
      ]

      iam_role_additional_policies = [
        "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
      ]
    }
    development = {
      max_size = 10

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
      max_size = 10

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

  vpc_id = data.aws_vpc.main.id
  subnet_ids = [
    for subnet in data.aws_subnet.main : subnet.id
  ]
  cluster_security_group_additional_rules = {
    egress_nodes_all = {
      description                = "Cluster to node all ports/protocols"
      protocol                   = "-1"
      from_port                  = 0
      to_port                    = 0
      type                       = "egress"
      source_node_security_group = true
    }
  }
  node_security_group_additional_rules = {
    ingress_self_all = {
      description = "Node to node all ports/protocols"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "ingress"
      self        = true
    }
    egress_any_all = {
      description = "Node to anywhere all ports/protocols"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "egress"
      cidr_blocks = ["0.0.0.0/0"]
    }
    ingress_cluster_all = {
      description                   = "Cluster to node all ports/protocols"
      protocol                      = "-1"
      from_port                     = 0
      to_port                       = 0
      type                          = "ingress"
      source_cluster_security_group = true
    }
  }

  aws_auth_roles    = local.cluster_roles
  aws_auth_users    = local.cluster_users
  aws_auth_accounts = local.cluster_accounts

  tags = {
    "Name"                   = "common-kubernetes"
    "Environment"            = "production"
    "GithubRepo"             = "terraform-aws-eks"
    "GithubOrg"              = "terraform-aws-modules"
    "karpenter.sh/discovery" = local.cluster_name
    "management:area"        = "cost"
    "management:product"     = "common"
    "management:type"        = "product"
  }
}
