module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 12.2.0"
  cluster_name    = var.cluster_name
  cluster_version = "1.17"
  enable_irsa     = true

  subnets = [
    aws_subnet.region_a.id,
    aws_subnet.region_b.id,
    aws_subnet.region_d.id,
  ]

  tags = {
    "Name"               = "integrates-cluster"
    "Environment"        = "production"
    "GithubRepo"         = "terraform-aws-eks"
    "GithubOrg"          = "terraform-aws-modules"
    "management:type"    = "production"
    "management:product" = "integrates"
  }

  vpc_id = var.fluid_vpc_id

  worker_groups = [
    {
      name                 = "large"
      instance_type        = "m5a.large"
      asg_min_size         = 10
      asg_desired_capacity = 10
      asg_max_size         = 10
      root_volume_type     = "gp2"
      root_volume_size     = "50"
      kubelet_extra_args   = "--node-labels=worker_group=large"
    },
    {
      name                 = "xlarge"
      instance_type        = "m5a.xlarge"
      asg_min_size         = 6
      asg_desired_capacity = 6
      asg_max_size         = 6
      root_volume_type     = "gp2"
      root_volume_size     = "50"
      kubelet_extra_args   = "--node-labels=worker_group=xlarge"
    },
  ]

  map_roles    = var.map_roles
  map_users    = var.map_users
  map_accounts = var.map_accounts
}
