module "fluidattacks_ci_cache" {
  source  = "npalm/gitlab-runner/aws//modules/cache"
  version = "4.30.0"

  environment             = "fluidattacks-ci-cache"
  cache_bucket_versioning = false
  cache_expiration_days   = 30
  cache_lifecycle_clear   = true
  create_cache_bucket     = true

  cache_bucket_name_include_account_id = false
  cache_lifecycle_prefix               = "fluidattacks-ci-cache"
  cache_bucket_prefix                  = "fluidattacks-ci-cache"

  tags = {
    "Name"            = "fluidattacks-ci-cache"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

module "fluidattacks_ci" {
  source   = "npalm/gitlab-runner/aws"
  version  = "4.30.0"
  for_each = toset(["1", "2", "3"])

  # AWS
  aws_region                             = "us-east-1"
  vpc_id                                 = var.autostaling_ci_vpc_id
  allow_iam_service_linked_role_creation = true
  enable_kms                             = true
  kms_deletion_window_in_days            = 30
  enable_manage_gitlab_token             = true
  enable_cloudwatch_logging              = false
  ami_filter                             = var.runner_ami

  # Cache
  cache_shared = true
  cache_bucket = {
    create = false
    policy = module.fluidattacks_ci_cache.policy_arn
    bucket = module.fluidattacks_ci_cache.bucket
  }

  # Runner
  instance_type                     = "c5a.large"
  runner_ami_filter                 = var.worker_ami
  enable_runner_ssm_access          = true
  enable_gitlab_runner_ssh_access   = false
  subnet_ids_gitlab_runner          = [var.autoscaling_ci_subnet_id]
  runner_instance_ebs_optimized     = true
  runner_instance_enable_monitoring = true
  runner_root_block_device          = var.runner_block_device
  userdata_pre_install              = data.local_file.init_runner.content
  gitlab_runner_registration_config = {
    registration_token = var.gitlabTokenFluidattacks
    tag_list           = "autoscaling"
    description        = "fluidattacks-ci-${each.key}"
    locked_to_project  = "true"
    run_untagged       = "false"
    maximum_timeout    = var.runner_timeout
    access_level       = "not_protected"
  }

  # Workers
  docker_machine_options = [
    "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
    "amazonec2-volume-type=gp3",
  ]
  docker_machine_spot_price_bid = ""
  docker_machine_instance_type  = "c5ad.large"
  runners_gitlab_url            = "https://gitlab.com"
  runners_executor              = "docker+machine"
  runners_root_size             = 10
  runners_concurrent            = 1000
  runners_ebs_optimized         = true
  runners_idle_count            = 3
  runners_idle_time             = 1800
  runners_image                 = "docker"
  runners_limit                 = 1000
  runners_max_builds            = 15
  runners_monitoring            = false
  runners_name                  = "fluidattacks-ci-${each.key}"
  runners_output_limit          = 4096
  runners_privileged            = false
  runners_pull_policy           = "always"
  runners_request_concurrency   = 10
  runners_request_spot_instance = true
  runners_use_private_address   = false
  runners_machine_autoscaling   = var.off_peak_periods
  subnet_id_runners             = var.autoscaling_ci_subnet_id

  # Tags
  environment = "makes-fluidattacks-ci-${each.key}"
  overrides = {
    name_runner_agent_instance  = "fluidattacks-ci-runner-${each.key}",
    name_docker_machine_runners = "fluidattacks-ci-worker-${each.key}",
    name_sg                     = "",
    name_iam_objects            = "",
  }
  tags = {
    "management:area" = "cost"
    "management:type" = "product"
  }
}

module "fluidattacks_ci_large" {
  source   = "npalm/gitlab-runner/aws"
  version  = "4.30.0"
  for_each = toset(["1"])

  # AWS
  aws_region                             = "us-east-1"
  vpc_id                                 = var.autostaling_ci_vpc_id
  allow_iam_service_linked_role_creation = true
  enable_kms                             = true
  kms_deletion_window_in_days            = 30
  enable_manage_gitlab_token             = true
  enable_cloudwatch_logging              = false
  ami_filter                             = var.runner_ami

  # Cache
  cache_shared = true
  cache_bucket = {
    create = false
    policy = module.fluidattacks_ci_cache.policy_arn
    bucket = module.fluidattacks_ci_cache.bucket
  }

  # Runner
  instance_type                     = "c5a.large"
  runner_ami_filter                 = var.worker_ami
  enable_runner_ssm_access          = true
  enable_gitlab_runner_ssh_access   = false
  subnet_ids_gitlab_runner          = [var.autoscaling_ci_subnet_id]
  runner_instance_ebs_optimized     = true
  runner_instance_enable_monitoring = true
  runner_root_block_device          = var.runner_block_device
  userdata_pre_install              = data.local_file.init_runner.content
  gitlab_runner_registration_config = {
    registration_token = var.gitlabTokenFluidattacks
    tag_list           = "autoscaling-large"
    description        = "fluidattacks-ci-large-${each.key}"
    locked_to_project  = "true"
    run_untagged       = "false"
    maximum_timeout    = var.runner_timeout
    access_level       = "not_protected"
  }

  # Workers
  docker_machine_options = [
    "amazonec2-volume-type=gp3",
  ]
  docker_machine_spot_price_bid = ""
  docker_machine_instance_type  = "m5a.large"
  runners_gitlab_url            = "https://gitlab.com"
  runners_executor              = "docker+machine"
  runners_root_size             = 35
  runners_concurrent            = 1000
  runners_ebs_optimized         = true
  runners_idle_count            = 3
  runners_idle_time             = 1800
  runners_image                 = "docker"
  runners_limit                 = 1000
  runners_max_builds            = 15
  runners_monitoring            = false
  runners_name                  = "fluidattacks-ci-large-${each.key}"
  runners_output_limit          = 4096
  runners_privileged            = false
  runners_pull_policy           = "always"
  runners_request_concurrency   = 3
  runners_request_spot_instance = true
  runners_use_private_address   = false
  runners_machine_autoscaling   = var.off_peak_periods
  subnet_id_runners             = var.autoscaling_ci_subnet_id

  # Tags
  environment = "makes-fluidattacks-ci-large-${each.key}"
  overrides = {
    name_runner_agent_instance  = "fluidattacks-ci-large-runner-${each.key}",
    name_docker_machine_runners = "fluidattacks-ci-large-worker-${each.key}",
    name_sg                     = "",
    name_iam_objects            = "",
  }
  tags = {
    "management:area" = "cost"
    "management:type" = "product"
  }
}
