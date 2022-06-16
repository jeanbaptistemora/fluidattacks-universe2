module "cluster" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 18.23.0"
  cluster_name    = "common"
  cluster_version = "1.22"
  enable_irsa     = true

  vpc_id = data.aws_vpc.main.id
  subnet_ids = [
    for subnet in data.aws_subnet.main : subnet.id
  ]

  eks_managed_node_group_defaults = {
    capacity_type          = "SPOT"
    force_update_version   = true
    ebs_optimized          = true
    enable_monitoring      = true
    vpc_security_group_ids = [data.aws_security_group.cloudflare.id]
  }

  eks_managed_node_groups = {
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

  aws_auth_roles    = var.map_roles
  aws_auth_users    = var.map_users
  aws_auth_accounts = var.map_accounts

  tags = {
    "Name"               = "common-kubernetes"
    "Environment"        = "production"
    "GithubRepo"         = "terraform-aws-eks"
    "GithubOrg"          = "terraform-aws-modules"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
