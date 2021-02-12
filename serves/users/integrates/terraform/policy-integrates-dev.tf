data "aws_iam_policy_document" "integrates-dev-policy-data" {

  # S3
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::fluidintegrates*/*",
      "arn:aws:s3:::fluidintegrates*",
      "arn:aws:s3:::integrates*/*",
      "arn:aws:s3:::integrates*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/*"
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
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/integrates-*"
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
      "ec2:Describe*",
    ]
    resources = ["*"]
  }

  # Elasticache
  statement {
    effect = "Allow"
    actions = [
      "elasticache:Describe*",
      "elasticache:List*"
    ]
    resources = ["*"]
  }

  # Lambda
  statement {
    effect  = "Allow"
    actions = ["lambda:*"]
    resources = [
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
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/integrates-*"
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
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/integrates-dev-*"
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
      "application-autoscaling:DeleteScalingPolicy",
    ]
    resources = ["*"]
  }

  # Autoscaling read
  statement {
    effect = "Allow"
    actions = [
      "autoscaling:DescribeLaunchConfigurations",
      "autoscaling:DescribeAutoScalingGroups"
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
    actions = ["cloudwatch:*"]
    resources = [
      "arn:aws:cloudwatch:${var.region}:${data.aws_caller_identity.current.account_id}:alarm:fi*"
    ]
  }
  statement {
    effect    = "Allow"
    actions   = ["cloudfront:*"]
    resources = ["*"]
  }

  # ACM create and read certificate
  statement {
    effect = "Allow"
    actions = [
      "acm:RequestCertificate",
      "acm:DescribeCertificate",
      "acm:ListTagsForCertificate",
    ]
    resources = [
      "*",
    ]
  }

  # S3 read over continuous data buckets
  statement {
    sid    = "s3ContinuousDataRead"
    effect = "Allow"
    actions = [
      "s3:Get*",
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::continuous-data",
      "arn:aws:s3:::continuous-data/*",
    ]
  }

  # DynamoDB for locking terraform state
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:DeleteItem",
      "dynamodb:GetItem",
      "dynamodb:PutItem",
    ]
    resources = [
      var.terraform_state_lock_arn,
    ]
  }

  # EKS read permissions
  statement {
    effect = "Allow"
    actions = [
      "eks:Describe*",
      "eks:List*",
    ]
    resources = ["*"]
  }

  # WAF read permissions
  statement {
    effect = "Allow"
    actions = [
      "wafv2:Describe*",
      "wafv2:List*",
      "wafv2:Get*",
      "wafv2:Check*",
    ]
    resources = ["*"]
  }

  # Secretsmanager for forces secrets
  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:DescribeSecret",
      "secretsmanager:GetResourcePolicy",
    ]
    resources = [
      "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:forces_token_*",
    ]
  }
}

resource "aws_iam_policy" "integrates-dev-policy" {
  description = "integrates-dev policy"
  name        = "integrates-dev-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy" {
  user       = "integrates-dev"
  policy_arn = aws_iam_policy.integrates-dev-policy.arn
}
