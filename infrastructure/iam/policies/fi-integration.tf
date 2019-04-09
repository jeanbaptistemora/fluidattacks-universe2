variable "fsBucket" {}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_iam_policy_document" "integrates-terraform" {
  policy_id = "IntegratesTerraform"

  statement {
    sid       = "ApplicationAutoscaling"
    effect    = "Allow"
    actions   = [
      "application-autoscaling:DeleteScalingPolicy",
      "application-autoscaling:DeregisterScalableTarget",
      "application-autoscaling:DescribeScalableTargets",
      "application-autoscaling:DescribeScalingActivities",
      "application-autoscaling:DescribeScalingPolicies",
      "application-autoscaling:PutScalingPolicy",
      "application-autoscaling:RegisterScalableTarget",
    ]
    resources = [
      "*"
    ]
  }

  statement {
    sid       = "CloudFront"
    effect    = "Allow"
    actions   = [
      "cloudfront:*"
    ]
    resources = [
      "*"
    ]
  }

  statement {
    sid       = "DynamoDB"
    effect    = "Allow"
    actions   = [
      "dynamodb:*"
    ]
    resources = [
      "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/FI*",
      "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/fi*"
    ]
  }

  statement {
    sid       = "IAMDynamoAutoScaling"
    effect    = "Allow"
    actions   = [
      "iam:PassRole"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable"
    ]
  }

  statement {
    sid = "S3"
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::fluidintegrates*",
      "arn:aws:s3:::fluidintegrates*/*"
    ]
  }

  statement {
    sid       = "TerraformState"
    effect    = "Allow"
    actions   = [
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject"
    ]
    resources = [
      "arn:aws:s3:::${var.fsBucket}",
      "arn:aws:s3:::${var.fsBucket}/integrates.tfstate"
    ]
  }
}

resource "aws_iam_policy" "integrates-terraform" {
  description = "Policy for Terraform deployments from Integrates"
  name        = "IntegratesTerraform"
  path        = "/"
  policy      = "${data.aws_iam_policy_document.integrates-terraform.json}"
}

data "aws_iam_policy_document" "fis3integrator-policy" {
  statement {
    sid = "VisualEditor0"
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "FI_S3INTEGRATION" {
  name        = "FI_S3INTEGRATION"
  path        = "/"
  description = "Policy for FI_S3INTEGRATION"

  policy = "${data.aws_iam_policy_document.fis3integrator-policy.json}"
}
