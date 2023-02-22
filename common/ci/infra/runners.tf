locals {
  user-data = {
    ephemeral-disk = <<-EOT
      Content-Type: multipart/mixed; boundary="==BOUNDARY=="
      MIME-Version: 1.0

      --==BOUNDARY==
      Content-Type: text/cloud-config; charset="us-ascii"
      MIME-Version: 1.0
      Content-Transfer-Encoding: 7bit
      Content-Disposition: attachment; filename="cloud-config.txt"

      disk_setup:
        /dev/nvme1n1:
          table_type: mbr
          layout: true
          overwrite: true

      fs_setup:
        - label: nvme
          filesystem: ext4
          device: /dev/nvme1n1
          partition: auto
          overwrite: true

      mounts:
        - [/dev/nvme1n1, /var/lib/docker]

      --==BOUNDARY==--
    EOT
  }
  runners = {
    small = {
      runner = {
        replicas   = 1
        instance   = "m5a.large"
        version    = "15.9.1"
        ami        = "ami-08a127d31bb7fa804"
        monitoring = true
        user-data  = ""
        disk = {
          size      = 15
          type      = "gp3"
          optimized = true
        }
        docker-machine = {
          version = "0.16.2-gitlab.15"
          options = []
        }
        tags = ["small"]
      }
      workers = {
        instance   = "c5ad.large"
        ami        = "ami-07dc2dd8e0efbc46a"
        user-data  = local.user-data.ephemeral-disk
        monitoring = false
        idle = {
          count = 32
          time  = 1800
        }
        disk = {
          size      = 10
          type      = "gp3"
          optimized = true
        }
      }
    }
    large = {
      runner = {
        replicas   = 1
        instance   = "m5a.large"
        version    = "15.9.1"
        ami        = "ami-08a127d31bb7fa804"
        monitoring = true
        user-data  = ""
        disk = {
          size      = 15
          type      = "gp3"
          optimized = true
        }
        docker-machine = {
          version = "0.16.2-gitlab.15"
          options = []
        }
        tags = ["large"]
      }
      workers = {
        instance   = "m5d.large"
        ami        = "ami-07dc2dd8e0efbc46a"
        user-data  = local.user-data.ephemeral-disk
        monitoring = false
        idle = {
          count = 8
          time  = 1800
        }
        disk = {
          size      = 10
          type      = "gp3"
          optimized = true
        }
      }
    }
  }
}

module "runners" {
  source  = "npalm/gitlab-runner/aws"
  version = "5.9.1"
  for_each = merge([
    for name, values in local.runners : {
      for replica in range(values.runner.replicas) : "${name}-${replica}" => values
    }
  ]...)

  # AWS
  aws_region                             = "us-east-1"
  vpc_id                                 = data.aws_vpc.main.id
  allow_iam_service_linked_role_creation = true
  enable_kms                             = true
  kms_deletion_window_in_days            = 30
  enable_manage_gitlab_token             = true
  enable_cloudwatch_logging              = false

  # Runner
  enable_runner_ssm_access          = true
  subnet_ids_gitlab_runner          = [data.aws_subnet.main.id]
  instance_type                     = each.value.runner.instance
  gitlab_runner_version             = each.value.runner.version
  runner_instance_enable_monitoring = each.value.runner.monitoring
  runner_instance_ebs_optimized     = each.value.runner.disk.optimized
  userdata_pre_install              = each.value.runner.user-data
  docker_machine_version            = each.value.runner.docker-machine.version
  docker_machine_options = concat(
    ["engine-install-url='https://releases.rancher.com/install-docker/20.10.21.sh'"],
    each.value.runner.docker-machine.options,
  )
  ami_filter = {
    image-id = [each.value.runner.ami]
  }
  runner_root_block_device = {
    delete_on_termination = true
    encrypted             = true
    volume_type           = each.value.runner.disk.type
    volume_size           = each.value.runner.disk.size
  }
  gitlab_runner_registration_config = {
    registration_token = var.gitlabRunnerToken
    tag_list           = join(",", each.value.runner.tags)
    description        = "common-ci-${each.key}"
    locked_to_project  = "true"
    run_untagged       = "false"
    maximum_timeout    = "86400"
    access_level       = "not_protected"
  }

  # Workers
  enable_docker_machine_ssm_access = true
  docker_machine_spot_price_bid    = ""
  runners_gitlab_url               = "https://gitlab.com"
  runners_executor                 = "docker+machine"
  runners_limit                    = 1000
  runners_max_builds               = 30
  runners_concurrent               = 1000
  runners_name                     = "common-ci-${each.key}"
  runners_output_limit             = 8192
  runners_privileged               = false
  runners_pull_policy              = "always"
  runners_request_concurrency      = 500
  runners_request_spot_instance    = true
  runners_use_private_address      = false
  subnet_id_runners                = data.aws_subnet.main.id
  runners_monitoring               = each.value.workers.monitoring
  docker_machine_instance_type     = each.value.workers.instance
  runners_root_size                = each.value.workers.disk.size
  runners_volume_type              = each.value.workers.disk.type
  runners_ebs_optimized            = each.value.workers.disk.optimized
  runners_userdata                 = each.value.workers.user-data
  runners_idle_count               = each.value.workers.idle.count
  runners_idle_time                = each.value.workers.idle.time
  runner_ami_filter = {
    image-id = [each.value.workers.ami]
  }
  runners_machine_autoscaling = [
    {
      periods = [
        "* * 0-6,20-23 * * mon-fri *",
        "* * * * * sat,sun *",
      ]
      idle_count = 0
      idle_time  = 1800
      timezone   = "America/Bogota"
    }
  ]

  # Cache
  cache_shared = true
  cache_bucket = {
    create = false
    policy = module.cache.policy_arn
    bucket = module.cache.bucket
  }

  # Tags
  environment = "common-ci-${each.key}"
  overrides = {
    name_runner_agent_instance  = "common-ci-runner-${each.key}",
    name_docker_machine_runners = "common-ci-worker-${each.key}",
    name_sg                     = "",
    name_iam_objects            = "",
  }
  tags = {
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
