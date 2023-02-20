locals {
  runners = {
    small = {
      runner = {
        version  = "15.4.0"
        replicas = 4
        tags     = ["small"]
      }
      workers = {
        instance  = "c5ad.large"
        root_size = 10
        docker_machine_options = [
          "amazonec2-volume-type=gp3",
          "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
          "engine-install-url='https://releases.rancher.com/install-docker/20.10.21.sh'",
        ]
        idle = {
          count = 5
          time  = 1800
        }
      }
    }
    large = {
      runner = {
        version  = "15.4.0"
        replicas = 1
        tags     = ["large"]
      }
      workers = {
        instance  = "m5d.large"
        root_size = 10
        docker_machine_options = [
          "amazonec2-volume-type=gp3",
          "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
          "engine-install-url='https://releases.rancher.com/install-docker/20.10.21.sh'",
        ]
        idle = {
          count = 5
          time  = 1800
        }
      }
    }
  }
}

module "runners" {
  source  = "npalm/gitlab-runner/aws"
  version = "5.1.0"
  for_each = merge([
    for name, values in local.runners : {
      for replica in range(values.runner.replicas) : "${name}_${replica}" => values
    }
  ]...)

  # AWS
  # https://gitlab.com/gitlab-org/gitlab-runner/-/tags?sort=version_desc
  aws_region                             = "us-east-1"
  vpc_id                                 = data.aws_vpc.main.id
  allow_iam_service_linked_role_creation = true
  enable_kms                             = true
  kms_deletion_window_in_days            = 30
  enable_manage_gitlab_token             = true
  enable_cloudwatch_logging              = false
  ami_filter = {
    "name" = ["amzn2-ami-hvm-2.0.20210721.2-x86_64-ebs"]
  }

  # Cache
  cache_shared = true
  cache_bucket = {
    create = false
    policy = module.cache.policy_arn
    bucket = module.cache.bucket
  }

  # Runner
  instance_type                     = "c5a.large"
  gitlab_runner_version             = each.value.runner.version
  enable_runner_ssm_access          = true
  subnet_ids_gitlab_runner          = [data.aws_subnet.main.id]
  runner_instance_ebs_optimized     = true
  runner_instance_enable_monitoring = true
  userdata_pre_install              = data.local_file.init_runner.content
  runner_ami_filter = {
    "name"     = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20210907"]
    "image-id" = ["ami-03a80f322a6053f85"]
  }
  runner_root_block_device = {
    delete_on_termination = true
    volume_type           = "gp3"
    volume_size           = 15
    encrypted             = true
    iops                  = 3000
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
  docker_machine_options           = each.value.workers.docker_machine_options
  docker_machine_spot_price_bid    = ""
  docker_machine_instance_type     = each.value.workers.instance
  runners_gitlab_url               = "https://gitlab.com"
  runners_executor                 = "docker+machine"
  runners_root_size                = each.value.workers.root_size
  runners_concurrent               = 1000
  runners_ebs_optimized            = true
  runners_idle_count               = each.value.workers.idle.count
  runners_idle_time                = each.value.workers.idle.time
  runners_image                    = "docker"
  runners_limit                    = 1000
  runners_max_builds               = 30
  runners_monitoring               = false
  runners_name                     = "common-ci-${each.key}"
  runners_output_limit             = 8192
  runners_privileged               = false
  runners_pull_policy              = "always"
  runners_request_concurrency      = 100
  runners_request_spot_instance    = true
  runners_use_private_address      = false
  subnet_id_runners                = data.aws_subnet.main.id
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
