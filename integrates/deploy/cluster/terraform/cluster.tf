module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.17"

  subnets = [
    aws_subnet.region_a.id,
    aws_subnet.region_b.id,
    aws_subnet.region_d.id,
  ]

  tags = {
    Environment = "production"
    GithubRepo  = "terraform-aws-eks"
    GithubOrg   = "terraform-aws-modules"
  }

  vpc_id = var.fluid_vpc_id

  worker_groups = [
    {
      name                 = "small"
      instance_type        = "t3.small"
      asg_min_size         = 2
      asg_desired_capacity = 2
      asg_max_size         = 2
      root_volume_type     = "gp2"
      root_volume_size     = "80"
    },
  ]

  map_roles    = var.map_roles
  map_users    = var.map_users
  map_accounts = var.map_accounts
}
