data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "newrelic_license_key" {}
variable "cloudflare_api_token" {}

data "cloudflare_zones" "fluidattacks_com" {
  filter {
    name = "fluidattacks.com"
  }
}
data "aws_security_group" "cloudflare" {
  name = "CloudFlare"
}
data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}
data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}
variable "region" {
  default = "us-east-1"
}
variable "fluid_vpc_id" {
  default = "vpc-0ea1c7bd6be683d2d"
}
variable "cluster_name" {
  default = "integrates-cluster"
}
variable "external_dns_version" {
  default = "1.1.7"
}

variable "map_accounts" {
  description = "Additional AWS account numbers to add to the aws-auth configmap."
  type        = list(string)

  default = [
    "205810638802",
  ]
}
variable "map_roles" {
  description = "Additional IAM roles to add to the aws-auth configmap."
  type = list(object({
    rolearn  = string
    username = string
    groups   = list(string)
  }))

  default = [
    {
      rolearn  = "arn:aws:iam::205810638802:role/integrates-prod"
      username = "role-integrates-prod"
      groups   = ["system:masters"]
    },
    {
      rolearn  = "arn:aws:iam::205810638802:role/integrates-dev"
      username = "role-integrates-dev"
      groups   = ["system:masters"]
    },
  ]
}

variable "map_users" {
  description = "Additional IAM users to add to the aws-auth configmap."
  type = list(object({
    userarn  = string
    username = string
    groups   = list(string)
  }))

  default = [
    {
      userarn  = "arn:aws:iam::205810638802:user/user-provision/serves-prod"
      username = "user-serves-prod"
      groups   = ["system:masters"]
    },
    {
      userarn  = "arn:aws:iam::205810638802:user/user-provision/serves-dev"
      username = "user-serves-dev"
      groups   = ["system:masters"]
    },
    {
      userarn  = "arn:aws:iam::205810638802:user/user-provision/integrates-prod"
      username = "user-integrates-prod"
      groups   = ["system:masters"]
    },
    {
      userarn  = "arn:aws:iam::205810638802:user/user-provision/integrates-dev"
      username = "user-integrates-dev"
      groups   = ["system:masters"]
    },
  ]
}
