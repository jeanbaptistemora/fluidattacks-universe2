module "cluster" {
  source                          = "terraform-aws-modules/eks/aws"
  version                         = "19.6.0"
  cluster_name                    = local.cluster_name
  cluster_version                 = "1.24"
  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = false
  enable_irsa                     = true

  # Nodes
  eks_managed_node_group_defaults = {
    capacity_type          = "SPOT"
    force_update_version   = true
    ebs_optimized          = true
    enable_monitoring      = true
    vpc_security_group_ids = [data.aws_security_group.cloudflare.id]
  }
  eks_managed_node_groups = {
    dev = {
      max_size = 100

      instance_types = [
        "m5.xlarge",
        "m5a.xlarge",
        "m5d.xlarge",
        "m5ad.xlarge",
      ]

      block_device_mappings = {
        xvda = {
          device_name = "/dev/xvda"
          ebs = {
            volume_size           = 35
            volume_type           = "gp3"
            encrypted             = true
            delete_on_termination = true
          }
        }
      }

      labels = {
        worker_group = "dev"
      }
    }
    prod_integrates = {
      max_size = 120

      instance_types = [
        "m5.large",
        "m5a.large",
        "m5d.large",
        "m5ad.large",
      ]

      block_device_mappings = {
        xvda = {
          device_name = "/dev/xvda"
          ebs = {
            volume_size           = 20
            volume_type           = "gp3"
            encrypted             = true
            delete_on_termination = true
          }
        }
      }

      labels = {
        worker_group = "prod_integrates"
      }
    }
  }

  # Network
  vpc_id     = data.aws_vpc.main.id
  subnet_ids = [for subnet in data.aws_subnet.main : subnet.id]

  # Auth
  manage_aws_auth_configmap = true
  aws_auth_accounts         = [data.aws_caller_identity.main.account_id]
  aws_auth_roles = concat(
    [
      for admin in local.admins : {
        rolearn  = data.aws_iam_role.main[admin].arn
        username = admin
        groups   = ["system:masters"]
      }
    ],
    [
      for user in local.users : {
        rolearn  = data.aws_iam_role.main[user].arn
        username = user
        groups   = distinct(["dev", user])
      }
    ],
  )

  # Encryption
  create_kms_key          = true
  enable_kms_key_rotation = true
  kms_key_aliases         = [local.cluster_name]
  kms_key_owners = [
    for admin in local.admins : data.aws_iam_role.main[admin].arn
  ]
  kms_key_administrators = [
    for user in local.users : data.aws_iam_role.main[user].arn
  ]

  tags = {
    "Name"               = local.cluster_name
    "Environment"        = "production"
    "GithubRepo"         = "terraform-aws-eks"
    "GithubOrg"          = "terraform-aws-modules"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
