module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 14.0.0"
  cluster_name    = var.cluster_name
  cluster_version = "1.17"
  enable_irsa     = true

  subnets = [
    aws_subnet.region_a.id,
    aws_subnet.region_b.id,
    aws_subnet.region_d.id,
  ]

  worker_additional_security_group_ids = [
    data.aws_security_group.cloudflare.id
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
      name                 = "ephemeral"
      instance_type        = "m5a.large"
      asg_min_size         = 5
      asg_desired_capacity = 11
      asg_max_size         = 11
      root_volume_type     = "gp2"
      root_volume_size     = "50"
      kubelet_extra_args   = "--node-labels=worker_group=ephemeral"
    },
    {
      name                 = "production"
      instance_type        = "m5a.large"
      asg_min_size         = 5
      asg_desired_capacity = 11
      asg_max_size         = 11
      root_volume_type     = "gp2"
      root_volume_size     = "50"
      kubelet_extra_args   = "--node-labels=worker_group=production"
    },
  ]

  worker_groups_launch_template = [
    {
      name                    = "development"
      override_instance_types = ["m5.xlarge", "m5a.xlarge", "m5d.xlarge", "m5ad.xlarge"]
      kubelet_extra_args      = "--node-labels=node.kubernetes.io/lifecycle=spot"
      kubelet_extra_args      = "--node-labels=worker_group=development"
      public_ip               = true

      asg_min_size         = 5
      asg_desired_capacity = 11
      asg_max_size         = 11

      root_volume_type = "gp3"
      root_volume_size = 50
      root_encrypted   = true
      ebs_optimized    = true

      spot_allocation_strategy = "lowest-price"
      spot_instance_pools      = 5
      spot_max_price           = "" # Defaults to on-demand price
    },
  ]

  map_roles    = var.map_roles
  map_users    = var.map_users
  map_accounts = var.map_accounts
}
