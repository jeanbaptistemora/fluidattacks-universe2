data "aws_caller_identity" "current" {}

data "local_file" "init_runner" {
  filename = "./init/runner.sh"
}

data "local_file" "init_worker" {
  filename = "./init/worker.sh"
}

variable "gitlabTokenFluidattacks" {
  default = "default-value"
}

variable "gitlabTokenAutonomicmind" {
  default = "default-value"
}

variable "gitlabTokenAutonomicjump" {
  default = "default-value"
}

#
# Constants
#

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

variable "ci_cache_buckets" {
  default = {
    autoscaling_ci_cache   = "autoscaling-ci-cache",
    autonomicmind_ci_cache = "autonomicmind-ci-cache",
    autonomicjump_ci_cache = "autonomicjump-ci-cache",
  }
}

data "aws_iam_policy_document" "lambda-assume-role-policy" {
  statement {
    sid    = "LambdaAssumeRolePolicy"
    effect = "Allow"

    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com",
        "edgelambda.amazonaws.com",
      ]
    }

    actions = [
      "sts:AssumeRole",
    ]
  }
}

#
# Reused infrastructure from other services
#

variable "autostaling_ci_vpc_id" {
  default = "vpc-0ea1c7bd6be683d2d"
}
