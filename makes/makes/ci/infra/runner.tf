data "local_file" "init_runner" {
  filename = "./init/runner.sh"
}

data "local_file" "init_worker" {
  filename = "./init/worker.sh"
}

variable "off_peak_periods" {
  type = list(object({
    periods    = list(string)
    idle_count = number
    idle_time  = number
    timezone   = string
  }))
  default = [
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
}

variable "runner_block_device" {
  type = object({
    delete_on_termination = bool
    volume_type           = string
    volume_size           = number
    encrypted             = bool
    iops                  = number
  })
  default = {
    delete_on_termination = true
    volume_type           = "gp3"
    volume_size           = 15
    encrypted             = true
    iops                  = 3000
  }
}

module "fluidattacks_ci_cache" {
  source  = "npalm/gitlab-runner/aws//modules/cache"
  version = "4.28.0"

  environment             = "fluidattacks-ci-cache"
  cache_bucket_versioning = false
  cache_expiration_days   = 30
  cache_lifecycle_clear   = true
  cache_lifecycle_prefix  = ""
  create_cache_bucket     = true

  tags = {
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

module "fluidattacks_ci" {
  source  = "npalm/gitlab-runner/aws"
  version = "4.28.0"

  # AWS
  aws_region                             = "us-east-1"
  vpc_id                                 = var.autostaling_ci_vpc_id
  allow_iam_service_linked_role_creation = true
  enable_kms                             = true
  kms_deletion_window_in_days            = 30
  enable_manage_gitlab_token             = true

  # Cache
  cache_bucket_versioning = false
  cache_expiration_days   = 30
  cache_shared            = true

  # Logs
  cloudwatch_logging_retention_in_days = 365
  enable_cloudwatch_logging            = true

  # Runner
  instance_type                     = "c5a.large"
  enable_runner_ssm_access          = true
  enable_gitlab_runner_ssh_access   = false
  subnet_ids_gitlab_runner          = ["subnet-0bceb7aa2c900324a"]
  runner_instance_ebs_optimized     = true
  runner_instance_enable_monitoring = true
  runner_root_block_device          = var.runner_block_device
  userdata_pre_install              = data.local_file.init_runner.content
  gitlab_runner_registration_config = {
    registration_token = var.fluidAttacksToken
    tag_list           = "autoscaling"
    description        = "fluidattacks-ci"
    locked_to_project  = "true"
    run_untagged       = "false"
    maximum_timeout    = "3600"
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
  runners_monitoring            = true
  runners_name                  = "fluidattacks-ci"
  runners_output_limit          = 4096
  runners_privileged            = false
  runners_pull_policy           = "always"
  runners_request_concurrency   = 10
  runners_request_spot_instance = true
  runners_use_private_address   = false
  runners_machine_autoscaling   = var.off_peak_periods
  subnet_id_runners             = "subnet-0bceb7aa2c900324a"

  # Tags
  environment = "makes-fluidattacks-ci"
  tags = {
    "management:type"    = "production"
    "management:product" = "makes"
  }
}
