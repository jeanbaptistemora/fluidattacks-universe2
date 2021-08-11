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
  docker_machine_options = [
    "amazonec2-request-spot-instance=true",
    "amazonec2-spot-price=",
    "amazonec2-access-key=__autoscaling_access_key__",
    "amazonec2-secret-key=__autoscaling_secret_key__",
    "amazonec2-region=us-east-1",
    "amazonec2-tags=use,ci,management:type,production,management:product,common",
    "amazonec2-vpc-id=vpc-0ea1c7bd6be683d2d",
    "amazonec2-subnet-id=subnet-0bceb7aa2c900324a",
    "amazonec2-zone=a",
    "amazonec2-use-private-address=true",
    "amazonec2-use-ebs-optimized-instance=true",
    "amazonec2-security-group=AutoscalingCISG",
    "amazonec2-ami=ami-013da1cc4ae87618c",
    "amazonec2-instance-type=c5ad.large",
    "amazonec2-userdata=/etc/gitlab-runner/init/worker.sh",
    "amazonec2-volume-type=gp3",
    "amazonec2-root-size=10"
  ]

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
