module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.14.0"

  name            = "fluid-cluster-vpc"
  cidr            = "10.0.0.0/16"
  azs             = var.availability-zone-names
  private_subnets = ["10.0.0.0/19", "10.0.32.0/19", "10.0.64.0/19"]

  tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}
