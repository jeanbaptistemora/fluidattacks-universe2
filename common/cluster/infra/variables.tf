locals {
  cluster_accounts = ["205810638802"]
  cluster_name     = "common"
  cluster_security_groups = {
    master = {
      egress_nodes_all = {
        description                = "Cluster to node all ports/protocols"
        protocol                   = "-1"
        from_port                  = 0
        to_port                    = 0
        type                       = "egress"
        source_node_security_group = true
      }
    }
    nodes = {
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
  }
  cluster_roles = [
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
  cluster_users = [
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

data "aws_security_group" "cloudflare" {
  name = "CloudFlare"
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
