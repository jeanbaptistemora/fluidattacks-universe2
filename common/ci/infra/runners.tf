locals {
  runners = {
    airs-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["airs-small"] },
      )
      workers = merge(
        local.config.small.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "airs" },
      )
    }
    airs-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["airs-large"] },
      )
      workers = merge(
        local.config.large.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "airs" },
      )
    }
    common-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["common-small"] },
      )
      workers = merge(
        local.config.small.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "common" },
      )
    }
    common-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["common-large"] },
      )
      workers = merge(
        local.config.large.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "common" },
      )
    }
    docs-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["docs-small"] },
      )
      workers = merge(
        local.config.small.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "docs" },
      )
    }
    docs-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["docs-large"] },
      )
      workers = merge(
        local.config.large.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "docs" },
      )
    }
    integrates-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["integrates-small"] },
      )
      workers = merge(
        local.config.small.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "integrates" },
      )
    }
    integrates-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["integrates-large"] },
      )
      workers = merge(
        local.config.large.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "integrates" },
      )
    }
    melts-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["melts-small"] },
      )
      workers = merge(
        local.config.small.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "melts" },
      )
    }
    melts-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["melts-large"] },
      )
      workers = merge(
        local.config.large.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "melts" },
      )
    }
    observes-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["observes-small"] },
      )
      workers = merge(
        local.config.small.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "observes" },
      )
    }
    observes-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["observes-large"] },
      )
      workers = merge(
        local.config.large.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "observes" },
      )
    }
    reviews-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["reviews-small"] },
      )
      workers = merge(
        local.config.small.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "reviews" },
      )
    }
    reviews-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["reviews-large"] },
      )
      workers = merge(
        local.config.large.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "reviews" },
      )
    }
    skims-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["skims-small"] },
      )
      workers = merge(
        local.config.small.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "skims" },
      )
    }
    skims-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["skims-large"] },
      )
      workers = merge(
        local.config.large.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "skims" },
      )
    }
    sorts-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["sorts-small"] },
      )
      workers = merge(
        local.config.small.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "sorts" },
      )
    }
    sorts-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["sorts-large"] },
      )
      workers = merge(
        local.config.large.workers,
        { idle-count = 0 }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "sorts" },
      )
    }
    small = {
      replicas = 4
      runner = merge(
        local.config.small.runner,
        { tags = ["small"] },
      )
      workers = merge(
        local.config.small.workers,
        { idle-count = 32 }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "common" },
      )
    }
    large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["large"] },
      )
      workers = merge(
        local.config.large.workers,
        { idle-count = 8 }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "common" },
      )
    }
  }
  config = {
    small = {
      replicas = 0
      runner = {
        instance   = "m5a.large"
        version    = "15.9.1"
        ami        = "ami-08a127d31bb7fa804"
        monitoring = true
        user-data  = ""

        disk-size      = 15
        disk-type      = "gp3"
        disk-optimized = true

        docker-machine-version = "0.16.2-gitlab.15"
        docker-machine-options = []

        tags = []
      }
      workers = {
        instance   = "c5ad.large"
        ami        = "ami-07dc2dd8e0efbc46a"
        user-data  = local.user-data.ephemeral-disk
        monitoring = false
        limit      = 1000

        idle-count = 0
        idle-time  = 1800

        disk-size      = 10
        disk-type      = "gp3"
        disk-optimized = true
      }
      tags = {
        "management:area" = "innovation"
        "management:type" = "product"
      }
    }
    large = {
      replicas = 0
      runner = {
        instance   = "m5a.large"
        version    = "15.9.1"
        ami        = "ami-08a127d31bb7fa804"
        monitoring = true
        user-data  = ""

        disk-size      = 15
        disk-type      = "gp3"
        disk-optimized = true

        docker-machine-version = "0.16.2-gitlab.15"
        docker-machine-options = []

        tags = []
      }
      workers = {
        instance   = "m5d.large"
        ami        = "ami-07dc2dd8e0efbc46a"
        user-data  = local.user-data.ephemeral-disk
        monitoring = false
        limit      = 1000

        idle-count = 0
        idle-time  = 1800

        disk-size      = 10
        disk-type      = "gp3"
        disk-optimized = true
      }
      tags = {
        "management:area" = "innovation"
        "management:type" = "product"
      }
    }
  }
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
}

module "runners" {
  source  = "npalm/gitlab-runner/aws"
  version = "5.9.1"
  for_each = merge([
    for name, values in local.runners : {
      for replica in range(values.replicas) : "${name}-${replica}" => values
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
  runner_instance_ebs_optimized     = each.value.runner.disk-optimized
  userdata_pre_install              = each.value.runner.user-data
  docker_machine_version            = each.value.runner.docker-machine-version
  docker_machine_options = concat(
    ["engine-install-url='https://releases.rancher.com/install-docker/20.10.21.sh'"],
    each.value.runner.docker-machine-options,
  )
  ami_filter = {
    image-id = [each.value.runner.ami]
  }
  runner_root_block_device = {
    delete_on_termination = true
    encrypted             = true
    volume_type           = each.value.runner.disk-type
    volume_size           = each.value.runner.disk-size
  }
  gitlab_runner_registration_config = {
    registration_token = var.gitlabRunnerToken
    tag_list           = join(",", each.value.runner.tags)
    description        = "ci-${each.key}"
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
  runners_max_builds               = 30
  runners_name                     = "ci-${each.key}"
  runners_output_limit             = 8192
  runners_privileged               = false
  runners_pull_policy              = "always"
  runners_request_spot_instance    = true
  runners_use_private_address      = false
  subnet_id_runners                = data.aws_subnet.main.id
  runners_idle_time                = each.value.workers.idle-time
  runners_idle_count               = each.value.workers.idle-count / each.value.replicas
  runners_limit                    = each.value.workers.limit / each.value.replicas
  runners_concurrent               = each.value.workers.limit / each.value.replicas
  runners_request_concurrency      = each.value.workers.limit / each.value.replicas / 2
  runners_monitoring               = each.value.workers.monitoring
  docker_machine_instance_type     = each.value.workers.instance
  runners_root_size                = each.value.workers.disk-size
  runners_volume_type              = each.value.workers.disk-type
  runners_ebs_optimized            = each.value.workers.disk-optimized
  runners_userdata                 = each.value.workers.user-data
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
  environment = "ci-${each.key}"
  overrides = {
    name_runner_agent_instance  = "ci-runner-${each.key}",
    name_docker_machine_runners = "ci-worker-${each.key}",
    name_sg                     = "",
    name_iam_objects            = "",
  }
  tags = each.value.tags
}
