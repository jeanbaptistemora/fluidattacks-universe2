provider "aws" {
  version = ">= 2.11"
  region  = var.region
}

provider "random" {
  version = "~> 2.1"
}

provider "local" {
  version = "~> 1.2"
}

provider "null" {
  version = "~> 2.1"
}

provider "template" {
  version = "~> 2.1"
}

locals {
  cluster_name = "fluid-cluster-${random_string.suffix.result}"
}

resource "random_string" "suffix" {
  length  = 5
  special = false
}

module "fluid-cluster" {
  source       = "terraform-aws-modules/eks/aws"
  cluster_name = local.cluster_name
  subnets      = module.vpc.private_subnets
  vpc_id       = module.vpc.vpc_id

  worker_groups = [
    {
      name                          = "conventional-workers"
      instance_type                 = "t3.nano"
      asg_max_size                  = 1
      tags = [{
        key                 = "Name"
        value               = "fluid-cluster-conventional-worker"
        propagate_at_launch = true
      }]
    }
  ]

  tags = {
    Name       = local.cluster_name
    GithubRepo = "terraform-aws-eks"
    GithubOrg  = "terraform-aws-modules"
  }
}
