data "aws_iam_policy_document" "integrates-prod-policy-data" {

  # S3
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::fluidintegrates*/*",
      "arn:aws:s3:::fluidintegrates*",
      "arn:aws:s3:::fi.binaryalert*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::servestf/integrates.tfstate",
      "arn:aws:s3:::servestf",
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/*"
    ]
  }

  # RDS
  statement {
    effect  = "Allow"
    actions = ["rds:*"]
    resources = [
      "arn:aws:rds:*:${data.aws_caller_identity.current.account_id}:db:django-db",
      "arn:aws:rds:*:${data.aws_caller_identity.current.account_id}:og:django-db",
      "arn:aws:rds:*:${data.aws_caller_identity.current.account_id}:pg:django-db",
      "arn:aws:rds:*:${data.aws_caller_identity.current.account_id}:subgrp:django-db"
    ]
  }

  # IAM
  statement {
    effect = "Allow"
    actions = [
      "iam:List*",
      "iam:Get*"
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["iam:*"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/integrates-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/fi_binaryalert*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/integrates-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/fi_binaryalert*"
    ]
  }
  statement {
    effect  = "Allow"
    actions = ["iam:PassRole"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable"
    ]
  }

  # EC2
  statement {
    effect = "Allow"
    actions = [
      "ec2:DeleteSubnet",
      "ec2:ModifySubnetAttribute",
      "ec2:CreateSubnet",
      "ec2:DescribeSubnets",
    ]
    resources = ["*"]
  }

  # Lambda
  statement {
    effect  = "Allow"
    actions = ["lambda:*"]
    resources = [
      "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:fi_binaryalert*",
      "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:integrates-*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "lambda:UpdateEventSourceMapping",
      "lambda:ListEventSourceMappings",
      "lambda:GetEventSourceMapping",
      "lambda:DeleteEventSourceMapping",
      "lambda:CreateEventSourceMapping"
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["logs:*"]
    resources = [
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/integrates-*",
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/fi_binaryalert*"
    ]
  }

  # KMS
  statement {
    effect = "Allow"
    actions = [
      "kms:UntagResource",
      "kms:TagResource",
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
      "kms:CreateKey",
      "kms:CreateAlias",
      "kms:UpdateAlias"
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["kms:*"]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/fi_binaryalert*",
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/integrates-prod-*"
    ]
  }

  # Kubernetes autoscaling
  statement {
    effect = "Allow"
    actions = [
      "application-autoscaling:RegisterScalableTarget",
      "application-autoscaling:PutScalingPolicy",
      "application-autoscaling:DescribeScalingPolicies",
      "application-autoscaling:DescribeScalingActivities",
      "application-autoscaling:DescribeScalableTargets",
      "application-autoscaling:DeregisterScalableTarget",
      "application-autoscaling:DeleteScalingPolicy"
    ]
    resources = ["*"]
  }

  # Others
  statement {
    effect    = "Allow"
    actions   = ["sqs:*"]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["sns:*"]
    resources = [
      "arn:aws:sns:${var.region}:${data.aws_caller_identity.current.account_id}:fi_binaryalert*"
    ]
  }
  statement {
    effect  = "Allow"
    actions = ["cloudwatch:*"]
    resources = [
      "arn:aws:cloudwatch:${var.region}:${data.aws_caller_identity.current.account_id}:alarm:fi*",
      "arn:aws:cloudwatch::${data.aws_caller_identity.current.account_id}:dashboard/BinaryAlert"
    ]
  }
  statement {
    effect    = "Allow"
    actions   = ["cloudfront:*"]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["events:*"]
    resources = [
      "arn:aws:events:${var.region}:${data.aws_caller_identity.current.account_id}:rule/fi_binaryalert*"
    ]
  }

}

resource "aws_iam_policy" "integrates-prod-policy" {
  description = "integrates-prod policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-policy.arn
}
