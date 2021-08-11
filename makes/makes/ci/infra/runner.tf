module "gitlab_runner" {
  source  = "npalm/gitlab-runner/aws"
  version = "4.28.0"

  aws_region                             = "us-east-1"
  vpc_id                                 = var.autostaling_ci_vpc_id
  allow_iam_service_linked_role_creation = true
  enable_kms                             = true
  kms_deletion_window_in_days            = 30
  enable_manage_gitlab_token             = true
  enable_runner_ssm_access               = true
  enable_gitlab_runner_ssh_access        = false
  docker_machine_spot_price_bid          = "0.6"
  subnet_id_runners                      = "subnet-0bceb7aa2c900324a"
  subnet_ids_gitlab_runner               = ["subnet-0bceb7aa2c900324a"]
  userdata_pre_install                   = data.local_file.init_runner.content

  cache_bucket_versioning = false
  cache_expiration_days   = 30
  cache_shared            = true

  cloudwatch_logging_retention_in_days = 365
  enable_cloudwatch_logging            = true

  gitlab_runner_registration_config = {
    registration_token = var.fluidAttacksToken
    tag_list           = "docker_spot_runner"
    description        = "runner public - auto"
    locked_to_project  = "true"
    run_untagged       = "false"
    maximum_timeout    = "3600"
    access_level       = "ref_protected"
  }
  runner_instance_ebs_optimized     = true
  runner_instance_enable_monitoring = true
  runner_root_block_device = {
    delete_on_termination = true
    volume_type           = "gp3"
    volume_size           = 15
    encrypted             = true
    iops                  = 3000
  }
  runners_concurrent    = 1000
  runners_ebs_optimized = true
  runners_executor      = "docker+machine"
  runners_gitlab_url    = "https://gitlab.com"
  runners_idle_count    = 0
  runners_idle_time     = 1800
  runners_image         = "docker"
  runners_limit         = 1000
  runners_max_builds    = 15
  runners_monitoring    = true
  runners_name          = "fluidattacks-autoscaling"
  runners_machine_autoscaling = [{
    periods = [
      "* * 0-6,20-23 * * mon-fri *",
      "* * * * * sat,sun *",
    ]
    idle_count = 0
    idle_time  = 1800
    timezone   = "America/Bogota"
  }]
  runners_output_limit          = 4096
  runners_privileged            = false
  runners_pull_policy           = "always"
  runners_request_concurrency   = 10
  runners_request_spot_instance = true
  runners_use_private_address   = false

  environment = "fluidattacks-autoscaling"
  overrides = {
    name_sg                     = "fluidattacks-autoscaling"
    name_runner_agent_instance  = "bastion"
    name_docker_machine_runners = "worker"
  }
  tags = {
    "Name"               = "AutoscalingCISG"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "null_resource" "cancel_spot_requests" {
  # Cancel active and open spot requests, terminate instances
  triggers = {
    environment = "fluidattacks-autoscaling"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "../../bin/cancel-spot-instances.sh ${self.triggers.environment}"
  }
}
