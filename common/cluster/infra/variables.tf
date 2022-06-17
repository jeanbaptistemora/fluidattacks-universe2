variable "kubeConfig" {}

data "aws_security_group" "cloudflare" {
  name = "CloudFlare"
}

locals {
  cluster_name = "common"
}

data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "main" {
  for_each = toset([
    "k8s_1",
    "k8s_2",
    "k8s_3",
  ])

  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = [each.key]
  }
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
      rolearn  = "arn:aws:iam::205810638802:role/dev"
      username = "dev"
      groups   = ["system:masters"]
    },
    {
      rolearn  = "arn:aws:iam::205810638802:role/prod_integrates"
      username = "prod_integrates"
      groups   = ["system:masters"]
    },
    {
      rolearn  = "arn:aws:iam::205810638802:role/prod_common"
      username = "prod_common"
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
      userarn  = "arn:aws:iam::205810638802:user/dev"
      username = "dev"
      groups   = ["system:masters"]
    },
    {
      userarn  = "arn:aws:iam::205810638802:user/prod_integrates"
      username = "prod_integrates"
      groups   = ["system:masters"]
    },
    {
      userarn  = "arn:aws:iam::205810638802:user/prod_common"
      username = "prod_common"
      groups   = ["system:masters"]
    },
  ]
}
variable "map_accounts" {
  description = "Additional AWS account numbers to add to the aws-auth configmap."
  type        = list(string)

  default = [
    "205810638802",
  ]
}
