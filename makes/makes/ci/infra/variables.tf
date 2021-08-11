data "aws_caller_identity" "current" {}

data "local_file" "init_runner" {
  filename = "./init/runner.sh"
}

data "local_file" "init_worker" {
  filename = "./init/worker.sh"
}

#
# Constants
#

variable "fluidAttacksToken" {
  default = "default-value"
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
