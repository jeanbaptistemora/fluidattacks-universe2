data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "region" {
  default = "us-east-1"
}

#
# Constants
#

variable "autoscaling_ci_s3_cache_bucket" {
  default = "autoscaling-ci-cache"
}

data "aws_iam_policy_document" "lambda-assume-role-policy" {
  statement {
    sid    = "LambdaAssumeRolePolicy"
    effect = "Allow"

    principals {
      type        = "Service"
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
