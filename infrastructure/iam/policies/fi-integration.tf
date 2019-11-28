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
      "arn:aws:s3:::fluidintegrates*/*",
      "arn:aws:s3:::fi.binaryalert*"
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

  # BinaryAlert Permissions
  statement {
    sid       = "AnalysisMonitoring"
    effect    = "Allow"
    actions   = [
      "cloudwatch:*"
    ]
    resources = [
      "arn:aws:cloudwatch::${data.aws_caller_identity.current.account_id}:dashboard/BinaryAlert",
      "arn:aws:cloudwatch:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:alarm:fi*"
    ]
  }

  statement {
    sid       = "EventsLog"
    effect    = "Allow"
    actions   = [
      "events:*"
    ]
    resources = [
      "arn:aws:events:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:rule/fi_binaryalert*"
    ]
  }

  statement {
    sid       = "IAMRead"
    effect    = "Allow"
    actions   = [
      "iam:Get*",
      "iam:List*"
    ]
    resources = [
      "*"
    ]
  }

  statement {
    sid       = "FunctionRoles"
    effect    = "Allow"
    actions   = [
      "iam:*"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/fi_binaryalert*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/fi_binaryalert*"
    ]
  }

  statement {
    sid       = "QueueKeyCreation"
    effect    = "Allow"
    actions   = [
      "kms:CreateKey",
      "kms:Describe*",
      "kms:Get*",
      "kms:List*",
      "kms:TagResource",
      "kms:UntagResource"
    ]
    resources = [
      "*"
    ]
  }

  statement {
    sid       = "QueueEncryption"
    effect    = "Allow"
    actions   = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:alias/fi_binaryalert*"
    ]
  }

  statement {
    sid       = "LambdaCreateMapping"
    effect    = "Allow"
    actions   = [
      "lambda:CreateEventSourceMapping",
      "lambda:DeleteEventSourceMapping",
      "lambda:UpdateEventSourceMapping",
      "lambda:GetEventSourceMapping",
      "lambda:ListEventSourceMappings"
    ]
    resources = [
      "*"
    ]
  }

  statement {
    sid       = "AnalysisFunctions"
    effect    = "Allow"
    actions   = [
      "lambda:*"
    ]
    resources = [
      "arn:aws:lambda:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:function:fi_binaryalert*"
    ]
  }

  statement {
    sid       = "LogsList"
    effect    = "Allow"
    actions   = [
      "logs:Describe*",
      "logs:List*",
    ]
    resources = ["*"]
  }

  statement {
    sid       = "FunctionLogs"
    effect    = "Allow"
    actions   = ["logs:*"]
    resources = [
        "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/fi_binaryalert*",
        "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/integrates-*"
        ]
  }

  statement {
    sid       = "ResultsNotification"
    effect    = "Allow"
    actions   = ["sns:*"]
    resources = ["arn:aws:sns:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:fi_binaryalert*"]
  }

  statement {
    sid       = "AnalysisQueue"
    effect    = "Allow"
    actions   = ["sqs:*"]
    resources = ["*"]
  }

  statement {
    sid       = "LambdaFunctions"
    effect    = "Allow"
    actions   = ["lambda:*"]
    resources = ["arn:aws:lambda:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:function:integrates-*"]
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
