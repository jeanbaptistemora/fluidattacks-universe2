locals {
  arch = {
    roles = [
      "dev",
      "prod_common",
    ]
    sizes = [
      "small",
    ]
  }
  runners = {
    for runner in setproduct(
      local.arch.roles,
      local.arch.sizes
    ) : join("_", runner) => { role = runner[0], size = runner[1] }
  }
}

module "runners" {
  source   = "npalm/gitlab-runner/aws"
  version  = "5.1.0"
  for_each = local.runners

  # AWS
  aws_region                             = "us-east-1"
  vpc_id                                 = data.aws_vpc.main.id
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
    policy = module.cache.policy_arn
    bucket = module.cache.bucket
  }

  # Runner
  instance_type                     = "c5a.large"
  runner_ami_filter                 = var.worker_ami
  enable_runner_ssm_access          = true
  subnet_ids_gitlab_runner          = [data.aws_subnet.main.id]
  runner_instance_ebs_optimized     = true
  runner_instance_enable_monitoring = true
  runner_root_block_device          = var.runner_block_device
  userdata_pre_install              = data.local_file.init_runner.content
  docker_machine_iam_policy_arns = [
    "arn:aws:iam::${data.aws_caller_identity.main.account_id}:policy/${each.value.role}"
  ]
  gitlab_runner_registration_config = {
    registration_token = var.gitlabTokenFluidattacks
    tag_list           = each.key
    description        = "common-ci-${each.key}"
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
  runners_idle_count            = 1
  runners_idle_time             = 1800
  runners_image                 = "docker"
  runners_limit                 = 1000
  runners_max_builds            = 15
  runners_monitoring            = false
  runners_name                  = "common-ci-${each.key}"
  runners_output_limit          = 4096
  runners_privileged            = false
  runners_pull_policy           = "always"
  runners_request_concurrency   = 10
  runners_request_spot_instance = true
  runners_use_private_address   = false
  runners_machine_autoscaling   = var.off_peak_periods
  subnet_id_runners             = data.aws_subnet.main.id

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