data "aws_caller_identity" "current" {}
data "aws_availability_zones" "available" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}
data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}
variable "region" {
  default = "us-east-1"
}
variable "vpc_id" {
  default = "vpc-0ea1c7bd6be683d2d"
}
variable "cluster_name" {
  default = "integrates-cluster"
}

variable "map_accounts" {
  description = "Additional AWS account numbers to add to the aws-auth configmap."
  type        = list(string)

  default = [
    data.aws_caller_identity.current.account_id,
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
      rolearn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/integrates-prod"
      username = "role-integrates-prod"
      groups   = ["system:masters"]
    },
    {
      rolearn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/integrates-dev"
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
      userarn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/integrates-prod"
      username = "user-integrates-prod"
      groups   = ["system:masters"]
    },
    {
      userarn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/integrates-dev"
      username = "user-integrates-dev"
      groups   = ["system:masters"]
    },
  ]
}
