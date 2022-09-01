locals {
  runners = {
    small = {
      awsRole      = ""
      access_level = "not_protected"
      root_size    = 10
      replicas     = 3
      instance     = "c5ad.large"
      tags         = ["small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    large = {
      awsRole      = ""
      access_level = "not_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
    dev_small = {
      awsRole      = "dev"
      access_level = "not_protected"
      root_size    = 10
      replicas     = 3
      instance     = "c5ad.large"
      tags         = ["dev_small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    dev_large = {
      awsRole      = "dev"
      access_level = "not_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["dev_large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
    prod_airs_small = {
      awsRole      = "prod_airs"
      access_level = "ref_protected"
      root_size    = 10
      replicas     = 1
      instance     = "c5ad.large"
      tags         = ["prod_airs_small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    prod_airs_large = {
      awsRole      = "prod_airs"
      access_level = "ref_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["prod_airs_large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
    prod_common_small = {
      awsRole      = "prod_common"
      access_level = "ref_protected"
      root_size    = 10
      replicas     = 1
      instance     = "c5ad.large"
      tags         = ["prod_common_small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    prod_common_large = {
      awsRole      = "prod_common"
      access_level = "ref_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["prod_common_large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
    prod_docs_small = {
      awsRole      = "prod_docs"
      access_level = "ref_protected"
      root_size    = 10
      replicas     = 1
      instance     = "c5ad.large"
      tags         = ["prod_docs_small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    prod_docs_large = {
      awsRole      = "prod_docs"
      access_level = "ref_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["prod_docs_large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
    prod_forces_small = {
      awsRole      = "prod_forces"
      access_level = "ref_protected"
      root_size    = 10
      replicas     = 1
      instance     = "c5ad.large"
      tags         = ["prod_forces_small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    prod_forces_large = {
      awsRole      = "prod_forces"
      access_level = "ref_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["prod_forces_large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
    prod_integrates_small = {
      awsRole      = "prod_integrates"
      access_level = "ref_protected"
      root_size    = 10
      replicas     = 1
      instance     = "c5ad.large"
      tags         = ["prod_integrates_small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    prod_integrates_large = {
      awsRole      = "prod_integrates"
      access_level = "ref_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["prod_integrates_large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
    prod_melts_small = {
      awsRole      = "prod_melts"
      access_level = "ref_protected"
      root_size    = 10
      replicas     = 1
      instance     = "c5ad.large"
      tags         = ["prod_melts_small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    prod_melts_large = {
      awsRole      = "prod_melts"
      access_level = "ref_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["prod_melts_large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
    prod_observes_small = {
      awsRole      = "prod_observes"
      access_level = "ref_protected"
      root_size    = 10
      replicas     = 1
      instance     = "c5ad.large"
      tags         = ["prod_observes_small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    prod_observes_large = {
      awsRole      = "prod_observes"
      access_level = "ref_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["prod_observes_large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
    prod_skims_small = {
      awsRole      = "prod_skims"
      access_level = "ref_protected"
      root_size    = 10
      replicas     = 1
      instance     = "c5ad.large"
      tags         = ["prod_skims_small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    prod_skims_large = {
      awsRole      = "prod_skims"
      access_level = "ref_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["prod_skims_large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
    prod_sorts_small = {
      awsRole      = "prod_sorts"
      access_level = "ref_protected"
      root_size    = 10
      replicas     = 1
      instance     = "c5ad.large"
      tags         = ["prod_sorts_small"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
        "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
      ]
    }
    prod_sorts_large = {
      awsRole      = "prod_sorts"
      access_level = "ref_protected"
      root_size    = 35
      replicas     = 1
      instance     = "m5a.large"
      tags         = ["prod_sorts_large"]
      docker_machine_options = [
        "amazonec2-volume-type=gp3",
      ]
    }
  }
}

module "runners" {
  source  = "npalm/gitlab-runner/aws"
  version = "5.1.0"
  for_each = merge([
    for name, values in local.runners : {
      for replica in range(values.replicas) : "${name}_${replica}" => values
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
  enable_runner_ssm_access          = true
  subnet_ids_gitlab_runner          = [data.aws_subnet.main.id]
  runner_instance_ebs_optimized     = true
  runner_instance_enable_monitoring = true
  userdata_pre_install              = data.local_file.init_runner.content
  runner_iam_policy_arns = each.value.awsRole != "" ? [
    "arn:aws:iam::${data.aws_caller_identity.main.account_id}:policy/${each.value.awsRole}"
  ] : []
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
    registration_token = var.gitlabTokenFluidattacks
    tag_list           = join(",", each.value.tags)
    description        = "common-ci-${each.key}"
    locked_to_project  = "true"
    run_untagged       = "false"
    maximum_timeout    = "86400"
    access_level       = each.value.access_level
  }

  # Workers
  docker_machine_options            = each.value.docker_machine_options
  docker_machine_spot_price_bid     = ""
  docker_machine_instance_type      = each.value.instance
  runners_gitlab_url                = "https://gitlab.com"
  runners_executor                  = "docker+machine"
  runners_root_size                 = each.value.root_size
  runners_concurrent                = 1000
  runners_ebs_optimized             = true
  runners_idle_count                = 3
  runners_idle_time                 = 1800
  runners_image                     = "docker"
  runners_limit                     = 1000
  runners_max_builds                = 30
  runners_monitoring                = false
  runners_name                      = "common-ci-${each.key}"
  runners_output_limit              = 4096
  runners_privileged                = false
  runners_pull_policy               = "always"
  runners_request_concurrency       = 10
  runners_request_spot_instance     = true
  runners_use_private_address       = false
  subnet_id_runners                 = data.aws_subnet.main.id
  runners_iam_instance_profile_name = each.value.awsRole
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
    "Management:Area"    = "innovation"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}
