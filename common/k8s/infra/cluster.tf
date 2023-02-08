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
    ci = {
      max_size = 450

      instance_types = ["c5ad.large"]

      iam_role_additional_policies = {
        ci_cache = module.ci_cache.policy_arn
        ssm_core = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
        ssm_role = "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
      }

      block_device_mappings = {
        xvda = {
          device_name = "/dev/xvda"
          ebs = {
            volume_size           = 15
            volume_type           = "gp3"
            encrypted             = true
            delete_on_termination = true
          }
        }
      }
      enable_bootstrap_user_data = true
      pre_bootstrap_user_data    = <<-EOT
        Content-Type: multipart/mixed; boundary="==BOUNDARY=="
        MIME-Version: 1.0

        --==BOUNDARY==
        Content-Type: text/x-shellscript; charset="us-ascii"

        #!/bin/bash

        # Install dependencies
        yum install -y parted

        # Make disk gpt and create partitions
        parted /dev/nvme1n1 --script -- mklabel gpt
        parted -a optimal /dev/nvme1n1 mkpart primary 0% 100%

        # Wait for partition to be visible
        sleep 1

        # Make partitions xfs
        mkfs -t xfs /dev/nvme1n1p1

        # Mount partitions
        service containerd stop
        mkdir -p /run/containerd
        mount /dev/nvme1n1p1 /run/containerd
        service containerd start

        --==BOUNDARY==--
      EOT

      labels = {
        worker_group = "ci"
      }

      tags = {
        "management:area"    = "innovation"
        "management:product" = "common"
        "management:type"    = "product"
      }
    }
    dev = {
      max_size = 100

      instance_types = [
        "m5.xlarge",
        "m5a.xlarge",
        "m5d.xlarge",
        "m5ad.xlarge",
      ]

      iam_role_additional_policies = {
        ssm_core = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
        ssm_role = "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
      }

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

      tags = {
        "management:area"    = "innovation"
        "management:product" = "integrates"
        "management:type"    = "product"
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

      iam_role_additional_policies = {
        ssm_core = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
        ssm_role = "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
      }

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

      tags = {
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
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
